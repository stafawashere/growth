---
title: LSN-CON-10007 Harmonic series, alternating harmonic series, and p-series
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10007, the harmonic series, the alternating harmonic series and the p-series criterion, built from authoring_bundle("BC-CON-10007") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10007 Harmonic series, alternating harmonic series, and p-series

Concept BC-CON-10007 (skills BC-SKL-10018, BC-SKL-10019, BC-SKL-10020), topic 10.5 of Unit 10, BC only (ced:190), loaded by three archetypes, BC-QA-10001, BC-QA-10004 and BC-QA-10015. Hard parent BC-CON-10003 (docs/lessons/unit-10/README.md, section 1); no outside hard parent, so geometric series behaviour is assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. Each of the first N terms of \(\sum\frac{4}{\sqrt n}\) is at least \(\frac{4}{\sqrt N}\), and the student says what the partial sums do as N grows. Key B, they grow without bound: \(S_N\ge4\sqrt N\), which the stem's inequality gives before any rule. The distractors are that they level off at a finite value and that they cannot be decided; both are false. The resolution shows the bound and states the threshold at \(p=1\), with no verdict word. Delivery: text. Source: BC-CON-10007 and the topic 10.5 section that ki-1 cites.

## Orientation

Served text (28 words), from BC-CON-10007 `description_plain` ("a short list of standard series whose behaviour is known") and the topic's Assessment behaviour paragraph: the multiple choice form gives a series and four candidate tests or asks for the values of p that make a series converge, and the free response form uses a p-series or the harmonic series as the comparison partner (research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series). No count, no frequency.

## Key ideas

All three skills map to one essential knowledge statement, BC-EK-LIM-7A7 (ced:190): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs Standard series and p-series (hypothesis: terms \(\frac1{n^p}\); conclusion: convergence when p exceeds 1, divergence when p is at most 1; the harmonic series is p equal to 1) and the alternating harmonic series, which BC-SKL-10020 recalls as convergent without a derivation. Notation line: the concept's `notation`. No anchor quote: the ced:190 sentence lists the series and adds no behaviour, and would cost 20 words in the brief band.

## Recognition

Three archetypes load the skills: BC-QA-10001 (family procedure-selection), BC-QA-10004 (convergence-test) and BC-QA-10015 (radius-interval). The examples and checks draw from BC-QA-10001's pseries form. BC-QA-10015 presents a power series with its radius, which the unit teaches at BC-CON-10020 and 10021, so an endpoint example would introduce a topic not yet met [inferred]. BC-QA-10004's forms are comparison and alternating, with no plain p-series form.

- BC-QA-10001 (research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series): `common_givens` "a series of numbers in sigma or expanded form"; `asked_to_produce` "a convergence or divergence verdict naming the series", "the name of an applicable test", "a check of that test's conditions"; `typical_wording` "determine whether the series converges or diverges, and justify your answer". The generator's pseries form is a constant multiple of \(\frac1{n^p}\).
- Shapes: BC-QA-10001 `official_examples` BC-MCQ-PE2012-009; BC-QA-10004 BC-MCQ-CED-019, BC-MCQ-PE2012-027 and BC-FRQ-2024-Q6-A; BC-QA-10015 uses the harmonic series as the comparison partner at an endpoint, the reason point resting on the test named (sg-24:19, sg-24:20).

