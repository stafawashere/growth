---
title: LSN-CON-01010 The squeeze theorem
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01010, the squeeze theorem, built from authoring_bundle("BC-CON-01010") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01010 The squeeze theorem

Concept BC-CON-01010 (skills BC-SKL-01032 to BC-SKL-01035), topic 1.8 of Unit 1, loaded by BC-QA-01005 (primary). The unit attack map places it tenth, after BC-CON-01009, and its delivery map picks motion for the key idea.

## Prediction

Served first, both bands. Pose on ex-1's own function: \(f(x)=2+3(x-1)\sin\frac{1}{x-1}\), with the sine factor named as having no limit at 1, and ask for the limit. Form `short_answer`, key 2, which is ex-1's answer. The resolution says that the bounded factor and the vanishing factor trap f between bounds that both tend to 2, from BC-CON-01010 and the topic 1.8 paragraph. It carries no verdict word, and it differs from chk-1, which supplies the inequality.

## Orientation

Served text, from BC-CON-01010 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-01-limits-continuity.md#1.8 Determining Limits Using the Squeeze Theorem): MCQ forms supply the inequality and ask for the limit; FRQ forms would demand the inequality and the two bound limits as separate steps. Stated as what a response shows. No count, no frequency. Delivered as a figure (Delivery).

## Key ideas

All four skills map to BC-EK-LIM-1E2 (ced:45): one core block, both bands.

- ki-1 (core). Paraphrase of the topic's Required mathematical knowledge paragraph (Squeeze theorem; Hypotheses as a separate demand, BC-MPS-3C on ced:45) and of BC-SKL-01035 (bound the oscillating part between negative one and one and multiply through). No quote in the served block, to hold the brief form under its cap. Notation line from the concept record and the topic: squeeze theorem; the inequality written with the trapped function in the middle.

## Recognition

- BC-QA-01005 (family squeeze-theorem, one FRQ part or a single MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-01005 Limit determined by the squeeze theorem with its hypotheses stated). `typical_wording`: "The stated inequality holds near the given input. Use it to determine the limit of the trapped function and justify your answer." `common_givens`: a function trapped between two bounding functions; a bounding inequality that holds near the input. `asked_to_produce`: a bounding inequality, the limits of the two bounds, the limit with justification. No official example. The signal is a sine or cosine of a reciprocal, or any factor with no limit of its own, multiplied by a factor that vanishes at the target, or a supplied inequality.

What says "not this concept": every factor has its own limit, so the product theorem settles it (BC-CON-01007; unit-01 README, Squeeze against direct substitution); a quotient giving zero over zero with polynomial parts (BC-CON-01008).

The contrast pair on st-1 takes its near miss from the first of those: `this` is a vanishing factor times a cosine of a reciprocal on BC-QA-01005, `not_this` is the same vanishing factor times a cosine of x, which has its own limit (BC-CON-01007), and the feature is that one factor has no limit of its own.

## Method choice

- st-1, BC-QA-01005, low and mid bands, verified (`asked_to_produce` and `common_givens` present). Method, `expected_solution_path[0]`: bound the oscillating factor between fixed values. Rival, `wrong_approaches`: substituting the target into the bounds instead of taking their limits (BC-ERR-01013). Separating feature: the oscillating factor has no limit, so the product theorem cannot be used and the bounds must be built.

## Solution path

- ex-1, BC-QA-01005, both bands, no calculator. Draw: target 1, shift 2, coefficient 3, power 1, wave sin, naming open, giving \(f(x)=2+3(x-1)\sin\frac{1}{x-1}\) (the `parameter_spec` notes). Power 1 makes the vanishing factor negative left of 1, the case the constraint forces. No published BC-QA-01005 draw matches. Steps follow `expected_solution_path`: bound the oscillation (no value); multiply and record the direction, written with \(3|x-1|\) so one inequality holds on both sides [inferred] (lower bound `new`); the two bound limits (`limit`, each after its bound); the conclusion (no value).

A fluent solver writes the inequality, both bound limits and the conclusion, and holds the bound on the sine in the head [inferred].

## Scoring

