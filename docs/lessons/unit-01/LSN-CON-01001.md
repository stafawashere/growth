---
title: LSN-CON-01001 Instantaneous rate of change as a limit of average rates
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01001, the instantaneous rate as the value average rates approach, built from authoring_bundle("BC-CON-01001") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01001 Instantaneous rate of change as a limit of average rates

Concept BC-CON-01001 (skills BC-SKL-01001, BC-SKL-01002, BC-SKL-01003, BC-SKL-01004), topic 1.1 of Unit 1, loaded by one archetype, BC-QA-01012 (family derivative-definition-limit). It is a root of the unit's concept order (docs/lessons/unit-01/README.md, section 1) and the first limit process the course builds.

## Orientation

Served text (40 words), from BC-CON-01001 `description_plain` and the topic's Assessment behaviour paragraph, which names the average rate with supporting work, the relation of the two kinds of rate, and formula or table sources (research/units/unit-01-limits-continuity.md#1.1 Introducing Calculus: Can Change Occur at an Instant?). No count, no frequency.

## Key ideas

The four skills map three BC-EK: BC-EK-CHA-1A2 (BC-SKL-01001, 01002), BC-EK-CHA-1A1 and BC-EK-CHA-1A3 (BC-SKL-01003, 01004), all on ced:38.

- ki-1 (core, BC-EK-CHA-1A3). The instantaneous rate is the value average rates approach over intervals containing the point, shrinking toward it; it is not the quotient evaluated at one point. No quote, to keep the brief band under its cap. Notation: instantaneous rate of change.
- ki-2 (extended, BC-EK-CHA-1A2). The average rate is the change in the function over the change in the input; a single point makes the denominator zero, so no average rate exists there. Anchor quote from ced:38 (19 words). Notation: average rate of change.
- ki-3 (extended, BC-EK-CHA-1A1). Calculus models change through limits; the rate at an instant is the limit the Unit 2 derivative is built on (topic 1.1 Prerequisites, BC-SKL-01003 to BC-TOP-0201). Anchor quote from ced:38 (8 words).

## Recognition

- BC-QA-01012 (family derivative-definition-limit; research/question-analysis/question-archetypes.md#BC-QA-01012 Instantaneous rate approached through average rates over shrinking intervals): `typical_wording` "Compute the average rate of change over each of the given intervals and describe what these values indicate about the rate at the named instant"; `common_givens` a quantity given by a formula or a table and a nested set of intervals closing on the instant; `asked_to_produce` the average rates, the value they approach, the instantaneous rate at the point. The signal is a list of intervals sharing one endpoint and shrinking, with a question about one instant. `multipart_structure` places it inside a multipart free response question; the topic's Assessment behaviour paragraph adds MCQ forms that ask for one average rate or for the statement relating the two kinds of rate. No `official_examples` are recorded.

What says "not this concept": a single interval with no instant named asks only for an average rate (BC-SKL-01001 alone); a stem naming a derivative value or a derivative rule belongs to Unit 2.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-01012. Cue, from `common_givens` and `asked_to_produce`: a quantity by formula or table and intervals closing on an instant, with a question about what the averages indicate. Method, `expected_solution_path[0]`: compute the average rate over each interval. First written line: the quotient over the first interval. Rival, `wrong_approaches`: the change reported without dividing (BC-ERR-01029), or one average taken as the exact rate (BC-ERR-01030). Separating feature: every average has a denominator, and only the value the averages approach is the rate at the instant.

The archetype record carries `asked_to_produce` and `common_givens`, so the block is verified. The research entry for BC-QA-01012 still reads "none recorded" for both; the snapshot record is the source (library gap, Sources).

## Solution path

- ex-1, BC-QA-01012, both bands, no calculator. Draw: quadratic 2, linear 1, constant 3, point 1, context particle, source formula, framing bare, so \(s(t)=2t^2+t+3\) and the rate at \(t=1\) is 5. The constraint `2 * quadratic * point + linear != 0` holds (5). Steps follow `expected_solution_path`: the quotient over \([1,1+h]\) (valued, new), the simplified quotient \(5+2h\) with the three averages 5.2, 5.02, 5.002 (valued, equivalent), the value approached (valued, limit as \(h\to0\)), and the naming of that value as the instantaneous rate (no value).

A fluent solver writes the quotient line, the averages and the named limit, and holds the expansion of the numerator in the head [inferred: settled by timing written against held steps in the modality A/B]. No productive-failure target sits in this concept, so no comparison callout.

## Scoring

None. BC-QA-01012 lists no `point_types`, so the lesson carries no what_a_reader_scores entry, no step carries a point tag and the lesson says nothing about points (plan 15, R14). The research entry's `Scoring pattern` names one point for the averages with supporting work and one for the description, but no BC-PT backs it, so it is not served.

## Traps

Two active errors meet the concept's skills, in the bundle's order; both are served in the low and mid bands.

- err-BC-ERR-01029 (BC-MIS-01017, BC-MIS-02001). Wrong step on ex-1's draw: the change \(s(1.1)-s(1)=0.52\) reported. Right step: \(0.52/0.1=5.2\). Distinct. Possible reason, words from BC-MIS-02001: the division by the change in the input is omitted.
- err-BC-ERR-01030 (BC-MIS-01017, BC-MIS-01003). Wrong step: the average over \([1,1.1]\), 5.2, given as the rate at \(t=1\). Right step: the limit 5. Distinct. Possible reason, words from BC-MIS-01017: the difference quotient over an interval is treated as the rate at an instant, so no limiting process is invoked.

## Representations

None. The topic's Representations paragraph names BC-REP-01, 03, 04 and 05 and two conversions (context to a difference quotient, a table to a sequence of average rates); the table of averages is carried by the orientation's table and ex-1's step 2, so no separate block is served.

## Prerequisite bridge

One bridge, BC-PRQ-06005 (supporting parent of all four skills), from its `description_plain` and `failure_signature`, gated by state.

## Time

BC-QA-01012 has `calculator_status` either and is one part of a multipart free response question. Under the task rule an either archetype takes Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout), and the choice is [inferred]: plan 15 gives no rule for either, and the free response shape would take 15.0 minutes per question. Inside 2.14 minutes a fluent solver writes the quotient over \([1,1+h]\), the simplified form, and the limit with its name; the numerator expansion is done in the head.