The signal in the stem: a general term with n in the base under a fixed power, often after a root or a reciprocal. The near miss of the contrast pair is a geometric term, \(\frac{3}{4^n}\), where n is in the exponent (docs/lessons/unit-10/README.md, section 3, the geometric against p-series confusion, BC-MIS-10003's probe). The two stems differ in where n sits.

What says "not this concept": n in the exponent (geometric, BC-CON-10003); a factorial or an nth power (the ratio test, BC-CON-10012); a term that is a rational expression in n with a constant ratio to no power of n (comparison, BC-CON-10009).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-10001. Cue from `common_givens`: a sigma series with n in the base under a fixed power. Method, `expected_solution_path[0]` "read the general term" and the next entry, matching its form to a test: the term as a multiple of \(\frac1{n^p}\) with p named. Rival, the p-series entries of `common_distractors` and the record's BC-ERR-10014: the threshold placed anywhere but 1. Separating feature: compare p with 1 and with no other number. Both cue fields exist, so the block is verified. The block carries the contrast pair. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10001, both bands, no calculator. Draw: form pseries, power 1/2, coefficient 4, start 1 (the other spec keys are carried unused). \(a_n=\frac{4}{\sqrt n}=4\cdot\frac1{n^{1/2}}\), \(p=\frac12\), diverges. No published item on BC-QA-10001 carries this draw (content/items_gen_unit10/ITM-GEN-10001-00 to 21 list none with all keys equal).
- ex-2, low band. Draw: form pseries, power 1, coefficient 7, start 2. \(a_n=\frac7n\), \(p=1\), the harmonic series times 7, diverges. Not equal to any published draw.
- ex-2 is faded from step 3: steps 1 and 2 (the term and the constant pulled out) are shown, the student writes p, and steps 3 and 4 then reveal. The fade falls there because reading the term repeats ex-1 and the edge case p equal to 1 is what the student must produce.
- Steps follow `expected_solution_path`: the general term (new), the constant multiple (equivalent), p (new), and the comparison with 1 (no value). A fluent solver writes the exponent and the comparison; the rewriting of a root as a power is held. The alternating harmonic series is taught in ki-1 and not worked here, since its convergence needs the alternating series test of BC-CON-10011. No productive-failure comparison: BC-CON-10007 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

None. BC-QA-10001 lists no `point_types`, so the lesson carries no what_a_reader_scores entry, no step carries a point tag and the lesson says nothing about points (plan 15, R14). The `scoring_pattern` says a test that does not fit the series earns nothing even when the conclusion is right (sg-21:23); it names no BC-PT and is not served.

## Traps

One active error meets the skills: BC-ERR-10014 (BC-MIS-10009 medium, BC-MIS-10005 high), served in both bands on ex-1's draw. Wrong step: \(p=\frac12<1\), so it converges. Right step: \(p=\frac12\le1\), so it diverges. Both hold the value \(\frac12\), so the relation is equivalent and the fix prompt false; the difference lives in the sentence. Possible reason, words from BC-MIS-10009: places the boundary elsewhere than at one.

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions general term to the name of a test and a standard series to its known behaviour; nothing figure-shaped (docs/lessons/unit-10/README.md, section 6).

## Prerequisite bridge

BC-PRQ-06002, BC-PRQ-06005 and BC-PRQ-10008, each from its `description_plain` and `failure_signature`, gated by state, in both bands.

## Time

Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout), the multiple choice form the topic names; BC-QA-10001 records no FRQ example with points [inferred]. A fluent solver writes the exponent and the comparison with 1; the rewriting of the root is held. The minutes go on reading p from the form.

## Checks

- chk-1, completion of ex-1, both bands. The constant already pulled out, p asked. Key \(\frac12\).
- chk-2, isomorph, both bands, no calculator. Draw: form pseries, power 4/3, coefficient 2, start 1. \(\sum\frac{2}{\sqrt[3]{n^4}}\), key \(p=\frac43\), so it converges. Not equal to a published draw.
- chk-3, MCQ, low band. Draw: form pseries, power 2/3, coefficient 5, start 1. \(a_n=\frac{5}{n^{2/3}}\). Key: it diverges since \(p\le1\). The record links one error, so all three distractors carry BC-ERR-10014 through distinct threshold mistakes: the threshold reversed (p below 1 read as convergence), the boundary placed at 0, and the boundary placed at one half. Each is a value the error produces on this draw.

## Delivery

- orientation, ki-1: text. Rule 6: BC-REP-11, 01, 04, none figure-bearing (docs/lessons/unit-10/README.md, section 6). No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, err-BC-ERR-10014: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10014, ex-2 (faded from step 3), chk-2, chk-3. 427 words, 2.9 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10014, chk-2. 339 words, 2.3 minutes.
- Refresher: ki-1, err-BC-ERR-10014, ex-1.

## Sources

