---
title: LSN-CON-02015 Derivatives of the remaining trigonometric functions by rewriting
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02015, the derivatives of tangent, cotangent, secant and cosecant by rewriting, built from authoring_bundle("BC-CON-02015") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02015 Derivatives of the remaining trigonometric functions by rewriting

Concept BC-CON-02015 (skills BC-SKL-02043, BC-SKL-02044, BC-SKL-02045, BC-SKL-02046), topic 2.10 of Unit 2, loaded by BC-QA-02010 only. The structure follows LSN-CON-02013.

## Prediction

Served first, both bands. On ex-1's function, \(h(x)=3\sec x-2\cot x\), the student picks the derivative of \(-2\cot x\): \(-2\csc^2x\), \(2\csc^2x\) or \(2\sec^2x\). Format `mcq`, key \(2\csc^2x\). The first distractor is the sign error BC-ERR-02025 records. The resolution states that the cotangent, written as \(\frac{\cos x}{\sin x}\), differentiates to \(-\csc^2x\) by the quotient rule and that the cofunctions carry a negative sign, in the words of BC-EK-FUN-3B3 on ced:69. Sources: BC-CON-02015, BC-EK-FUN-3B3, ced:69 [verified].

## Orientation

Served text, from BC-CON-02015 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.10 Finding the Derivatives of Tangent, Cotangent, Secant, and/or Cosecant Functions): rewrite, quotient rule, identity. The sentence on the requested trigonometric form was cut to bring the brief form under 450 words. No count, no frequency.

## Key ideas

One BC-EK maps to the four skills, BC-EK-FUN-3B3 (ced:69), so one core block, both bands.

- ki-1 (core). The rewriting, the four results and why the identity choice is assessed, paraphrased from the Rewriting, Results and Why the rewriting matters paragraphs. The anchor quote was dropped to bring the brief form under 450 words. The concept's notation field is empty, so the notation line is the topic's [inferred source choice].

## Recognition

- BC-QA-02010 (family rule-manipulation, single MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-02010 Derivative of a tangent, cotangent, secant, or cosecant expression): `typical_wording` "Find the derivative of the given function."; `common_givens` an expression containing tangent, cotangent, secant or cosecant; `asked_to_produce` the derivative. The signal is one of the four names in the stem; the spec always pairs a tangent or secant with a cofunction, so one term carries a negative sign. No `official_examples`.

The contrast pair on st-1 takes its near miss from the sibling concept BC-CON-02012. `this` pairs a tangent with a cosecant on BC-QA-02010 (a different draw from every published item). `not_this` pairs a sine with a cosine, which reads as the same kind of trigonometric expression but needs no rewriting; the feature is one of the four reciprocal or quotient functions named in the stem.

What says "not this concept": only sine and cosine as whole terms (BC-CON-02012); a quotient of polynomial and trigonometric pieces with no reciprocal function (BC-CON-02014).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-02010. Method, `expected_solution_path[0]`: rewrite the function using sine and cosine, served with no leading label. Rival, `wrong_approaches`: numerator and denominator differentiated separately (BC-ERR-02026). Separating feature: after rewriting, a variable denominator.

## Solution path

- ex-1, BC-QA-02010, both bands, no calculator. Draw: first sec, second cot, coefficients 3 and \(-2\), evaluate expression: \(h(x)=3\sec x-2\cot x\). Steps follow `expected_solution_path`: rewrite, quotient rule (differentiate), Pythagorean identity, requested form. In an MCQ a fluent solver writes the final line from the four results and holds the derivation in the head [inferred]; a justification variant writes every line.

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

None. BC-QA-02010 lists no `point_types`, so no step is tagged and the lesson says nothing about points beyond the error records' consequence text.

## Traps

Three active errors meet the concept's skills, in the bundle's order. Low band all three, mid band the first two.

