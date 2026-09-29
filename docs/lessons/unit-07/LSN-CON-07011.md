---
title: LSN-CON-07011 Logistic differential equation
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-07011, the logistic differential equation, built from authoring_bundle("BC-CON-07011") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-07011 Logistic differential equation

Concept BC-CON-07011 (skills BC-SKL-07039, BC-SKL-07043), topic 7.9 of Unit 7 (BC only), loaded by BC-QA-07009 (family logistic-model). BC-SKL-07043 has hard parents BC-SKL-07041 and BC-SKL-07042 in BC-CON-07012, so its interpretation skill is credited after LSN-CON-07012's (docs/lessons/unit-07/README.md, section 1).

## Prediction

Form mcq, both bands, on ex-1's own numbers. The stem gives a rate jointly proportional to P and 600 - P and asks what dP/dt does as P nears 600. Key B: it nears zero. Distractors: it grows larger, and it stays constant. The factor 600 - P is in the stem, so the answer follows before any rule. The resolution names 600 as the carrying capacity (BC-EK-FUN-7H1, ced:145). Delivery: text.

## Orientation

Served text, from BC-CON-07011 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations): the model from the joint proportionality statement, a reading without solving, and a sentence with the quantity and units.

## Key ideas

- ki-1 (core), BC-EK-FUN-7H1 (ced:145). Paraphrase of the Model paragraph. Notation from the concept record.
- ki-2 (core), BC-EK-FUN-7H2 (ced:145). Paraphrase of the Reasoning without solving and Carrying capacity paragraphs.

No anchor quotes.

## Recognition

BC-QA-07009 (research/question-analysis/question-archetypes.md#BC-QA-07009 Logistic model interpreted without solving): `typical_wording` "the quantity is modelled by the given logistic differential equation with the given initial value; find the limit of the quantity as the independent variable grows without bound"; `common_givens` a logistic equation and an initial value strictly between zero and the carrying capacity; `asked_to_produce` the carrying capacity, the limiting value, the fastest change value, an interpretation. Shape: one or two FRQ parts or one MCQ; `official_examples` BC-MCQ-CED-017, BC-MCQ-PE2012-014.

The signal: "jointly proportional to the quantity and the difference between the quantity and" a level, or a right side quadratic in y with a zero at a positive level. Not this concept: "proportional to the quantity" alone is exponential (BC-CON-07010). The fastest change value is LSN-CON-07012.

The near miss on the contrast pair is the exponential model of BC-CON-07010: a rate proportional to P alone, with no factor that vanishes at a level. The feature is a factor a - P, or a P^2 term, beside P.

## Method choice

- st-1, BC-QA-07009, both bands. Method, `expected_solution_path[0]`: read the zeros of the right side. Rival, `wrong_approaches`: separating with partial fractions when only the limit was asked for. Separating feature: a value or meaning is asked, not a formula. The archetype carries `asked_to_produce` and `common_givens`.

The strategy fields carry no leading label, since the reader prints Cue, First line, Rival and Separating feature. st-1 carries the contrast pair, served in both bands.

## Solution path

- ex-1, BC-QA-07009, both bands, no calculator. Draw: factored, capacity 600, rate 1/4, start share 1/5, deer, so P(0) = 120 and k = 1/2400 [inferred rendering]. No published BC-QA-07009 draw matches.
- Steps: the equation (new); right side zero (new); zeros (solve); right side (new); its value at 120 (evaluate); the limit (new); the sentence (no value).
- A fluent solver writes the equation, the zeros, the sign and the sentence [inferred].

One worked example only, so there is no fade.

## Scoring

BC-QA-07009 lists no `point_types`, so no what_a_reader_scores entry and no point tag; the served text names no point beyond the error records' scoring_consequence.

## Traps

Three errors meet the skills, all served in the low band, the first two in the mid band. All on ex-1's draw.

- err-BC-ERR-07039: kP alone. Possible reason from BC-MIS-07024.
- err-BC-ERR-07043: 600 with no sentence; the values are equal, so the relation is equivalent. Possible reason from BC-MIS-07023.
- err-BC-ERR-07044: the solved formula. Possible reason from BC-MIS-07025.

## Representations

None. The topic's Representations paragraph names BC-REP-04, 05 and 06, none figure-bearing.

## Prerequisite bridge

- BC-PRQ-07003, from its `description_plain` and `failure_signature`.

## Time

BC-QA-07009 is `either`, one or two FRQ parts or one MCQ; the MCQ shape is taken, Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]. The minutes go on the zeros and the sign; nothing is solved.

## Checks

