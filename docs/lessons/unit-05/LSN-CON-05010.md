---
title: LSN-CON-05010 A sole relative extremum as an absolute extremum
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05010, raising a relative extremum to an absolute one when it is the only critical point on the interval, built from authoring_bundle("BC-CON-05010") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05010 A sole relative extremum as an absolute extremum

Concept BC-CON-05010 (skill BC-SKL-05038), topic 5.7 of Unit 5. One archetype in the bundle loads it, BC-QA-05013 (family extremum-classification). Unit parents BC-CON-05005 and 05009; it closes the optimisation argument of BC-CON-05013 (docs/lessons/unit-05/README.md, section 1).

## Prediction

Both bands, first. Poses ex-1's own numbers: g(x) = 2x^3 - 9x^2 + 1 has one critical point on x > 0, at x = 3, where g''(3) = 18, and the student predicts what g has on x > 0. Form `mcq`, three options, key A (an absolute minimum at x = 3). The resolution names continuity and the sole critical point. Sources: BC-CON-05010 and the topic 5.7 section.

## Orientation

Served text, from BC-CON-05010 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.7 Using the Second Derivative Test to Determine Extrema): a response that claims an absolute extremum from a derivative test writes that the critical point is the only one on the interval. No count, no frequency.

## Key ideas

BC-SKL-05038 maps to BC-EK-FUN-4A8 (ced:105): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Sole critical point extension, Local scope): f continuous on the interval, exactly one critical point there, and that point a relative extremum, give the absolute extremum; without the uniqueness sentence the argument stays local (sg-25:5, sg-22:12). Anchor quote from ced:105, 15 words. Notation line from the concept record.

## Recognition

