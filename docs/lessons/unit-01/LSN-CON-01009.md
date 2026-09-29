---
title: LSN-CON-01009 Selection of a procedure for a limit
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01009, selecting a procedure for a limit from its form under substitution, built from authoring_bundle("BC-CON-01009") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01009 Selection of a procedure for a limit

Concept BC-CON-01009 (skills BC-SKL-01029, BC-SKL-01030, BC-SKL-01031), topic 1.7 of Unit 1, loaded by BC-QA-01014 (primary). The unit attack map places it ninth, after BC-CON-01007 and BC-CON-01008, with text delivery.

## Prediction

Served first, both bands. Pose on ex-1's own quotient: substitution at \(x=-2\) gives 0 over 0, and the student writes the limit. Form `short_answer`, key \(\frac{3}{5}\), which is ex-1's answer. The resolution says that the form after substitution picks the procedure and that zero over zero calls for rewriting, from BC-CON-01009 and the topic 1.7 paragraph. It carries no verdict word.

## Orientation

Served text, from BC-CON-01009 `description_plain` (the form under substitution decides the method) and the topic's Required mathematical knowledge and Assessment behaviour paragraphs (research/units/unit-01-limits-continuity.md#1.7 Selecting Procedures for Determining Limits), stated as what a response shows: the substitution, the named form, the procedure it calls for. No count, no frequency.

## Key ideas

No skill of BC-CON-01009 lists `essential_knowledge` (BC-SKL-01029, 01030, 01031 carry an empty list), and ced:44 prints no essential knowledge statement for topic 1.7, so the one core block carries `ek_id` null and is tagged [inferred].

- ki-1 (core). Paraphrase of the topic's Required mathematical knowledge paragraph (Classification under substitution; Procedure set available in Unit 1). No quote in the served block, to hold the brief form under its cap. Notation line from the topic: the classification stated in words before any computation (the concept's `notation` field is empty).

## Recognition

- BC-QA-01014 (family procedure-selection, single MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-01014 Procedure selected for a limit from the form of the expression). `typical_wording`: "For each of the given limits, identify an appropriate method and use it to determine the limit." `asked_to_produce`: a classification of the form after substitution, an appropriate procedure, the value. `common_givens` is empty. No official example. The signal is a stem that asks for a method or offers several limits side by side with no method named; the multi-concept form mixes a determinate substitution, an indeterminate quotient and a limit at infinity in one item (research/units/unit-01-limits-continuity.md#1.7 Selecting Procedures for Determining Limits).

What says "not this concept": a stem that already names the method (squeeze, a supplied inequality, BC-CON-01010) or supplies the limits of the pieces (BC-CON-01007); a stem that says the form is zero over zero and asks only for the value (BC-CON-01008).

The contrast pair on st-1 takes its near miss from the first of those: `this` is a limit with no method named on BC-QA-01014, `not_this` is a stem that names the squeeze theorem (BC-CON-01010), and the feature is that no method is named.

## Method choice

- st-1, BC-QA-01014, low and mid bands. Cue from `typical_wording` and `asked_to_produce`, tagged `evidence_tag: inferred` because `common_givens` is empty. Method, `expected_solution_path[0]`: substitute the target input into each expression; the first written line is that substitution and the named form. Rival, `wrong_approaches`: dividing the numerator limit by a denominator limit of zero (BC-ERR-01006). Separating feature: the quotient theorem needs a nonzero denominator limit; a zero there sends the choice to rewriting (zero over zero) or to one sided signs (nonzero over zero).

## Solution path

- ex-1, BC-QA-01014, both bands, no calculator. Draw: form factor, target \(-2\), top_root 1, bottom_root 3, root_value 1, lead_top 2, lead_bottom 3, pole_power 1, giving \(\frac{x^2+x-2}{x^2-x-6}\) [inferred shape, see Sources]. Steps follow `expected_solution_path`: substitute (the quotient, `new`), classify (no value: zero over zero), carry out the named procedure (the cancelled quotient, `equivalent`), evaluate (`limit`, x to \(-2\)). No published BC-QA-01014 draw matches.

A fluent solver writes the rewritten quotient and the value and classifies in the head [inferred]. One example only: the other forms (infinite, at_infinity) belong to BC-CON-01016 and BC-CON-01017 lessons, and an infinite value cannot be confirmed by the checker's equivalence test.

## Scoring

None. BC-QA-01014 lists no `point_types`; the lesson carries no `what_a_reader_scores` entry and no step tags a point. The error blocks keep their record text only.

## Traps

The bundle lists eight errors; the first four in its order are served (all linked BC-MIS severity high). Mid band the first two. All sit on ex-1's draw.

- err-BC-ERR-01003. Wrong: no limit because the quotient is undefined at \(-2\) (`nan`). Right: \(\frac{3}{5}\). Distinct. Reason, words from BC-MIS-01001.
- err-BC-ERR-01006. Wrong: the quotient theorem gives \(\frac{0}{0}\) (`nan`). Right: \(\frac{3}{5}\). Distinct. Reason, words from BC-MIS-01005.
- err-BC-ERR-01008. Wrong: 0. Right: \(\frac{3}{5}\). Distinct. Reason, words from BC-MIS-01006.
- err-BC-ERR-01009. Wrong: no limit (`nan`). Right: \(\frac{3}{5}\). Distinct. Reason, words from BC-MIS-01006.

BC-ERR-01019, 01020, 01023 and 01021 fall beyond the cap of four.

## Representations

None. The topic's Representations paragraph names BC-REP-01 and BC-REP-04 with the conversion expression to named procedure; nothing is figure-shaped.

## Prerequisite bridge

Two BC-PRQ parents, supporting edges, gated by state: BC-PRQ-01001 (factoring) and BC-PRQ-01008 (domain). Each bridge restates `description_plain` and names the `failure_signature`.

## Time

BC-QA-01014 is `no_calculator`, "Typically a single multiple choice item", so Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout). A fluent solver substitutes and classifies in the head (steps 1 and 2) and writes the cancelled quotient and the value (steps 3 and 4) [inferred]. Most of the budget goes to the rewriting once the form is named.