- chk-1, completion of ex-1, both bands. Key 600.
- chk-2, isomorph, both bands. Draw: expanded, capacity 900, rate 1/3, start share 1/10, fish. Key 900.
- chk-3, MCQ, low band, statement key. Draw: factored, capacity 400, rate 1/2, start share 1/4, rumor. Distractors: grows without bound (BC-ERR-07039), 400 alone (BC-ERR-07043), nothing until solved (BC-ERR-07044).

## Delivery

- orientation, ki-1, ki-2: text, rule 6. The representations are BC-REP-04, 05, 06. Rule 3 would allow a logistic curve with a stepped initial value; it is served once, on LSN-CON-07012's ki-1, where the limit is the idea being taught [inferred].
- ex-1 and the three error blocks: step_reveal, rule 1.

- No drawn block: the machine record carries `no_figure_reason`. The representations are BC-REP-04, 05 and 06, none figure-bearing, and the solution curve is drawn once, on LSN-CON-07012.
- pr-1: text, rule 6.

## Band plan

- Low (full), in served order: prediction, orientation, the bridge, ki-1, ki-2, st-1 with the contrast pair, ex-1, chk-1, the three error blocks, chk-2, chk-3. 574 words, 3.83 minutes (cap 900 and 6).
- Mid (brief), in served order: prediction, orientation, the bridges, the core key ideas, st-1 with the contrast pair, ex-1, chk-1, the first two error blocks, chk-2. 450 words, 3.0 minutes (cap 450 and 3). The orientation, the strategy fields, the ki-1 text and the ex-1 cues were shortened to fit 450.
- Refresher: the core key ideas, the error blocks, ex-1.

## Sources

- BC-CON-07011; BC-SKL-07039, BC-SKL-07043; BC-EK-FUN-7H1, BC-EK-FUN-7H2; ced:145
- BC-QA-07009; BC-MCQ-CED-017, BC-MCQ-PE2012-014
- BC-ERR-07039, BC-ERR-07043, BC-ERR-07044; BC-MIS-07023, BC-MIS-07024, BC-MIS-07025
- BC-PRQ-07003
- research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations
- research/question-analysis/question-archetypes.md#BC-QA-07009 Logistic model interpreted without solving
- research/exam/exam-structure.md#Section and part layout
- pr-1 and the contrast pair draw on the concept record, the key idea's BC-EK and the cited topic section.
- [inferred] Part I-A for an either archetype. Settled by an official calculator status.
- [inferred] k = 1/2400 from the draw. Settled by a spec naming the joint constant.
- [inferred] The solved formula in the BC-ERR-07044 step. Settled by a CAS check.
- [inferred] ki-2 as text. Settled by the modality A/B.
- [inferred] Written and held steps. Settled by per-step timing data.

## Machine record