- BC-CON-10007; BC-SKL-10018, BC-SKL-10019, BC-SKL-10020; BC-EK-LIM-7A7; ced:190
- BC-QA-10001, BC-QA-10004, BC-QA-10015
- BC-ERR-10014; BC-MIS-10009, BC-MIS-10003
- BC-PRQ-06002, BC-PRQ-06005, BC-PRQ-10008
- research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series
- research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series
- research/exam/exam-structure.md#Section and part layout
- [inferred] the held step, Part A for a no-point archetype, the choice of BC-QA-10001 over BC-QA-10015 and the delivery choice, each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10007",
 "kind": "concept",
 "target_id": "BC-CON-10007",
 "unit": "10",
 "skills": [
  "BC-SKL-10018",
  "BC-SKL-10019",
  "BC-SKL-10020"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. Each of the first N terms of \\(\\sum_{n=1}^{\\infty}\\frac{4}{\\sqrt n}\\) is at least \\(\\frac{4}{\\sqrt N}\\). What do the partial sums \\(S_N\\) do as N grows?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "They level off at a finite value.",
    "is_key": false
   },
   {
    "id": "B",
    "label": "They grow without bound.",
    "is_key": true
   },
   {
    "id": "C",
    "label": "They cannot be decided from the terms.",
    "is_key": false
   }
  ],
  "resolution": "\\(S_N\\ge N\\cdot\\frac{4}{\\sqrt N}=4\\sqrt N\\), which grows without bound. A p-series \\(\\sum\\frac1{n^p}\\) behaves this way when \\(p\\le1\\) and settles when \\(p>1\\).",
  "sources": [
   "BC-CON-10007",
   "research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series"
  ]
 },
 "no_figure_reason": "The criterion compares one exponent with 1. No skill carries a figure-bearing representation, and the key idea names three standard series rather than a process.",
 "orientation": {
  "text": "A response classifies the series as harmonic, alternating harmonic or a p-series, names p, and states the known behaviour: a p-series converges exactly when p exceeds 1.",
  "sources": [
   "BC-CON-10007",
   "research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A7",
   "depth": "core",
   "text": "\\(\\sum\\frac1{n^p}\\) converges when \\(p>1\\) and diverges when \\(p\\le1\\). The harmonic series is the case \\(p=1\\) and diverges. The alternating harmonic series \\(\\sum\\frac{(-1)^{n+1}}{n}\\) converges.",
   "notation": "p-series; harmonic series",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A7",
    "ced:190",
    "research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10001",
   "cue": "A series in sigma form with n in the base under a fixed power.",
   "method": "The term as a multiple of \\(\\frac1{n^p}\\), with p named.",
   "rival": "The threshold placed anywhere but at 1.",
   "separating_feature": "Compare p with 1, and no other number.",
   "sources": [
    "BC-QA-10001",
    "research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Determine whether \\(\\sum_{n=1}^{\\infty}\\frac{3}{n^{4/3}}\\) converges or diverges, and justify.",
     "archetype_id": "BC-QA-10001"
    },
    "not_this": {
     "text": "Determine whether \\(\\sum_{n=1}^{\\infty}\\frac{3}{4^n}\\) converges or diverges, and justify.",
     "why_not": "The index is in the exponent, so the terms share a ratio and it is geometric."
    },
    "feature": "n in the base under a fixed power is a p-series. n in the exponent is geometric."
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
    "form": "pseries",
    "power": "1/2",
    "coefficient": "4",
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
    "text": "Write \\(\\sum_{n=1}^{\\infty}\\frac{4}{\\sqrt n}\\) as a multiple of a p-series, name p, and state whether the series converges.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Sigma form: read \\(a_n\\).",
     "why": "n sits in the base under a fixed power.",
     "expr": "4/sqrt(n)",
     "relation": "new"
    },
    {
     "cue": "Pull out the constant.",
     "why": "A constant multiple keeps the behaviour.",
     "expr": "4*(1/n**(1/2))",
     "relation": "equivalent"
    },
    {
     "cue": "Read p from the exponent.",
     "why": "\\(\\sqrt n=n^{1/2}\\).",
     "expr": "1/2",
     "relation": "new"
    },
    {
     "cue": "Compare p with 1.",
     "why": "\\(p\\le1\\), so the series diverges."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1/2"
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
    "form": "pseries",
    "power": "1",
    "coefficient": "7",
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
    "text": "Write \\(\\sum_{n=2}^{\\infty}\\frac{7}{n}\\) as a multiple of a p-series, name p, and state whether the series converges.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Sigma form: read \\(a_n\\).",
     "why": "n sits in the base under a fixed power.",
     "expr": "7/n",
     "relation": "new"
    },
    {
     "cue": "Pull out the constant.",
     "why": "A constant multiple keeps the behaviour.",
     "expr": "7*(1/n**1)",
     "relation": "equivalent"
    },
    {
     "cue": "Read p from the exponent.",
     "why": "\\(n=n^1\\), so \\(p=1\\).",
     "expr": "1",
     "relation": "new"
    },
    {
     "cue": "Compare p with 1.",
     "why": "\\(p=1\\) is the harmonic series, which diverges, so a multiple of it diverges."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-10014",
   "observed_behavior": "The response reports a p-series with p at most one as convergent, or treats the harmonic series as convergent.",
   "scoring_consequence": "The verdict is wrong, so the reasoning point and the answer point are both lost.",
   "wrong_step": {
    "text": "\\(p=\\frac12<1\\), so it converges.",
    "expr": "1/2"
   },
   "right_step": {
    "text": "\\(p=\\frac12\\le1\\), so it diverges.",
    "expr": "1/2"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-10009",
    "text": "places the boundary elsewhere than at one"
   },
   "sources": [
    "BC-ERR-10014",
    "BC-MIS-10009"
   ],
   "fix_prompt": false
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "Rewrite roots and reciprocals as powers."
  },
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Tell \\(f'\\) from \\(f\\)."
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
   "archetype_id": "BC-QA-10001",
   "parameter_draw": {
    "form": "pseries",
    "power": "1/2",
    "coefficient": "4",
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
    "text": "\\(a_n=\\frac{4}{\\sqrt n}=4\\cdot\\frac{1}{n^p}\\). Give p.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "1/2"
   },
   "steps": [
    {
     "text": "The general term.",
     "expr": "4/sqrt(n)",
     "relation": "new"
    },
    {
     "text": "The exponent of n.",
     "expr": "1/2",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10018"
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
    "form": "pseries",
    "power": "4/3",
    "coefficient": "2",
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
    "text": "Write \\(\\sum_{n=1}^{\\infty}\\frac{2}{\\sqrt[3]{n^4}}\\) as a multiple of a p-series and give p.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "4/3"
   },
   "steps": [
    {
     "text": "The general term.",
     "expr": "2/n**(4/3)",
     "relation": "new"
    },
    {
     "text": "As a multiple of \\(\\frac1{n^p}\\).",
     "expr": "2*(1/n**(4/3))",
     "relation": "equivalent"
    },
    {
     "text": "The exponent of n.",
     "expr": "4/3",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10018",
    "BC-SKL-10019"
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
    "power": "2/3",
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
   "stem": {
    "text": "Let \\(a_n=\\frac{5}{n^{2/3}}\\). Which statement about \\(\\sum_{n=1}^{\\infty}a_n\\) is correct?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "diverges, since p = 2/3 is at most 1"
   },
   "steps": [
    {
     "text": "The general term.",
     "expr": "5/n**(2/3)",
     "relation": "new"
    },
    {
     "text": "As a multiple of \\(\\frac1{n^p}\\).",
     "expr": "5*(1/n**(2/3))",
     "relation": "equivalent"
    },
    {
     "text": "The exponent of n.",
     "expr": "2/3",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "It diverges, since \\(p=\\frac23\\le1\\).",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "It converges, since \\(p=\\frac23<1\\).",
     "error_path": "BC-ERR-10014",
     "derivation": "the threshold reversed, so p below 1 is read as convergence"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "It converges, since \\(p=\\frac23>0\\).",
     "error_path": "BC-ERR-10014",
     "derivation": "the boundary placed at 0 instead of 1"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "It converges, since \\(p=\\frac23>\\frac12\\).",
     "error_path": "BC-ERR-10014",
     "derivation": "the boundary placed at one half instead of 1"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10019"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10007"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11, 01, 04 on BC-SKL-10018 to 10020, none figure-bearing; the idea is a threshold on one exponent, not a process (docs/lessons/unit-10/README.md, section 6)",
   "sources": [
    "BC-SKL-10018",
    "BC-SKL-10019",
    "BC-SKL-10020"
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
   "block": "err-BC-ERR-10014",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10014",
  "ex-1"
 ],
 "read_minutes": {
  "full": 2.9,
  "brief": 2.3
 },
 "word_count": {
  "full": 427,
  "brief": 339
 },
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "The harmonic series is the case p equals one."
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the exponent and the comparison with 1, and holds the rewriting of the root as a power.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "BC-QA-10001 records no FRQ example with points, so its multiple choice form is timed against Section I Part A at 2.14 minutes.",
   "settles": "Timing data on series items split by exam part."
  },
  {
   "claim": "The examples and checks use BC-QA-10001 rather than BC-QA-10015, because the endpoint archetype presents a power series and its radius, which the unit teaches after this concept.",
   "settles": "A library link from a p-series skill to a BC-QA-10015 draw that shows a numerical endpoint series alone."
  },
  {
   "claim": "The delivery choice serves better than the alternatives.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-10007",
  "BC-SKL-10018",
  "BC-SKL-10019",
  "BC-SKL-10020",
  "BC-EK-LIM-7A7",
  "ced:190",
  "BC-QA-10001",
  "BC-QA-10015",
  "BC-ERR-10014",
  "BC-MIS-10009",
  "BC-PRQ-06002",
  "BC-PRQ-06005",
  "BC-PRQ-10008",
  "BC-REP-11",
  "research/exam/exam-structure.md#Section and part layout",
  "research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series",
  "research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series"
 ]
}
```
