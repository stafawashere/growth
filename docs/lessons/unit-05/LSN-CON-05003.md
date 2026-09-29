---
title: LSN-CON-05003 Critical points and the local versus global distinction
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05003, critical points and the local versus global distinction, built from authoring_bundle("BC-CON-05003") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05003 Critical points and the local versus global distinction

Concept BC-CON-05003 (skills BC-SKL-05010 to BC-SKL-05013), topic 5.2 of Unit 5. Five archetypes load its skills; BC-QA-05006, BC-QA-05007 and BC-QA-05014 have a first skill in the concept (primary), BC-QA-05003 and BC-QA-05010 do not. The lesson's worked example is BC-QA-05014, the one archetype whose whole demand is the critical point list. No unit parent (docs/lessons/unit-05/README.md, section 1).

## Prediction

One multiple choice question on worked example 1's own numbers, asked before the rule is shown: f is \(3(x-1)^{2/3}/(x+2)\), its derivative is given, and the student picks the inputs that are critical points. The key is 1 and 7, ex-1's answer; the distractors are 7 alone (BC-ERR-05011) and -2, 1 and 7 (BC-ERR-05010). The resolution, shown on the key idea screen beside the student's choice, names the two sources and the domain condition. No verdict word. Sources: BC-CON-05003 and the topic 5.2 section the key ideas cite (ced:100).

## Orientation

Served text, from BC-CON-05003 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.2 Extreme Value Theorem, Global Versus Local Extrema, and Critical Points): a response writes f'(x) = 0 as an equation, adds inputs in the domain where f' fails to exist, and does not call a critical point an extremum, or a relative extremum absolute, without an argument. No count, no frequency.

## Key ideas

Two BC-EK map to the skills: BC-EK-FUN-1C2 (BC-SKL-05010, 05011) and BC-EK-FUN-1C3 (BC-SKL-05012, 05013), both on ced:100. Two core blocks, both bands.

- ki-1 (core, BC-EK-FUN-1C2). Paraphrase of the Required mathematical knowledge paragraph (Critical point): f' zero or f' failing to exist, with c in the domain. The anchor quote is dropped: with the prediction and the contrast pair added the brief form passed its cap, and the orientation, the bridges, the strategy fields and the key idea texts were shortened first, then the quote as the last resort.
- ki-2 (core, BC-EK-FUN-1C3). Paraphrase of One-way containment and Local against global: every local extremum is at a critical point, not conversely (sg-23:13), and a local extremum is compared only with nearby values. No quote.

## Recognition