```json
{
 "id": "LSN-CON-07011",
 "kind": "concept",
 "target_id": "BC-CON-07011",
 "unit": "07",
 "skills": [
  "BC-SKL-07039",
  "BC-SKL-07043"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Before the rule: deer P grow at a rate jointly proportional to P and 600 - P. What does dP/dt do as P nears 600?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "It grows larger.",
    "is_key": false
   },
   {
    "id": "B",
    "label": "It nears zero.",
    "is_key": true
   },
   {
    "id": "C",
    "label": "It stays constant.",
    "is_key": false
   }
  ],
  "resolution": "The rate is a constant times P(600 - P), zero at P = 600, so P levels off there: the carrying capacity.",
  "sources": [
   "BC-CON-07011",
   "BC-EK-FUN-7H1",
   "research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations"
  ]
 },
 "no_figure_reason": "Both key ideas are symbolic: an equation from a proportionality statement, and a sign read from its right side. No skill carries a figure-bearing representation, and the solution curve is drawn once, in the next lesson.",
 "orientation": {
  "text": "A response writes dy/dt = ky(a - y) from a joint proportionality statement and reads it without solving.",
  "sources": [
   "BC-CON-07011",
   "research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-7H1",
   "depth": "core",
   "text": "A rate jointly proportional to y and a - y gives dy/dt = ky(a - y); the factor a - y makes the rate vanish at a.",
   "notation": "dy/dt = ky(a - y)",
   "quote": null,
   "sources": [
    "BC-EK-FUN-7H1",
    "ced:145",
    "research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-7H2",
   "depth": "core",
   "text": "The right side is zero at 0 and a and positive between, so a solution starting between rises toward a. The sentence names quantity, units and direction.",
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
   "cue": "A logistic equation; a limit or meaning is asked.",
   "method": "The right side set equal to zero.",
   "rival": "Partial fractions when only the limit was asked.",
   "separating_feature": "A value is asked, not a formula for y.",
   "sources": [
    "BC-QA-07009"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "dP/dt = (1/10)P(1 - P/500), P(0) = 50. Find the limit of P(t) as t grows.",
     "archetype_id": "BC-QA-07009"
    },
    "not_this": {
     "text": "dP/dt = P/10, P(0) = 50. Find the limit of P(t) as t grows.",
     "why_not": "The right side is proportional to P alone: exponential, no ceiling."
    },
    "feature": "A factor 500 - P beside P, against P alone."
   }
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
    "form": "factored",
    "capacity": 600,
    "rate": "1/4",
    "start_share": "1/5",
    "context": "deer"
   },
   "problem": {
    "text": "Deer P grow at a rate jointly proportional to P and 600 - P, constant 1/2400; P(0) = 120. Write the equation; find and interpret the limit of P(t).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Jointly proportional.",
     "why": "A constant times the product.",
     "expr": "dPdt = P*(600 - P)/2400",
     "relation": "new"
    },
    {
     "cue": "A limit is asked.",
     "why": "Equilibria: zeros of the right side.",
     "expr": "P*(600 - P)/2400 = 0",
     "relation": "new"
    },
    {
     "cue": "Solve.",
     "why": "The nonzero zero is the capacity.",
     "expr": "FiniteSet(0, 600)",
     "relation": "solve",
     "variable": "P"
    },
    {
     "cue": "120 lies between.",
     "why": "The sign there gives the direction.",
     "expr": "P*(600 - P)/2400",
     "relation": "new"
    },
    {
     "cue": "At P = 120.",
     "why": "Positive: P rises.",
     "expr": "24",
     "relation": "evaluate",
     "subs": {
      "P": "120"
     }
    },
    {
     "cue": "The limit.",
     "why": "P cannot cross 600.",
     "expr": "600",
     "relation": "new"
    },
    {
     "cue": "Interpret.",
     "why": "The deer population approaches 600 deer."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "600"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-07039",
   "observed_behavior": "The response writes a constant multiple of the quantity alone, losing the factor that encodes the carrying capacity.",
   "scoring_consequence": "The model is exponential rather than logistic and has no ceiling.",
   "wrong_step": {
    "text": "dP/dt = kP.",
    "expr": "dPdt = k*P"
   },
   "right_step": {
    "text": "dP/dt = kP(600 - P).",
    "expr": "dPdt = k*P*(600 - P)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07024",
    "text": "without the factor that makes the rate vanish at the carrying capacity"
   },
   "sources": [
    "BC-ERR-07039",
    "BC-MIS-07024"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07043",
   "observed_behavior": "The response gives the two numbers and never says what they mean for the population being modelled.",
   "scoring_consequence": "An interpretation point is lost because the sentence is incomplete.",
   "wrong_step": {
    "text": "600, with no sentence.",
    "expr": "600"
   },
   "right_step": {
    "text": "The deer population approaches 600 deer.",
    "expr": "600"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-07023",
    "text": "reports the number and leaves the quantity, the units, and the direction implicit"
   },
   "sources": [
    "BC-ERR-07043",
    "BC-MIS-07023"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-07044",
   "observed_behavior": "The response separates the logistic equation with partial fractions and solves it in order to report a limit the equation gives directly.",
   "scoring_consequence": "Time is spent on work the question did not ask for, and an error inside it costs the value that the equation alone would have given.",
   "wrong_step": {
    "text": "Partial fractions, the solved formula, then its limit.",
    "expr": "600/(1 + 4*exp(-t/4))"
   },
   "right_step": {
    "text": "Zeros 0 and 600, rate positive at 120.",
    "expr": "600"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07025",
    "text": "does not read the capacity off the zeros of the right side and reaches for partial fractions instead"
   },
   "sources": [
    "BC-ERR-07044",
    "BC-MIS-07025"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-07003",
   "text": "Jointly proportional means a constant times the product; without it, the constant is omitted."
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
    5,
    6,
    7
   ]
  },
  "skipped_steps": {
   "ex-1": [
    2,
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
   "archetype_id": "BC-QA-07009",
   "parameter_draw": {
    "form": "factored",
    "capacity": 600,
    "rate": "1/4",
    "start_share": "1/5",
    "context": "deer"
   },
   "completes": "ex-1",
   "stem": {
    "text": "dP/dt = P(600 - P)/2400, P(0) = 120, zeros 0 and 600. Find the limit of P(t).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "600"
   },
   "steps": [
    {
     "text": "The right side.",
     "expr": "P*(600 - P)/2400",
     "relation": "new"
    },
    {
     "text": "At P = 120.",
     "expr": "24",
     "relation": "evaluate",
     "subs": {
      "P": "120"
     }
    },
    {
     "text": "Positive, so P rises to 600.",
     "expr": "600",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07043"
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
    "form": "expanded",
    "capacity": 900,
    "rate": "1/3",
    "start_share": "1/10",
    "context": "fish"
   },
   "stem": {
    "text": "Fish: dF/dt = F/3 - F^2/2700, F(0) = 90. Find the limit of F(t).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "900"
   },
   "steps": [
    {
     "text": "Right side zero.",
     "expr": "F/3 - F**2/2700 = 0",
     "relation": "new"
    },
    {
     "text": "Zeros.",
     "expr": "FiniteSet(0, 900)",
     "relation": "solve",
     "variable": "F"
    },
    {
     "text": "The right side.",
     "expr": "F/3 - F**2/2700",
     "relation": "new"
    },
    {
     "text": "At F = 90.",
     "expr": "27",
     "relation": "evaluate",
     "subs": {
      "F": "90"
     }
    },
    {
     "text": "Positive, so F rises to 900.",
     "expr": "900",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07043"
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
    "capacity": 400,
    "rate": "1/2",
    "start_share": "1/4",
    "context": "rumor"
   },
   "stem": {
    "text": "R people have heard a rumor, dR/dt = (1/2)R(1 - R/400), R(0) = 100. Which answer is complete?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "rumor_count_approaches_400_people"
   },
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "R grows without bound.",
     "error_path": "BC-ERR-07039",
     "derivation": "the factor 1 - R/400 dropped, leaving exponential growth"
    },
    {
     "id": "B",
     "is_key": true,
     "label": "The number who have heard the rumor rises toward 400 people.",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "label": "400.",
     "error_path": "BC-ERR-07043",
     "derivation": "the number with no quantity, units or direction"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "Nothing, until R(t) is solved by partial fractions.",
     "error_path": "BC-ERR-07044",
     "derivation": "the equation solved before the limit is read"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07043"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows; BC-REP-04, BC-REP-05, BC-REP-06",
   "sources": [
    "BC-SKL-07039"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a verbal statement to an equation; BC-REP-04, BC-REP-06 on BC-SKL-07039, none figure-bearing",
   "sources": [
    "BC-SKL-07039"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a reading of the equation; BC-REP-04, BC-REP-05 on BC-SKL-07043. The stepped logistic curve that rule 3 allows is served once, in LSN-CON-07012, where the limit and the fastest change are the idea",
   "sources": [
    "BC-SKL-07043"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07039",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07043",
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
  "err-BC-ERR-07039",
  "err-BC-ERR-07043",
  "err-BC-ERR-07044",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-07-differential-equations.md",
   "line": "no part in 2023 to 2025 asked for the logistic model to be solved"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-07009 is calculator status either; the lesson takes Section I Part A, 2.14 minutes, the no-calculator MCQ shape.",
   "settles": "An official record fixing the calculator status of the logistic item."
  },
  {
   "claim": "The worked example states the constant of proportionality as 1/2400, the draw's rate 1/4 divided by the capacity 600, so the joint proportionality form matches the factored form r P (1 - P/M).",
   "settles": "A BC-QA-07009 parameter_spec that names the joint proportionality constant."
  },
  {
   "claim": "The solved formula in the BC-ERR-07044 wrong step, 600/(1 + 4e^(-t/4)), is computed for the draw, not quoted from a source.",
   "settles": "A CAS check in the build pipeline."
  },
  {
   "claim": "ki-2 stays text here although rule 3 would allow a stepped logistic curve; the curve is served once, in LSN-CON-07012.",
   "settles": "The modality A/B in the build plan."
  },
  {
   "claim": "A fluent solver skips writing the zero equation and the right side restated, and writes the zeros, the sign value and the sentence.",
   "settles": "Per-step timing data from the fluency telemetry."
  }
 ],
 "sources": [
  "BC-CON-07011",
  "BC-SKL-07039",
  "BC-SKL-07043",
  "BC-EK-FUN-7H1",
  "BC-EK-FUN-7H2",
  "ced:145",
  "BC-QA-07009",
  "BC-ERR-07039",
  "BC-ERR-07043",
  "BC-ERR-07044",
  "BC-MIS-07023",
  "BC-MIS-07024",
  "BC-MIS-07025",
  "BC-PRQ-07003",
  "research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations",
  "research/question-analysis/question-archetypes.md#BC-QA-07009 Logistic model interpreted without solving",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 574,
  "brief": 450
 },
 "read_minutes": {
  "full": 3.83,
  "brief": 3.0
 }
}
```
