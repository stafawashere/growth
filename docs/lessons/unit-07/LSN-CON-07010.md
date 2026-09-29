---
title: LSN-CON-07010 Exponential growth and decay model
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-07010, the exponential growth and decay model, built from authoring_bundle("BC-CON-07010") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-07010 Exponential growth and decay model

Concept BC-CON-07010 (skills BC-SKL-07034 to BC-SKL-07038), topic 7.8 of Unit 7, loaded by BC-QA-07008 (family exponential-model) and BC-QA-07011. Its hard parents in Unit 7 are BC-CON-07001, BC-CON-07007 and BC-CON-07008 (docs/lessons/unit-07/README.md, section 1).

## Orientation

Served text, from BC-CON-07010 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-07-differential-equations.md#7.8 Exponential Models with Differential Equations): the model from the proportionality statement, the solution with the initial value as coefficient, k from a second pair, and k interpreted.

## Key ideas

Three BC-EK statements; at most two core.

- ki-1 (core), BC-EK-FUN-7F2 (ced:144). Paraphrase of the Model and solution and Sign of the constant paragraphs. Notation: dy/dt = ky.
- ki-2 (core), BC-EK-FUN-7G1 (ced:144). Paraphrase of the Model and solution and Determining the constant paragraphs. Served as a table.
- ki-3 (extended, low band), BC-EK-FUN-7F1 (ced:144). Paraphrase of the Other applications paragraph.

No anchor quotes.

## Recognition

BC-QA-07008 (research/question-analysis/question-archetypes.md#BC-QA-07008 Exponential growth or decay model solved and interpreted): `typical_wording` "the rate of change of the quantity is proportional to the quantity; find an expression for the quantity at time t and state what the constant means in context"; `common_givens` a proportionality statement, an initial value, usually a second data pair; `asked_to_produce` the equation, the exponential solution, the constant, an interpretation with units. Shape: a multipart FRQ or one MCQ; `official_examples` BC-MCQ-SAMPLE-010.

Not this concept: "jointly proportional to the quantity and the difference between the quantity and" a level is logistic (BC-CON-07011); a rate in t alone is an accumulation (BC-CON-07008).

## Method choice

- st-1, BC-QA-07008, both bands. Method, `expected_solution_path[0]`: write the proportional model. Rival, `wrong_approaches`: treating the constant of proportionality and the constant of integration as the same object. Separating feature: y0 is the coefficient, fixed by the initial value; k needs a second pair. The separation is held in the head once the form is known (BC-EK-FUN-7G1).

## Solution path

- ex-1, BC-QA-07008, both bands, no calculator. Draw: growth, factor 3, initial 200, elapsed 2, context bacteria, so later = 600 and k = (ln 3)/2, exact. No published BC-QA-07008 draw matches.
- Steps: model (new); solution with the coefficient (new); second pair (evaluate at t = 2); k (solve); P(t) (new); interpretation (no value).
- A fluent solver writes lines 2 to 5; the model and the interpretation are held when not asked [inferred].

## Scoring

BC-QA-07008 lists no `point_types`, so no what_a_reader_scores entry and no point tag; the served text names no point beyond the error records' scoring_consequence.

## Traps

Six errors meet the skills; the first four in the bundle's order are served, mid band the first two. All on ex-1's draw.

- err-BC-ERR-07001: dP/dt = P. Possible reason from BC-MIS-07001.
- err-BC-ERR-07034: a line through the two pairs. Possible reason from BC-MIS-07021.
- err-BC-ERR-07035: 200 inside the exponent. Possible reason from BC-MIS-07022.
- err-BC-ERR-07036: k from the initial value alone. Possible reason from BC-MIS-07022.

## Representations

None as a separate block. The topic names the conversion of two data pairs to a determined constant (BC-REP-03 to BC-REP-01); ki-2's table carries it.

## Prerequisite bridge

- BC-PRQ-06003, BC-PRQ-07001, BC-PRQ-07003, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-07008 is `either`, a multipart FRQ or one MCQ; the MCQ shape is taken, Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]. The minutes go on the logarithm step; the model and coefficient are written at once.