None. BC-QA-01005 lists no `point_types`; its `scoring_pattern` names three points (inequality, bound limits, conclusion) with no official free response part in 2023 to 2025 (research/question-analysis/question-archetypes.md#BC-QA-01005 Limit determined by the squeeze theorem with its hypotheses stated), so no `what_a_reader_scores` entry and no point tag. For the author only: hypothesis verification is the family the research describes for other theorems (research/scoring/common-point-losses.md#Justification points; research/scoring/justification-requirements.md#Theorem hypotheses); the lesson does not state a point.

## Traps

Three error blocks, all on ex-1's draw, in the bundle's order (each links a high severity misconception, so the order falls to id): BC-ERR-01012 (BC-MIS-01008, BC-MIS-01007) and BC-ERR-01013 (BC-MIS-01008, BC-MIS-01001) in both bands, BC-ERR-99008 (BC-MIS-99009, BC-MIS-01015) in the low band only, since the mid band shows the first two. BC-ERR-99008 is held by BC-SKL-01032 (name what must hold before the theorem may be used). Its record names only the Mean Value Theorem, the Intermediate Value Theorem and L'Hospital's Rule, so the block stages the L'Hospital move (cr-23:16: the rule used without first checking that the limits of the numerator and of the denominator were both 0) on a quotient drawn for this block from ex-1's vanishing factor \(3(x-1)\). The rule itself is Unit 4 (ced:93); staging it here is [inferred].

- err-BC-ERR-01012. Wrong: \(2-3(x-1)\) as the lower bound. Right: \(2-3|x-1|\). Distinct. Reason, words from BC-MIS-01008.
- err-BC-ERR-01013. Wrong: the bound evaluated at 1, value 2. Right: the bound's limit, 2. Equivalent: the value agrees, the theorem is not applied, which is the record's consequence. Reason, words from BC-MIS-01008.
- err-BC-ERR-99008. Wrong: L'Hospital's Rule on \(\lim_{x\to1}\frac{3(x-1)}{x+1}\) with the form unchecked, \(\frac{3}{1}=3\). Right: the limits are 0 and 2, not both 0, so the limit is \(\frac{0}{2}=0\). Distinct (SymPy: the quotient's limit is 0, the derivative quotient's is 3). Reason, words from BC-MIS-99009.

## Representations

None as a separate block. The topic's Representations paragraph names one graphical conversion (a graph showing the trapped curve to the stated inequality); the orientation figure and the ki-1 motion carry it, so a third figure would add a representation with nothing new to read.

## Prerequisite bridge

Two BC-PRQ parents, supporting edges, gated by state: BC-PRQ-01005 (bounds on sine and cosine) and BC-PRQ-01010 (interval notation). Each restates `description_plain` and names the `failure_signature`.

## Time

BC-QA-01005 is `no_calculator`, one FRQ part or a single MCQ. The MCQ shape is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout); the FRQ shape has no official example to fix its share [inferred]. On the MCQ a fluent solver writes the bound line and reads the limit; on a free response part every valued line of ex-1 is written, and the sine bound (step 1) is held in the head [inferred].

## Checks

- chk-1, completion of ex-1, both bands: the inequality is given, the student takes the limits. Key 2.
- chk-2, isomorph, both bands: target \(-2\), shift \(-1\), coefficient \(-2\), power 2, wave cos, naming named. Key \(-1\).
- chk-3, MCQ, low band, key form statement: which line justifies \(\lim_{x\to0}(3+x^3\sin\frac1x)=3\). Every option reaches 3, so the options are justifications, not values: the three errors change the argument, not the number. Distractors carry BC-ERR-01013 (both bounds evaluated at 0), BC-ERR-01012 (\(x^3\) bounds not reversed for \(x<0\)), BC-ERR-01013 again (the upper bound alone evaluated at 0).

## Delivery

- orientation: figure. Rule 3, BC-REP-02 on BC-SKL-01033 and BC-SKL-01035; the unit-01 README gives figure. Spec: the two bounds dashed, \(f\) solid, the open point \((1,2)\), labels inside.
- ki-1: motion. Rule 2, a limit being taken (the bounds pinching toward 1), as the README names. Three frames at half-widths 1, 0.1 and 0.01; arrow keys step; reduced motion cross-fades on key press; the fallback is the static strip.
- ex-1 and the three error blocks: step_reveal. Rule 1.

The lesson already carries drawn blocks (orientation figure, ki-1 motion), so no `no_figure_reason` is stated. Every non-text choice is [inferred], settled by the modality A/B.

## Band plan