- BC-QA-05014 (research/question-analysis/question-archetypes.md#BC-QA-05014 Every critical point found, including inputs where the derivative fails to exist): `typical_wording` "find all critical points of f"; `common_givens` a quotient with a fractional power or an absolute value in the numerator, the input excluded from the domain; `asked_to_produce` the complete list. The signal: "all critical points" beside a fractional power, an absolute value or a denominator. No `official_examples`.
- BC-QA-05006 (research/question-analysis/question-archetypes.md#BC-QA-05006 Absolute extremum by the candidates test with a global justification): "absolute ... on the closed interval", official BC-FRQ-2013-Q4-B, 2022-Q3-D, 2023-Q4-D, 2025-Q1-D, 2025-Q4-D, 2026-Q4-D. Taught in BC-CON-05006; here only its first point, the equation f'(x) = 0.
- BC-QA-05003 (research/question-analysis/question-archetypes.md#BC-QA-05003 Relative extremum classified from the behaviour of the first derivative): "relative minimum, relative maximum, or neither at the named input". Here only the neither case: a critical point without a sign change.

The near miss served in the contrast pair of st-1 comes from the `wrong_approaches` entry of BC-QA-05014 and BC-ERR-05011: the same function with the stem asking only for the solutions of f'(x) = 0, which leaves out the inputs where f' fails to exist. The pair differs in the one thing the feature names, all critical points against the zeros of f' only.

BC-QA-05007 and BC-QA-05010 are served by BC-CON-05005 and BC-CON-05002. What says "not this concept": a stem naming an interval of increase (BC-CON-05004).

## Method choice

Three strategy blocks; st-1 serves both bands.

- st-1, BC-QA-05014. Method, `expected_solution_path[0]`: differentiate the function. Rival, `wrong_approaches`: setting only the derivative equal to zero. Separating feature: a fractional power or absolute value makes f' fail to exist somewhere.
- st-2, BC-QA-05006. Method: consider the derivative equal to zero and solve. Rival, `wrong_approaches`: appealing to the Extreme Value Theorem as though it located the extremum. Separating feature: the word absolute.
- st-3, BC-QA-05003. Method: locate the named input on the derivative information. Rival, `wrong_approaches`: the second derivative test from a graph of f' whose slope is not discussed. Separating feature: a critical point with no sign change is neither.

All three archetypes carry `asked_to_produce` and `common_givens`; none is tagged inferred.

## Solution path

- ex-1, BC-QA-05014, both bands, no calculator. Draw: shape cusp, root 1, pole -2, multiplier 3, so f(x) = 3(x - 1)^(2/3)/(x + 2); cusp_zero = 3(1) - 2(-2) = 7, as the spec derives. No published BC-QA-05014 item carries this draw. Steps follow `expected_solution_path`: f (new), f' (differentiate), f' = 0 (new, tagged BC-PT-99013), its root (solve), the denominator (new), its roots (solve), -2 discarded (no value, outside the domain), the list (new).

A fluent solver writes f', the equation f'(x) = 0 (the scored form, sg-25:5), and the list; the denominator's roots are read off, not written.

## Scoring

BC-QA-05014 lists BC-PT-99013; ex-1 tags it on the equation step, and the line is `reader_checks(["BC-PT-99013"])`, copied into the machine record. For the author: the solved critical value alone does not earn it (sg-25:5, sg-25:19; research/scoring/justification-requirements.md#Sign analysis of a derivative); a local test does not justify a global claim (sg-25:5, research/scoring/justification-requirements.md#Global versus local arguments); a local argument where a global one was required is a named justification loss (research/scoring/common-point-losses.md#Justification points).

## Traps

Five active errors meet the skills; the first four in the bundle's order are served (low band all four, mid band the first two). BC-ERR-05013 is left out by the cap of 4 and is served in BC-CON-05005.

- err-BC-ERR-05009: the list without the equation, against the equation. Statement-shaped. No possible reason line: neither linked description names the missing equation.
- err-BC-ERR-05010: f' left unreduced as (7 - x)(x + 2)/((x - 1)^(1/3)(x + 2)^3), whose numerator vanishes at -2, so -2 is kept, against the list without it (f(-2) undefined). No possible reason line: BC-MIS-05012 speaks of intervals, not critical points.
- err-BC-ERR-05011: {7} against {1, 7}. Possible reason, words from BC-MIS-05009.
- err-BC-ERR-05012 on ex-1's f over [0, 10]: the relative maximum f(7) = 6^(2/3)/3 reported as the maximum, against f(0) = 3/2. Possible reason, words from BC-MIS-05007.

## Representations

None as a separate block. The topic's Representations paragraph names the graph of f' to the critical points of f (BC-REP-02 to BC-REP-04), which the orientation and ki-2 figures carry.

## Prerequisite bridge

- BC-PRQ-05001, BC-PRQ-05003, BC-PRQ-05006, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-05014 is `no_calculator` and a single multiple choice or short answer question, so Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout). The minutes go on the derivative and the denominator check; the list follows at once.

## Checks

- chk-1, completion of ex-1, both bands: f' and its zero are given, the student adds the inputs where f' fails to exist. Key {1, 7}.
- chk-2, isomorph, both bands. Draw: shape vertical, root 3, pole 1, multiplier 2; f(x) = 2(x - 3)^(1/3)/(x - 1), vertical_zero 4. Key {3, 4}.
- chk-3, MCQ, low band. Draw: shape cusp, root -1, pole 2, multiplier -2; f(x) = -2(x + 1)^(2/3)/(x - 2). Key: the response with the equation and the list {-7, -1}. Distractors: the list with no equation (BC-ERR-05009), -7, -1 and 2 (BC-ERR-05010), -7 only (BC-ERR-05011). A statement key, since the key is a response, with option labels.

## Delivery

- orientation: figure. Rule 4 on BC-REP-02 in BC-SKL-05010 to 05013 (docs/lessons/unit-05/README.md, section 6) [inferred; settled by the modality A/B].
- ki-1: figure (a smooth turn, a cusp, a corner and a vertical tangent). Rule 4; BC-QA-05014 `difficulty_variables` "whether the failure is a cusp, a vertical tangent or a corner" is categorical, so static.
- ki-2: figure (a relative maximum below an endpoint value; a flat point with no sign change). Rule 4 on BC-REP-02 in BC-SKL-05012, 05013.
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full), in served order: prediction, orientation, the three bridges, ki-1, ki-2, st-1 with its contrast pair, st-2, st-3, ex-1 with its scoring line, chk-1, the four error blocks, chk-2, chk-3. 697 words, 4.7 minutes (cap 900 and 6). There is one worked example, so nothing is faded.
- Mid (brief): prediction, orientation, the bridges, ki-1, ki-2, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-05009, err-BC-ERR-05010, chk-2. 449 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, ki-2, err-BC-ERR-05009, err-BC-ERR-05010, err-BC-ERR-05011, err-BC-ERR-05012, ex-1.

## Sources

- BC-CON-05003; BC-SKL-05010 to BC-SKL-05013; BC-EK-FUN-1C2, BC-EK-FUN-1C3; ced:100
- BC-QA-05014, BC-QA-05006, BC-QA-05003, BC-QA-05007, BC-QA-05010; BC-FRQ-2013-Q4-B, BC-FRQ-2022-Q3-D, BC-FRQ-2023-Q4-D, BC-FRQ-2025-Q1-D, BC-FRQ-2025-Q4-D, BC-FRQ-2026-Q4-D
- BC-PT-99013; sg-25:5, sg-25:19, sg-23:13
- BC-ERR-05009, BC-ERR-05010, BC-ERR-05011, BC-ERR-05012, BC-ERR-05013; BC-MIS-05009, BC-MIS-05007
- BC-PRQ-05001, BC-PRQ-05003, BC-PRQ-05006
- research/units/unit-05-analytical-applications-differentiation.md#5.2 Extreme Value Theorem, Global Versus Local Extrema, and Critical Points
- research/question-analysis/question-archetypes.md#BC-QA-05014 Every critical point found, including inputs where the derivative fails to exist
- research/question-analysis/question-archetypes.md#BC-QA-05006 Absolute extremum by the candidates test with a global justification
- research/question-analysis/question-archetypes.md#BC-QA-05003 Relative extremum classified from the behaviour of the first derivative
- research/scoring/justification-requirements.md#Global versus local arguments
- research/scoring/justification-requirements.md#Sign analysis of a derivative
- research/scoring/common-point-losses.md#Justification points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Every figure choice. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-05003",
 "kind": "concept",
 "target_id": "BC-CON-05003",
 "unit": "05",
 "skills": [
  "BC-SKL-05010",
  "BC-SKL-05011",
  "BC-SKL-05012",
  "BC-SKL-05013"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "f(x) = 3(x - 1)^(2/3)/(x + 2) and f'(x) = (7 - x)/((x - 1)^(1/3)(x + 2)^2). Which inputs are critical points?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "7 only",
    "is_key": false
   },
   {
    "id": "B",
    "label": "1 and 7",
    "is_key": true
   },
   {
    "id": "C",
    "label": "-2, 1 and 7",
    "is_key": false
   }
  ],
  "resolution": "f' is zero at 7 and undefined at 1, where f is defined. At -2, f is undefined.",
  "sources": [
   "BC-CON-05003",
   "ced:100"
  ]
 },
 "orientation": {
  "text": "A response writes f'(x) = 0 and adds the inputs where f' fails to exist.",
  "sources": [
   "BC-CON-05003",
   "research/units/unit-05-analytical-applications-differentiation.md#5.2 Extreme Value Theorem, Global Versus Local Extrema, and Critical Points"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-1C2",
   "depth": "core",
   "text": "Critical points: f'(c) = 0 or f'(c) failing to exist (cusp, corner, vertical tangent), with c in the domain.",
   "notation": "critical point",
   "quote": null,
   "sources": [
    "BC-EK-FUN-1C2",
    "ced:100",
    "research/units/unit-05-analytical-applications-differentiation.md#5.2 Extreme Value Theorem, Global Versus Local Extrema, and Critical Points"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-1C3",
   "depth": "core",
   "text": "Every relative extremum sits at a critical point, not conversely. A relative extremum beats nearby values; an absolute one beats every value.",
   "notation": "relative extremum; absolute extremum",
   "quote": null,
   "sources": [
    "BC-EK-FUN-1C3",
    "ced:100",
    "sg-23:13",
    "research/units/unit-05-analytical-applications-differentiation.md#5.2 Extreme Value Theorem, Global Versus Local Extrema, and Critical Points"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-05014",
   "cue": "All critical points, from a quotient with a fractional power.",
   "method": "f'(x).",
   "rival": "Setting only f'(x) = 0.",
   "separating_feature": "A fractional power can make f' undefined.",
   "sources": [
    "BC-QA-05014"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find all critical points of f(x) = 5(x + 2)^(2/3)/(x - 4).",
     "archetype_id": "BC-QA-05014"
    },
    "not_this": {
     "text": "Solve f'(x) = 0 for f(x) = 5(x + 2)^(2/3)/(x - 4).",
     "why_not": "It asks only for zeros of f'."
    },
    "feature": "All critical points, or only zeros of f'."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-05006",
   "cue": "Absolute extremum on a closed interval, from f or f' and the interval.",
   "method": "f'(x) = 0, as an equation.",
   "rival": "Citing the Extreme Value Theorem to locate it.",
   "separating_feature": "Absolute asks for a comparison with every candidate.",
   "sources": [
    "BC-QA-05006"
   ],
   "evidence_tag": "verified"
  },
  {
   "id": "st-3",
   "archetype_id": "BC-QA-05003",
   "cue": "Maximum, minimum or neither at a named input, from f' information.",
   "method": "Locate the input on f'.",
   "rival": "The second derivative test with the slope of f' never discussed.",
   "separating_feature": "No sign change means neither.",
   "sources": [
    "BC-QA-05003"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-05014",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "shape": "cusp",
    "root": 1,
    "pole": -2,
    "multiplier": 3
   },
   "problem": {
    "text": "Find all critical points of f(x) = 3(x - 1)^(2/3)/(x + 2).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "All critical points: start from f.",
     "why": "Both sources come from f'.",
     "expr": "3*(x - 1)**(2/3)/(x + 2)",
     "relation": "new"
    },
    {
     "cue": "Differentiate.",
     "why": "Quotient rule, then factor.",
     "expr": "(7 - x)/((x - 1)**(1/3)*(x + 2)**2)",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "cue": "Source one: f' = 0.",
     "why": "The equation is the scored line.",
     "expr": "7 - x = 0",
     "relation": "new",
     "point_type_id": "BC-PT-99013"
    },
    {
     "cue": "Solve.",
     "why": "One zero.",
     "expr": "7",
     "relation": "solve",
     "variable": "x"
    },
    {
     "cue": "Source two: denominator zero.",
     "why": "f' fails to exist there.",
     "expr": "(x - 1)**(1/3)*(x + 2)**2 = 0",
     "relation": "new"
    },
    {
     "cue": "Solve.",
     "why": "Two inputs.",
     "expr": "FiniteSet(-2, 1)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "cue": "Is f defined there?",
     "why": "f(-2) is undefined: out. f(1) = 0: a cusp, kept."
    },
    {
     "cue": "Collect.",
     "why": "Both sources, domain checked.",
     "expr": "FiniteSet(1, 7)",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "FiniteSet(1, 7)"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99013"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99013",
     "text": "Considers the derivative set equal to zero. Earned by: Presenting the equation derivative equals zero, or an equivalent equation, or discussing the sign change of the derivative, or using the phrase critical points of the function (sg-25:5, sg-26:17). Not earned by: Presenting only the solved critical value, which sg-25:5, sg-25:9, sg-26:17 and sg-25:19 all state is not sufficient."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-05009",
   "wrong_step": {
    "text": "x = 7 written alone.",
    "expr": "zeros_listed_only"
   },
   "right_step": {
    "text": "7 - x = 0 written.",
    "expr": "derivative_set_equal_to_zero"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05009"
   ],
   "observed_behavior": "The response writes down the inputs at which the derivative vanishes but never presents the equation setting the derivative equal to zero.",
   "scoring_consequence": "The first point of the candidates test is lost; the 2023 guideline states that listing the zeros is not sufficient.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05010",
   "wrong_step": {
    "text": "Unreduced f' numerator (7 - x)(x + 2) vanishes at -2: kept.",
    "expr": "FiniteSet(-2, 1, 7)"
   },
   "right_step": {
    "text": "f(-2) undefined: dropped.",
    "expr": "FiniteSet(1, 7)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05010"
   ],
   "observed_behavior": "The response keeps an input at which the derivative expression vanishes although the function itself is undefined there.",
   "scoring_consequence": "The candidate list is wrong and the comparison that follows cannot be correct.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05011",
   "wrong_step": {
    "text": "Only x = 7.",
    "expr": "FiniteSet(7)"
   },
   "right_step": {
    "text": "x = 1 and x = 7.",
    "expr": "FiniteSet(1, 7)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05009",
    "text": "does not look for corners, cusps, or vertical tangents"
   },
   "sources": [
    "BC-ERR-05011",
    "BC-MIS-05009"
   ],
   "observed_behavior": "The response finds only the zeros of the derivative and skips corners, cusps, and vertical tangents.",
   "scoring_consequence": "A candidate is missing, so the comparison may select the wrong extremum and the justification is incomplete.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05012",
   "wrong_step": {
    "text": "On [0, 10], the maximum is f(7).",
    "expr": "6**(2/3)/3"
   },
   "right_step": {
    "text": "f(0) = 3/2 is larger.",
    "expr": "3/2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05007",
    "text": "takes a local high or low point as the largest or smallest value on the whole interval"
   },
   "sources": [
    "BC-ERR-05012",
    "BC-MIS-05007"
   ],
   "observed_behavior": "The response finds a local high or low point and reports it as the largest or smallest value on the interval without comparing the rest.",
   "scoring_consequence": "The justification point is lost because the argument is local where a global claim was asked for.",
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-05001",
   "text": "Zero a factor."
  },
  {
   "prq_id": "BC-PRQ-05003",
   "text": "Keep inputs where f exists."
  },
  {
   "prq_id": "BC-PRQ-05006",
   "text": "Check whether the curve is f or f'."
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
    8
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    4,
    5,
    6,
    7
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
   "archetype_id": "BC-QA-05014",
   "parameter_draw": {
    "shape": "cusp",
    "root": 1,
    "pole": -2,
    "multiplier": 3
   },
   "completes": "ex-1",
   "stem": {
    "text": "f'(x) = (7 - x)/((x - 1)^(1/3)(x + 2)^2), zero at 7. Finish the critical point list.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "FiniteSet(1, 7)"
   },
   "steps": [
    {
     "text": "Denominator zero.",
     "expr": "(x - 1)**(1/3)*(x + 2)**2 = 0",
     "relation": "new"
    },
    {
     "text": "x = -2 or 1.",
     "expr": "FiniteSet(-2, 1)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "text": "-2 is outside the domain.",
     "expr": "FiniteSet(1, 7)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05011"
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
   "archetype_id": "BC-QA-05014",
   "parameter_draw": {
    "shape": "vertical",
    "root": 3,
    "pole": 1,
    "multiplier": 2
   },
   "stem": {
    "text": "Find all critical points of f(x) = 2(x - 3)^(1/3)/(x - 1).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "FiniteSet(3, 4)"
   },
   "steps": [
    {
     "text": "f.",
     "expr": "2*(x - 3)**(1/3)/(x - 1)",
     "relation": "new"
    },
    {
     "text": "f'.",
     "expr": "2*(8 - 2*x)/(3*(x - 3)**(2/3)*(x - 1)**2)",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "text": "f' = 0.",
     "expr": "8 - 2*x = 0",
     "relation": "new"
    },
    {
     "text": "x = 4.",
     "expr": "4",
     "relation": "solve",
     "variable": "x"
    },
    {
     "text": "f' fails at 3 (f defined) and 1 (not in domain).",
     "expr": "FiniteSet(3, 4)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05010",
    "BC-SKL-05011"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-05014",
   "parameter_draw": {
    "shape": "cusp",
    "root": -1,
    "pole": 2,
    "multiplier": -2
   },
   "stem": {
    "text": "f(x) = -2(x + 1)^(2/3)/(x - 2), f'(x) = 2(x + 7)/(3(x + 1)^(1/3)(x - 2)^2). Which response is complete?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "FiniteSet(-7, -1)",
    "label": "f'(x) = 0 at -7; f' undefined at -1: -7, -1."
   },
   "steps": [],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "-7 and -1, no equation written.",
     "error_path": "BC-ERR-05009",
     "derivation": "the list with the equation f'(x) = 0 never presented"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "f'(x) = 0 at -7; undefined at -1 and 2: -7, -1, 2.",
     "error_path": "BC-ERR-05010",
     "derivation": "x = 2 kept although f is undefined there"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "f'(x) = 0 at -7: -7 only.",
     "error_path": "BC-ERR-05011",
     "derivation": "the cusp at x = -1 skipped"
    },
    {
     "id": "D",
     "is_key": true,
     "label": "f'(x) = 0 at -7; f' undefined at -1: -7, -1.",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05010",
    "BC-SKL-05011"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-05010 to 05013; unit README delivery map",
   "sources": [
    "BC-SKL-05010",
    "BC-SKL-05011"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "curve": "3(x - 1)^(2/3)/(x + 2)",
    "window": {
     "x": [
      -1,
      12
     ],
     "y": [
      -0.5,
      2
     ]
    },
    "points": [
     {
      "at": [
       1,
       0
      ],
      "style": "filled"
     },
     {
      "at": [
       7,
       1.1
      ],
      "style": "filled"
     }
    ],
    "labels": [
     {
      "text": "x = 1: f' does not exist (cusp)",
      "placement": "inside"
     },
     {
      "text": "x = 7: f' = 0",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same graph static, both points and labels shown",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-05010, 05011; BC-QA-05014 difficulty_variables name a categorical shape, so static",
   "sources": [
    "BC-SKL-05011",
    "BC-QA-05014"
   ],
   "spec": {
    "kind": "graph_panels",
    "representations": [
     "BC-REP-02"
    ],
    "panels": [
     {
      "curves": [
       {
        "expr": "2 - x**2"
       }
      ],
      "points": [
       {
        "x": 0
       }
      ]
     },
     {
      "curves": [
       {
        "expr": "abs(x)**(2/3)"
       }
      ],
      "points": [
       {
        "x": 0
       }
      ]
     },
     {
      "curves": [
       {
        "expr": "abs(x)"
       }
      ],
      "points": [
       {
        "x": 0
       }
      ]
     },
     {
      "curves": [
       {
        "expr": "x**(1/3)"
       }
      ],
      "points": [
       {
        "x": 0
       }
      ]
     }
    ],
    "labels": [
     {
      "text": "f' = 0",
      "placement": "inside"
     },
     {
      "text": "cusp: f' does not exist",
      "placement": "inside"
     },
     {
      "text": "corner: f' does not exist",
      "placement": "inside"
     },
     {
      "text": "vertical tangent: f' does not exist",
      "placement": "inside"
     }
    ],
    "window": {
     "x": [
      -2,
      2
     ],
     "y": [
      -2,
      3
     ]
    }
   },
   "fallback": "four static panels in a row with the same labels",
   "keyboard": "no control; the panels are read in order with Tab"
  },
  {
   "block": "ki-2",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-05012, 05013",
   "sources": [
    "BC-SKL-05012",
    "BC-SKL-05013"
   ],
   "spec": {
    "kind": "graph_panels",
    "representations": [
     "BC-REP-02"
    ],
    "panels": [
     {
      "window": {
       "x": [
        -1,
        4.5
       ],
       "y": [
        2,
        8
       ]
      },
      "curves": [
       {
        "expr": "-x**3/3 + 2*x**2 - 3*x + 5",
        "domain": [
         -0.5,
         4
        ]
       }
      ],
      "points": [
       {
        "x": -0.5
       },
       {
        "x": 3
       },
       {
        "x": 4
       }
      ],
      "labels": [
       {
        "text": "relative max, not absolute",
        "placement": "inside",
        "at": "above (3, 5)"
       },
       {
        "text": "endpoint higher",
        "placement": "inside",
        "at": "right (-0.5, 7.042)"
       }
      ]
     },
     {
      "window": {
       "x": [
        -2,
        2
       ],
       "y": [
        -3,
        3
       ]
      },
      "curves": [
       {
        "expr": "x**3"
       }
      ],
      "points": [
       {
        "x": 0,
        "y": 0
       }
      ],
      "labels": [
       {
        "text": "f' = 0, no sign change: neither",
        "placement": "inside"
       }
      ]
     }
    ]
   },
   "fallback": "the two panels static with the same labels",
   "keyboard": "no control; the panels are read in order with Tab"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05009",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05010",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05011",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05012",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-05009",
  "err-BC-ERR-05010",
  "err-BC-ERR-05011",
  "err-BC-ERR-05012",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/justification-requirements.md",
   "line": "The sharpest recurring rule is that a local argument does not justify a global claim."
  }
 ],
 "inferred": [
  {
   "claim": "The orientation, ki-1 and ki-2 are served as static figures rather than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-05003",
  "BC-EK-FUN-1C2",
  "BC-EK-FUN-1C3",
  "ced:100",
  "BC-QA-05014",
  "BC-QA-05006",
  "BC-QA-05003",
  "BC-QA-05007",
  "BC-QA-05010",
  "BC-PT-99013",
  "sg-25:5",
  "sg-25:19",
  "sg-23:13",
  "BC-ERR-05009",
  "BC-ERR-05010",
  "BC-ERR-05011",
  "BC-ERR-05012",
  "BC-ERR-05013",
  "BC-MIS-05009",
  "BC-MIS-05007",
  "BC-PRQ-05001",
  "BC-PRQ-05003",
  "BC-PRQ-05006",
  "research/units/unit-05-analytical-applications-differentiation.md#5.2 Extreme Value Theorem, Global Versus Local Extrema, and Critical Points",
  "research/question-analysis/question-archetypes.md#BC-QA-05014 Every critical point found, including inputs where the derivative fails to exist",
  "research/question-analysis/question-archetypes.md#BC-QA-05006 Absolute extremum by the candidates test with a global justification",
  "research/question-analysis/question-archetypes.md#BC-QA-05003 Relative extremum classified from the behaviour of the first derivative",
  "research/scoring/justification-requirements.md#Global versus local arguments",
  "research/scoring/justification-requirements.md#Sign analysis of a derivative",
  "research/scoring/common-point-losses.md#Justification points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 696,
  "brief": 448
 },
 "read_minutes": {
  "full": 4.7,
  "brief": 3.0
 }
}
```