## Checks

- chk-1, completion of ex-1, both bands. Key 200e^((ln 3)t/2).
- chk-2, isomorph, both bands. Draw: decay, factor 5/2, initial 500, elapsed 2, users. Key 500e^((ln(2/5))t/2).
- chk-3, MCQ, low band. Draw: decay, factor 2, initial 400, elapsed 3, mold. Key 400e^(-(ln 2)t/3). Distractors: 400e^t (BC-ERR-07001), 400 - 200t/3 (BC-ERR-07034), e^(-400(ln 2)t/3) (BC-ERR-07035).

## Delivery

- orientation, ki-1, ki-3: text, rule 6.
- ki-2: table, rule 5: BC-REP-03 on BC-SKL-07036 (docs/lessons/unit-07/README.md, section 6) [inferred; settled by the modality A/B].
- ex-1 and the four error blocks: step_reveal, rule 1.

## Band plan

- Low (full): orientation, ki-1 to ki-3, st-1, ex-1, the four error blocks, chk-1 to chk-3, the three bridges. 555 words, 3.7 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, ki-2, st-1, ex-1, err-BC-ERR-07001, err-BC-ERR-07034, chk-1, chk-2, the three bridges. 407 words, 2.8 minutes (cap 450 and 3).
- Refresher: ki-1, ki-2, the four error blocks, ex-1.

## Sources

- BC-CON-07010; BC-SKL-07034 to BC-SKL-07038; BC-EK-FUN-7F1, BC-EK-FUN-7F2, BC-EK-FUN-7G1; ced:144
- BC-QA-07008; BC-MCQ-SAMPLE-010
- BC-ERR-07001, BC-ERR-07034, BC-ERR-07035, BC-ERR-07036; BC-MIS-07001, BC-MIS-07021, BC-MIS-07022
- BC-PRQ-06003, BC-PRQ-07001, BC-PRQ-07003
- research/units/unit-07-differential-equations.md#7.8 Exponential Models with Differential Equations
- research/question-analysis/question-archetypes.md#BC-QA-07008 Exponential growth or decay model solved and interpreted
- research/exam/exam-structure.md#Section and part layout
- [inferred] Part I-A for an either archetype. Settled by an official calculator status.
- [inferred] The interpretation line. Settled by a rubric for BC-QA-07008.
- [inferred] ki-2 as a table. Settled by the modality A/B.
- [inferred] Held steps. Settled by per-step timing data.
- [inferred] No block for BC-QA-07011 here. Settled by a template ruling on secondary archetypes.

## Machine record