- err-BC-ERR-02021 (BC-MIS-02012): numerator reversed on the secant term. Distinct, `fix_prompt` true.
- err-BC-ERR-02025 (BC-MIS-02013): the cotangent derivative without its sign. Distinct, `fix_prompt` true.
- err-BC-ERR-02026: pieces differentiated separately, \(2\tan x\). Distinct, `fix_prompt` true. No possible reason: neither linked BC-MIS description names this move.

## Representations

None. The topic's Representations paragraph names BC-REP-01 and BC-REP-04; the conversion is symbolic.

## Prerequisite bridge

- BC-PRQ-02002 (Reciprocal and quotient trigonometric identities), from its `description_plain` and `failure_signature`, served when that state is unmet.

## Time

BC-QA-02010 is `no_calculator` and a single MCQ, so the part is Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout; plan 15, Fluency). The rewriting and quotient lines are the recovery route when a result is in doubt.

## Checks

- chk-1, completion of ex-1, both bands: the simplified quotient given, the requested form written. Key equals ex-1's answer.
- chk-2, isomorph on BC-QA-02010, both bands: \(4\tan x+\cot x\). Key \(4\sec^2x-\csc^2x\).
- chk-3, MCQ on BC-QA-02010, low band: \(2\tan x+3\csc x\) at \(\frac{\pi}{4}\). Key \(4-3\sqrt2\). Distractors \(-4-3\sqrt2\) (BC-ERR-02021), \(4+3\sqrt2\) (BC-ERR-02025), \(-2\) (BC-ERR-02026), each the value its error path produces on this draw.

No draw equals a published BC-QA-02010 `parameter_draw`.

## Delivery

- orientation, ki-1: text. Rule 5, BC-REP-01 and 04 only; unit README delivery map.
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-02021, err-BC-ERR-02025, err-BC-ERR-02026: step_reveal. Rule 1.

No drawn block applies: BC-REP-04 is not figure-bearing under rules 2 to 5 and no key idea describes a process, so the machine record states `no_figure_reason` [inferred; settled by the modality A/B].

## Band plan

- Low (full): prediction, orientation, the bridge, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-02021, err-BC-ERR-02025, err-BC-ERR-02026, chk-2, chk-3. 486 words, 3.3 minutes (cap 900 and 6). No second example, so no fade.
- Mid (brief): prediction, orientation, the bridge, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-02021, err-BC-ERR-02025, chk-2. 442 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02021, err-BC-ERR-02025, err-BC-ERR-02026, ex-1.

## Sources

