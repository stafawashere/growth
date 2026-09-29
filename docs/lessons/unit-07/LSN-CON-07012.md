---
title: LSN-CON-07012 Carrying capacity and the point of fastest change
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-07012, the carrying capacity and the value of fastest change in a logistic model, built from authoring_bundle("BC-CON-07012") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-07012 Carrying capacity and the point of fastest change

Concept BC-CON-07012 (skills BC-SKL-07040, BC-SKL-07041, BC-SKL-07042), topic 7.9 of Unit 7 (BC only), loaded by BC-QA-07009. Its hard parents are BC-CON-07005 and BC-CON-07011 through BC-SKL-07039 (docs/lessons/unit-07/README.md, section 1).

## Orientation

Served text, from BC-CON-07012 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations): the capacity from the zeros, the limit with the sign as reason, and the fastest change at half the capacity, with nothing solved.

## Key ideas

Three BC-EK statements; at most two core.

- ki-1 (core), BC-EK-FUN-7H3 (ced:145). Paraphrase of the Carrying capacity paragraph. Served as an interactive.
- ki-2 (core), BC-EK-FUN-7H4 (ced:145). Paraphrase of the Fastest change paragraph.
- ki-3 (extended, low band), BC-EK-FUN-7H2 (ced:145). Paraphrase of the Reasoning without solving paragraph.

No anchor quotes.

## Recognition

BC-QA-07009 (research/question-analysis/question-archetypes.md#BC-QA-07009 Logistic model interpreted without solving): `typical_wording` "find the limit of the quantity as the independent variable grows without bound, and the value of the quantity when it is changing fastest"; `common_givens` a logistic equation and an initial value strictly between zero and the carrying capacity; `asked_to_produce` the carrying capacity, the limiting value, the fastest change value. Shape: one or two FRQ parts or one MCQ; `official_examples` BC-MCQ-CED-017, BC-MCQ-PE2012-014.

The confusable set LSN-DEC-07-01 (BC-SKL-07041 against BC-SKL-07042, docs/lessons/unit-07/README.md, section 3) is decided by the words of the stem: "limit ... grows without bound" selects the zeros and the sign; "when it is changing fastest" selects the vertex of the right side. Not this concept: an exponential model, whose right side has one zero.

## Method choice

- st-1, BC-QA-07009, both bands. Method, `expected_solution_path[0]`: read the zeros of the right side; then the sign at the initial value (step 3) or the maximum of the quadratic (step 4). Rival, `wrong_approaches`: partial fractions when only the limit was asked for. Separating feature: the asked quantity, limit or fastest change. The archetype carries `asked_to_produce` and `common_givens`.

## Solution path

- ex-1, BC-QA-07009, both bands, no calculator. Draw: expanded, capacity 800, rate 2/5, start share 1/5, fish, so P(0) = 160 and half = 400. No published BC-QA-07009 draw matches.
- Steps: right side zero (new); zeros (solve); right side (new); its value at 160 (evaluate); right side (new); its derivative in P (differentiate); the vertex (solve); both values (new).
- A fluent solver writes the zeros, the sign value, the derivative, the vertex and the pair [inferred].

## Scoring

BC-QA-07009 lists no `point_types`, so no what_a_reader_scores entry and no point tag; the served text names no point beyond the error records' scoring_consequence.

## Traps

Four errors meet the skills, in the bundle's order, mid band the first two. All on ex-1's draw.

- err-BC-ERR-07040: 2/5 as the capacity. Possible reason from BC-MIS-07025.
- err-BC-ERR-07041: 800 with no reason; equal values, relation equivalent. No possible reason line.
- err-BC-ERR-07042: fastest at 800. Possible reason from BC-MIS-07027.
- err-BC-ERR-07044: the solved formula. Possible reason from BC-MIS-07025.

## Representations

None as a separate block. The topic's Representations paragraph names BC-REP-04, 05, 06; the process picture is ki-1's interactive.

## Prerequisite bridge

- BC-PRQ-05001, from its `description_plain` and `failure_signature`.

## Time

BC-QA-07009 is `either`, one or two FRQ parts or one MCQ; the MCQ shape is taken, Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]. The vertex is half the capacity, held in the head once the zeros are read (docs/lessons/unit-07/README.md, section 5).