## Checks

- chk-1, completion of ex-1, both bands: the cancelled quotient is given. Key \(\frac{3}{5}\).
- chk-2, isomorph, both bands: form factor, target 1, top_root \(-4\), bottom_root 5. Key \(-\frac{5}{4}\).
- chk-3, MCQ, low band, key form statement: which step follows zero over zero at \(x=4\). Key: factor, divide out, substitute. Distractors carry BC-ERR-01008 (report 0), BC-ERR-01009 (report no limit), BC-ERR-01006 (divide the limits). The options are procedures, as `asked_to_produce` names ("an appropriate procedure for each limit").

## Delivery

- orientation: text; ki-1: text. Rule 5; the unit-01 README gives text for BC-CON-01009 (BC-REP-01 and BC-REP-04 only). The machine record states `no_figure_reason`: no figure-bearing BC-REP on any skill and no process in the key idea.
- ex-1 and the four error blocks: step_reveal. Rule 1.

The README notes a decision lesson (`contrast`) would carry the method choice across BC-CON-01007, 01008, 01016 and 01017 if confusable_sets returned it; the unit has no derived set, so this lesson stays text.

## Band plan

- Low (full): pr-1, orientation, two bridges when gated in, ki-1, st-1 with its contrast, ex-1, chk-1, err-BC-ERR-01003, err-BC-ERR-01006, err-BC-ERR-01008, err-BC-ERR-01009, chk-2, chk-3. There is no second example, so nothing fades. 576 words, 4.0 minutes (cap 900 and 6).
- Mid (brief): pr-1, orientation, bridges when gated in, ki-1, st-1 with its contrast, ex-1, chk-1, err-BC-ERR-01003, err-BC-ERR-01006, chk-2. 433 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-01009; BC-SKL-01029, BC-SKL-01030, BC-SKL-01031, BC-SKL-01021; ced:44
- BC-QA-01014
- BC-ERR-01003, BC-ERR-01006, BC-ERR-01008, BC-ERR-01009; BC-MIS-01001, BC-MIS-01005, BC-MIS-01006
- BC-PRQ-01001, BC-PRQ-01008
- research/units/unit-01-limits-continuity.md#1.7 Selecting Procedures for Determining Limits
- research/question-analysis/question-archetypes.md#BC-QA-01014 Procedure selected for a limit from the form of the expression
- research/exam/exam-structure.md#Section and part layout
- [inferred] ki-1 has no BC-EK. Settled by a library pass mapping the skills to a BC-EK.
- [inferred] st-1 rests on `typical_wording`. Settled by `common_givens` on BC-QA-01014.
- [inferred] The factor form's shape. Settled by the BC-QA-01014 template.
- [inferred] Classification held in the head. Settled by timed response logs.