- Low (full): pr-1, orientation, two bridges when gated in, ki-1, st-1 with its contrast, ex-1, chk-1, err-BC-ERR-01012, err-BC-ERR-01013, err-BC-ERR-99008, chk-2, chk-3. There is no second example, so nothing fades. 577 words, 4.0 minutes (cap 900 and 6).
- Mid (brief): pr-1, orientation, bridges when gated in, ki-1, st-1 with its contrast, ex-1, chk-1, err-BC-ERR-01012, err-BC-ERR-01013, chk-2. 434 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-01010; BC-SKL-01032, BC-SKL-01033, BC-SKL-01034, BC-SKL-01035; BC-EK-LIM-1E2; ced:45
- BC-QA-01005
- BC-ERR-01012, BC-ERR-01013, BC-ERR-99008; BC-MIS-01008, BC-MIS-99009
- cr-23:16; ced:93
- BC-PRQ-01005, BC-PRQ-01010
- research/units/unit-01-limits-continuity.md#1.8 Determining Limits Using the Squeeze Theorem
- research/question-analysis/question-archetypes.md#BC-QA-01005 Limit determined by the squeeze theorem with its hypotheses stated
- research/exam/exam-structure.md#Section and part layout
- research/scoring/common-point-losses.md#Justification points
- research/scoring/justification-requirements.md#Theorem hypotheses
- [inferred] Non-text delivery modes. Settled by the modality A/B.
- [inferred] The absolute value form of the bound. Settled by an official guideline or CED example.
- [inferred] Part I-A for the squeeze archetype. Settled by an official FRQ part with a guideline.
- [inferred] BC-ERR-99008's L'Hospital move staged in a Unit 1 lesson on a quotient drawn for the block. Settled by a squeeze-scoped error record or an official Unit 1 item applying the rule to a form that is not indeterminate.

## Machine record