## Checks

- chk-1, completion of ex-1, both bands. Key (800, 400).
- chk-2, isomorph, both bands. Draw: factored, capacity 1200, rate 1/3, start share 1/4, app. Key (1200, 600).
- chk-3, MCQ, low band. Draw: factored, capacity 1000, rate 1/5, start share 1/10, fish. Key 500. Distractors: 1000 (BC-ERR-07042), 1/10 and 0 (BC-ERR-07040).

## Delivery

- orientation, ki-2, ki-3: text, rule 6.
- ki-1: interactive, rule 3. The limit is a process idea; the student steps P(0) through 160, 400, 640 and 960 and reads the level approached and the sign at the start. BC-QA-07009 `difficulty_variables` names the initial value above or below the capacity. This departs from the unit README's text choice, which predates the rule 3 clause [inferred; settled by the modality A/B].
- ex-1 and the four error blocks: step_reveal, rule 1.

## Band plan

- Low (full): orientation, ki-1 to ki-3, st-1, ex-1, the four error blocks, chk-1 to chk-3, the bridge. 568 words, 3.8 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, ki-2, st-1, ex-1, err-BC-ERR-07040, err-BC-ERR-07041, chk-1, chk-2, the bridge. 418 words, 2.8 minutes (cap 450 and 3).
- Refresher: ki-1, ki-2, the four error blocks, ex-1.

## Sources

- BC-CON-07012; BC-SKL-07040, BC-SKL-07041, BC-SKL-07042; BC-EK-FUN-7H2, BC-EK-FUN-7H3, BC-EK-FUN-7H4; ced:145
- BC-QA-07009; BC-MCQ-CED-017, BC-MCQ-PE2012-014
- BC-ERR-07040, BC-ERR-07041, BC-ERR-07042, BC-ERR-07044; BC-MIS-07025, BC-MIS-07027
- BC-PRQ-05001
- research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations
- research/question-analysis/question-archetypes.md#BC-QA-07009 Logistic model interpreted without solving
- research/exam/exam-structure.md#Section and part layout
- [inferred] Part I-A for an either archetype. Settled by an official calculator status.
- [inferred] ki-1 as an interactive. Settled by the modality A/B.
- [inferred] Stepper values beyond the spec. Settled by an interactive parameter_spec.
- [inferred] Two distractors on BC-ERR-07040. Settled by a further error record.
- [inferred] The solved formula in the BC-ERR-07044 step. Settled by a CAS check.
- [inferred] Written and held steps. Settled by per-step timing data.

## Machine record