## Checks

- chk-1, completion of ex-1, both bands: the averages \(5+2h\) are given, the student states the value approached. Key 5, equal to ex-1's answer.
- chk-2, isomorph on BC-QA-01012, both bands: \(s(t)=3t^2-2t+1\), rate at \(t=1\). Key 4.
- chk-3, MCQ on BC-QA-01012, low band: \(V(t)=t^2+2t+4\), rate at \(t=2\). Key 6. Distractors: 0.61 (BC-ERR-01029, the change over \([2,2.1]\)), 6.1 (BC-ERR-01030, the average over \([2,2.1]\) as the exact rate), 0.0601 (BC-ERR-01029, the change over \([2,2.01]\)).

No example or check draw equals a published BC-QA-01012 `parameter_draw` (content/items_*), which the checker confirms.

## Delivery

- orientation: table. Rule 4, BC-REP-03 on BC-SKL-01001 and BC-SKL-01004; the unit README's delivery map picks table. The three intervals, changes and averages of ex-1's draw.
- ki-1: motion. Rule 2, a limit process named by BC-SKL-01003 and BC-SKL-01004 (averages over shrinking intervals): a secant through \(t=1\) and \(t=1+h\) closing on the tangent as \(h\) takes 1, 0.5, 0.1, 0.01. Reduced motion cross-fades frames on a key press.
- ki-2, ki-3: text. Rule 5; BC-SKL-01002 carries BC-REP-04 only, and ki-3 is a statement about the course.
- ex-1: step_reveal, rule 1; the model the unit README names (averages at shrinking h) is carried inside step 2 as a three-row table, not a separate block.
- err-BC-ERR-01029, err-BC-ERR-01030: step_reveal, rule 1.

Every non-text choice is [inferred], settled by the modality A/B in the build plan.

## Band plan

- Low (full): orientation, ki-1, ki-2, ki-3, st-1, ex-1, err-BC-ERR-01029, err-BC-ERR-01030, chk-1, chk-2, chk-3, bridge BC-PRQ-06005 when the state gates it. 576 words, 3.9 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, both error blocks, chk-1, chk-2, bridge when gated. 441 words, 2.95 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-01029, err-BC-ERR-01030, ex-1.

## Sources