```json
{
 "id": "LSN-CON-07010",
 "kind": "concept",
 "target_id": "BC-CON-07010",
 "unit": "07",
 "skills": [
  "BC-SKL-07034",
  "BC-SKL-07035",
  "BC-SKL-07036",
  "BC-SKL-07037",
  "BC-SKL-07038"
 ],
 "orientation": {
  "text": "A response writes dy/dt = ky, then y = y0 e^(kt) with the initial value as coefficient, finds k from a second data pair, and says what k means, with direction and units.",
  "sources": [
   "BC-CON-07010",
   "research/units/unit-07-differential-equations.md#7.8 Exponential Models with Differential Equations"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-7F2",
   "depth": "core",
   "text": "A rate proportional to the size of the quantity gives dy/dt = ky. Positive k is growth, negative k decay; the size of k sets how fast.",
   "notation": "dy/dt = ky",
   "quote": null,
   "sources": [
    "BC-EK-FUN-7F2",
    "ced:144",
    "research/units/unit-07-differential-equations.md#7.8 Exponential Models with Differential Equations"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-7G1",
   "depth": "core",
   "text": "With y = y0 at t = 0, y = y0 e^(kt): the initial value is the coefficient, k is in the exponent. A second data pair fixes k through a logarithm.",
   "notation": "y = y sub 0 e^(kt)",
   "quote": null,
   "sources": [
    "BC-EK-FUN-7G1",
    "ced:144",
    "research/units/unit-07-differential-equations.md#7.8 Exponential Models with Differential Equations"
   ]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-FUN-7F1",
   "depth": "extended",
   "text": "Motion along a line is the other application: a velocity or position given by a differential equation is solved the same way, and the answer is the quantity asked for, not the one a derivative away.",
   "notation": "motion along a line",
   "quote": null,
   "sources": [
    "BC-EK-FUN-7F1",
    "ced:144",
    "research/units/unit-07-differential-equations.md#7.8 Exponential Models with Differential Equations"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-07008",
   "cue": "The rate of change is proportional to the quantity, with an initial value and a second data pair.",
   "method": "First written line: dy/dt = ky, then y = y0 e^(kt).",
   "rival": "Rival: treating the constant of proportionality and the constant of integration as the same object.",
   "separating_feature": "y0 is the coefficient; k needs the second pair.",
   "sources": [
    "BC-QA-07008"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-07008",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "change": "growth",
    "factor": "3",
    "initial": 200,
    "elapsed": 2,
    "context": "bacteria"
   },
   "problem": {
    "text": "Bacteria P grow at a rate proportional to P; P(0) = 200, P(2) = 600, t in hours. Find P(t); interpret k.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Proportional to P.",
     "why": "A constant multiple, k.",
     "expr": "dPdt = k*P",
     "relation": "new"
    },
    {
     "cue": "P(0) = 200.",
     "why": "The coefficient.",
     "expr": "P = 200*exp(k*t)",
     "relation": "new"
    },
    {
     "cue": "P(2) = 600.",
     "why": "Only a second pair reaches k.",
     "expr": "600 = 200*exp(2*k)",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     }
    },
    {
     "cue": "k is in the exponent.",
     "why": "e^(2k) = 3, take ln.",
     "expr": "log(3)/2",
     "relation": "solve",
     "variable": "k"
    },
    {
     "cue": "The stem asks for P(t).",
     "why": "Put k back.",
     "expr": "P = 200*exp(log(3)*t/2)",
     "relation": "new"
    },
    {
     "cue": "The stem asks what k means.",
     "why": "k = (ln 3)/2 > 0: growth, per hour; the count triples every 2 hours."
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "200*exp(log(3)*t/2)"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-07001",
   "observed_behavior": "The response writes the derivative equal to the quantity itself, with no constant of proportionality.",
   "scoring_consequence": "The model is wrong by a factor and every later value built on it is wrong.",
   "wrong_step": {
    "text": "dP/dt = P.",
    "expr": "dPdt = P"
   },
   "right_step": {
    "text": "dP/dt = kP.",
    "expr": "dPdt = k*P"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07001",
    "text": "drops the constant of proportionality"
   },
   "sources": [
    "BC-ERR-07001",
    "BC-MIS-07001"
   ]
  },
  {
   "error_id": "BC-ERR-07034",
   "observed_behavior": "The response writes the quantity as the initial value plus a constant multiple of the independent variable.",
   "scoring_consequence": "The model is the wrong family and no later value is right.",
   "wrong_step": {
    "text": "A line through (0, 200) and (2, 600).",
    "expr": "P = 200 + 200*t"
   },
   "right_step": {
    "text": "An exponential through both.",
    "expr": "P = 200*exp(log(3)*t/2)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07021",
    "text": "treats a constant rate constant as a constant rate, so the model comes out linear"
   },
   "sources": [
    "BC-ERR-07034",
    "BC-MIS-07021"
   ]
  },
  {
   "error_id": "BC-ERR-07035",
   "observed_behavior": "The response writes the initial value inside the exponent, or the rate constant as a multiplier outside it.",
   "scoring_consequence": "The formula fails the initial condition or the differential equation.",
   "wrong_step": {
    "text": "200 inside the exponent.",
    "expr": "P = exp(200*k*t)"
   },
   "right_step": {
    "text": "200 as the coefficient.",
    "expr": "P = 200*exp(k*t)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07022",
    "text": "does not see that the initial value fixes the leading coefficient"
   },
   "sources": [
    "BC-ERR-07035",
    "BC-MIS-07022"
   ]
  },
  {
   "error_id": "BC-ERR-07036",
   "observed_behavior": "The response computes the constant from the initial condition alone, with no second value.",
   "scoring_consequence": "The constant is undetermined and the reported value is arbitrary.",
   "wrong_step": {
    "text": "k taken from 200 alone.",
    "expr": "k = log(200)"
   },
   "right_step": {
    "text": "k from P(2) = 600.",
    "expr": "k = log(3)/2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07022",
    "text": "a second pair is needed for the exponent"
   },
   "sources": [
    "BC-ERR-07036",
    "BC-MIS-07022"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06003",
   "text": "ln turns e^(2k) = 3 into 2k = ln 3; without it, logarithms stay uncombined."
  },
  {
   "prq_id": "BC-PRQ-07001",
   "text": "A logarithm of both sides isolates k; without it, the second pair gives no k."
  },
  {
   "prq_id": "BC-PRQ-07003",
   "text": "Proportional to means a constant multiple; without it, the constant is lost."
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
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    6
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
   "archetype_id": "BC-QA-07008",
   "parameter_draw": {
    "change": "growth",
    "factor": "3",
    "initial": 200,
    "elapsed": 2,
    "context": "bacteria"
   },
   "completes": "ex-1",
   "stem": {
    "text": "P = 200e^(kt), and P(2) = 600 gives k = (ln 3)/2. Write P(t).",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "200*exp(log(3)*t/2)"
   },
   "steps": [
    {
     "text": "The model.",
     "expr": "P = 200*exp(k*t)",
     "relation": "new"
    },
    {
     "text": "k substituted.",
     "expr": "P = 200*exp(log(3)*t/2)",
     "relation": "evaluate",
     "subs": {
      "k": "log(3)/2"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07035"
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
   "archetype_id": "BC-QA-07008",
   "parameter_draw": {
    "change": "decay",
    "factor": "5/2",
    "initial": 500,
    "elapsed": 2,
    "context": "users"
   },
   "stem": {
    "text": "Users U decrease at a rate proportional to U; U(0) = 500, U(2) = 200. Find U(t).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "500*exp(log(2/5)*t/2)"
   },
   "steps": [
    {
     "text": "Model with the initial value.",
     "expr": "U = 500*exp(k*t)",
     "relation": "new"
    },
    {
     "text": "Second pair.",
     "expr": "200 = 500*exp(2*k)",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     }
    },
    {
     "text": "k.",
     "expr": "log(2/5)/2",
     "relation": "solve",
     "variable": "k"
    },
    {
     "text": "Put k back.",
     "expr": "U = 500*exp(log(2/5)*t/2)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07035",
    "BC-SKL-07036"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-07008",
   "parameter_draw": {
    "change": "decay",
    "factor": "2",
    "initial": 400,
    "elapsed": 3,
    "context": "mold"
   },
   "stem": {
    "text": "Mold M decays at a rate proportional to M. M(0) = 400 and M(3) = 200. Which is M(t)?",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "400*exp(-log(2)*t/3)"
   },
   "steps": [
    {
     "text": "Model with the initial value.",
     "expr": "M = 400*exp(k*t)",
     "relation": "new"
    },
    {
     "text": "Second pair.",
     "expr": "200 = 400*exp(3*k)",
     "relation": "evaluate",
     "subs": {
      "t": "3"
     }
    },
    {
     "text": "k.",
     "expr": "-log(2)/3",
     "relation": "solve",
     "variable": "k"
    },
    {
     "text": "Put k back.",
     "expr": "M = 400*exp(-log(2)*t/3)",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "400*exp(t)",
     "error_path": "BC-ERR-07001",
     "derivation": "dM/dt = M, no constant of proportionality"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "400*exp(-log(2)*t/3)",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "400 - 200*t/3",
     "error_path": "BC-ERR-07034",
     "derivation": "a line through (0, 400) and (3, 200)"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "exp(-400*log(2)*t/3)",
     "error_path": "BC-ERR-07035",
     "derivation": "400 written inside the exponent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07034",
    "BC-SKL-07035"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows; BC-REP-04, BC-REP-05, BC-REP-06",
   "sources": [
    "BC-SKL-07034"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a verbal statement to an equation; BC-REP-04, BC-REP-06 on BC-SKL-07034",
   "sources": [
    "BC-SKL-07034",
    "BC-SKL-07037"
   ]
  },
  {
   "block": "ki-2",
   "mode": "table",
   "reason": "rule 5: BC-REP-03 on BC-SKL-07036, two data pairs that fix k (docs/lessons/unit-07/README.md, section 6)",
   "sources": [
    "BC-SKL-07036"
   ],
   "spec": {
    "kind": "table",
    "representations": [
     "BC-REP-03"
    ],
    "columns": [
     "t (hours)",
     "P(t)",
     "what it fixes"
    ],
    "rows": [
     [
      "0",
      "200",
      "the coefficient y0"
     ],
     [
      "2",
      "600",
      "k, through ln 3 = 2k"
     ]
    ],
    "labels": [
     {
      "text": "initial value: coefficient",
      "placement": "inside"
     },
     {
      "text": "second pair: exponent",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same two rows as a sentence: P(0) = 200 fixes the coefficient; P(2) = 600 fixes k = (ln 3)/2",
   "keyboard": "static table; Tab reaches it and a screen reader reads rows in order"
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 6: BC-REP-01, BC-REP-05, BC-REP-06 on BC-SKL-07038",
   "sources": [
    "BC-SKL-07038"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07001",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07034",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07035",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07036",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-07001",
  "err-BC-ERR-07034",
  "err-BC-ERR-07035",
  "err-BC-ERR-07036",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-07-differential-equations.md",
   "line": "One further data pair beyond the initial condition determines the constant through a logarithm."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-07008 is calculator status either; the lesson takes Section I Part A, 2.14 minutes, the no-calculator MCQ shape, because the draw keeps k exact.",
   "settles": "An official record fixing the calculator status of the exponential model item."
  },
  {
   "claim": "The interpretation line in ex-1 (growth, per hour, triples every 2 hours) rests on the Sign of the constant paragraph; no rubric for BC-QA-07008 is recorded.",
   "settles": "A scoring guideline part scoring the interpretation of k."
  },
  {
   "claim": "ki-2 is served as a table rather than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "No strategy block for BC-QA-07011, which loads BC-SKL-07038 through its accumulation form; that archetype's block sits in LSN-CON-07008 and LSN-CON-07009.",
   "settles": "A template ruling on whether a secondary archetype needs its own block in every concept it loads."
  },
  {
   "claim": "A fluent solver holds the model line and the interpretation in the head when the stem asks only for P(t).",
   "settles": "Per-step timing data from the fluency telemetry."
  }
 ],
 "sources": [
  "BC-CON-07010",
  "BC-SKL-07034",
  "BC-SKL-07035",
  "BC-SKL-07036",
  "BC-SKL-07037",
  "BC-SKL-07038",
  "BC-EK-FUN-7F1",
  "BC-EK-FUN-7F2",
  "BC-EK-FUN-7G1",
  "ced:144",
  "BC-QA-07008",
  "BC-ERR-07001",
  "BC-ERR-07034",
  "BC-ERR-07035",
  "BC-ERR-07036",
  "BC-MIS-07001",
  "BC-MIS-07021",
  "BC-MIS-07022",
  "BC-PRQ-06003",
  "BC-PRQ-07001",
  "BC-PRQ-07003",
  "research/units/unit-07-differential-equations.md#7.8 Exponential Models with Differential Equations",
  "research/question-analysis/question-archetypes.md#BC-QA-07008 Exponential growth or decay model solved and interpreted",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 555,
  "brief": 407
 },
 "read_minutes": {
  "full": 3.7,
  "brief": 2.8
 }
}
```