```json
{
 "id": "LSN-CON-07012",
 "kind": "concept",
 "target_id": "BC-CON-07012",
 "unit": "07",
 "skills": [
  "BC-SKL-07040",
  "BC-SKL-07041",
  "BC-SKL-07042"
 ],
 "orientation": {
  "text": "A response reads the carrying capacity from the zeros of the right side, gives the limit with the sign of the rate at the initial value as its reason, and places the fastest change at half the carrying capacity. Nothing is solved.",
  "sources": [
   "BC-CON-07012",
   "research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-7H3",
   "depth": "core",
   "text": "The right side ky(a - y) is zero at y = 0 and y = a. A solution starting strictly between them has a positive rate and rises toward a, so a is the limit as t grows without bound. The reason is the sign of the rate, not a solved formula.",
   "notation": "carrying capacity",
   "quote": null,
   "sources": [
    "BC-EK-FUN-7H3",
    "ced:145",
    "research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-7H4",
   "depth": "core",
   "text": "As a function of y the right side is a quadratic with zeros 0 and a, so it is largest at y = a/2. The quantity changes fastest at half the carrying capacity; at a the rate is zero.",
   "notation": "half of the carrying capacity",
   "quote": null,
   "sources": [
    "BC-EK-FUN-7H4",
    "ced:145",
    "research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations"
   ]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-FUN-7H2",
   "depth": "extended",
   "text": "Both values come from the equation and the initial value alone. The solution also has a point of inflection at a/2.",
   "notation": "the limit as t grows without bound",
   "quote": null,
   "sources": [
    "BC-EK-FUN-7H2",
    "ced:145",
    "research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-07009",
   "cue": "A logistic equation and an initial value; the stem asks for the limit, or the value when changing fastest.",
   "method": "First written line: the zeros of the right side; then the sign, or the vertex.",
   "rival": "Rival: separating the logistic equation with partial fractions when only the limit was asked for.",
   "separating_feature": "Limit: zeros and sign. Fastest: vertex of the right side.",
   "sources": [
    "BC-QA-07009"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-07009",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "form": "expanded",
    "capacity": 800,
    "rate": "2/5",
    "start_share": "1/5",
    "context": "fish"
   },
   "problem": {
    "text": "Fish P: dP/dt = 2P/5 - P^2/2000, P(0) = 160. Find the limit of P(t) and the value of P when it grows fastest.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "A limit: the equilibria.",
     "why": "Zeros of the right side.",
     "expr": "2*P/5 - P**2/2000 = 0",
     "relation": "new"
    },
    {
     "cue": "Solve.",
     "why": "800 is the carrying capacity.",
     "expr": "FiniteSet(0, 800)",
     "relation": "solve",
     "variable": "P"
    },
    {
     "cue": "P(0) = 160 is between.",
     "why": "The sign there gives the direction.",
     "expr": "2*P/5 - P**2/2000",
     "relation": "new"
    },
    {
     "cue": "At P = 160.",
     "why": "Positive: P rises toward 800.",
     "expr": "256/5",
     "relation": "evaluate",
     "subs": {
      "P": "160"
     }
    },
    {
     "cue": "Fastest: the largest rate.",
     "why": "Maximise the quadratic right side.",
     "expr": "2*P/5 - P**2/2000",
     "relation": "new"
    },
    {
     "cue": "Differentiate in P.",
     "why": "The vertex is where this is zero.",
     "expr": "2/5 - P/1000",
     "relation": "differentiate",
     "variable": "P"
    },
    {
     "cue": "Solve.",
     "why": "Half of 800.",
     "expr": "400",
     "relation": "solve",
     "variable": "P"
    },
    {
     "cue": "Both values asked.",
     "why": "Limit 800; fastest at 400.",
     "expr": "Tuple(800, 400)",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "Tuple(800, 400)"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-07040",
   "observed_behavior": "The response reports the constant of proportionality, or zero, as the carrying capacity.",
   "scoring_consequence": "Every later value built on the capacity is wrong.",
   "wrong_step": {
    "text": "2/5 read as the capacity.",
    "expr": "2/5"
   },
   "right_step": {
    "text": "The nonzero zero.",
    "expr": "800"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07025",
    "text": "does not read the capacity off the zeros of the right side"
   },
   "sources": [
    "BC-ERR-07040",
    "BC-MIS-07025"
   ]
  },
  {
   "error_id": "BC-ERR-07041",
   "observed_behavior": "The response names a limit without saying why solutions move toward it from the given initial value.",
   "scoring_consequence": "The reason point is lost even when the value is right.",
   "wrong_step": {
    "text": "800, no reason.",
    "expr": "800"
   },
   "right_step": {
    "text": "Rate positive at 160, zero at 800.",
    "expr": "800"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-07041"
   ]
  },
  {
   "error_id": "BC-ERR-07042",
   "observed_behavior": "The response says the quantity changes fastest when it reaches its ceiling.",
   "scoring_consequence": "The value is wrong, and it contradicts the equation the response itself wrote.",
   "wrong_step": {
    "text": "Fastest at 800.",
    "expr": "800"
   },
   "right_step": {
    "text": "Fastest at 400.",
    "expr": "400"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07027",
    "text": "equates the largest value of the quantity with the largest value of its rate"
   },
   "sources": [
    "BC-ERR-07042",
    "BC-MIS-07027"
   ]
  },
  {
   "error_id": "BC-ERR-07044",
   "observed_behavior": "The response separates the logistic equation with partial fractions and solves it in order to report a limit the equation gives directly.",
   "scoring_consequence": "Time is spent on work the question did not ask for, and an error inside it costs the value that the equation alone would have given.",
   "wrong_step": {
    "text": "The solved formula first.",
    "expr": "800/(1 + 4*exp(-2*t/5))"
   },
   "right_step": {
    "text": "Zeros and sign.",
    "expr": "800"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07025",
    "text": "reaches for partial fractions instead"
   },
   "sources": [
    "BC-ERR-07044",
    "BC-MIS-07025"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-05001",
   "text": "Setting a factored expression equal to zero lists its zeros; without it, no equilibrium appears."
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
    6,
    7,
    8
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    3,
    5
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
   "archetype_id": "BC-QA-07009",
   "parameter_draw": {
    "form": "expanded",
    "capacity": 800,
    "rate": "2/5",
    "start_share": "1/5",
    "context": "fish"
   },
   "completes": "ex-1",
   "stem": {
    "text": "dP/dt = 2P/5 - P^2/2000, P(0) = 160; the limit is 800. Find P when fastest; give (limit, fastest).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Tuple(800, 400)"
   },
   "steps": [
    {
     "text": "The right side.",
     "expr": "2*P/5 - P**2/2000",
     "relation": "new"
    },
    {
     "text": "Its derivative in P.",
     "expr": "2/5 - P/1000",
     "relation": "differentiate",
     "variable": "P"
    },
    {
     "text": "Vertex.",
     "expr": "400",
     "relation": "solve",
     "variable": "P"
    },
    {
     "text": "Both values.",
     "expr": "Tuple(800, 400)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07042"
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
   "archetype_id": "BC-QA-07009",
   "parameter_draw": {
    "form": "factored",
    "capacity": 1200,
    "rate": "1/3",
    "start_share": "1/4",
    "context": "app"
   },
   "stem": {
    "text": "App users: dA/dt = (A/3)(1 - A/1200), A(0) = 300. Give (limit, value when fastest).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Tuple(1200, 600)"
   },
   "steps": [
    {
     "text": "Zeros.",
     "expr": "A/3*(1 - A/1200) = 0",
     "relation": "new"
    },
    {
     "text": "0 and 1200.",
     "expr": "FiniteSet(0, 1200)",
     "relation": "solve",
     "variable": "A"
    },
    {
     "text": "Right side.",
     "expr": "A/3*(1 - A/1200)",
     "relation": "new"
    },
    {
     "text": "Derivative.",
     "expr": "1/3 - A/1800",
     "relation": "differentiate",
     "variable": "A"
    },
    {
     "text": "Vertex.",
     "expr": "600",
     "relation": "solve",
     "variable": "A"
    },
    {
     "text": "Both.",
     "expr": "Tuple(1200, 600)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07041",
    "BC-SKL-07042"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-07009",
   "parameter_draw": {
    "form": "factored",
    "capacity": 1000,
    "rate": "1/5",
    "start_share": "1/10",
    "context": "fish"
   },
   "stem": {
    "text": "dF/dt = (F/5)(1 - F/1000), F(0) = 100. At what F is the fish population growing fastest?",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "500"
   },
   "steps": [
    {
     "text": "Right side.",
     "expr": "F/5*(1 - F/1000)",
     "relation": "new"
    },
    {
     "text": "Derivative.",
     "expr": "1/5 - F/2500",
     "relation": "differentiate",
     "variable": "F"
    },
    {
     "text": "Vertex.",
     "expr": "500",
     "relation": "solve",
     "variable": "F"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "1000",
     "error_path": "BC-ERR-07042",
     "derivation": "fastest placed at the ceiling"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "500",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "1/10",
     "error_path": "BC-ERR-07040",
     "derivation": "the constant 1/5 read as the capacity, then halved"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "0",
     "error_path": "BC-ERR-07040",
     "derivation": "zero read as the capacity, then halved"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07042"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows; BC-REP-06, BC-REP-04, BC-REP-01",
   "sources": [
    "BC-SKL-07040"
   ]
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 3: the limit as t grows without bound is a process idea, and its parameter, the initial value, is discrete and chosen by the student with one stepper; BC-QA-07009 difficulty_variables names whether the initial value is above or below the carrying capacity. The curve is the process's own picture, not a representation the stem carries (BC-SKL-07041 lists no figure-bearing BC-REP)",
   "sources": [
    "BC-SKL-07041",
    "BC-QA-07009"
   ],
   "spec": {
    "kind": "solution_curves",
    "representations": [
     "BC-REP-06"
    ],
    "equation": "dP/dt = 2P/5 - P^2/2000",
    "window": {
     "t": [
      0,
      30
     ],
     "P": [
      0,
      1000
     ]
    },
    "controls": [
     {
      "type": "stepper",
      "parameter": "P(0)",
      "values": [
       160,
       400,
       640,
       960
      ],
      "start": 160
     }
    ],
    "drawn": [
     "the solution curve from the chosen P(0)",
     "the equilibrium lines P = 0 and P = 800",
     "the sign of dP/dt at P(0)"
    ],
    "labels": [
     {
      "text": "P = 800: rate zero",
      "placement": "inside"
     },
     {
      "text": "P = 400: rate largest",
      "placement": "inside"
     },
     {
      "text": "sign of dP/dt at P(0)",
      "placement": "inside"
     }
    ],
    "question": "From each starting value, which level does the curve approach, and what does the sign of dP/dt at the start say?"
   },
   "fallback": "a static figure of the four solution curves from P(0) = 160, 400, 640 and 960, with P = 800 and P = 400 marked, each label inside the figure",
   "keyboard": "Tab focuses the stepper; up and down arrow keys change P(0) through the four values; Enter reads the sign of dP/dt at P(0) and the level approached"
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a quadratic's vertex; BC-REP-06, BC-REP-01 on BC-SKL-07042, and the curve on ki-1 already marks P = 400",
   "sources": [
    "BC-SKL-07042"
   ]
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 6: a statement about reading without solving",
   "sources": [
    "BC-SKL-07041"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07040",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07041",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07042",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07044",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-07040",
  "err-BC-ERR-07041",
  "err-BC-ERR-07042",
  "err-BC-ERR-07044",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-07-differential-equations.md",
   "line": "so it is largest at half the carrying capacity, which is where the quantity changes fastest and where the solution has a point of inflection"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-07009 is calculator status either; the lesson takes Section I Part A, 2.14 minutes, the no-calculator MCQ shape.",
   "settles": "An official record fixing the calculator status of the logistic item."
  },
  {
   "claim": "ki-1 is served as an interactive with one stepper on the initial value under TEMPLATE rule 3, although docs/lessons/unit-07/README.md, section 6 left LSN-CON-07012 as text pending BC-REP-02 on BC-SKL-07041; the rule 3 clause for a discrete, student-chosen parameter of a process idea now covers it.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "The stepper values 400, 640 and 960 go beyond the parameter_spec, whose initial value stays below half the capacity; they show the other approaches to the capacity.",
   "settles": "A parameter_spec for the interactive, or an archetype draw with the initial value above the capacity."
  },
  {
   "claim": "chk-3 carries two distractors on BC-ERR-07040 (the constant and zero, both named in its observed behaviour), because BC-ERR-07041 produces no distinct value.",
   "settles": "A further BC-ERR record on BC-SKL-07042 that produces a wrong value."
  },
  {
   "claim": "The solved formula in the BC-ERR-07044 wrong step, 800/(1 + 4e^(-2t/5)), is computed for the draw, not quoted from a source.",
   "settles": "A CAS check in the build pipeline."
  },
  {
   "claim": "A fluent solver skips writing the zero equation and the restated right side.",
   "settles": "Per-step timing data from the fluency telemetry."
  }
 ],
 "sources": [
  "BC-CON-07012",
  "BC-SKL-07040",
  "BC-SKL-07041",
  "BC-SKL-07042",
  "BC-EK-FUN-7H2",
  "BC-EK-FUN-7H3",
  "BC-EK-FUN-7H4",
  "ced:145",
  "BC-QA-07009",
  "BC-ERR-07040",
  "BC-ERR-07041",
  "BC-ERR-07042",
  "BC-ERR-07044",
  "BC-MIS-07025",
  "BC-MIS-07027",
  "BC-PRQ-05001",
  "research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations",
  "research/question-analysis/question-archetypes.md#BC-QA-07009 Logistic model interpreted without solving",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 568,
  "brief": 418
 },
 "read_minutes": {
  "full": 3.8,
  "brief": 2.8
 }
}
```