- BC-CON-01001; BC-SKL-01001, BC-SKL-01002, BC-SKL-01003, BC-SKL-01004; BC-EK-CHA-1A1, BC-EK-CHA-1A2, BC-EK-CHA-1A3; ced:38
- BC-QA-01012; BC-TOP-0101, BC-TOP-0201
- BC-ERR-01029, BC-ERR-01030; BC-MIS-01017, BC-MIS-02001, BC-MIS-01003
- BC-PRQ-06005
- research/units/unit-01-limits-continuity.md#1.1 Introducing Calculus: Can Change Occur at an Instant?
- research/question-analysis/question-archetypes.md#BC-QA-01012 Instantaneous rate approached through average rates over shrinking intervals
- research/exam/exam-structure.md#Section and part layout
- docs/lessons/unit-01/README.md, sections 1, 5 and 6
- [inferred] Exam part I-A for an either archetype shaped as a free response part. Settled by a plan 15 budget rule for calculator_status either.
- [inferred] Which steps a fluent solver holds in the head. Settled by timing written against held steps.
- [inferred] Table, motion as the delivery modes. Settled by the modality A/B.
- Library gap: research/question-analysis/question-archetypes.md records no common givens or produced objects for BC-QA-01012, while the snapshot record holds both.

## Machine record