## Machine record

```json
{
 "id": "LSN-CON-01009",
 "kind": "concept",
 "target_id": "BC-CON-01009",
 "unit": "01",
 "skills": [
  "BC-SKL-01029",
  "BC-SKL-01030",
  "BC-SKL-01031"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Substituting x = -2 into \\(\\frac{x^2+x-2}{x^2-x-6}\\) gives 0 over 0. What is the limit as x approaches -2?",
   "command_verb": "predict"
  },
  "format": "short_answer",
  "key": {
   "form": "numeric",
   "expr": "3/5"
  },
  "resolution": "The form after substitution picks the procedure: zero over zero calls for rewriting, and the rewritten quotient gives \\(\\frac{3}{5}\\) at -2.",
  "sources": [
   "BC-CON-01009",
   "research/units/unit-01-limits-continuity.md#1.7 Selecting Procedures for Determining Limits"
  ]
 },
 "no_figure_reason": "A classification rule stated in words. No skill carries a figure-bearing representation and the key idea describes no process to watch, so text and the step reveal serve.",
 "orientation": {
  "text": "A response substitutes the target first and names what comes out: a value, zero over zero, or a nonzero number over zero. That form picks the procedure.",
  "sources": [
   "BC-CON-01009",
   "research/units/unit-01-limits-continuity.md#1.7 Selecting Procedures for Determining Limits"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": null,
   "depth": "core",
   "text": "Substituting gives a value, zero over zero, or a nonzero number over zero. A value is the limit; zero over zero calls for rewriting; nonzero over zero calls for the sign on each side. L'Hospital's rule is not in the Unit 1 set.",
   "notation": "classification",
   "quote": null,
   "sources": [
    "ced:44",
    "research/units/unit-01-limits-continuity.md#1.7 Selecting Procedures for Determining Limits"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01014",
   "cue": "Several limits, no method named.",
   "method": "Substitute the target and classify the form.",
   "rival": "Dividing by a zero denominator limit.",
   "separating_feature": "A zero denominator limit sends the choice to rewriting or signs.",
   "sources": [
    "BC-QA-01014",
    "BC-ERR-01006"
   ],
   "evidence_tag": "inferred",
   "contrast": {
    "this": {
     "text": "Identify a method for \\(\\lim_{x\\to3}\\frac{x^2-9}{x^2-5x+6}\\) and use it.",
     "archetype_id": "BC-QA-01014"
    },
    "not_this": {
     "text": "Use the squeeze theorem to find \\(\\lim_{x\\to0}x^2\\sin\\frac{1}{x}\\).",
     "why_not": "The stem names the method, so nothing is selected."
    },
    "feature": "The stem names no method."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01014",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "target": -2,
    "top_root": 1,
    "bottom_root": 3,
    "root_value": 1,
    "lead_top": 2,
    "lead_bottom": 3,
    "form": "factor",
    "pole_power": 1
   },
   "problem": {
    "text": "Identify a method for \\(\\lim_{x\\to-2}\\frac{x^2+x-2}{x^2-x-6}\\) and use it.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "No method is named, so substitute the target first.",
     "why": "Top: \\(4-2-2=0\\). Bottom: \\(4+2-6=0\\).",
     "expr": "(x**2+x-2)/(x**2-x-6)",
     "relation": "new"
    },
    {
     "cue": "Both parts are 0: the form is zero over zero.",
     "why": "Zero over zero is indeterminate, so the procedure is rewriting; both polynomials factor."
    },
    {
     "cue": "Each polynomial vanishes at \\(-2\\), so each holds \\(x+2\\).",
     "why": "Dividing out \\(x+2\\) is valid for every \\(x\\ne-2\\).",
     "expr": "(x-1)/(x-3)",
     "relation": "equivalent"
    },
    {
     "cue": "The new quotient is defined at \\(-2\\): substitution now settles it.",
     "why": "\\(\\frac{-3}{-5}=\\frac{3}{5}\\).",
     "expr": "3/5",
     "relation": "limit",
     "variable": "x",
     "point": "-2"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "3/5"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01003",
   "observed_behavior": "The response states that the limit does not exist on the grounds that the function has no value at the input.",
   "scoring_consequence": "Both the value point and any justification point are lost.",
   "wrong_step": {
    "text": "The quotient is undefined at \\(-2\\), so the limit is reported not to exist.",
    "expr": "nan"
   },
   "right_step": {
    "text": "The limit uses inputs near \\(-2\\) only: \\(\\frac{3}{5}\\).",
    "expr": "3/5"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01001",
    "text": "a missing or displaced function value is read as a missing or displaced limit"
   },
   "sources": [
    "BC-ERR-01003",
    "BC-MIS-01001"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01006",
   "observed_behavior": "The response divides the limit of the numerator by the limit of the denominator although the denominator limit is zero.",
   "scoring_consequence": "The value point is lost and any justification naming the theorem is incorrect.",
   "wrong_step": {
    "text": "The quotient theorem gives \\(\\frac{0}{0}\\).",
    "expr": "0/0"
   },
   "right_step": {
    "text": "The denominator limit is 0, so the theorem does not apply; rewrite to \\(\\frac{3}{5}\\).",
    "expr": "3/5"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01005",
    "text": "applies the quotient and composite theorems as formal rules without the denominator condition"
   },
   "sources": [
    "BC-ERR-01006",
    "BC-MIS-01005"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01008",
   "observed_behavior": "The response reports zero because the numerator tends to zero, without attending to the denominator.",
   "scoring_consequence": "The value point is lost and the rewriting step is absent.",
   "wrong_step": {
    "text": "The numerator tends to 0, so 0 is reported.",
    "expr": "0"
   },
   "right_step": {
    "text": "Both parts tend to 0, so rewrite: \\(\\frac{3}{5}\\).",
    "expr": "3/5"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01006",
    "text": "the symbol zero over zero as an answer, reading it as zero"
   },
   "sources": [
    "BC-ERR-01008",
    "BC-MIS-01006"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01009",
   "observed_behavior": "The response states that the limit does not exist because substitution gives zero over zero.",
   "scoring_consequence": "The value point and the rewriting point are lost.",
   "wrong_step": {
    "text": "Zero over zero is reported as no limit.",
    "expr": "nan"
   },
   "right_step": {
    "text": "Zero over zero calls for rewriting: \\(\\frac{3}{5}\\).",
    "expr": "3/5"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01006",
    "text": "a nonexistence verdict rather than as a signal to rewrite"
   },
   "sources": [
    "BC-ERR-01009",
    "BC-MIS-01006"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-01001",
   "text": "Factor, then cancel a common factor. Stopping at zero over zero unfactored marks this gap."
  },
  {
   "prq_id": "BC-PRQ-01008",
   "text": "State where an expression is defined, including zeros of a denominator. Counting points outside the domain marks this gap."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    3,
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    2
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
   "archetype_id": "BC-QA-01014",
   "parameter_draw": {
    "target": -2,
    "top_root": 1,
    "bottom_root": 3,
    "root_value": 1,
    "lead_top": 2,
    "lead_bottom": 3,
    "form": "factor",
    "pole_power": 1
   },
   "completes": "ex-1",
   "stem": {
    "text": "The form is zero over zero and factoring leaves \\(\\frac{x-1}{x-3}\\) for \\(x\\ne-2\\). Find the limit at \\(-2\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "3/5"
   },
   "steps": [
    {
     "text": "The rewritten quotient \\(\\frac{x-1}{x-3}\\).",
     "expr": "(x-1)/(x-3)",
     "relation": "new"
    },
    {
     "text": "Substitution gives \\(\\frac{3}{5}\\).",
     "expr": "3/5",
     "relation": "limit",
     "variable": "x",
     "point": "-2"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01030"
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
   "archetype_id": "BC-QA-01014",
   "parameter_draw": {
    "target": 1,
    "top_root": -4,
    "bottom_root": 5,
    "root_value": 3,
    "lead_top": 1,
    "lead_bottom": 2,
    "form": "factor",
    "pole_power": 2
   },
   "stem": {
    "text": "Identify a method for \\(\\lim_{x\\to1}\\frac{x^2+3x-4}{x^2-6x+5}\\) and use it.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-5/4"
   },
   "steps": [
    {
     "text": "Substitution gives zero over zero.",
     "expr": "(x**2+3*x-4)/(x**2-6*x+5)",
     "relation": "new"
    },
    {
     "text": "Divide out \\(x-1\\).",
     "expr": "(x+4)/(x-5)",
     "relation": "equivalent"
    },
    {
     "text": "Substitute 1.",
     "expr": "-5/4",
     "relation": "limit",
     "variable": "x",
     "point": "1"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01029",
    "BC-SKL-01030"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-01014",
   "parameter_draw": {
    "target": 4,
    "top_root": -1,
    "bottom_root": 2,
    "root_value": 2,
    "lead_top": 3,
    "lead_bottom": 1,
    "form": "factor",
    "pole_power": 1
   },
   "stem": {
    "text": "Substitution into \\(\\frac{x^2-3x-4}{x^2-6x+8}\\) at \\(x=4\\) gives 0 over 0. Which step comes next?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "rewrite_by_factoring"
   },
   "steps": [
    {
     "text": "The quotient.",
     "expr": "(x**2-3*x-4)/(x**2-6*x+8)",
     "relation": "new"
    },
    {
     "text": "Divide out \\(x-4\\).",
     "expr": "(x+1)/(x-2)",
     "relation": "equivalent"
    },
    {
     "text": "Substitute 4.",
     "expr": "5/2",
     "relation": "limit",
     "variable": "x",
     "point": "4"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "Report the limit as 0",
     "error_path": "BC-ERR-01008",
     "derivation": "the numerator limit alone"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "Report that the limit does not exist",
     "error_path": "BC-ERR-01009",
     "derivation": "zero over zero read as nonexistence"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "Divide the numerator limit by the denominator limit",
     "error_path": "BC-ERR-01006",
     "derivation": "quotient theorem with a zero denominator limit"
    },
    {
     "id": "D",
     "is_key": true,
     "label": "Factor, divide out \\(x-4\\), and substitute",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01029",
    "BC-SKL-01030"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-SKL-01029 to 01031 carry BC-REP-01 and BC-REP-04 only (unit-01 README delivery map)",
   "sources": [
    "BC-SKL-01030"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: a classification rule with no figure-bearing BC-REP",
   "sources": [
    "BC-SKL-01029"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01003",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01006",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01008",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01009",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-01003",
  "err-BC-ERR-01006",
  "err-BC-ERR-01008",
  "err-BC-ERR-01009",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-01-limits-continuity.md",
   "line": "The first is the answer, the second calls for rewriting, and the third calls for one sided sign analysis."
  }
 ],
 "inferred": [
  {
   "claim": "No skill of BC-CON-01009 lists essential_knowledge, so ki-1 carries ek_id null and paraphrases the topic's Required mathematical knowledge paragraph.",
   "settles": "A library pass mapping BC-SKL-01029 to 01031 to a BC-EK (ced:44 prints no essential knowledge statement for topic 1.7)."
  },
  {
   "claim": "BC-QA-01014 has no common_givens, so st-1 rests on typical_wording and asked_to_produce.",
   "settles": "A common_givens entry on BC-QA-01014 from an official item."
  },
  {
   "claim": "The factor form of BC-QA-01014 has the shape (x - target)(x - top_root) over (x - target)(x - bottom_root), as BC-QA-01004 states; the BC-QA-01014 notes say only that it gives zero over zero.",
   "settles": "The BC-QA-01014 item template or a notes entry giving the factor form."
  },
  {
   "claim": "A fluent solver classifies in the head and writes the rewritten quotient and the value.",
   "settles": "Timed response logs on BC-QA-01014 items."
  }
 ],
 "sources": [
  "BC-CON-01009",
  "BC-SKL-01029",
  "BC-SKL-01030",
  "BC-SKL-01031",
  "BC-SKL-01021",
  "ced:44",
  "BC-QA-01014",
  "BC-ERR-01003",
  "BC-ERR-01006",
  "BC-ERR-01008",
  "BC-ERR-01009",
  "BC-MIS-01001",
  "BC-MIS-01005",
  "BC-MIS-01006",
  "BC-PRQ-01001",
  "BC-PRQ-01008",
  "research/units/unit-01-limits-continuity.md#1.7 Selecting Procedures for Determining Limits",
  "research/question-analysis/question-archetypes.md#BC-QA-01014 Procedure selected for a limit from the form of the expression",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "read_minutes": {
  "full": 4.0,
  "brief": 3.0
 },
 "word_count": {
  "full": 575,
  "brief": 432
 }
}
```
