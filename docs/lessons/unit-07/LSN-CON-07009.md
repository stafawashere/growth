---
title: LSN-CON-07009 Domain restrictions on a particular solution
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-07009, the interval on which a particular solution holds, built from authoring_bundle("BC-CON-07009") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-07009 Domain restrictions on a particular solution

Concept BC-CON-07009 (skill BC-SKL-07031), topic 7.7 of Unit 7, loaded by BC-QA-07011. Its hard parent in Unit 7 is BC-CON-07007 (docs/lessons/unit-07/README.md, section 1).

## Prediction

Form mcq, both bands, on ex-1's own numbers. The stem gives the formula y = 1/(4 - 2x), which solves the equation and is undefined at x = 2, and asks where the solution through (1, 1/2) exists. Key B: only on the side of x = 2 holding x = 1. The distractors are every x and only x = 1. The stem needs no rule to read and asks for the domain claim, not ex-1's interval. The resolution restates the interval rule of BC-EK-FUN-7E3 (ced:143). Delivery: text.

## Orientation

Served text, from BC-CON-07009 `description_plain` and the topic's Domain restriction and Assessment behaviour paragraphs (research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables): the particular solution comes with the interval containing the initial input on which the formula is defined.

## Key ideas

- ki-1 (core, both bands), BC-EK-FUN-7E3 (ced:143). Paraphrase of the Domain restriction paragraph. The clause on why the other piece is excluded is [inferred]. Notation line from the concept record. No anchor quote.

## Recognition

BC-QA-07011 (research/question-analysis/question-archetypes.md#BC-QA-07011 Particular solution with a domain restriction or an accumulation form): `typical_wording` "find the particular solution ... and state the interval on which the solution is valid"; `asked_to_produce` the particular solution and the interval of validity; `common_givens` a differential equation and an initial condition. The signal: the words interval, domain or valid beside particular solution, or a solution formula with a denominator or a logarithm. Shape: one no-calculator FRQ part or one MCQ; no `official_examples`.

Not this concept: a particular solution with no interval asked (BC-CON-07008), or a right side in x alone (the accumulation form, no break).

The near miss on the contrast pair is the same equation and initial condition with no interval asked: a particular solution alone (BC-CON-07008), where no domain statement is demanded. The feature is the words "the interval on which it is valid".

## Method choice

- st-1, BC-QA-07011, both bands. Method, `expected_solution_path`: produce the general solution, fix the constant and branch, then identify where the expression fails to be defined (step 3) and report the interval containing the initial input. Rival, `wrong_approaches`: choosing the branch by the sign of the constant rather than by the initial condition. Separating feature: the interval must contain x0. The archetype carries `asked_to_produce` and `common_givens`.

The strategy fields carry no leading label, since the reader prints Cue, First line, Rival and Separating feature. st-1 carries the contrast pair, served in both bands.

## Solution path

- ex-1, BC-QA-07011, both bands, no calculator. Draw: form restricted, rate 2, initial 1/2, start 1, so dy/dx = 2y^2 with y(1) = 1/2; blowup 1 + 1/(2 * 1/2) = 2, k y0 > 0, so the interval is left of 2. No published BC-QA-07011 draw matches.
- Steps: separated (new); antiderivatives with C (new); initial values (evaluate); C (solve); y (new); denominator zero (new); the break (solve); the interval (new).
- A fluent solver writes every line; the side choice is one clause beside the interval [inferred].

One worked example only, so there is no fade.

## Scoring

BC-QA-07011 lists no `point_types`, so no what_a_reader_scores entry and no point tag; the served text names no point beyond the error record's scoring_consequence.

## Traps

One error meets the skill: BC-ERR-07031, both bands, on ex-1's draw: every x claimed against x < 2. Possible reason from BC-MIS-07019.

## Representations

None. The topic's Representations paragraph names symbolic conversions only.

## Prerequisite bridge

- BC-PRQ-05003, from its `description_plain` and `failure_signature`.

## Time

BC-QA-07011 is `no_calculator`, one FRQ part or one MCQ; the FRQ form is taken, Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred]. No points are recorded (docs/lessons/unit-07/README.md, section 5). The minutes go on the solution; the break and the side are two short lines.

## Checks

- chk-1, completion of ex-1, both bands: the solution is given; the student states the interval. Key x < 2.
- chk-2, isomorph, both bands. Draw: restricted, rate -1, initial 2, start 0; blowup -1/2, k y0 < 0, so the right side. Key x > -1/2.
- No chk-3: one error record only, so no MCQ with three error paths [inferred].

## Delivery

- orientation, ki-1: text, rule 6: BC-REP-01 and BC-REP-04 only (docs/lessons/unit-07/README.md, section 6).
- ex-1 and err-BC-ERR-07031: step_reveal, rule 1.

- No drawn block: the machine record carries `no_figure_reason`. No skill lists a figure-bearing BC-REP and no key idea describes a process.
- pr-1: text, rule 6.

## Band plan