```json
{
 "id": "LSN-CON-01010",
 "kind": "concept",
 "target_id": "BC-CON-01010",
 "unit": "01",
 "skills": [
  "BC-SKL-01032",
  "BC-SKL-01033",
  "BC-SKL-01034",
  "BC-SKL-01035"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "\\(f(x)=2+3(x-1)\\sin\\frac{1}{x-1}\\), and \\(\\sin\\frac{1}{x-1}\\) oscillates without a limit at 1. What is \\(\\lim_{x\\to1}f(x)\\)?",
   "command_verb": "predict"
  },
  "format": "short_answer",
  "key": {
   "form": "numeric",
   "expr": "2"
  },
  "resolution": "The sine factor is bounded and \\(3(x-1)\\) vanishes, so f is trapped between bounds that both tend to 2.",
  "sources": [
   "BC-CON-01010",
   "research/units/unit-01-limits-continuity.md#1.8 Determining Limits Using the Squeeze Theorem"
  ]
 },
 "orientation": {
  "text": "A response shows the trapped function between two bounds near the target, the limit of each bound, and the conclusion that the trapped function shares that limit.",
  "sources": [
   "BC-CON-01010",
   "research/units/unit-01-limits-continuity.md#1.8 Determining Limits Using the Squeeze Theorem"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-1E2",
   "depth": "core",
   "text": "If \\(g(x)\\le f(x)\\le h(x)\\) near \\(c\\) and \\(g\\) and \\(h\\) both tend to \\(L\\), then \\(\\lim_{x\\to c}f(x)=L\\). The hypotheses are their own demand: the inequality is shown, and each bound's limit is taken. The usual case bounds an oscillating factor between \\(-1\\) and 1.",
   "notation": "squeeze theorem; the inequality written with the trapped function in the middle",
   "quote": null,
   "sources": [
    "BC-EK-LIM-1E2",
    "ced:45",
    "research/units/unit-01-limits-continuity.md#1.8 Determining Limits Using the Squeeze Theorem"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01005",
   "cue": "An oscillating factor times a vanishing factor.",
   "method": "Bound the oscillating factor between fixed values.",
   "rival": "Substituting the target into the bounds.",
   "separating_feature": "The oscillating factor has no limit of its own.",
   "sources": [
    "BC-QA-01005",
    "BC-ERR-01013"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find \\(\\lim_{x\\to0}x^2\\cos\\frac{1}{x}\\) and justify.",
     "archetype_id": "BC-QA-01005"
    },
    "not_this": {
     "text": "Find \\(\\lim_{x\\to0}x^2\\cos x\\).",
     "why_not": "Each factor has its own limit, so the product theorem settles it."
    },
    "feature": "One factor has no limit of its own."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01005",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "target": 1,
    "shift": 2,
    "coefficient": 3,
    "power": 1,
    "wave": "sin",
    "naming": "open"
   },
   "problem": {
    "text": "Let \\(f(x)=2+3(x-1)\\sin\\frac{1}{x-1}\\). Find \\(\\lim_{x\\to1}f(x)\\) and justify the answer.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "\\(\\sin\\frac{1}{x-1}\\) oscillates near 1 and has no limit there.",
     "why": "It is bounded: \\(-1\\le\\sin\\frac{1}{x-1}\\le1\\) for every \\(x\\ne1\\)."
    },
    {
     "cue": "The vanishing factor \\(3(x-1)\\) is negative left of 1.",
     "why": "Bounding by \\(3|x-1|\\) keeps one inequality valid on both sides: \\(f(x)\\ge2-3|x-1|\\).",
     "expr": "2 - 3*Abs(x-1)",
     "relation": "new"
    },
    {
     "cue": "The stem asks for a limit, so take the limit of the lower bound.",
     "why": "\\(2-3|x-1|\\to2\\) as \\(x\\to1\\).",
     "expr": "2",
     "relation": "limit",
     "variable": "x",
     "point": "1"
    },
    {
     "cue": "The same bound gives \\(f(x)\\le2+3|x-1|\\).",
     "why": "The upper bound is needed too; one side alone traps nothing.",
     "expr": "2 + 3*Abs(x-1)",
     "relation": "new"
    },
    {
     "cue": "Take the limit of the upper bound.",
     "why": "\\(2+3|x-1|\\to2\\) as \\(x\\to1\\).",
     "expr": "2",
     "relation": "limit",
     "variable": "x",
     "point": "1"
    },
    {
     "cue": "Both bounds tend to 2 and trap \\(f\\) near 1.",
     "why": "By the squeeze theorem, \\(\\lim_{x\\to1}f(x)=2\\)."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "2"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01012",
   "observed_behavior": "The response multiplies the bounding inequality by a factor that is negative on one side of the target without reversing the inequality there.",
   "scoring_consequence": "The point for establishing the bounding inequality is lost.",
   "wrong_step": {
    "text": "Multiplying by \\(3(x-1)\\) without reversal: \\(2-3(x-1)\\le f(x)\\), false for \\(x<1\\).",
    "expr": "2 - 3*(x-1)"
   },
   "right_step": {
    "text": "With \\(3|x-1|\\): \\(2-3|x-1|\\le f(x)\\) on both sides.",
    "expr": "2 - 3*Abs(x-1)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01008",
    "text": "handles the inequality as an equation"
   },
   "sources": [
    "BC-ERR-01012",
    "BC-MIS-01008"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01013",
   "observed_behavior": "The response substitutes the target input into the bounding functions rather than evaluating their limits.",
   "scoring_consequence": "The conclusion point is lost because the theorem has not been applied.",
   "wrong_step": {
    "text": "\\(x=1\\) is put into the bound: \\(2-3|1-1|=2\\).",
    "expr": "2 - 3*Abs(1-1)"
   },
   "right_step": {
    "text": "The limit of the bound: \\(\\lim_{x\\to1}(2-3|x-1|)=2\\).",
    "expr": "2"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-01008",
    "text": "treats the bounding functions as things to evaluate at the target rather than as functions whose limits must agree"
   },
   "sources": [
    "BC-ERR-01013",
    "BC-MIS-01008"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-99008",
   "observed_behavior": "Responses apply the Mean Value Theorem, the Intermediate Value Theorem or L'Hospital's Rule without establishing continuity from differentiability, without bounding the target value between two function values, or without confirming the indeterminate form.",
   "scoring_consequence": "The condition point is not earned; in several years this was the point earned by the smallest proportion of responses on the question.",
   "wrong_step": {
    "text": "L'Hospital's Rule on \\(\\lim_{x\\to1}\\frac{3(x-1)}{x+1}\\) with the form unchecked: \\(\\frac{3}{1}=3\\).",
    "expr": "3"
   },
   "right_step": {
    "text": "The numerator tends to 0 and the denominator to 2, not both 0, so the limit is \\(\\frac{0}{2}=0\\).",
    "expr": "0"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-99009",
    "text": "recalls a theorem by its conclusion and applies it without establishing the conditions"
   },
   "sources": [
    "BC-ERR-99008",
    "BC-MIS-99009",
    "BC-SKL-01032",
    "cr-23:16"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-01005",
   "text": "Sine and cosine stay between \\(-1\\) and 1. Treating an oscillating factor as unbounded marks this gap."
  },
  {
   "prq_id": "BC-PRQ-01010",
   "text": "Read open and closed intervals as inequalities. A conclusion stated on the wrong interval marks this gap."
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
    4,
    5,
    6
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
   "archetype_id": "BC-QA-01005",
   "parameter_draw": {
    "target": 1,
    "shift": 2,
    "coefficient": 3,
    "power": 1,
    "wave": "sin",
    "naming": "open"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For \\(x\\ne1\\), \\(2-3|x-1|\\le f(x)\\le2+3|x-1|\\). Find \\(\\lim_{x\\to1}f(x)\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "2"
   },
   "steps": [
    {
     "text": "The upper bound.",
     "expr": "2 + 3*Abs(x-1)",
     "relation": "new"
    },
    {
     "text": "Its limit at 1 is 2, as is the lower bound's.",
     "expr": "2",
     "relation": "limit",
     "variable": "x",
     "point": "1"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01034"
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
   "archetype_id": "BC-QA-01005",
   "parameter_draw": {
    "target": -2,
    "shift": -1,
    "coefficient": -2,
    "power": 2,
    "wave": "cos",
    "naming": "named"
   },
   "stem": {
    "text": "Use the squeeze theorem to find \\(\\lim_{x\\to-2}\\left(-1-2(x+2)^2\\cos\\frac{1}{x+2}\\right)\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-1"
   },
   "steps": [
    {
     "text": "Upper bound \\(-1+2(x+2)^2\\).",
     "expr": "-1 + 2*(x+2)**2",
     "relation": "new"
    },
    {
     "text": "Its limit at \\(-2\\).",
     "expr": "-1",
     "relation": "limit",
     "variable": "x",
     "point": "-2"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01035"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-01005",
   "parameter_draw": {
    "target": 0,
    "shift": 3,
    "coefficient": 1,
    "power": 3,
    "wave": "sin",
    "naming": "open"
   },
   "stem": {
    "text": "Which line justifies \\(\\lim_{x\\to0}\\left(3+x^3\\sin\\frac{1}{x}\\right)=3\\)?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "abs_bounds_then_limits"
   },
   "steps": [
    {
     "text": "Upper bound \\(3+|x|^3\\).",
     "expr": "3 + Abs(x)**3",
     "relation": "new"
    },
    {
     "text": "Its limit at 0.",
     "expr": "3",
     "relation": "limit",
     "variable": "x",
     "point": "0"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "At \\(x=0\\) the bounds \\(3-|x|^3\\) and \\(3+|x|^3\\) both equal 3.",
     "error_path": "BC-ERR-01013",
     "derivation": "bounds evaluated at the target"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "\\(3-x^3\\le f(x)\\le3+x^3\\) near 0, and both bounds tend to 3.",
     "error_path": "BC-ERR-01012",
     "derivation": "inequality not reversed where x cubed is negative"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "At \\(x=0\\) the upper bound \\(3+|x|^3\\) equals 3, so \\(f\\) tends to 3.",
     "error_path": "BC-ERR-01013",
     "derivation": "upper bound evaluated at the target"
    },
    {
     "id": "D",
     "is_key": true,
     "label": "\\(3-|x|^3\\le f(x)\\le3+|x|^3\\) for \\(x\\ne0\\), and both bounds tend to 3.",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01032",
    "BC-SKL-01033",
    "BC-SKL-01034"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-01033 and BC-SKL-01035 (unit-01 README delivery map)",
   "sources": [
    "BC-SKL-01033",
    "BC-SKL-01035"
   ],
   "spec": {
    "kind": "graph",
    "window": {
     "x": [
      0,
      2
     ],
     "y": [
      -1,
      5
     ]
    },
    "curves": [
     {
      "expr": "2 - 3*Abs(x-1)",
      "style": "dashed",
      "label": {
       "text": "lower bound",
       "placement": "inside"
      }
     },
     {
      "expr": "2 + 3*Abs(x-1)",
      "style": "dashed",
      "label": {
       "text": "upper bound",
       "placement": "inside"
      }
     },
     {
      "expr": "2 + 3*(x-1)*sin(1/(x-1))",
      "style": "solid",
      "label": {
       "text": "f",
       "placement": "inside"
      }
     }
    ],
    "points": [
     {
      "x": 1,
      "y": 2,
      "style": "open",
      "label": {
       "text": "(1, 2)",
       "placement": "inside"
      }
     }
    ],
    "labels": [
     {
      "text": "trapped between the bounds",
      "placement": "inside"
     }
    ],
    "representations": [
     "graph"
    ]
   },
   "fallback": "Alt text and the inequality \\(2-3|x-1|\\le f(x)\\le2+3|x-1|\\) in words, with the point \\((1,2)\\) named.",
   "keyboard": "none needed: a static figure"
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: a limit being taken, the bounds pinching toward the input; rule 3, BC-REP-02 on BC-SKL-01033 and BC-SKL-01035",
   "sources": [
    "BC-SKL-01033",
    "BC-SKL-01035"
   ],
   "spec": {
    "kind": "graph_sweep",
    "parameter": "half-width of the window about x = 1",
    "curves": [
     {
      "expr": "2 - 3*Abs(x-1)",
      "label": {
       "text": "g",
       "placement": "inside"
      }
     },
     {
      "expr": "2 + 3*Abs(x-1)",
      "label": {
       "text": "h",
       "placement": "inside"
      }
     },
     {
      "expr": "2 + 3*(x-1)*sin(1/(x-1))",
      "label": {
       "text": "f",
       "placement": "inside"
      }
     }
    ],
    "frames": [
     {
      "window": {
       "x": [
        0,
        2
       ],
       "y": [
        -1,
        5
       ]
      },
      "label": {
       "text": "half-width 1",
       "placement": "inside"
      }
     },
     {
      "window": {
       "x": [
        0.9,
        1.1
       ],
       "y": [
        1.7,
        2.3
       ]
      },
      "label": {
       "text": "half-width 0.1",
       "placement": "inside"
      }
     },
     {
      "window": {
       "x": [
        0.99,
        1.01
       ],
       "y": [
        1.97,
        2.03
       ]
      },
      "label": {
       "text": "half-width 0.01",
       "placement": "inside"
      }
     }
    ],
    "labels": [
     {
      "text": "g and h meet at height 2",
      "placement": "inside"
     }
    ],
    "representations": [
     "graph"
    ]
   },
   "fallback": "The three frames as a static strip, each labelled with its half-width, the gap between g and h stated under each.",
   "keyboard": "Left and right arrow keys step between frames; Home returns to the first frame.",
   "reduced_motion": "No auto-advance; each key press cross-fades to the next frame."
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01012",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99008",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-01012",
  "err-BC-ERR-01013",
  "err-BC-ERR-99008",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/question-analysis/question-archetypes.md",
   "line": "No official free response part in 2023 to 2025 assesses the squeeze theorem."
  }
 ],
 "inferred": [
  {
   "claim": "The non-text delivery modes chosen here serve the content better than text and step reveal.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "Bounding by the absolute value of the vanishing factor, rather than splitting the two sides, is the first written inequality a fluent solver uses.",
   "settles": "An official scoring guideline or CED example writing the squeeze inequality with an absolute value."
  },
  {
   "claim": "The squeeze archetype sits in Section I Part A; no free response part in 2023 to 2025 assesses it.",
   "settles": "An official free response part on the squeeze theorem with its scoring guideline."
  },
  {
   "claim": "BC-ERR-99008 names no squeeze move, so its L'Hospital's Rule move is staged on a quotient drawn for the block from ex-1's vanishing factor, a rule the student meets in Unit 4 (ced:93).",
   "settles": "A squeeze-scoped error record, or an official Unit 1 item on which L'Hospital's Rule is applied to a form that is not indeterminate."
  }
 ],
 "sources": [
  "BC-CON-01010",
  "BC-SKL-01032",
  "BC-SKL-01033",
  "BC-SKL-01034",
  "BC-SKL-01035",
  "BC-EK-LIM-1E2",
  "ced:45",
  "BC-QA-01005",
  "BC-ERR-01012",
  "BC-ERR-01013",
  "BC-ERR-99008",
  "BC-MIS-01008",
  "BC-MIS-99009",
  "cr-23:16",
  "ced:93",
  "BC-PRQ-01005",
  "BC-PRQ-01010",
  "research/units/unit-01-limits-continuity.md#1.8 Determining Limits Using the Squeeze Theorem",
  "research/question-analysis/question-archetypes.md#BC-QA-01005 Limit determined by the squeeze theorem with its hypotheses stated",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/justification-requirements.md#Theorem hypotheses",
  "research/scoring/common-point-losses.md#Justification points"
 ],
 "read_minutes": {
  "full": 4.0,
  "brief": 3.0
 },
 "word_count": {
  "full": 576,
  "brief": 433
 }
}
```