- BC-CON-02015; BC-SKL-02043, BC-SKL-02044, BC-SKL-02045, BC-SKL-02046; BC-EK-FUN-3B3; ced:69
- BC-QA-02010
- BC-ERR-02021, BC-ERR-02025, BC-ERR-02026; BC-MIS-02012, BC-MIS-02013
- BC-PRQ-02002
- research/units/unit-02-differentiation-definition-properties.md#2.10 Finding the Derivatives of Tangent, Cotangent, Secant, and/or Cosecant Functions
- research/question-analysis/question-archetypes.md#BC-QA-02010 Derivative of a tangent, cotangent, secant, or cosecant expression
- research/exam/exam-structure.md#Section and part layout
- [inferred] Notation line from the topic. Settled by a staging pass.
- [inferred] The written and held lines under MCQ time. Settled by timing data on BC-QA-02010 items.
- [inferred] No drawn block, `no_figure_reason` stated. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-02015",
 "kind": "concept",
 "target_id": "BC-CON-02015",
 "unit": "02",
 "skills": [
  "BC-SKL-02043",
  "BC-SKL-02044",
  "BC-SKL-02045",
  "BC-SKL-02046"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict before the rule. In \\(h(x)=3\\sec x-2\\cot x\\), the cotangent term is written with sine and cosine and differentiated. What is the derivative of \\(-2\\cot x\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(-2\\csc^2x\\), keeping the sign of the term",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(2\\csc^2x\\), the negative sign of the cotangent rule carried through",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(2\\sec^2x\\), the cofunctions exchanged",
    "is_key": false
   }
  ],
  "resolution": "Written as \\(\\frac{\\cos x}{\\sin x}\\), the cotangent differentiates by the quotient rule to \\(-\\csc^2x\\). With the coefficient \\(-2\\), the term gives \\(2\\csc^2x\\). The two cofunctions carry a negative sign.",
  "sources": [
   "BC-CON-02015",
   "BC-EK-FUN-3B3",
   "ced:69"
  ]
 },
 "no_figure_reason": "The skills carry BC-REP-01 and BC-REP-04, neither figure-bearing under the delivery rules, and the conversion is symbolic with no process, so no figure, table or motion fits.",
 "orientation": {
  "text": "A response differentiates tangent, cotangent, secant or cosecant by writing it with sine and cosine, applying the quotient rule, and simplifying with the Pythagorean identity.",
  "sources": [
   "BC-CON-02015",
   "research/units/unit-02-differentiation-definition-properties.md#2.10 Finding the Derivatives of Tangent, Cotangent, Secant, and/or Cosecant Functions"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3B3",
   "depth": "core",
   "text": "Each of the four is a quotient of sine and cosine, so rewriting it lets the quotient rule differentiate it. Simplified with \\(\\sin^2x+\\cos^2x=1\\): \\((\\tan x)'=\\sec^2x\\), \\((\\cot x)'=-\\csc^2x\\), \\((\\sec x)'=\\sec x\\tan x\\), \\((\\csc x)'=-\\csc x\\cot x\\). The two cofunctions carry the negative sign. Choosing the identity is part of the work.",
   "notation": "The result written in the trigonometric form the question requests.",
   "quote": null,
   "sources": [
    "BC-EK-FUN-3B3",
    "ced:69",
    "research/units/unit-02-differentiation-definition-properties.md#2.10 Finding the Derivatives of Tangent, Cotangent, Secant, and/or Cosecant Functions"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-02010",
   "cue": "The stem asks for the derivative of an expression containing tangent, cotangent, secant or cosecant.",
   "method": "Each such function rewritten with sine and cosine.",
   "rival": "The rival is differentiating the numerator and denominator of the rewritten quotient separately.",
   "separating_feature": "After rewriting, a variable sits in the denominator, so the quotient rule applies.",
   "sources": [
    "BC-QA-02010"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Let \\(g(x)=5\\tan x-\\csc x\\). Find \\(g'(x)\\).",
     "archetype_id": "BC-QA-02010"
    },
    "not_this": {
     "text": "Let \\(r(x)=5\\sin x-\\cos x\\). Find \\(r'(x)\\).",
     "why_not": "Only sine and cosine appear, so their own rules apply with no rewriting."
    },
    "feature": "Tangent, cotangent, secant or cosecant named in the stem."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-02010",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "first": "sec",
    "second": "cot",
    "first_coefficient": "3",
    "second_coefficient": "-2",
    "evaluate": "expression",
    "angle": "1/6"
   },
   "problem": {
    "text": "Let \\(h(x)=3\\sec x-2\\cot x\\). Find \\(h'(x)\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Secant and cotangent: rewrite with sine and cosine.",
     "why": "\\(\\sec x=\\frac{1}{\\cos x}\\), \\(\\cot x=\\frac{\\cos x}{\\sin x}\\).",
     "expr": "3/cos(x)-2*cos(x)/sin(x)",
     "relation": "new"
    },
    {
     "cue": "Variable denominators: quotient rule on each term.",
     "why": "Denominator times the numerator's derivative, minus the reverse, over the square.",
     "expr": "3*sin(x)/cos(x)**2-2*(-sin(x)*sin(x)-cos(x)*cos(x))/sin(x)**2",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "cue": "The second numerator is \\(-(\\sin^2x+\\cos^2x)\\).",
     "why": "The Pythagorean identity makes it \\(-1\\).",
     "expr": "3*sin(x)/cos(x)**2+2/sin(x)**2",
     "relation": "equivalent"
    },
    {
     "cue": "The stem gave secant and cotangent: return to that family.",
     "why": "\\(\\frac{\\sin x}{\\cos^2x}=\\sec x\\tan x\\), \\(\\frac{1}{\\sin^2x}=\\csc^2x\\).",
     "expr": "3*sec(x)*tan(x)+2*csc(x)**2",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "3*sec(x)*tan(x)+2*csc(x)**2"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-02021",
   "observed_behavior": "The response subtracts in the opposite order in the numerator of the quotient rule.",
   "scoring_consequence": "The result point is lost because the derivative carries the wrong sign.",
   "wrong_step": {
    "text": "On \\(\\frac{3}{\\cos x}\\), numerator reversed: \\(-3\\sec x\\tan x\\).",
    "expr": "-3*sec(x)*tan(x)+2*csc(x)**2"
   },
   "right_step": {
    "text": "\\(3\\sec x\\tan x+2\\csc^2x\\).",
    "expr": "3*sec(x)*tan(x)+2*csc(x)**2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02012",
    "text": "the two numerator terms as interchangeable"
   },
   "sources": [
    "BC-ERR-02021",
    "BC-MIS-02012"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-02025",
   "observed_behavior": "The response gives the derivative of cotangent or cosecant without the negative sign.",
   "scoring_consequence": "The result point is lost.",
   "wrong_step": {
    "text": "\\((\\cot x)'\\) taken as \\(\\csc^2x\\): \\(3\\sec x\\tan x-2\\csc^2x\\).",
    "expr": "3*sec(x)*tan(x)-2*csc(x)**2"
   },
   "right_step": {
    "text": "\\((\\cot x)'=-\\csc^2x\\), so \\(+2\\csc^2x\\).",
    "expr": "3*sec(x)*tan(x)+2*csc(x)**2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02013",
    "text": "signs and cofunction pairings are exchanged"
   },
   "sources": [
    "BC-ERR-02025",
    "BC-MIS-02013"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-02026",
   "observed_behavior": "The response differentiates the numerator and the denominator of a rewritten trigonometric quotient separately.",
   "scoring_consequence": "The rule point and the result point are both lost.",
   "wrong_step": {
    "text": "\\(\\frac{0}{-\\sin x}\\) and \\(\\frac{-\\sin x}{\\cos x}\\): \\(2\\tan x\\).",
    "expr": "2*tan(x)"
   },
   "right_step": {
    "text": "The quotient rule on each term.",
    "expr": "3*sec(x)*tan(x)+2*csc(x)**2"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-02026"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-02002",
   "text": "Each of the four is written with sine and cosine: \\(\\tan x=\\frac{\\sin x}{\\cos x}\\), \\(\\sec x=\\frac{1}{\\cos x}\\), and \\(\\sin^2x+\\cos^2x=1\\). An attempt with no rule to hand and no rewriting is the gap to close first."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    2,
    3
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
   "archetype_id": "BC-QA-02010",
   "parameter_draw": {
    "first": "sec",
    "second": "cot",
    "first_coefficient": "3",
    "second_coefficient": "-2",
    "evaluate": "expression",
    "angle": "1/6"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The quotient rule gives \\(h'(x)=\\frac{3\\sin x}{\\cos^2x}+\\frac{2}{\\sin^2x}\\). Write \\(h'(x)\\) with secant, tangent and cosecant.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "3*sec(x)*tan(x)+2*csc(x)**2"
   },
   "steps": [
    {
     "text": "The simplified quotient line.",
     "expr": "3*sin(x)/cos(x)**2+2/sin(x)**2",
     "relation": "new"
    },
    {
     "text": "In the requested form.",
     "expr": "3*sec(x)*tan(x)+2*csc(x)**2",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02045"
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
   "archetype_id": "BC-QA-02010",
   "parameter_draw": {
    "first": "tan",
    "second": "cot",
    "first_coefficient": "4",
    "second_coefficient": "1",
    "evaluate": "expression",
    "angle": "1/3"
   },
   "stem": {
    "text": "Let \\(h(x)=4\\tan x+\\cot x\\). Find \\(h'(x)\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "4*sec(x)**2-csc(x)**2"
   },
   "steps": [
    {
     "text": "Rewrite.",
     "expr": "4*sin(x)/cos(x)+cos(x)/sin(x)",
     "relation": "new"
    },
    {
     "text": "Quotient rule, simplified.",
     "expr": "4/cos(x)**2-1/sin(x)**2",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "text": "Requested form.",
     "expr": "4*sec(x)**2-csc(x)**2",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02044"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-02010",
   "parameter_draw": {
    "first": "tan",
    "second": "csc",
    "first_coefficient": "2",
    "second_coefficient": "3",
    "evaluate": "point",
    "angle": "1/4"
   },
   "stem": {
    "text": "If \\(h(x)=2\\tan x+3\\csc x\\), then \\(h'(\\frac{\\pi}{4})=\\)",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "4-3*sqrt(2)"
   },
   "steps": [
    {
     "text": "The derivative.",
     "expr": "2*sec(x)**2-3*csc(x)*cot(x)",
     "relation": "new"
    },
    {
     "text": "At \\(\\frac{\\pi}{4}\\).",
     "expr": "4-3*sqrt(2)",
     "relation": "evaluate",
     "subs": {
      "x": "pi/4"
     }
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "-4-3*sqrt(2)",
     "error_path": "BC-ERR-02021",
     "derivation": "numerator reversed on the tangent term"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "4+3*sqrt(2)",
     "error_path": "BC-ERR-02025",
     "derivation": "the cosecant derivative without its negative sign"
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "-2",
     "error_path": "BC-ERR-02026",
     "derivation": "term by term: tan gives -cot, csc gives 0"
    },
    {
     "id": "D",
     "is_key": true,
     "expr": "4-3*sqrt(2)",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02044",
    "BC-SKL-02045"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-REP-01 and BC-REP-04 on BC-SKL-02043 to 02046, none figure-bearing; unit README delivery map",
   "sources": [
    "BC-SKL-02043",
    "BC-SKL-02046"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: identities and rules, symbolic",
   "sources": [
    "BC-SKL-02044",
    "BC-SKL-02045"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02021",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02025",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02026",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-02021",
  "err-BC-ERR-02025",
  "err-BC-ERR-02026",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.3,
  "brief": 3.0
 },
 "word_count": {
  "full": 486,
  "brief": 442
 },
 "research_lines": [
  {
   "file": "research/units/unit-02-differentiation-definition-properties.md",
   "line": "MCQ forms ask for the derivative of an expression containing one of the four functions."
  }
 ],
 "inferred": [
  {
   "claim": "BC-CON-02015 carries an empty notation field, so the key idea's notation line is taken from the topic's Notation paragraph.",
   "settles": "A library staging pass filling the concept's notation."
  },
  {
   "claim": "A fluent MCQ solver writes only the final derivative, quoting the four results, while the rewriting and quotient lines are held in the head; the topic's justification variants demand the derivation instead.",
   "settles": "Timing data on BC-QA-02010 items by whether the rewriting line is written."
  },
  {
   "claim": "No non-text delivery mode serves this concept better than text and step reveal.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-02015",
  "BC-SKL-02043",
  "BC-SKL-02044",
  "BC-SKL-02045",
  "BC-SKL-02046",
  "BC-EK-FUN-3B3",
  "ced:69",
  "BC-QA-02010",
  "BC-ERR-02021",
  "BC-ERR-02025",
  "BC-ERR-02026",
  "BC-MIS-02012",
  "BC-MIS-02013",
  "BC-PRQ-02002",
  "research/units/unit-02-differentiation-definition-properties.md#2.10 Finding the Derivatives of Tangent, Cotangent, Secant, and/or Cosecant Functions",
  "research/question-analysis/question-archetypes.md#BC-QA-02010 Derivative of a tangent, cotangent, secant, or cosecant expression",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