BC-QA-05013 (research/question-analysis/question-archetypes.md#BC-QA-05013 Second derivative test applied at a critical point): `typical_wording` "determine whether the critical point is the location of a relative minimum, a relative maximum, or neither"; `common_givens` a function and a critical point; `difficulty_variables` "whether the question demands a global claim". The signal for this concept: the word "absolute", or "on the interval", beside a function with one critical point inside the stated interval. The global demand is what changes the justification (sg-25:19). Shape: one part of an FRQ or an MCQ; no `official_examples` in the record, and BC-ERR-05039 cites BC-FRQ-2022-Q3-D.

What says "not this concept" (the contrast pair's near miss is the relative-only claim of BC-CON-05009 and the local-for-global rival of BC-ERR-05039 and BC-MIS-05018): "relative" alone (BC-CON-05009), or a closed interval with endpoints to compare (candidates test, BC-CON-05006).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-05013. Method, `expected_solution_path[0]`: confirm the first derivative is zero at the point, then count the zeros of f prime inside the interval. Rival, `wrong_approaches`: classifying from the sign of the function value. Separating feature: the uniqueness sentence, "the only critical point on the interval", is what turns the local verdict into a global one (research/scoring/justification-requirements.md#Global versus local arguments). Not tagged inferred.

## Solution path

- ex-1, BC-QA-05013, both bands, no calculator. Draw: first_root 0, second_root 3, other_input -2, tested_root second, leading_sign 1, constant 1, letter g, given function. g'(x) = 6x(x - 3), g(x) = 2x^3 - 9x^2 + 1, asked on x > 0 [inferred: the interval is not a parameter of the spec]. No published BC-QA-05013 item carries this draw.
- Steps: g prime (new); its zeros (solve); only x = 3 in the interval (no value); g double prime (new); g''(3) = 18 (evaluate); the global conclusion with the uniqueness clause (no value). A fluent solver writes all of them; the uniqueness sentence is the step most often left in the head (BC-ERR-05039 `non_conceptual_causes`).

## Scoring

BC-QA-05013 lists no `point_types`, so no what_a_reader_scores entry and no point tag. For the author: a local argument followed by the statement that it is the only critical point in the interval earns the global justification (sg-25:5, sg-22:12); a local argument alone does not (research/scoring/common-point-losses.md#Justification points).

## Traps

One active error meets the skill: BC-ERR-05039, both bands, on ex-1's draw. Statement-shaped: the absolute claim with no uniqueness clause against the claim with it. Possible reason, words from BC-MIS-05018.

## Representations

None. The topic's Representations paragraph names BC-REP-01, 03 and 06 only.

## Prerequisite bridge

None.

## Time

BC-QA-05013 is `either`, an MCQ or one FRQ part, so Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred]. The minutes go on the zeros of g prime and the check of which lie in the interval; the conclusion is one sentence.

## Checks

Two checks: the bundle holds one error, so no three-distractor MCQ can be built [inferred].

- chk-1, completion of ex-1, both bands: g''(3) = 18 and x = 3 the only critical point on x > 0 given. Key: absolute minimum at x = 3.
- chk-2, isomorph, both bands. Draw: first_root -3, second_root 2, other_input 4, tested_root first, leading_sign -1, constant 0, letter f, given derivative, on x < 0. Key: absolute minimum at x = -3.

## Delivery

- orientation: text. Rule 5: BC-SKL-05038 carries BC-REP-01, 04, 05 (docs/lessons/unit-05/README.md, section 6).
- ki-1: text. Rule 5. No block is drawn, so the machine record carries `no_figure_reason`: BC-SKL-05038 carries BC-REP-01, 04 and 05, none figure-bearing, and no key idea describes a process. Example 1 is the only worked example, so nothing is faded.
- ex-1 and err-BC-ERR-05039: step_reveal. Rule 1.

## Band plan

- Low (full): served order of 2026-09-29: prediction, orientation, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-05039, chk-2. 441 words, 3.0 minutes (cap 900 and 6). No scoring lines, no bridges, no representations.
- Mid (brief): the same blocks. 441 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-05039, ex-1.

## Sources

- Prediction and contrast pair: BC-CON-05010, BC-CON-05009, BC-ERR-05039, BC-MIS-05018 (as above).

- BC-CON-05010; BC-SKL-05038; BC-EK-FUN-4A8; ced:105
- BC-QA-05013; sg-22:12, sg-25:5, sg-25:19
- BC-ERR-05039; BC-MIS-05018, BC-MIS-05007
- research/units/unit-05-analytical-applications-differentiation.md#5.7 Using the Second Derivative Test to Determine Extrema
- research/question-analysis/question-archetypes.md#BC-QA-05013 Second derivative test applied at a critical point
- research/scoring/justification-requirements.md#Global versus local arguments
- research/scoring/common-point-losses.md#Justification points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Section I Part A for an either archetype. Settled by a calculator status on BC-QA-05013.
- [inferred] The interval added to the draw. Settled by an interval parameter in the BC-QA-05013 parameter_spec.
- [inferred] Two checks only. Settled by a second and third BC-ERR record on BC-SKL-05038.

## Machine record

```json
{
 "id": "LSN-CON-05010",
 "kind": "concept",
 "target_id": "BC-CON-05010",
 "unit": "05",
 "skills": [
  "BC-SKL-05038"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. \\(g(x)=2x^3-9x^2+1\\) has one critical point on \\(x>0\\), at \\(x=3\\), where \\(g''(3)=18\\). What does \\(g\\) have on \\(x>0\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "An absolute minimum at \\(x=3\\)",
    "is_key": true
   },
   {
    "id": "B",
    "label": "Only a relative minimum at \\(x=3\\)",
    "is_key": false
   },
   {
    "id": "C",
    "label": "No minimum at all",
    "is_key": false
   }
  ],
  "resolution": "\\(g\\) is continuous and \\(x=3\\) is its only critical point on \\(x>0\\), where \\(g''(3)>0\\), so the relative minimum is the absolute minimum.",
  "sources": [
   "BC-CON-05010",
   "research/units/unit-05-analytical-applications-differentiation.md#5.7 Using the Second Derivative Test to Determine Extrema"
  ]
 },
 "orientation": {
  "text": "A response claiming an absolute extremum from a derivative test writes that the function is continuous and that this is the only critical point on the interval.",
  "sources": [
   "BC-CON-05010",
   "research/units/unit-05-analytical-applications-differentiation.md#5.7 Using the Second Derivative Test to Determine Extrema"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-4A8",
   "depth": "core",
   "text": "Three facts make a local verdict global: \\(f\\) is continuous on the interval, has exactly one critical point there, and that point is a relative extremum. The derivative test supplies the third fact. The sentence naming the only critical point supplies the second, and it is written, not implied.",
   "notation": "sole critical point",
   "quote": {
    "text": "When a continuous function has only one critical point on an interval on its domain",
    "source": "ced:105"
   },
   "sources": [
    "BC-EK-FUN-4A8",
    "ced:105",
    "sg-22:12",
    "sg-25:5",
    "research/units/unit-05-analytical-applications-differentiation.md#5.7 Using the Second Derivative Test to Determine Extrema"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-05013",
   "cue": "Absolute extremum on an interval, from a function with one critical point there?",
   "method": "Confirm \\(f'(c)=0\\), then list every zero of \\(f'\\) in the interval.",
   "rival": "The sign of the function value.",
   "separating_feature": "Absolute needs the only critical point on the interval beside the local verdict.",
   "sources": [
    "BC-QA-05013"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "\\(f(x)=x^3-12x\\) on \\(x>0\\). Justify that \\(f\\) has an absolute minimum.",
     "archetype_id": "BC-QA-05013"
    },
    "not_this": {
     "text": "\\(f(x)=x^3-12x\\). Justify that \\(f\\) has a relative minimum at \\(x=2\\).",
     "why_not": "Relative asks for the local test alone, with no uniqueness clause."
    },
    "feature": "Absolute on an interval adds the only critical point."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-05013",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "first_root": 0,
    "second_root": 3,
    "other_input": -2,
    "tested_root": "second",
    "leading_sign": 1,
    "constant": 1,
    "letter": "g",
    "given": "function"
   },
   "problem": {
    "text": "Let \\(g(x)=2x^3-9x^2+1\\) for \\(x>0\\). Does \\(g\\) have an absolute minimum on \\(x>0\\)? Justify.",
    "command_verb": "justify"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "An extremum question starts at the critical points.",
     "why": "\\(g'(x)=6x^2-18x\\).",
     "expr": "6*x**2 - 18*x",
     "relation": "new"
    },
    {
     "cue": "Critical points: \\(g'(x)=0\\).",
     "why": "\\(6x(x-3)=0\\).",
     "expr": "FiniteSet(0, 3)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "cue": "The stem fixes the interval \\(x>0\\).",
     "why": "\\(x=0\\) is outside it, so \\(x=3\\) is the only critical point on the interval."
    },
    {
     "cue": "One critical point: classify it with the second derivative.",
     "why": "\\(g''(x)=12x-18\\).",
     "expr": "12*x - 18",
     "relation": "new"
    },
    {
     "cue": "Evaluate at \\(x=3\\).",
     "why": "\\(g''(3)=18>0\\): a relative minimum.",
     "expr": "18",
     "relation": "evaluate",
     "subs": {
      "x": "3"
     }
    },
    {
     "cue": "The stem says absolute, so the local verdict needs uniqueness.",
     "why": "\\(g\\) is continuous and \\(x=3\\) is its only critical point on \\(x>0\\), so the relative minimum is the absolute minimum."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "absolute_minimum_at_3"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-05039",
   "observed_behavior": "The response extends a relative extremum to an absolute one without saying that there is only one critical point on the interval.",
   "scoring_consequence": "The justification is incomplete because the step that makes the local claim global is missing.",
   "wrong_step": {
    "text": "\\(g''(3)=18>0\\), so \\(g\\) has an absolute minimum at \\(x=3\\).",
    "expr": "absolute_claim_from_local_test_alone"
   },
   "right_step": {
    "text": "\\(g''(3)>0\\), and \\(x=3\\) is the only critical point on \\(x>0\\), so the minimum is absolute.",
    "expr": "absolute_claim_with_uniqueness_clause"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05018",
    "text": "treats a first or second derivative test as a proof that the extremum is the largest or smallest on the whole interval"
   },
   "sources": [
    "BC-ERR-05039",
    "BC-MIS-05018"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    3,
    4,
    5,
    6
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
   "archetype_id": "BC-QA-05013",
   "parameter_draw": {
    "first_root": 0,
    "second_root": 3,
    "other_input": -2,
    "tested_root": "second",
    "leading_sign": 1,
    "constant": 1,
    "letter": "g",
    "given": "function"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For \\(g(x)=2x^3-9x^2+1\\) on \\(x>0\\): \\(g'(3)=0\\), \\(g''(3)=18\\), and \\(g'\\) has no other zero there. Write the conclusion with its reason.",
    "command_verb": "justify"
   },
   "key": {
    "form": "statement",
    "expr": "absolute_minimum_at_3"
   },
   "steps": [
    {
     "text": "\\(g''(x)=12x-18\\).",
     "expr": "12*x - 18",
     "relation": "new"
    },
    {
     "text": "\\(g''(3)=18>0\\), and \\(x=3\\) is the only critical point on \\(x>0\\).",
     "expr": "18",
     "relation": "evaluate",
     "subs": {
      "x": "3"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05038"
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
   "archetype_id": "BC-QA-05013",
   "parameter_draw": {
    "first_root": -3,
    "second_root": 2,
    "other_input": 4,
    "tested_root": "first",
    "leading_sign": -1,
    "constant": 0,
    "letter": "f",
    "given": "derivative"
   },
   "stem": {
    "text": "\\(f'(x)=-6(x+3)(x-2)\\) and \\(f\\) is continuous. Does \\(f\\) have an absolute extremum on \\(x<0\\)? Justify.",
    "command_verb": "justify"
   },
   "key": {
    "form": "statement",
    "expr": "absolute_minimum_at_minus_3"
   },
   "steps": [
    {
     "text": "Zeros of \\(f'\\): \\(-3\\) and \\(2\\); only \\(-3\\) lies in \\(x<0\\).",
     "expr": "-6*(x + 3)*(x - 2)",
     "relation": "new"
    },
    {
     "text": "\\(f'(-3)=0\\).",
     "expr": "0",
     "relation": "evaluate",
     "subs": {
      "x": "-3"
     }
    },
    {
     "text": "\\(f''(x)=-12x-6\\).",
     "expr": "-12*x - 6",
     "relation": "new"
    },
    {
     "text": "\\(f''(-3)=30>0\\): relative minimum, the only critical point on \\(x<0\\), so absolute.",
     "expr": "30",
     "relation": "evaluate",
     "subs": {
      "x": "-3"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05038"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-SKL-05038 carries BC-REP-01, 04, 05 only",
   "sources": [
    "BC-SKL-05038"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: a theorem statement with no figure-bearing representation",
   "sources": [
    "BC-SKL-05038"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05039",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-05039",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.0,
  "brief": 3.0
 },
 "word_count": {
  "full": 441,
  "brief": 441
 },
 "research_lines": [
  {
   "file": "research/scoring/justification-requirements.md",
   "line": "sg-22:12 states directly that a justification using a local argument must also state that the critical value is the only critical point."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-05013 has calculator_status either; the lesson places it in Section I Part A at 2.14 minutes.",
   "settles": "A single calculator status on BC-QA-05013 or an official example fixing its part."
  },
  {
   "claim": "The intervals x > 0 and x < 0 are added to the draws; the BC-QA-05013 parameter_spec has no interval parameter.",
   "settles": "An interval parameter in the BC-QA-05013 parameter_spec."
  },
  {
   "claim": "The lesson carries two checks: the bundle lists one error, BC-ERR-05039, so no MCQ with three error-path distractors can be built.",
   "settles": "Further BC-ERR records on BC-SKL-05038 in the bundle's errors list."
  }
 ],
 "sources": [
  "BC-CON-05010",
  "BC-SKL-05038",
  "BC-EK-FUN-4A8",
  "ced:105",
  "BC-QA-05013",
  "sg-22:12",
  "sg-25:5",
  "sg-25:19",
  "BC-ERR-05039",
  "BC-MIS-05018",
  "BC-MIS-05007",
  "research/units/unit-05-analytical-applications-differentiation.md#5.7 Using the Second Derivative Test to Determine Extrema",
  "research/question-analysis/question-archetypes.md#BC-QA-05013 Second derivative test applied at a critical point",
  "research/scoring/justification-requirements.md#Global versus local arguments",
  "research/scoring/common-point-losses.md#Justification points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "no_figure_reason": "A theorem statement about one critical point with a uniqueness clause. Its only skill carries BC-REP-01, 04 and 05, none figure-bearing, and no key idea describes a process."
}
```