- Low (full), in served order: prediction, orientation, the bridge, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-07031, chk-2. 436 words, 2.91 minutes (cap 900 and 6).
- Mid (brief), in served order: the same blocks. 436 words, 2.91 minutes (cap 450 and 3). The orientation, the bridge, the strategy fields, the ki-1 text and the ex-1 cues were shortened to fit 450.
- Refresher: the core key ideas, the error blocks, ex-1.

## Sources

- BC-CON-07009; BC-SKL-07031; BC-EK-FUN-7E3; ced:143
- BC-QA-07011
- BC-ERR-07031; BC-MIS-07019
- BC-PRQ-05003
- research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables
- research/question-analysis/question-archetypes.md#BC-QA-07011 Particular solution with a domain restriction or an accumulation form
- research/exam/exam-structure.md#Section and part layout
- pr-1 and the contrast pair draw on the concept record, the key idea's BC-EK and the cited topic section.
- [inferred] Two checks, one error record. Settled by more BC-ERR records on BC-SKL-07031.
- [inferred] Part II-B. Settled by a BC-PT mapping for BC-QA-07011.
- [inferred] Why the other piece is excluded. Settled by a cached source sentence.
- [inferred] integrand set to gauss on a restricted draw. Settled by the spec.

## Machine record

```json
{
 "id": "LSN-CON-07009",
 "kind": "concept",
 "target_id": "BC-CON-07009",
 "unit": "07",
 "skills": [
  "BC-SKL-07031"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Before the rule: y = 1/(4 - 2x) solves dy/dx = 2y^2, y(1) = 1/2, and is undefined at x = 2. Where does the solution exist?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "For every x.",
    "is_key": false
   },
   {
    "id": "B",
    "label": "Only on the side of x = 2 holding x = 1.",
    "is_key": true
   },
   {
    "id": "C",
    "label": "Only at x = 1.",
    "is_key": false
   }
  ],
  "resolution": "The solution lives on the largest interval containing x = 1 where the formula is defined: x < 2.",
  "sources": [
   "BC-CON-07009",
   "BC-EK-FUN-7E3",
   "research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables"
  ]
 },
 "no_figure_reason": "The rule is a domain statement read from a formula's denominator. No skill carries a figure-bearing representation and no key idea describes a process, so nothing here is drawn.",
 "orientation": {
  "text": "A response gives the particular solution and the interval containing the initial input on which its formula is defined.",
  "sources": [
   "BC-CON-07009",
   "research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-7E3",
   "depth": "core",
   "text": "A solution formula can fail to be defined where a denominator vanishes or a logarithm or root loses its domain. The particular solution is taken on the largest interval containing the initial input on which the formula is defined. The curve through the initial point cannot cross the break.",
   "notation": "domain restriction; interval containing the initial input",
   "quote": null,
   "sources": [
    "BC-EK-FUN-7E3",
    "ced:143",
    "research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-07011",
   "cue": "The stem asks for the interval of validity.",
   "method": "The solution's denominator set equal to zero, then the side holding the initial input.",
   "rival": "Choosing the branch by the constant's sign, not the initial condition.",
   "separating_feature": "The interval must contain the initial input.",
   "sources": [
    "BC-QA-07011"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "dy/dx = y^2/2, y(0) = 1. Find the particular solution and state the interval on which it is valid.",
     "archetype_id": "BC-QA-07011"
    },
    "not_this": {
     "text": "dy/dx = y^2/2, y(0) = 1. Find the particular solution.",
     "why_not": "No interval is asked."
    },
    "feature": "The words \"the interval on which it is valid\"."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-07011",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "form": "restricted",
    "rate": 2,
    "initial": "1/2",
    "start": 1,
    "integrand": "gauss"
   },
   "problem": {
    "text": "dy/dx = 2y^2 with y(1) = 1/2. Find the interval on which the particular solution is valid.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The right side is in y only.",
     "why": "Separate: y with dy.",
     "expr": "dy/y**2 = 2*dx",
     "relation": "new"
    },
    {
     "cue": "One variable per side.",
     "why": "Integrate each; one C.",
     "expr": "-1/y = 2*x + C",
     "relation": "new"
    },
    {
     "cue": "y(1) = 1/2.",
     "why": "Fix C first.",
     "expr": "-2 = 2 + C",
     "relation": "evaluate",
     "subs": {
      "x": "1",
      "y": "1/2"
     }
    },
    {
     "cue": "One unknown.",
     "why": "Solve for C.",
     "expr": "-4",
     "relation": "solve",
     "variable": "C"
    },
    {
     "cue": "Solve for y.",
     "why": "So y = 1/(4 - 2x).",
     "expr": "y = 1/(4 - 2*x)",
     "relation": "new"
    },
    {
     "cue": "A quotient: where is it undefined?",
     "why": "The denominator vanishes there.",
     "expr": "4 - 2*x = 0",
     "relation": "new"
    },
    {
     "cue": "The break.",
     "why": "x = 2 splits the line.",
     "expr": "2",
     "relation": "solve",
     "variable": "x"
    },
    {
     "cue": "The initial input 1 lies left of 2.",
     "why": "The largest interval holding 1 where it is defined.",
     "expr": "Interval(-oo, 2, True, True)",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "Interval(-oo, 2, True, True)"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-07031",
   "observed_behavior": "The response claims the solution formula holds for every input, or reports an interval that does not contain the initial input.",
   "scoring_consequence": "A demanded domain statement is lost and the reported solution overreaches.",
   "wrong_step": {
    "text": "y = 1/(4 - 2x) claimed for every x.",
    "expr": "Interval(-oo, oo)"
   },
   "right_step": {
    "text": "Only x < 2, the side holding x = 1.",
    "expr": "Interval(-oo, 2, True, True)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07019",
    "text": "reports the algebraic expression with no regard for where it is defined or which branch contains the initial point"
   },
   "sources": [
    "BC-ERR-07031",
    "BC-MIS-07019"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-05003",
   "text": "The domain is the set of inputs where the function is defined."
  }
 ],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8
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
   "archetype_id": "BC-QA-07011",
   "parameter_draw": {
    "form": "restricted",
    "rate": 2,
    "initial": "1/2",
    "start": 1,
    "integrand": "gauss"
   },
   "completes": "ex-1",
   "stem": {
    "text": "y = 1/(4 - 2x) solves dy/dx = 2y^2 with y(1) = 1/2. State the interval on which it is the particular solution.",
    "command_verb": "state"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval(-oo, 2, True, True)"
   },
   "steps": [
    {
     "text": "Denominator zero.",
     "expr": "4 - 2*x = 0",
     "relation": "new"
    },
    {
     "text": "The break.",
     "expr": "2",
     "relation": "solve",
     "variable": "x"
    },
    {
     "text": "The side holding x = 1.",
     "expr": "Interval(-oo, 2, True, True)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07031"
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
   "archetype_id": "BC-QA-07011",
   "parameter_draw": {
    "form": "restricted",
    "rate": -1,
    "initial": "2",
    "start": 0,
    "integrand": "gauss"
   },
   "stem": {
    "text": "dy/dx = -y^2 with y(0) = 2. Find the interval on which the particular solution is valid.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval(-1/2, oo, True, True)"
   },
   "steps": [
    {
     "text": "Separate.",
     "expr": "dy/y**2 = -dx",
     "relation": "new"
    },
    {
     "text": "Integrate.",
     "expr": "-1/y = -x + C",
     "relation": "new"
    },
    {
     "text": "x = 0, y = 2.",
     "expr": "-1/2 = C",
     "relation": "evaluate",
     "subs": {
      "x": "0",
      "y": "2"
     }
    },
    {
     "text": "C.",
     "expr": "-1/2",
     "relation": "solve",
     "variable": "C"
    },
    {
     "text": "Solve for y.",
     "expr": "y = 2/(2*x + 1)",
     "relation": "new"
    },
    {
     "text": "Denominator zero.",
     "expr": "2*x + 1 = 0",
     "relation": "new"
    },
    {
     "text": "The break.",
     "expr": "-1/2",
     "relation": "solve",
     "variable": "x"
    },
    {
     "text": "The side holding x = 0.",
     "expr": "Interval(-1/2, oo, True, True)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07031"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows; BC-REP-01 and BC-REP-04 only on BC-SKL-07031",
   "sources": [
    "BC-SKL-07031"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a rule about where a formula is defined; BC-REP-01, BC-REP-04 on BC-SKL-07031, none figure-bearing",
   "sources": [
    "BC-SKL-07031"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07031",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-07031",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-07-differential-equations.md",
   "line": "A particular solution is taken on the largest interval containing the initial input on which the expression is defined and continuous"
  }
 ],
 "inferred": [
  {
   "claim": "The bundle holds one error for this concept (BC-ERR-07031), fewer than the three distinct error paths check 3 needs, so the lesson carries two checks.",
   "settles": "Further BC-ERR records on BC-SKL-07031, for example an interval reported on the wrong side of the break."
  },
  {
   "claim": "The exam part is II-B: BC-QA-07011 is one FRQ part or one MCQ and carries no point_types.",
   "settles": "A BC-PT mapping or an official example for BC-QA-07011."
  },
  {
   "claim": "The reason that the other piece belongs to a different solution (the curve through the initial point cannot cross the break) paraphrases BC-EK-FUN-7E3 beyond its wording.",
   "settles": "A cached CED or scoring guideline sentence stating why the interval must contain the initial input."
  },
  {
   "claim": "The integrand label is irrelevant to the restricted form and is set to gauss only to complete the draw.",
   "settles": "A parameter_spec that drops integrand when form is restricted."
  }
 ],
 "sources": [
  "BC-CON-07009",
  "BC-SKL-07031",
  "BC-EK-FUN-7E3",
  "ced:143",
  "BC-QA-07011",
  "BC-ERR-07031",
  "BC-MIS-07019",
  "BC-PRQ-05003",
  "research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables",
  "research/question-analysis/question-archetypes.md#BC-QA-07011 Particular solution with a domain restriction or an accumulation form",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 436,
  "brief": 436
 },
 "read_minutes": {
  "full": 2.91,
  "brief": 2.91
 }
}
```
