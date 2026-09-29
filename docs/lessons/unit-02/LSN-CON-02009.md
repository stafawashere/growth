---
title: LSN-CON-02009 Ways a derivative fails to exist at a point of continuity
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02009, the ways a derivative fails to exist at a point of continuity, built from authoring_bundle("BC-CON-02009") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02009 Ways a derivative fails to exist at a point of continuity

Concept BC-CON-02009 (skills BC-SKL-02021, BC-SKL-02022, BC-SKL-02023), topic 2.4 of Unit 2, loaded by BC-QA-02005 (primary) and BC-QA-05014. The structure follows LSN-CON-02013.

## Orientation

Served text (46 words), from BC-CON-02009 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist): MCQ forms ask whether the function is differentiable at a named point and why, and the reason carries its own weight. Delivered as a static three panel figure (Delivery).

## Key ideas

One BC-EK maps to the three skills, BC-EK-FUN-2A2 (ced:63), so one core block, both bands.

- ki-1 (core). The converse fails, with the two CED routes (unequal one sided limits of the quotient at the corner of \(|x|\), a vertical tangent at the cube root), paraphrased from the Converse fails paragraph. Anchor quote (14 words) from ced:63. Notation line: corner; vertical tangent.

## Recognition

- BC-QA-02005 (family differentiability-and-continuity, single MCQ or one part, no calculator; research/question-analysis/question-archetypes.md#BC-QA-02005 Point of non-differentiability identified on a continuous function): `typical_wording` "Is the given function differentiable at the named input? Give a reason for your answer."; `common_givens` a piecewise rule, a graph with its tangent lines described, an absolute value function; `asked_to_produce` a verdict, a reason from one sided slopes or the tangent line, the inputs where the function is continuous but not differentiable. The signal is the word differentiable asked about a named input, with a fractional power, an absolute value or a piecewise boundary there. `official_examples`: BC-MCQ-CED-002, BC-MCQ-SAMPLE-003, BC-MCQ-PE2012-011.
- BC-QA-05014 (family critical-points; research/question-analysis/question-archetypes.md#BC-QA-05014 Every critical point found, including inputs where the derivative fails to exist): `typical_wording` "find all critical points of f"; `common_givens` a quotient with a fractional power or absolute value in the numerator. The signal is a critical point question on such a rule, where the inputs with no derivative join the list.

What says "not this concept": the stem states differentiability and asks for continuity (BC-CON-02008); the function is discontinuous at the input, so the contrapositive settles it (BC-SKL-02024).

## Method choice

Two strategy blocks, low and mid bands, the first only in mid.

- st-1, BC-QA-02005. Method, `expected_solution_path[0]`: confirm that the function is continuous at the input; then the two one sided quotients. Rival, `wrong_approaches`: continuity taken as differentiability (BC-ERR-02012) or the look of the graph (BC-ERR-02013). Separating feature: continuity is only the entry condition.
- st-2, BC-QA-05014. Method, `expected_solution_path[0]`: differentiate. Rival, `wrong_approaches`: setting only the derivative equal to zero. Separating feature: the fractional power or absolute value marks an input with no derivative where the function is defined.

## Solution path

- ex-1, BC-QA-02005, both bands, no calculator. Draw: coefficient 2, exponent 2/3, point 1, shift 3, giving \(f(x)=2(x-1)^{2/3}+3\) (the `parameter_spec` notes: an even numerator gives a cusp, one sided quotients of opposite signs). Steps follow `expected_solution_path`: continuity (no value), right quotient and its limit \(\infty\), left quotient and its limit \(-\infty\), the verdict. A fluent solver writes the two limits and the verdict and holds the continuity check and the quotient setup in the head.

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

None. Neither BC-QA-02005 nor the example's steps carry point types; BC-QA-05014 lists BC-PT-99013 but no example is drawn from it, so no reader checklist is served and the lesson says nothing about points beyond the error records' consequence text.

## Traps

Three active errors meet the concept's skills, in the bundle's order. Low band all three, mid band the first two.

- err-BC-ERR-02012 (BC-MIS-02006). Wrong: continuity at 1 taken to give \(f'(1)=0\). Right: the right quotient tends to \(\infty\). Distinct.
- err-BC-ERR-02013 (BC-MIS-02007). Wrong: the graph read as sharp. Right: the quotient and its one sided limits. Distinct.
- err-BC-ERR-03012 (BC-MIS-02007). Wrong: the numerator of \(f'(x)=\frac{4}{3(x-1)^{1/3}}\) set to zero for the vertical tangent. Right: the denominator set to zero, \(x=1\). Distinct. The record is scoped to parametric slopes; its skills include BC-SKL-02023 [inferred applicability, listed under Sources].

## Representations

None as a separate block. The topic's Representations paragraph (a graph to a verdict on differentiability) is carried by the orientation figure and the ki-1 motion.

## Prerequisite bridge

- BC-PRQ-02001 (Expanding and simplifying a difference quotient), from its `description_plain` and `failure_signature`, served when that state is unmet.

## Time

BC-QA-02005 is `no_calculator` and a single MCQ or one part, so the part is Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout; plan 15, Fluency). A fluent solver writes the two one sided limits and the verdict with its reason; continuity and the quotient setup are read, not written.

## Checks

- chk-1, completion of ex-1, both bands: the two limits given, the student states the verdict and reason. Statement key.
- chk-2, isomorph on BC-QA-02005, both bands: \(f(x)=3(x+2)^{1/5}+1\) at \(x=-2\), a vertical tangent. Statement key.
- chk-3, MCQ on BC-QA-02005, low band: \(f(x)=-(x-2)^{2/3}\) at 2. Key D. Distractors: A (BC-ERR-02012), B (BC-ERR-02013), C (BC-ERR-03012).

No draw equals a published BC-QA-02005 `parameter_draw`.

## Delivery

- orientation: figure, three static panels (corner, cusp, vertical tangent) with labels inside. Rule 3, BC-REP-02 on all three skills; unit README delivery map [inferred].
- ki-1: motion, left and right secants of \(|x|\) from the origin closing as \(h\) shrinks, slopes \(-1\) and 1 labelled inside; reduced motion steps frames on key press; fallback the last frame with a slope table. Rule 2 [inferred; settled by the modality A/B].
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-02012, err-BC-ERR-02013, err-BC-ERR-03012: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, st-2, ex-1, err-BC-ERR-02012, err-BC-ERR-02013, err-BC-ERR-03012, chk-1, chk-2, chk-3, the bridge. 0 words, 6.0 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, err-BC-ERR-02012, err-BC-ERR-02013, chk-1, chk-2, the bridge. 0 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02012, err-BC-ERR-02013, err-BC-ERR-03012, ex-1.

## Sources

- BC-CON-02009; BC-SKL-02021, BC-SKL-02022, BC-SKL-02023; BC-EK-FUN-2A2; ced:63
- BC-QA-02005, BC-QA-05014; BC-MCQ-CED-002, BC-MCQ-SAMPLE-003, BC-MCQ-PE2012-011
- BC-ERR-02012, BC-ERR-02013, BC-ERR-03012; BC-MIS-02006, BC-MIS-02007
- BC-PRQ-02001
- research/units/unit-02-differentiation-definition-properties.md#2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist
- research/question-analysis/question-archetypes.md#BC-QA-02005 Point of non-differentiability identified on a continuous function
- research/question-analysis/question-archetypes.md#BC-QA-05014 Every critical point found, including inputs where the derivative fails to exist
- research/exam/exam-structure.md#Section and part layout
- [inferred] Motion and figure modes. Settled by the modality A/B.
- [inferred] No corner draw exists in BC-QA-02005's spec. Settled by a staging pass adding the shape.
- [inferred] BC-ERR-03012 applied to a power's vertical tangent. Settled by a library review of its skills.

## Machine record

```json
{
 "id": "LSN-CON-02009",
 "kind": "concept",
 "target_id": "BC-CON-02009",
 "unit": "02",
 "skills": [
  "BC-SKL-02021",
  "BC-SKL-02022",
  "BC-SKL-02023"
 ],
 "orientation": {
  "text": "A response decides whether a derivative exists where the function is continuous, and names the reason from the one sided difference quotients: a corner, a cusp or a vertical tangent means no derivative. Continuity alone never settles it.",
  "sources": [
   "BC-CON-02009",
   "research/units/unit-02-differentiation-definition-properties.md#2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-2A2",
   "depth": "core",
   "text": "A continuous function can fail to be differentiable at a point of its domain (BC-EK-FUN-2A2, ced:63). At a corner, as for \\(|x|\\) at 0, the quotient has different limits from left and right. At a vertical tangent, as for the cube root at 0, the tangent has no slope. The verdict comes from the one sided quotients, not the look of the graph.",
   "notation": "corner; vertical tangent",
   "quote": {
    "text": "A continuous function may fail to be differentiable at a point in its domain.",
    "source": "ced:63"
   },
   "sources": [
    "BC-EK-FUN-2A2",
    "ced:63",
    "research/units/unit-02-differentiation-definition-properties.md#2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-02005",
   "cue": "The stem names an input of continuity and asks whether the function is differentiable there, with a reason.",
   "method": "First line: continuity at the input, then the two one sided quotients.",
   "rival": "Rival: differentiability from continuity (BC-ERR-02012), or the look of the graph (BC-ERR-02013).",
   "separating_feature": "Continuity is only the entry condition; the verdict needs both one sided limits of the quotient.",
   "sources": [
    "BC-QA-02005"
   ],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-05014",
   "cue": "The stem asks for all critical points of a quotient with a fractional power or an absolute value.",
   "method": "First written line: the derivative, then its zeros and the inputs where it fails to exist.",
   "rival": "The rival is setting only the derivative equal to zero.",
   "separating_feature": "A fractional power or absolute value marks an input where the function is defined but has no derivative.",
   "sources": [
    "BC-QA-05014"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-02005",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "coefficient": "2",
    "exponent": "2/3",
    "point": "1",
    "shift": "3"
   },
   "problem": {
    "text": "Let \\(f(x)=2(x-1)^{2/3}+3\\), the power read as a real cube root. Is \\(f\\) differentiable at \\(x=1\\)? Give a reason.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The stem asks about \\(x=1\\): confirm continuity first.",
     "why": "\\(f(1)=3\\) and the power is continuous."
    },
    {
     "cue": "Right side, \\(h>0\\): write the quotient.",
     "why": "\\(\\frac{f(1+h)-f(1)}{h}=\\frac{2h^{2/3}}{h}\\).",
     "expr": "2*h**(2/3)/h",
     "relation": "new"
    },
    {
     "cue": "Let \\(h\\to0^+\\).",
     "why": "\\(2h^{-1/3}\\) grows without bound.",
     "expr": "oo",
     "relation": "limit",
     "variable": "h",
     "point": "0",
     "dir": "+"
    },
    {
     "cue": "Left side, \\(h<0\\), where \\(h^{2/3}=(-h)^{2/3}\\).",
     "why": "Positive numerator, negative \\(h\\).",
     "expr": "2*(-h)**(2/3)/h",
     "relation": "new"
    },
    {
     "cue": "Let \\(h\\to0^-\\).",
     "why": "The quotient falls without bound.",
     "expr": "-oo",
     "relation": "limit",
     "variable": "h",
     "point": "0",
     "dir": "-"
    },
    {
     "cue": "Verdict with reason: compare the sides.",
     "why": "Opposite infinite limits: a cusp. Not differentiable at 1."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "not differentiable",
    "text": "f is not differentiable at x = 1: the one sided quotients tend to infinity and negative infinity."
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-02012",
   "observed_behavior": "The response concludes that a function is differentiable at a point because it is continuous there.",
   "scoring_consequence": "A justification point is lost because the claim is not supported by the theorem.",
   "wrong_step": {
    "text": "Continuous at 1, so \\(f'(1)=0\\).",
    "expr": "0"
   },
   "right_step": {
    "text": "The right quotient tends to \\(\\infty\\).",
    "expr": "oo"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02006",
    "text": "continuity at a point is taken to supply a derivative there"
   },
   "sources": [
    "BC-ERR-02012",
    "BC-MIS-02006"
   ]
  },
  {
   "error_id": "BC-ERR-02013",
   "observed_behavior": "The response says the derivative does not exist because the graph looks sharp, without reference to the one sided slopes.",
   "scoring_consequence": "The reason point is lost although the verdict may be correct.",
   "wrong_step": {
    "text": "The graph looks sharp at 1.",
    "expr": "2*(x-1)**(2/3)+3"
   },
   "right_step": {
    "text": "One sided quotient limits \\(\\infty\\) and \\(-\\infty\\).",
    "expr": "2*h**(2/3)/h"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02007",
    "text": "decides whether a derivative exists from how the curve looks"
   },
   "sources": [
    "BC-ERR-02013",
    "BC-MIS-02007"
   ]
  },
  {
   "error_id": "BC-ERR-03012",
   "observed_behavior": "The denominator of dy/dx is set to zero when a horizontal tangent is requested, or the numerator when a vertical tangent is requested.",
   "scoring_consequence": "The reported point is wrong and the reasoning point is not available.",
   "wrong_step": {
    "text": "For a vertical tangent, the numerator 4 of \\(f'(x)=\\frac{4}{3(x-1)^{1/3}}\\) is set to zero: no solution.",
    "expr": "4"
   },
   "right_step": {
    "text": "The denominator \\(3(x-1)^{1/3}\\) is set to zero: \\(x=1\\).",
    "expr": "1"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02007",
    "text": "a vertical tangent is read as a slope"
   },
   "sources": [
    "BC-ERR-03012",
    "BC-MIS-02007"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-02001",
   "text": "One sided quotients rest on simplifying a difference quotient: evaluate at the shifted input, subtract, divide out the common factor. A quotient written but never reduced to a form where the increment can go to zero is the gap to close first."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    3,
    5,
    6
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
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
   "archetype_id": "BC-QA-02005",
   "parameter_draw": {
    "coefficient": "2",
    "exponent": "2/3",
    "point": "1",
    "shift": "3"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The quotients at 1 tend to \\(\\infty\\) (right) and \\(-\\infty\\) (left). State the verdict and reason.",
    "command_verb": "state"
   },
   "key": {
    "form": "statement",
    "expr": "not differentiable",
    "text": "Not differentiable: the one sided quotients have opposite infinite limits, a cusp."
   },
   "steps": [
    {
     "text": "Right quotient \\(2h^{2/3}/h\\).",
     "expr": "2*h**(2/3)/h",
     "relation": "new"
    },
    {
     "text": "It tends to \\(\\infty\\).",
     "expr": "oo",
     "relation": "limit",
     "variable": "h",
     "point": "0",
     "dir": "+"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02022"
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
   "archetype_id": "BC-QA-02005",
   "parameter_draw": {
    "coefficient": "3",
    "exponent": "1/5",
    "point": "-2",
    "shift": "1"
   },
   "stem": {
    "text": "Let \\(f(x)=3(x+2)^{1/5}+1\\), the power read as a real fifth root. Is \\(f\\) differentiable at \\(x=-2\\)? Give a reason.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "not differentiable",
    "text": "Not differentiable: both one sided quotients grow without bound, a vertical tangent."
   },
   "steps": [
    {
     "text": "Right quotient \\(3h^{1/5}/h\\).",
     "expr": "3*h**(1/5)/h",
     "relation": "new"
    },
    {
     "text": "It tends to \\(\\infty\\).",
     "expr": "oo",
     "relation": "limit",
     "variable": "h",
     "point": "0",
     "dir": "+"
    },
    {
     "text": "Left quotient, \\(h<0\\): \\(-3(-h)^{1/5}/h\\).",
     "expr": "-3*(-h)**(1/5)/h",
     "relation": "new"
    },
    {
     "text": "It also tends to \\(\\infty\\).",
     "expr": "oo",
     "relation": "limit",
     "variable": "h",
     "point": "0",
     "dir": "-"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02023"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-02005",
   "parameter_draw": {
    "coefficient": "-1",
    "exponent": "2/3",
    "point": "2",
    "shift": "0"
   },
   "stem": {
    "text": "Let \\(f(x)=-(x-2)^{2/3}\\), the power read as a real cube root. Which statement about \\(f\\) at \\(x=2\\) is correct?",
    "command_verb": "choose"
   },
   "key": {
    "form": "statement",
    "expr": "D",
    "text": "Not differentiable: the one sided quotients tend to negative infinity and infinity."
   },
   "steps": [
    {
     "text": "Right quotient \\(-h^{2/3}/h\\).",
     "expr": "-h**(2/3)/h",
     "relation": "new"
    },
    {
     "text": "It tends to \\(-\\infty\\).",
     "expr": "-oo",
     "relation": "limit",
     "variable": "h",
     "point": "0",
     "dir": "+"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "Differentiable, because \\(f\\) is continuous at \\(x=2\\).",
     "error_path": "BC-ERR-02012",
     "derivation": "continuity taken to supply a derivative"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "Not differentiable, because the graph has a sharp point at \\(x=2\\).",
     "error_path": "BC-ERR-02013",
     "derivation": "verdict from the look of the graph"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "Differentiable: the numerator of \\(f'(x)\\) is never zero, so there is no vertical tangent.",
     "error_path": "BC-ERR-03012",
     "derivation": "numerator set to zero for a vertical tangent"
    },
    {
     "id": "D",
     "is_key": true,
     "label": "Not differentiable: the one sided quotients tend to \\(-\\infty\\) and \\(\\infty\\).",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02022"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-02021, 02022 and 02023; unit README delivery map; the orientation names three fixed shapes, nothing varies",
   "sources": [
    "BC-SKL-02021",
    "BC-SKL-02022",
    "BC-SKL-02023"
   ],
   "spec": {
    "kind": "graph_panels",
    "panels": [
     {
      "curve": "Abs(x)",
      "window": {
       "x": [
        -2,
        2
       ],
       "y": [
        -1,
        2
       ]
      },
      "labels": [
       {
        "text": "corner: slopes -1 and 1",
        "placement": "inside"
       }
      ]
     },
     {
      "curve": "Abs(x)**(2/3)",
      "window": {
       "x": [
        -2,
        2
       ],
       "y": [
        -1,
        2
       ]
      },
      "labels": [
       {
        "text": "cusp: quotients to -oo and oo",
        "placement": "inside"
       }
      ]
     },
     {
      "curve": "sign(x)*Abs(x)**(1/3)",
      "window": {
       "x": [
        -2,
        2
       ],
       "y": [
        -2,
        2
       ]
      },
      "labels": [
       {
        "text": "vertical tangent: no slope",
        "placement": "inside"
       }
      ]
     }
    ],
    "labels": [
     {
      "text": "each continuous at x = 0, none differentiable there",
      "placement": "inside"
     }
    ]
   },
   "fallback": "Alt text naming the three graphs, each continuous at 0, with the one sided behaviour of each written in words.",
   "keyboard": "none needed: a static figure; panels reached in reading order with Tab"
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: the key idea describes a one sided limit being taken, left and right secants closing to two slopes; unit README delivery map",
   "sources": [
    "BC-SKL-02022",
    "BC-QA-02005"
   ],
   "spec": {
    "kind": "graph_sweep",
    "parameter": "h, the run of each secant from (0, 0)",
    "curves": [
     {
      "expr": "Abs(x)",
      "label": {
       "text": "y = |x|",
       "placement": "inside"
      }
     }
    ],
    "frames": [
     {
      "h": 1
     },
     {
      "h": 0.5
     },
     {
      "h": 0.1
     },
     {
      "h": 0.01
     }
    ],
    "secants": [
     {
      "from": [
       0,
       0
      ],
      "to": "(h, |h|)",
      "label": {
       "text": "right secant slope 1",
       "placement": "inside"
      }
     },
     {
      "from": [
       0,
       0
      ],
      "to": "(-h, |h|)",
      "label": {
       "text": "left secant slope -1",
       "placement": "inside"
      }
     }
    ],
    "labels": [
     {
      "text": "two slopes, no single tangent",
      "placement": "inside"
     }
    ]
   },
   "fallback": "The last frame static, with a two row table of secant slopes at h = 1, 0.5, 0.1, 0.01: right 1, 1, 1, 1; left -1, -1, -1, -1.",
   "reduced_motion": "No auto-advance; each frame cross-fades to the next on the student's key press.",
   "keyboard": "Right and Left arrow keys step the frames; Home returns to h = 1"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02012",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-03012",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-02012",
  "err-BC-ERR-02013",
  "err-BC-ERR-03012",
  "ex-1"
 ],
 "read_minutes": {
  "full": 6.0,
  "brief": 3.0
 },
 "word_count": {
  "full": 0,
  "brief": 0
 },
 "research_lines": [
  {
   "file": "research/question-analysis/question-archetypes.md",
   "line": "the reason must refer to the one sided behaviour of the difference quotient or to the tangent line rather than to the appearance of the graph alone"
  }
 ],
 "inferred": [
  {
   "claim": "Motion for the one sided secants and a static three panel figure for the orientation serve better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "The parameter_spec of BC-QA-02005 draws only powers, so no example shows a corner; the corner is carried by the motion on |x| from ced:63.",
   "settles": "A library staging pass adding an absolute value or piecewise shape to the spec."
  },
  {
   "claim": "BC-ERR-03012 is scoped to parametric and implicit slopes; its use here on the vertical tangent of a power rests on its skill list naming BC-SKL-02023.",
   "settles": "A library review of BC-ERR-03012's skills."
  }
 ],
 "sources": [
  "BC-CON-02009",
  "BC-SKL-02021",
  "BC-SKL-02022",
  "BC-SKL-02023",
  "BC-EK-FUN-2A2",
  "ced:63",
  "BC-QA-02005",
  "BC-QA-05014",
  "BC-ERR-02012",
  "BC-ERR-02013",
  "BC-ERR-03012",
  "BC-MIS-02006",
  "BC-MIS-02007",
  "BC-PRQ-02001",
  "research/units/unit-02-differentiation-definition-properties.md#2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist",
  "research/question-analysis/question-archetypes.md#BC-QA-02005 Point of non-differentiability identified on a continuous function",
  "research/question-analysis/question-archetypes.md#BC-QA-05014 Every critical point found, including inputs where the derivative fails to exist",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
