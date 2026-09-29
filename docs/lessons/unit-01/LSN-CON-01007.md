---
title: LSN-CON-01007 Limit theorems for combinations of functions
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01007, limits of sums, products, quotients and composites from the limits of their pieces, with the denominator and continuity conditions, built from authoring_bundle("BC-CON-01007") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01007 Limit theorems for combinations of functions

Concept BC-CON-01007 (skills BC-SKL-01018, BC-SKL-01019, BC-SKL-01020, BC-SKL-01021, BC-SKL-01022), topic 1.5 of Unit 1, loaded by BC-QA-01003 (limit-by-theorems) and BC-QA-01014 (procedure-selection). Its hard parent is BC-CON-01006 and BC-CON-01009 hangs from it (docs/lessons/unit-01/README.md, section 1).

## Prediction

Served first, both bands. Pose on ex-1's own numbers: the limits 2 and 3 at \(x=1\) beside the differing table values, with \(h(x)=x^2+2\), and ask what \(h(f(x))/g(x)\) approaches. Form `short_answer`, key 2, which is ex-1's answer. The resolution says that the theorems combine the supplied limits and not the table values, from BC-CON-01007 and the topic 1.5 paragraph. It carries no verdict word.

## Orientation

Served text, from BC-CON-01007 `description_plain` and the topic 1.5 Assessment behaviour paragraph, which supplies the limits of two functions and asks for the limit of a combination, and tests the denominator condition (research/units/unit-01-limits-continuity.md#1.5 Determining Limits Using Algebraic Properties of Limits). No count, no frequency.

## Key ideas

All five skills map one BC-EK, BC-EK-LIM-1D2 (ced:42), so one core block, both bands.

- ki-1 (core, BC-EK-LIM-1D2). Limits pass through sums, differences, products, quotients and composites; the quotient theorem needs a nonzero denominator limit, the composite theorem an outer function continuous at the inner limit; for a function continuous at the input the limit is the value, which is what makes substitution legitimate. Paraphrased from the topic 1.5 Limit theorems and Direct substitution paragraphs. No quote. Notation from the concept record: limit theorems.

## Recognition

- BC-QA-01003 (research/question-analysis/question-archetypes.md#BC-QA-01003 Limit evaluated by limit theorems from given limits or tabulated values): `typical_wording` "Given the stated limits of f and g at the named input, find the limit of the indicated combination"; `common_givens` the limits of two functions at a point, a graph of line segments and an arc, a quotient built from a function, its derivative and an elementary function; `asked_to_produce` the limit of the combination as a single value. The signal is limits handed over in the stem next to a table of values that differ from them. FRQ example BC-FRQ-2019-Q3-D (one point, sg-19:4).
- BC-QA-01014 (research/question-analysis/question-archetypes.md#BC-QA-01014 Procedure selected for a limit from the form of the expression): `typical_wording` "For each of the given limits, identify an appropriate method and use it to determine the limit". `common_givens` is empty, so the cue rests on the wording. The signal is an expression to substitute into, whose form after substitution picks the method.

What says "not this concept": zero over zero after substitution sends the limit to rewriting (BC-CON-01008); a nonzero number over zero points to an infinite limit (BC-CON-01016); both from the unit README's neighbour table.

The contrast pair on st-1 takes its near miss from that neighbour: `this` is supplied limits of f and g on BC-QA-01003, `not_this` is a formula that gives zero over zero on substitution (BC-CON-01008), and the feature is limits given against a formula alone.

## Method choice

Two strategy blocks, low band both, mid band st-1.

- st-1, BC-QA-01003, verified. Method, `expected_solution_path[0]`: record the supplied limits. Rival, `wrong_approaches`: a denominator limit of zero divided by (BC-ERR-01006), the composite in the wrong order (BC-ERR-01007). Separating feature: the theorems use limits only, and a quotient needs a nonzero denominator limit.
- st-2, BC-QA-01014, `evidence_tag` inferred (no `common_givens`). Method: substitute the target input into each expression. Rival: the quotient of limits taken with a zero denominator (BC-ERR-01006). Separating feature: a real value after substitution settles the limit; zero over zero sends it to rewriting.

## Solution path

- ex-1, BC-QA-01003, both bands, no calculator. Draw: point 1, shift 2, limit_f 2, limit_g 3, table_f [0, 4, 1, -2, 3, 1], table_g [1, -1, 2, 3, -2, 4], justify bare. Every constraint holds: \(h(1)=3\) lies in 0 to 5 and differs from 1; the tabulated \(f(1)=4\) and \(g(1)=-1\) differ from the limits; the four derived values key 2, both_values \(-18\), denominator_value \(-6\), wrong_order \(-2/3\) are distinct. Steps: record the limits (no value), check the denominator (no value), apply the composite theorem, \(h(2)=6\) (valued, new), divide by the limit of g and report (valued, new, tagged BC-PT-99004).
- ex-2, BC-QA-01014, low band only, no calculator. Draw: target 2, top_root -1, bottom_root 3, root_value 1, lead_top 1, lead_bottom 1, form factor, pole_power 1, giving \((x^2-x-2)/(x^2-5x+6)\); the construction of the factor form from these parameters is [inferred]. Steps: substitute and see zero over zero (no value), the expression (valued, new), the cancelled form (valued, equivalent), the limit (valued, limit at 2). Answer \(-3\). Faded from step 3: steps 1 and 2 are shown (the zero over zero reading and the expression), the student writes the cancelled form and the limit, and then steps 3 and 4 appear. The fade falls there because the substitution and the choice to rewrite are the method decision, and the last two steps are the algebra the student can produce from it.

A fluent solver on ex-1 writes the substituted combination and the value, holding the record of supplied limits in the head (docs/lessons/unit-01/README.md, section 5).

## Scoring

BC-QA-01003 lists BC-PT-99004; ex-1 tags it on the value step, so one line, generated by `reader_checks(["BC-PT-99004"])` and copied into the machine record: "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4)..." The research entry for BC-QA-01003 records "none recorded" for point types; the snapshot record is the source. BC-QA-01014 lists none, so ex-2 carries no tag and no line.

Point losses research/scoring names for this shape: an unrequired simplification that introduces an error loses the answer point (research/scoring/common-point-losses.md#Answer points, BC-ERR-99022).

## Traps

Three active errors, in the bundle's order; the mid band shows the first two.

- err-BC-ERR-01001 (BC-MIS-01001, BC-MIS-01003). On ex-1's draw: the tabulated \(f(1)=4\) and \(g(1)=-1\) used, giving \(-18\). Right: the limits give 2. Distinct.
- err-BC-ERR-01006 (BC-MIS-01005, BC-MIS-01006). On ex-1's draw, so the mid band shows it beside the example it serves: the limit of \(f(x)/(g(x)-3)\) at 1 taken as 2 over \(3-3\) (an undefined quotient). Right: the denominator limit is 0, so the quotient theorem does not apply. Distinct. Possible reason from BC-MIS-01005.
- err-BC-ERR-01007 (BC-MIS-01005, BC-MIS-01001). On ex-1's draw: \(f(h(1))=f(3)=-2\) over 3. Right: \(h(2)/3=2\). Distinct.

## Representations

None. The topic 1.5 Representations paragraph names supplied limits to the limit of a combination and a piecewise rule to matched one sided limits; the first is the ki-1 table, the second belongs to BC-CON-01004.

## Prerequisite bridge

Two bridges, BC-PRQ-01008 (supporting parent of BC-SKL-01021) and BC-PRQ-06005, gated by state.

## Time

BC-QA-01003 is `no_calculator` and a single MCQ: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). The minutes go to reading which numbers are limits and which are table values; the arithmetic is one line.

## Checks

- chk-1, completion of ex-1, both bands. Key 2.
- chk-2, isomorph on BC-QA-01003, both bands: point 1, shift 1, limits \(-2\) and \(-1\). Key \(-5\).
- chk-3, MCQ on BC-QA-01003, low band: point 2, shift \(-3\), limits 3 and 2, table \(f(1)=2\), \(f(2)=-1\), \(g(2)=4\). Key 3. Distractors from the spec's derived values: \(-1/2\) (BC-ERR-01001, both table values), \(3/2\) (BC-ERR-01001, the table value of g), 1 (BC-ERR-01007, \(f(h(2))\) over 2).

## Delivery

- orientation: table. Rule 4, BC-REP-03 on BC-SKL-01018 to 01020; the unit README picks table. The supplied limits beside the tabulated values of ex-1.
- ki-1: table. Rule 4, the theorems as a table of combination against limit, with the two conditions in the last rows.
- ex-1, ex-2, err blocks: step_reveal, rule 1.

Every non-text choice is [inferred], settled by the modality A/B.

## Band plan

- Low (full): pr-1, orientation, bridges when gated, ki-1, st-1 with its contrast, st-2, ex-1 with its scoring line, chk-1, three error blocks, ex-2 faded from step 3, chk-2, chk-3.
- Mid (brief): pr-1, orientation, bridges when gated, ki-1, st-1 with its contrast, ex-1 with its scoring line, chk-1, err-BC-ERR-01001, err-BC-ERR-01006, chk-2.
- Totals: full 647 words, 4.4 minutes (cap 900 and 6); brief 449 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-01007; BC-SKL-01018, BC-SKL-01019, BC-SKL-01020, BC-SKL-01021, BC-SKL-01022; BC-EK-LIM-1D2; ced:42
- BC-QA-01003, BC-QA-01014; BC-FRQ-2019-Q3-D; sg-19:4
- BC-PT-99004; sg-25:3, sg-26:4, sg-25:2, sg-26:2; BC-ERR-99022
- BC-ERR-01001, BC-ERR-01006, BC-ERR-01007; BC-MIS-01001, BC-MIS-01003, BC-MIS-01005, BC-MIS-01006
- BC-PRQ-01008, BC-PRQ-06005
- research/units/unit-01-limits-continuity.md#1.5 Determining Limits Using Algebraic Properties of Limits
- research/question-analysis/question-archetypes.md#BC-QA-01003 Limit evaluated by limit theorems from given limits or tabulated values
- research/question-analysis/question-archetypes.md#BC-QA-01014 Procedure selected for a limit from the form of the expression
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] st-2 rests on typical_wording. Settled by common_givens on BC-QA-01014.
- [inferred] ex-2's factor form built as (x - target)(x - top_root) over (x - target)(x - bottom_root). Settled by the BC-QA-01014 generation template.
- [inferred] Table as the delivery mode. Settled by the modality A/B.
- Library gap: research/question-analysis/question-archetypes.md records no point types for BC-QA-01003 while the snapshot lists BC-PT-99004; BC-QA-01014 `common_givens` is empty.

## Machine record

```json
{
 "id": "LSN-CON-01007",
 "kind": "concept",
 "target_id": "BC-CON-01007",
 "unit": "01",
 "skills": [
  "BC-SKL-01018",
  "BC-SKL-01019",
  "BC-SKL-01020",
  "BC-SKL-01021",
  "BC-SKL-01022"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "At x = 1, f tends to 2 and g to 3, though f(1) = 4, g(1) = -1. With h(x) = x^2 + 2, what does h(f(x))/g(x) approach?",
   "command_verb": "predict"
  },
  "format": "short_answer",
  "key": {
   "form": "numeric",
   "expr": "2"
  },
  "resolution": "The limits combine, not the table values: h(2) over 3 is 2.",
  "sources": [
   "BC-CON-01007",
   "research/units/unit-01-limits-continuity.md#1.5 Determining Limits Using Algebraic Properties of Limits"
  ]
 },
 "orientation": {
  "text": "A response combines the pieces' limits and checks conditions.",
  "sources": [
   "BC-CON-01007",
   "research/units/unit-01-limits-continuity.md#1.5 Determining Limits Using Algebraic Properties of Limits"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-1D2",
   "depth": "core",
   "text": "Limits pass through combinations; a quotient needs a nonzero denominator limit.",
   "notation": "",
   "quote": null,
   "sources": [
    "BC-EK-LIM-1D2",
    "ced:42",
    "research/units/unit-01-limits-continuity.md#1.5 Determining Limits Using Algebraic Properties of Limits"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01003",
   "cue": "Limits given at one input.",
   "method": "Record the supplied limits.",
   "rival": "A zero denominator limit divided by.",
   "separating_feature": "Theorems take limits only.",
   "sources": [
    "BC-QA-01003",
    "BC-ERR-01006",
    "BC-ERR-01007"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Limits at x = 2: f 5, g 4. Find the limit of f(x)g(x).",
     "archetype_id": "BC-QA-01003"
    },
    "not_this": {
     "text": "Evaluate the limit of (x^2 - 4)/(x - 2) at x = 2.",
     "why_not": "Zero over zero calls for rewriting."
    },
    "feature": "Limits given, not a formula."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-01014",
   "cue": "Several limits, each to be matched to a method and evaluated.",
   "method": "Substitute the target input into each expression.",
   "rival": "The quotient of limits taken with a zero denominator.",
   "separating_feature": "A real value settles the limit; zero over zero sends it to rewriting.",
   "sources": [
    "BC-QA-01014",
    "BC-ERR-01006"
   ],
   "evidence_tag": "inferred"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01003",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "point": 1,
    "shift": 2,
    "limit_f": 2,
    "limit_g": 3,
    "table_f": [
     0,
     4,
     1,
     -2,
     3,
     1
    ],
    "table_g": [
     1,
     -1,
     2,
     3,
     -2,
     4
    ],
    "justify": "bare"
   },
   "problem": {
    "text": "Limits at x = 1: f 2, g 3. Table: f(1) = 4, g(1) = -1, f(3) = -2. With h(x) = x^2 + 2, find the limit of h(f(x))/g(x) at x = 1.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The stem supplies limits at 1: 2 for f, 3 for g.",
     "why": "Limits, not table values, feed the theorems."
    },
    {
     "cue": "A quotient: check the denominator limit.",
     "why": "3 is not 0: the quotient theorem applies."
    },
    {
     "cue": "h is continuous, so the composite gives h(2).",
     "why": "The outer function takes the inner limit.",
     "expr": "2**2 + 2",
     "relation": "new"
    },
    {
     "cue": "The stem asks for a value.",
     "why": "6 over 3.",
     "expr": "2",
     "relation": "new",
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "2"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-01014",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "target": 2,
    "top_root": -1,
    "bottom_root": 3,
    "root_value": 1,
    "lead_top": 1,
    "lead_bottom": 1,
    "form": "factor",
    "pole_power": 1
   },
   "problem": {
    "text": "Find the limit of (x^2 - x - 2)/(x^2 - 5x + 6) as x approaches 2.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Substitute 2: numerator 0, denominator 0.",
     "why": "The denominator limit is 0, so the quotient theorem does not apply."
    },
    {
     "cue": "Zero over zero calls for rewriting.",
     "why": "Both factor with x - 2.",
     "expr": "(x**2 - x - 2)/(x**2 - 5*x + 6)",
     "relation": "new"
    },
    {
     "cue": "Cancel x - 2, valid for x not 2.",
     "why": "The limit ignores x = 2 itself.",
     "expr": "(x + 1)/(x - 3)",
     "relation": "equivalent"
    },
    {
     "cue": "Now substitution gives a real value.",
     "why": "3 over -1.",
     "expr": "-3",
     "relation": "limit",
     "variable": "x",
     "point": "2"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "-3"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99004"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99004",
     "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-01001",
   "observed_behavior": "The response gives the plotted or defined value of the function at the input in place of the value the function approaches there.",
   "scoring_consequence": "The reading point is lost, and in a continuity part the comparison of limit with value collapses.",
   "wrong_step": {
    "text": "Table values 4, -1 used: -18.",
    "expr": "(4**2 + 2)/(-1)"
   },
   "right_step": {
    "text": "Limits 2 and 3: 2.",
    "expr": "(2**2 + 2)/3"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-01001"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01006",
   "observed_behavior": "The response divides the limit of the numerator by the limit of the denominator although the denominator limit is zero.",
   "scoring_consequence": "The value point is lost and any justification naming the theorem is incorrect.",
   "wrong_step": {
    "text": "f/(g - 3) at 1 as 2/0.",
    "expr": "2/(3 - 3)"
   },
   "right_step": {
    "text": "Denominator limit 0: theorem fails.",
    "expr": "3 - 3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01005",
    "text": "without the denominator condition"
   },
   "sources": [
    "BC-ERR-01006",
    "BC-MIS-01005"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01007",
   "observed_behavior": "The response applies the inner function to the limit of the outer function rather than the outer function to the limit of the inner.",
   "scoring_consequence": "The value point is lost.",
   "wrong_step": {
    "text": "f(h(1)) = f(3) = -2, over 3.",
    "expr": "-2/3"
   },
   "right_step": {
    "text": "h at the limit of f, over 3: 2.",
    "expr": "(2**2 + 2)/3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01005",
    "text": "applies the quotient and composite theorems as formal rules"
   },
   "sources": [
    "BC-ERR-01007",
    "BC-MIS-01005"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-01008",
   "text": "Substitution needs the input inside the domain."
  },
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Reading f(g(x)) at an input."
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
   ],
   "ex-2": [
    2,
    3,
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    2
   ],
   "ex-2": [
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
   "archetype_id": "BC-QA-01003",
   "parameter_draw": {
    "point": 1,
    "shift": 2,
    "limit_f": 2,
    "limit_g": 3,
    "table_f": [
     0,
     4,
     1,
     -2,
     3,
     1
    ],
    "table_g": [
     1,
     -1,
     2,
     3,
     -2,
     4
    ],
    "justify": "bare"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The theorems give the limit as (2^2 + 2)/3. Find its value.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "2"
   },
   "steps": [
    {
     "text": "(2^2 + 2)/3.",
     "expr": "(2**2 + 2)/3",
     "relation": "new"
    },
    {
     "text": "That is 2.",
     "expr": "2",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01020",
    "BC-SKL-01022"
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
   "archetype_id": "BC-QA-01003",
   "parameter_draw": {
    "point": 1,
    "shift": 1,
    "limit_f": -2,
    "limit_g": -1,
    "table_f": [
     3,
     0,
     1,
     2,
     -4,
     4
    ],
    "table_g": [
     1,
     2,
     -3,
     1,
     4,
     -2
    ],
    "justify": "bare"
   },
   "stem": {
    "text": "Limits at 1: f -2, g -1. Table: f(1) = 0, g(1) = 2. With h(x) = x^2 + 1, find the limit of h(f(x))/g(x) at 1.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-5"
   },
   "steps": [
    {
     "text": "h(-2) over -1.",
     "expr": "((-2)**2 + 1)/(-1)",
     "relation": "new"
    },
    {
     "text": "That is -5.",
     "expr": "-5",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01020",
    "BC-SKL-01022"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-01003",
   "parameter_draw": {
    "point": 2,
    "shift": -3,
    "limit_f": 3,
    "limit_g": 2,
    "table_f": [
     1,
     2,
     -1,
     4,
     0,
     -3
    ],
    "table_g": [
     2,
     1,
     4,
     -3,
     1,
     2
    ],
    "justify": "bare"
   },
   "stem": {
    "text": "Limits at 2: f 3, g 2. Table: f(1) = 2, f(2) = -1, g(2) = 4. With h(x) = x^2 - 3, find the limit of h(f(x))/g(x) at x = 2.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "3"
   },
   "steps": [
    {
     "text": "h(3) over 2.",
     "expr": "(3**2 - 3)/2",
     "relation": "new"
    },
    {
     "text": "That is 3.",
     "expr": "3",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "-1/2",
     "error_path": "BC-ERR-01001",
     "derivation": "table values f(2) = -1 and g(2) = 4 used: (1 - 3)/4"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "3/2",
     "error_path": "BC-ERR-01001",
     "derivation": "table value g(2) = 4 used for the denominator: 6/4"
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "1",
     "error_path": "BC-ERR-01007",
     "derivation": "composition reversed: f(h(2)) = f(1) = 2, over 2"
    },
    {
     "id": "D",
     "is_key": true,
     "expr": "3",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01020",
    "BC-SKL-01022"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "table",
   "reason": "rule 4: BC-REP-03 on BC-SKL-01018, 01019, 01020; unit README delivery map",
   "sources": [
    "BC-SKL-01018",
    "BC-SKL-01019",
    "BC-SKL-01020"
   ],
   "spec": {
    "kind": "table",
    "columns": [
     "function",
     "limit at x = 1",
     "table value at x = 1"
    ],
    "rows": [
     [
      "f",
      "2",
      "4"
     ],
     [
      "g",
      "3",
      "-1"
     ]
    ],
    "labels": [
     {
      "text": "theorems use this column: limits",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the two rows as static text",
   "keyboard": "no control; cells reached in reading order with Tab"
  },
  {
   "block": "ki-1",
   "mode": "table",
   "reason": "rule 4: BC-REP-03 on BC-SKL-01018 to 01020, the table of supplied limits; the conditions sit as its last rows",
   "sources": [
    "BC-SKL-01018",
    "BC-SKL-01020",
    "BC-SKL-01022"
   ],
   "spec": {
    "kind": "table",
    "columns": [
     "combination",
     "limit",
     "condition"
    ],
    "rows": [
     [
      "f + g",
      "L + M",
      "none"
     ],
     [
      "f g",
      "L M",
      "none"
     ],
     [
      "f / g",
      "L / M",
      "M not 0"
     ],
     [
      "h(f)",
      "h(L)",
      "h continuous at L"
     ]
    ],
    "labels": [
     {
      "text": "L, M: limits of f and g",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the four rows as static text",
   "keyboard": "no control; cells reached in reading order with Tab"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1; the supplied limits and table values render as a table in the problem",
   "sources": [
    "BC-SKL-01020"
   ]
  },
  {
   "block": "ex-2",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01001",
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
   "block": "err-BC-ERR-01007",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-01001",
  "err-BC-ERR-01006",
  "err-BC-ERR-01007",
  "ex-1"
 ],
 "read_minutes": {
  "full": 4.4,
  "brief": 3.0
 },
 "word_count": {
  "full": 646,
  "brief": 448
 },
 "research_lines": [
  {
   "file": "research/units/unit-01-limits-continuity.md",
   "line": "The quotient theorem requires that the limit of the denominator is not zero"
  }
 ],
 "inferred": [
  {
   "claim": "st-2 rests on typical_wording because BC-QA-01014 has no common_givens.",
   "settles": "A library pass filling common_givens on BC-QA-01014."
  },
  {
   "claim": "ex-2's factor form is built as (x - target)(x - top_root) over (x - target)(x - bottom_root).",
   "settles": "The BC-QA-01014 generation template under app/generation/templates."
  },
  {
   "claim": "Table serves the orientation and key idea better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-01007",
  "BC-SKL-01018",
  "BC-SKL-01019",
  "BC-SKL-01020",
  "BC-SKL-01021",
  "BC-SKL-01022",
  "BC-EK-LIM-1D2",
  "ced:42",
  "BC-QA-01003",
  "BC-QA-01014",
  "BC-FRQ-2019-Q3-D",
  "sg-19:4",
  "BC-PT-99004",
  "sg-25:3",
  "sg-26:4",
  "BC-ERR-01001",
  "BC-ERR-01006",
  "BC-ERR-01007",
  "BC-MIS-01005",
  "BC-ERR-99022",
  "BC-PRQ-01008",
  "BC-PRQ-06005",
  "research/units/unit-01-limits-continuity.md#1.5 Determining Limits Using Algebraic Properties of Limits",
  "research/scoring/common-point-losses.md#Answer points",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