```json
{
 "id": "LSN-CON-01001",
 "kind": "concept",
 "target_id": "BC-CON-01001",
 "unit": "01",
 "skills": [
  "BC-SKL-01001",
  "BC-SKL-01002",
  "BC-SKL-01003",
  "BC-SKL-01004"
 ],
 "orientation": {
  "text": "A response divides the change in a quantity by the change in the input over intervals closing on an instant, then names the value those averages approach as the rate at that instant. Stems give a formula or a table.",
  "sources": [
   "BC-CON-01001",
   "research/units/unit-01-limits-continuity.md#1.1 Introducing Calculus: Can Change Occur at an Instant?"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-1A3",
   "depth": "core",
   "text": "The rate at an instant is the value that average rates approach as intervals containing the point shrink toward it (BC-EK-CHA-1A3, ced:38). It is never the quotient evaluated at the point itself.",
   "notation": "instantaneous rate of change",
   "quote": null,
   "sources": [
    "BC-EK-CHA-1A3",
    "ced:38",
    "research/units/unit-01-limits-continuity.md#1.1 Introducing Calculus: Can Change Occur at an Instant?"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-1A2",
   "depth": "extended",
   "text": "The average rate of change of f from a to b is (f(b) - f(a))/(b - a), with a not equal to b. At a single point the change in the input is zero, so the quotient divides by zero and no average rate exists there (BC-EK-CHA-1A2, ced:38).",
   "notation": "average rate of change",
   "quote": {
    "text": "the average rate of change is undefined at a point where the change in the independent variable would be zero.",
    "source": "ced:38"
   },
   "sources": [
    "BC-EK-CHA-1A2",
    "ced:38"
   ]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-CHA-1A1",
   "depth": "extended",
   "text": "Calculus models change through limits (BC-EK-CHA-1A1, ced:38). The rate at an instant is the first such limit, and it is the definition the derivative of Unit 2 is built on.",
   "notation": "",
   "quote": {
    "text": "Calculus uses limits to understand and model dynamic change.",
    "source": "ced:38"
   },
   "sources": [
    "BC-EK-CHA-1A1",
    "ced:38",
    "BC-TOP-0201"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01012",
   "cue": "Intervals closing on one instant, with a formula or table, and a question about what the averages indicate.",
   "method": "First line: the quotient over the first interval.",
   "rival": "The change reported undivided (BC-ERR-01029), or one average taken as the exact rate (BC-ERR-01030).",
   "separating_feature": "Each average has a denominator; only their limit is the rate at the instant.",
   "sources": [
    "BC-QA-01012"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01012",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "quadratic": 2,
    "linear": 1,
    "constant": 3,
    "point": 1,
    "context": "particle",
    "source": "formula",
    "framing": "bare"
   },
   "problem": {
    "text": "Let s(t) = 2t^2 + t + 3. Find the average rate of change of s over [1, 1 + h] for h = 0.1, 0.01, 0.001, and state what these indicate about the rate at t = 1.",
    "command_verb": "compute"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Every interval starts at t = 1: one quotient over [1, 1 + h].",
     "why": "Change in s over change in t, with s(1) = 6.",
     "expr": "(2*(1+h)**2 + (1+h) + 3 - 6)/h",
     "relation": "new"
    },
    {
     "cue": "The numerator is 5h + 2h^2, so divide by h.",
     "why": "Averages: 5.2, 5.02, 5.002.",
     "expr": "5 + 2*h",
     "relation": "equivalent"
    },
    {
     "cue": "The stem asks what they indicate: take their limit as h shrinks.",
     "why": "5 + 2h approaches 5; no single interval gives 5.",
     "expr": "5",
     "relation": "limit",
     "variable": "h",
     "point": "0"
    },
    {
     "cue": "The stem asks about t = 1: name the limit as that rate.",
     "why": "That limit is the definition of the rate."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "5"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01029",
   "observed_behavior": "The response reports the change in the function over the interval without dividing by the change in the input.",
   "scoring_consequence": "The point for the average rate with supporting work is lost because the quotient is absent.",
   "wrong_step": {
    "text": "s(1.1) - s(1) = 0.52 reported as the rate.",
    "expr": "2*(11/10)**2 + 11/10 + 3 - 6"
   },
   "right_step": {
    "text": "Divided by 0.1: 5.2.",
    "expr": "(2*(11/10)**2 + 11/10 + 3 - 6)/(1/10)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02001",
    "text": "the division by the change in the input is omitted"
   },
   "sources": [
    "BC-ERR-01029",
    "BC-MIS-02001"
   ]
  },
  {
   "error_id": "BC-ERR-01030",
   "observed_behavior": "The response gives an average rate as the exact instantaneous rate at a point.",
   "scoring_consequence": "A point requiring the limiting description is lost, although an approximation phrased as an estimate can still earn credit.",
   "wrong_step": {
    "text": "5.2, the average over [1, 1.1], given as the rate.",
    "expr": "26/5"
   },
   "right_step": {
    "text": "The averages approach 5, the rate.",
    "expr": "5"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01017",
    "text": "no limiting process is invoked"
   },
   "sources": [
    "BC-ERR-01030",
    "BC-MIS-01017"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Each average needs the quantity at both ends of its interval. The failure: a value read for the wrong input, or f and f' interchanged."
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
    3,
    4
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
   "archetype_id": "BC-QA-01012",
   "parameter_draw": {
    "quadratic": 2,
    "linear": 1,
    "constant": 3,
    "point": 1,
    "context": "particle",
    "source": "formula",
    "framing": "bare"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For s(t) = 2t^2 + t + 3 the averages over [1, 1 + h] are 5 + 2h. Find the rate of s at t = 1.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "5"
   },
   "steps": [
    {
     "text": "The averages are 5 + 2h.",
     "expr": "5 + 2*h",
     "relation": "new"
    },
    {
     "text": "As h approaches 0 they approach 5.",
     "expr": "5",
     "relation": "limit",
     "variable": "h",
     "point": "0"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01004"
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
   "archetype_id": "BC-QA-01012",
   "parameter_draw": {
    "quadratic": 3,
    "linear": -2,
    "constant": 1,
    "point": 1,
    "context": "particle",
    "source": "formula",
    "framing": "bare"
   },
   "stem": {
    "text": "Let s(t) = 3t^2 - 2t + 1. From average rates over [1, 1 + h], find the rate of s at t = 1.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "4"
   },
   "steps": [
    {
     "text": "The quotient over [1, 1 + h], with s(1) = 2.",
     "expr": "(3*(1+h)**2 - 2*(1+h) + 1 - 2)/h",
     "relation": "new"
    },
    {
     "text": "It simplifies to 4 + 3h.",
     "expr": "4 + 3*h",
     "relation": "equivalent"
    },
    {
     "text": "The averages approach 4.",
     "expr": "4",
     "relation": "limit",
     "variable": "h",
     "point": "0"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01004"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-01012",
   "parameter_draw": {
    "quadratic": 1,
    "linear": 2,
    "constant": 4,
    "point": 2,
    "context": "tank",
    "source": "formula",
    "framing": "bare"
   },
   "stem": {
    "text": "Let V(t) = t^2 + 2t + 4. Which value do average rates of V over [2, 2 + h] approach as h shrinks?",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "6"
   },
   "steps": [
    {
     "text": "The quotient over [2, 2 + h], with V(2) = 12.",
     "expr": "((2+h)**2 + 2*(2+h) + 4 - 12)/h",
     "relation": "new"
    },
    {
     "text": "It simplifies to 6 + h.",
     "expr": "6 + h",
     "relation": "equivalent"
    },
    {
     "text": "The averages approach 6.",
     "expr": "6",
     "relation": "limit",
     "variable": "h",
     "point": "0"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "61/100",
     "error_path": "BC-ERR-01029",
     "derivation": "V(2.1) - V(2) = 0.61, the change with no division"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "61/10",
     "error_path": "BC-ERR-01030",
     "derivation": "the average over [2, 2.1], 6.1, taken as the exact rate"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "6",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "601/10000",
     "error_path": "BC-ERR-01029",
     "derivation": "V(2.01) - V(2) = 0.0601, the change with no division"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01001",
    "BC-SKL-01004"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "table",
   "reason": "rule 4: BC-REP-03 on BC-SKL-01001 and BC-SKL-01004; unit README delivery map",
   "sources": [
    "BC-SKL-01001",
    "BC-SKL-01004"
   ],
   "spec": {
    "kind": "table",
    "columns": [
     "interval",
     "change in s",
     "change in t",
     "average rate"
    ],
    "rows": [
     [
      "[1, 1.1]",
      "0.52",
      "0.1",
      "5.2"
     ],
     [
      "[1, 1.01]",
      "0.0502",
      "0.01",
      "5.02"
     ],
     [
      "[1, 1.001]",
      "0.005002",
      "0.001",
      "5.002"
     ]
    ],
    "labels": [
     {
      "text": "s(t) = 2t^2 + t + 3",
      "placement": "inside"
     },
     {
      "text": "average rate = change in s / change in t",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same three rows as static text beside the orientation",
   "keyboard": "no control; table cells are reached in reading order with Tab"
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: a limit process, averages over shrinking intervals (BC-SKL-01003, BC-SKL-01004)",
   "sources": [
    "BC-SKL-01003",
    "BC-SKL-01004"
   ],
   "spec": {
    "kind": "graph_sweep",
    "curves": [
     {
      "id": "s",
      "expr": "2*t**2 + t + 3",
      "domain": [
       0,
       2.2
      ]
     }
    ],
    "parameter": {
     "name": "h",
     "frames": [
      1,
      0.5,
      0.1,
      0.01
     ]
    },
    "overlays": [
     {
      "kind": "secant",
      "through": [
       "1",
       "1 + h"
      ]
     },
     {
      "kind": "tangent",
      "at": "1",
      "shown": "last frame"
     }
    ],
    "labels": [
     {
      "text": "s(t) = 2t^2 + t + 3",
      "placement": "inside"
     },
     {
      "text": "secant slope 5 + 2h",
      "placement": "inside"
     },
     {
      "text": "tangent slope 5 at t = 1",
      "placement": "inside"
     }
    ]
   },
   "fallback": "four static frames in a row, secant slopes 7, 6, 5.2 and 5.02 labelled inside each, the tangent drawn in the last",
   "keyboard": "Right and Left arrow keys step the frames; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 5: a definition; BC-SKL-01002 carries BC-REP-04 only",
   "sources": [
    "BC-SKL-01002"
   ]
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 5: a statement about the course with no figure-bearing representation",
   "sources": [
    "BC-SKL-01003"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1; the three averages render as a table inside step 2",
   "sources": [
    "BC-SKL-01004"
   ]
  },
  {
   "block": "err-BC-ERR-01029",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01030",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-01029",
  "err-BC-ERR-01030",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.9,
  "brief": 2.95
 },
 "word_count": {
  "full": 576,
  "brief": 441
 },
 "research_lines": [
  {
   "file": "research/units/unit-01-limits-continuity.md",
   "line": "The rate at an instant is not computed by evaluating the quotient at a single point."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-01012 has calculator_status either and a free response shape; the lesson takes Section I Part A, 2.14 minutes.",
   "settles": "A plan 15 budget rule for calculator_status either."
  },
  {
   "claim": "A fluent solver holds the numerator expansion in the head.",
   "settles": "Timing of written against held steps in the modality A/B."
  },
  {
   "claim": "Table for the orientation and motion for ki-1 serve better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-01001",
  "BC-SKL-01001",
  "BC-SKL-01002",
  "BC-SKL-01003",
  "BC-SKL-01004",
  "BC-EK-CHA-1A1",
  "BC-EK-CHA-1A2",
  "BC-EK-CHA-1A3",
  "ced:38",
  "BC-QA-01012",
  "BC-ERR-01029",
  "BC-ERR-01030",
  "BC-MIS-01017",
  "BC-MIS-02001",
  "BC-MIS-01003",
  "BC-PRQ-06005",
  "research/units/unit-01-limits-continuity.md#1.1 Introducing Calculus: Can Change Occur at an Instant?",
  "research/question-analysis/question-archetypes.md#BC-QA-01012 Instantaneous rate approached through average rates over shrinking intervals",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
