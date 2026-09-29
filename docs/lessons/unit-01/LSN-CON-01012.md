---
title: LSN-CON-01012 Classification of discontinuities
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01012, classifying discontinuities as removable, jump or vertical asymptote, built from authoring_bundle("BC-CON-01012") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01012 Classification of discontinuities

Concept BC-CON-01012 (skills BC-SKL-01039 to BC-SKL-01042), topic 1.10 of Unit 1, loaded by BC-QA-01007 (primary), BC-QA-01006 and BC-QA-01009. The unit attack map places it twelfth, after BC-CON-01006 and BC-CON-01008, with figure delivery.

## Prediction

Served first, both bands, on ex-1's rule. Form: `mcq`, three options, key B. The question asks for the concept's core claim, that the one sided limits settle the type, before it is stated. Distractor A is the asymptote reading of a zero denominator, distractor C the jump. The resolution states what the reduced rule gives and the deciding rule in the record's words. Sources: BC-CON-01012 and the topic section the key idea cites. Delivery: text.

## Orientation

Served text, from BC-CON-01012 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-01-limits-continuity.md#1.10 Exploring Types of Discontinuities): MCQ forms ask for the classification of each break; justification variants demand the limits that support it. No count, no frequency. Delivered as a figure.

## Key ideas

All four skills map to BC-EK-LIM-2A1 (ced:47): one core block, both bands.

- ki-1 (core). Paraphrase of the topic's Required mathematical knowledge paragraph (Types; Deciding rule) and of BC-SKL-01042 (check each branch boundary and each excluded point). No anchor quote, to keep the brief form under its cap. Notation line from the concept record and the topic.

## Recognition

- BC-QA-01007 (primary; discontinuity-classification, single MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-01007 Discontinuity classified from a rule or a graph). `typical_wording`: "Classify each discontinuity of the given function and give a reason for each classification." `common_givens` and `asked_to_produce` are empty in research/question-analysis; the snapshot record's `asked_to_produce` holds the classification and a reason. The signal: a rational rule with a factor in the denominator, or a graph with breaks, and the words "classify" or "type".
- BC-QA-01006 (continuity-at-a-point, FRQ part or MCQ; research/question-analysis/question-archetypes.md#BC-QA-01006 Continuity at a point tested against the three conditions). "Determine whether the given function is continuous at the named input." The signal is a verdict, not a type; BC-CON-01013 owns it, this lesson uses its piecewise shape for the jump.
- BC-QA-01009 (infinite-limit-asymptote, MCQ; research/question-analysis/question-archetypes.md#BC-QA-01009 Vertical asymptote located and the one sided infinite limits stated). "Find the vertical asymptotes ... describe the behaviour." The signal is asymptote location and sided infinite limits; BC-CON-01016 owns it.

What says "not this concept": a question about removing the break with a parameter (BC-QA-01008, BC-CON-01015); a limit at infinity (BC-CON-01017).

The near miss for st-1 comes from BC-QA-01008 (BC-CON-01015), listed above as "not this concept": the same rational rule with a hole, but the stem asks for a constant that repairs it instead of a type. The unit-01 README row for removable against vertical asymptote separates the two by whether the factor cancels.

## Method choice

Three strategy blocks, low band all, mid band st-1. None of the three archetypes has `common_givens`, so each carries `evidence_tag: inferred`.

- st-1, BC-QA-01007. Method, `expected_solution_path[0]`: locate the inputs where the function is undefined or the rule changes. Rival (`wrong_approaches`): an asymptote at a cancelling factor (BC-ERR-01018). Separating feature: whether the factor cancels (the unit-01 README row, Removable against vertical asymptote).
- st-2, BC-QA-01006. Method: evaluate the function at the named input. Rival: continuity from matching one sided limits (BC-ERR-01015). Separating feature: a verdict needs the value; a type does not.
- st-3, BC-QA-01009. Method: factor numerator and denominator. Rival: one two sided infinite limit where the signs differ (BC-ERR-01019). Separating feature: the sign on each side.

## Solution path

- ex-1, BC-QA-01007, both bands: coefficient 2, cancelled_root 1, pole \(-1\), zero 3, form factored, target removable; \(f(x)=\frac{2(x-1)(x-3)}{(x-1)(x+1)^2}\) (the `parameter_spec` notes). Steps follow `expected_solution_path`: locate (the rule, `new`), reduce (`equivalent`), one sided limits at 1 (`limit`, value \(-1\)), classify removable; at \(-1\) the squared factor gives \(-\infty\) on both sides, stated in words since the checker cannot confirm an infinite value. Answer form statement.
- ex-2, BC-QA-01006, low band: boundary 2, jump, closed side left, left_limit 3, right_limit \(-1\), slopes 1 and 2, point_value 3 (the closed left side gives \(f(2)=3\)); \(x+1\) for \(x\le2\), \(2x-5\) for \(x>2\) [inferred shape]. Left limit 3 (`limit`, dir \(-\)), right limit \(-1\) (`limit`, dir +), jump. Fade: `fade_from` 4. Steps 1 to 3 (the left rule, the left limit 3, the right rule) are shown; the student writes the right limit and the type, and steps 4 and 5 then reveal. The fade falls there because the left limit has just modelled the move the right limit repeats, and the type follows from comparing the two.

No published draw matches either. A fluent solver writes the reduced form and the limits [inferred].

## Scoring

None. BC-QA-01007, 01006 and 01009 list no `point_types`; no `what_a_reader_scores` entry, no point tag. For the author: how long a reason is depends on the command verb (research/scoring/justification-requirements.md#Justify, give a reason, and give reasons), and neither archetype has an FRQ example that settles which verb it carries (unit-01 README).

## Traps

The bundle lists five errors; the first four in its order are served (linked BC-MIS all severity high). Mid band the first two.

- err-BC-ERR-01003 (ex-1). Wrong: no limit at 1. Right: \(-1\). Distinct. Reason, words from BC-MIS-01001.
- err-BC-ERR-01015 (ex-1). Wrong: \(-1\) taken as continuity. Right: \(f(1)\) undefined (`nan`). Distinct. Reason, words from BC-MIS-01009.
- err-BC-ERR-01017 (ex-2). Wrong: right limit from \(x+1\), 3. Right: from \(2x-5\), \(-1\). Distinct. No possible reason (see Sources).
- err-BC-ERR-01018 (ex-1). Wrong: \(x=1\). Right: \(x=-1\). Distinct. Reason, words from BC-MIS-01011.

BC-ERR-01020 falls beyond the cap.

All four blocks are distinct, so all four carry `fix_prompt` true.

## Representations

None as a separate block. The topic's Representations paragraph names rule to classification and graph to classification; the orientation figure and the ki-1 panels carry the graph side.

## Prerequisite bridge

Five BC-PRQ parents, supporting edges, gated by state: BC-PRQ-01001, 01003, 01006, 01008, 01009. Each bridge is cut to one short line from `description_plain`, with the `failure_signature` kept where it fits, to stay under the brief cap.

## Time

BC-QA-01007 is `no_calculator`, a single MCQ: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). A fluent solver writes the reduced form and the limit at the cancelled input and reads the location and classification without writing them [inferred].

## Checks

- chk-1, completion of ex-1, both bands: the limit and the missing value are given; the student classifies. Key statement, removable at \(x=1\).
- chk-2, isomorph, both bands: coefficient \(-1\), cancelled_root 2, pole 0, zero \(-3\). Key statement, removable at \(x=2\), limit \(-\frac{5}{4}\).
- chk-3, MCQ, low band: coefficient 3, cancelled_root \(-2\), pole 1, zero 0, target asymptote. Key: removable at \(-2\), asymptote at 1. Distractors carry BC-ERR-01018, BC-ERR-01003, BC-ERR-01015.

## Delivery

- orientation: figure. Rule 3 (README: figure). The ex-1 graph: hole at \((1,-1)\), asymptote \(x=-1\), labels inside.
- ki-1: figure, three panels side by side (removable, jump, asymptote). Rule 3; not promoted to interactive, since BC-QA-01007 `difficulty_variables` name no varying quantity (README).
- ex-1, ex-2 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full), in the served order of 2026-09-29: prediction, orientation, bridges when gated in, ki-1, st-1, st-2, st-3 (contrast pair on st-1), ex-1 and its scoring lines (none), chk-1, err-BC-ERR-01003, err-BC-ERR-01015, err-BC-ERR-01017, err-BC-ERR-01018 (each a fix prompt), ex-2 faded from step 4, chk-2, representations (none), chk-3. 731 words, 4.88 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, bridges when gated in, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-01003, err-BC-ERR-01015, chk-2. 448 words, 2.99 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-01012; BC-SKL-01039, BC-SKL-01040, BC-SKL-01041, BC-SKL-01042; BC-EK-LIM-2A1; ced:47
- BC-QA-01007, BC-QA-01006, BC-QA-01009
- BC-ERR-01003, BC-ERR-01015, BC-ERR-01017, BC-ERR-01018, BC-ERR-01019; BC-MIS-01001, BC-MIS-01009, BC-MIS-01011
- BC-PRQ-01001, BC-PRQ-01003, BC-PRQ-01006, BC-PRQ-01008, BC-PRQ-01009
- research/units/unit-01-limits-continuity.md#1.10 Exploring Types of Discontinuities
- research/question-analysis/question-archetypes.md#BC-QA-01007 Discontinuity classified from a rule or a graph
- research/question-analysis/question-archetypes.md#BC-QA-01006 Continuity at a point tested against the three conditions
- research/question-analysis/question-archetypes.md#BC-QA-01009 Vertical asymptote located and the one sided infinite limits stated
- research/exam/exam-structure.md#Section and part layout
- research/scoring/justification-requirements.md#Justify, give a reason, and give reasons
- [inferred] Non-text delivery modes. Settled by the modality A/B.
- [inferred] Strategy blocks on `typical_wording`. Settled by `common_givens` on the three archetypes.
- [inferred] The ex-2 piecewise shape. Settled by the BC-QA-01006 template.
- [inferred] Lines held in the head. Settled by timed response logs.
- [inferred] No possible reason for BC-ERR-01017. Settled by a branch-selection misconception record.
- Prediction and contrast stems: written for this lesson, no published item shares them (content/items_* searched). Citations sit in each block's `sources` array, never in served text.

## Machine record

```json
{
 "id": "LSN-CON-01012",
 "kind": "concept",
 "target_id": "BC-CON-01012",
 "unit": "01",
 "skills": [
  "BC-SKL-01039",
  "BC-SKL-01040",
  "BC-SKL-01041",
  "BC-SKL-01042"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Before the rule: what do the outputs of \\(f(x)=\\frac{2(x-1)(x-3)}{(x-1)(x+1)^2}\\) do as \\(x\\) nears 1?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Grow without bound on both sides.",
    "is_key": false
   },
   {
    "id": "B",
    "label": "Approach \\(-1\\) from both sides.",
    "is_key": true
   },
   {
    "id": "C",
    "label": "Approach different values from each side.",
    "is_key": false
   }
  ],
  "resolution": "The factor \\(x-1\\) divides out, leaving \\(\\frac{2(x-3)}{(x+1)^2}\\), which tends to \\(-1\\) from both sides: equal finite one sided limits, so a removable break.",
  "sources": [
   "BC-CON-01012",
   "research/units/unit-01-limits-continuity.md#1.10 Exploring Types of Discontinuities"
  ]
 },
 "orientation": {
  "text": "A response names each break removable, jump, or vertical asymptote, and backs the name with the one sided limits there.",
  "sources": [
   "BC-CON-01012",
   "research/units/unit-01-limits-continuity.md#1.10 Exploring Types of Discontinuities"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-2A1",
   "depth": "core",
   "text": "Three types, settled by the one sided limits. Both exist and agree: removable. Both exist and differ: jump. At least one is infinite: vertical asymptote. The function value decides only whether a break is present.",
   "notation": "removable, jump, vertical asymptote",
   "quote": null,
   "sources": [
    "BC-EK-LIM-2A1",
    "ced:47",
    "research/units/unit-01-limits-continuity.md#1.10 Exploring Types of Discontinuities"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01007",
   "cue": "Classify each discontinuity of a rule or graph, with a reason.",
   "method": "Locate the inputs where the function is undefined or the rule changes.",
   "rival": "Naming an asymptote at a factor that divides out.",
   "separating_feature": "Whether the denominator factor cancels.",
   "sources": [
    "BC-QA-01007"
   ],
   "evidence_tag": "inferred",
   "contrast": {
    "this": {
     "text": "Let \\(g(x)=\\frac{(x-2)(x+4)}{(x-2)(x-5)}\\). Classify each discontinuity of \\(g\\).",
     "archetype_id": "BC-QA-01007"
    },
    "not_this": {
     "text": "Let \\(h(x)=\\frac{x^2-4}{x-2}\\) for \\(x\\ne2\\), \\(h(2)=a\\). Find \\(a\\) so \\(h\\) is continuous.",
     "why_not": "It asks for a repairing value, not a name."
    },
    "feature": "Name the break, or choose a repairing value."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-01006",
   "cue": "Determine whether a piecewise function is continuous at a named input, and justify.",
   "method": "Evaluate the function at the named input.",
   "rival": "Continuity from matching one sided limits alone.",
   "separating_feature": "A continuity verdict needs the value; a type needs only the one sided limits.",
   "sources": [
    "BC-QA-01006"
   ],
   "evidence_tag": "inferred"
  },
  {
   "id": "st-3",
   "archetype_id": "BC-QA-01009",
   "cue": "Find the vertical asymptotes and describe the behaviour near each.",
   "method": "Factor numerator and denominator.",
   "rival": "One two sided infinite limit where the sides differ in sign.",
   "separating_feature": "The sign of the reduced quotient on each side of each remaining zero.",
   "sources": [
    "BC-QA-01009"
   ],
   "evidence_tag": "inferred"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01007",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "coefficient": 2,
    "cancelled_root": 1,
    "pole": -1,
    "zero": 3,
    "form": "factored",
    "target": "removable"
   },
   "problem": {
    "text": "Let \\(f(x)=\\frac{2(x-1)(x-3)}{(x-1)(x+1)^2}\\). Classify each discontinuity of \\(f\\).",
    "command_verb": "classify"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The denominator vanishes at \\(x=1\\) and \\(x=-1\\).",
     "why": "Only these inputs can hold a break.",
     "expr": "2*(x-1)*(x-3)/((x-1)*(x+1)**2)",
     "relation": "new"
    },
    {
     "cue": "The factor \\(x-1\\) sits in top and bottom.",
     "why": "Dividing it out is valid for \\(x\\ne1\\).",
     "expr": "2*(x-3)/(x+1)**2",
     "relation": "equivalent"
    },
    {
     "cue": "The reduced form is defined at 1.",
     "why": "Both one sided limits at 1 equal \\(-1\\).",
     "expr": "-1",
     "relation": "limit",
     "variable": "x",
     "point": "1"
    },
    {
     "cue": "Finite, equal limits at 1, but \\(f(1)\\) is undefined.",
     "why": "Removable discontinuity at \\(x=1\\)."
    },
    {
     "cue": "At \\(x=-1\\) the factor \\((x+1)^2\\) remains.",
     "why": "\\(f\\to-\\infty\\) on both sides: vertical asymptote \\(x=-1\\)."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "x = 1"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-01006",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "boundary": 2,
    "left_limit": 3,
    "right_limit": -1,
    "point_value": 3,
    "left_slope": 1,
    "right_slope": 2,
    "closed_side": "left",
    "break_kind": "jump"
   },
   "problem": {
    "text": "Let \\(f(x)=x+1\\) for \\(x\\le2\\) and \\(f(x)=2x-5\\) for \\(x>2\\). Classify the break at \\(x=2\\).",
    "command_verb": "classify"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Left of 2 the rule is \\(x+1\\).",
     "why": "The left branch gives the left limit.",
     "expr": "x + 1",
     "relation": "new"
    },
    {
     "cue": "Take the left limit at 2.",
     "why": "It is 3.",
     "expr": "3",
     "relation": "limit",
     "variable": "x",
     "point": "2",
     "dir": "-"
    },
    {
     "cue": "Right of 2 the rule is \\(2x-5\\).",
     "why": "The right branch gives the right limit.",
     "expr": "2*x - 5",
     "relation": "new"
    },
    {
     "cue": "Take the right limit at 2.",
     "why": "It is \\(-1\\).",
     "expr": "-1",
     "relation": "limit",
     "variable": "x",
     "point": "2",
     "dir": "+"
    },
    {
     "cue": "Both limits are finite and differ.",
     "why": "Jump discontinuity at \\(x=2\\)."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "x = 2"
   },
   "fade_from": 4
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01003",
   "observed_behavior": "The response states that the limit does not exist on the grounds that the function has no value at the input.",
   "scoring_consequence": "Both the value point and any justification point are lost.",
   "wrong_step": {
    "text": "\\(f(1)\\) is undefined, so no limit at 1 is reported.",
    "expr": "nan"
   },
   "right_step": {
    "text": "The limit at 1 is \\(-1\\); only the value is missing.",
    "expr": "-1"
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
   "error_id": "BC-ERR-01015",
   "observed_behavior": "The response concludes continuity because the two one sided limits agree, without comparing them with the function value.",
   "scoring_consequence": "The justification point is lost, and a parameter solved this way can be wrong when the defined value differs.",
   "wrong_step": {
    "text": "Both limits at 1 equal \\(-1\\), so \\(f\\) is called continuous.",
    "expr": "-1"
   },
   "right_step": {
    "text": "\\(f(1)\\) is undefined: removable, not continuous.",
    "expr": "2*(1-1)*(1-3)/((1-1)*(1+1)**2)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01009",
    "text": "holds one of the three conditions as the whole definition"
   },
   "sources": [
    "BC-ERR-01015",
    "BC-MIS-01009"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01017",
   "observed_behavior": "The response substitutes the boundary input into the branch that does not apply on that side.",
   "scoring_consequence": "The one sided limit is wrong and every point depending on it is lost.",
   "wrong_step": {
    "text": "The right limit at 2 taken from \\(x+1\\): 3.",
    "expr": "2 + 1"
   },
   "right_step": {
    "text": "From \\(2x-5\\): \\(-1\\).",
    "expr": "2*2 - 5"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-01017"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01018",
   "observed_behavior": "The response names a vertical asymptote at an input where the factor divides out of the rational expression.",
   "scoring_consequence": "The location point is lost and the classification is wrong.",
   "wrong_step": {
    "text": "Vertical asymptote at \\(x=1\\).",
    "expr": "x = 1"
   },
   "right_step": {
    "text": "\\(x-1\\) divides out; the asymptote is \\(x=-1\\).",
    "expr": "x = -1"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01011",
    "text": "reads any zero of the original denominator as unbounded behaviour without simplifying first"
   },
   "sources": [
    "BC-ERR-01018",
    "BC-MIS-01011"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-01001",
   "text": "Factor and cancel a common factor."
  },
  {
   "prq_id": "BC-PRQ-01003",
   "text": "Pick the branch for each side."
  },
  {
   "prq_id": "BC-PRQ-01006",
   "text": "Rewrite an absolute value as two branches."
  },
  {
   "prq_id": "BC-PRQ-01008",
   "text": "State where an expression is defined."
  },
  {
   "prq_id": "BC-PRQ-01009",
   "text": "Find a quotient's sign on each side of a zero."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3
   ],
   "ex-2": [
    2,
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    4,
    5
   ],
   "ex-2": [
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
   "archetype_id": "BC-QA-01007",
   "parameter_draw": {
    "coefficient": 2,
    "cancelled_root": 1,
    "pole": -1,
    "zero": 3,
    "form": "factored",
    "target": "removable"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For the \\(f\\) above, \\(\\lim_{x\\to1}f(x)=-1\\) and \\(f(1)\\) is undefined. Classify the break at \\(x=1\\).",
    "command_verb": "classify"
   },
   "key": {
    "form": "statement",
    "expr": "x = 1"
   },
   "steps": [
    {
     "text": "The reduced form.",
     "expr": "2*(x-3)/(x+1)**2",
     "relation": "new"
    },
    {
     "text": "Its limit at 1 is \\(-1\\): removable.",
     "expr": "-1",
     "relation": "limit",
     "variable": "x",
     "point": "1"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01039"
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
   "archetype_id": "BC-QA-01007",
   "parameter_draw": {
    "coefficient": -1,
    "cancelled_root": 2,
    "pole": 0,
    "zero": -3,
    "form": "factored",
    "target": "removable"
   },
   "stem": {
    "text": "Let \\(f(x)=\\frac{-(x-2)(x+3)}{(x-2)x^2}\\). Classify the discontinuity at \\(x=2\\).",
    "command_verb": "classify"
   },
   "key": {
    "form": "statement",
    "expr": "x = 2"
   },
   "steps": [
    {
     "text": "Divide out \\(x-2\\).",
     "expr": "-(x+3)/x**2",
     "relation": "new"
    },
    {
     "text": "The limit at 2 is \\(-\\frac{5}{4}\\), finite on both sides: removable.",
     "expr": "-5/4",
     "relation": "limit",
     "variable": "x",
     "point": "2"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01039"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-01007",
   "parameter_draw": {
    "coefficient": 3,
    "cancelled_root": -2,
    "pole": 1,
    "zero": 0,
    "form": "factored",
    "target": "asymptote"
   },
   "stem": {
    "text": "Let \\(f(x)=\\frac{3x(x+2)}{(x+2)(x-1)^2}\\). Which classifies its discontinuities?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "x = 1"
   },
   "steps": [
    {
     "text": "Divide out \\(x+2\\).",
     "expr": "3*x/(x-1)**2",
     "relation": "new"
    },
    {
     "text": "Limit at \\(-2\\) is \\(-\\frac{2}{3}\\); \\((x-1)^2\\) remains.",
     "expr": "-2/3",
     "relation": "limit",
     "variable": "x",
     "point": "-2"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "Vertical asymptotes at \\(x=-2\\) and \\(x=1\\).",
     "error_path": "BC-ERR-01018",
     "derivation": "the cancelled factor read as an asymptote"
    },
    {
     "id": "B",
     "is_key": true,
     "label": "Removable at \\(x=-2\\); vertical asymptote at \\(x=1\\).",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "label": "No limit at \\(x=-2\\) because \\(f(-2)\\) is undefined; vertical asymptote at \\(x=1\\).",
     "error_path": "BC-ERR-01003",
     "derivation": "undefined value read as no limit"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "Continuous at \\(x=-2\\), since both one sided limits equal \\(-\\frac{2}{3}\\).",
     "error_path": "BC-ERR-01015",
     "derivation": "matching limits read as continuity"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01039",
    "BC-SKL-01041"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-01039, 01040 and 01041 (unit-01 README delivery map)",
   "sources": [
    "BC-SKL-01039"
   ],
   "spec": {
    "kind": "graph",
    "window": {
     "x": [
      -3,
      4
     ],
     "y": [
      -6,
      3
     ]
    },
    "curves": [
     {
      "expr": "2*(x-3)/(x+1)**2",
      "label": {
       "text": "f",
       "placement": "inside"
      }
     }
    ],
    "points": [
     {
      "x": 1,
      "y": -1,
      "style": "open",
      "label": {
       "text": "hole at (1, -1)",
       "placement": "inside"
      }
     }
    ],
    "asymptotes": [
     {
      "x": -1,
      "style": "dashed",
      "label": {
       "text": "x = -1",
       "placement": "inside"
      }
     }
    ],
    "labels": [
     {
      "text": "two breaks, two types",
      "placement": "inside"
     }
    ],
    "representations": [
     "graph"
    ]
   },
   "fallback": "Alt text: a hole at \\((1,-1)\\) and a dashed vertical asymptote at \\(x=-1\\), with the curve falling on both sides of it.",
   "keyboard": "none needed: a static figure"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-01039, 01040, 01041; not promoted, BC-QA-01007 difficulty_variables name no varying quantity",
   "sources": [
    "BC-SKL-01039",
    "BC-SKL-01040",
    "BC-SKL-01041"
   ],
   "spec": {
    "kind": "panels",
    "panels": [
     {
      "title": {
       "text": "removable: limits agree, finite",
       "placement": "inside"
      },
      "curves": [
       {
        "expr": "x + 1"
       }
      ],
      "points": [
       {
        "x": 1,
        "y": 2,
        "style": "open",
        "label": {
         "text": "hole",
         "placement": "inside"
        }
       }
      ]
     },
     {
      "title": {
       "text": "jump: limits finite, differ",
       "placement": "inside"
      },
      "curves": [
       {
        "expr": "x + 1",
        "domain": [
         -1,
         2
        ]
       },
       {
        "expr": "2*x - 5",
        "domain": [
         2,
         4
        ]
       }
      ],
      "points": [
       {
        "x": 2,
        "y": 3,
        "style": "closed",
        "label": {
         "text": "f(2)",
         "placement": "inside"
        }
       }
      ]
     },
     {
      "title": {
       "text": "asymptote: a limit is infinite",
       "placement": "inside"
      },
      "curves": [
       {
        "expr": "1/(x-1)"
       }
      ],
      "asymptotes": [
       {
        "x": 1,
        "label": {
         "text": "x = 1",
         "placement": "inside"
        }
       }
      ]
     }
    ],
    "labels": [
     {
      "text": "type read from the one sided limits",
      "placement": "inside"
     }
    ],
    "representations": [
     "graph"
    ]
   },
   "fallback": "The three panels as a static row with the deciding rule written under each.",
   "keyboard": "none needed: a static figure"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "ex-2",
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
   "block": "err-BC-ERR-01015",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01017",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01018",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-01003",
  "err-BC-ERR-01015",
  "err-BC-ERR-01017",
  "err-BC-ERR-01018",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-01-limits-continuity.md",
   "line": "The function value at the input plays no part in the classification, only in whether a discontinuity is present."
  }
 ],
 "inferred": [
  {
   "claim": "The non-text delivery modes chosen here serve the content better than text and step reveal.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "BC-QA-01007, BC-QA-01006 and BC-QA-01009 have no common_givens, so st-1, st-2 and st-3 rest on typical_wording and carry evidence_tag inferred.",
   "settles": "common_givens entries on those archetypes from official items."
  },
  {
   "claim": "The piecewise rule of ex-2 follows the BC-QA-01006 notes: linear branches through the boundary at left_limit and right_limit, the boundary on the closed side's branch, so point_value is the closed side's limit, f(2) = 3.",
   "settles": "The BC-QA-01006 item template."
  },
  {
   "claim": "A fluent solver writes the reduced form and the limit, and reads the location and the classification without writing them, on the MCQ shape.",
   "settles": "Timed response logs on BC-QA-01007 items."
  },
  {
   "claim": "BC-ERR-01017 carries no possible_reason: neither linked misconception (BC-MIS-01009, BC-MIS-01019) describes a branch choice.",
   "settles": "A misconception record for branch selection at a boundary."
  }
 ],
 "sources": [
  "BC-CON-01012",
  "BC-SKL-01039",
  "BC-SKL-01040",
  "BC-SKL-01041",
  "BC-SKL-01042",
  "BC-EK-LIM-2A1",
  "ced:47",
  "BC-QA-01007",
  "BC-QA-01006",
  "BC-QA-01009",
  "BC-ERR-01003",
  "BC-ERR-01015",
  "BC-ERR-01017",
  "BC-ERR-01018",
  "BC-ERR-01019",
  "BC-MIS-01001",
  "BC-MIS-01009",
  "BC-MIS-01011",
  "BC-PRQ-01001",
  "BC-PRQ-01003",
  "BC-PRQ-01006",
  "BC-PRQ-01008",
  "BC-PRQ-01009",
  "research/units/unit-01-limits-continuity.md#1.10 Exploring Types of Discontinuities",
  "research/question-analysis/question-archetypes.md#BC-QA-01007 Discontinuity classified from a rule or a graph",
  "research/question-analysis/question-archetypes.md#BC-QA-01006 Continuity at a point tested against the three conditions",
  "research/question-analysis/question-archetypes.md#BC-QA-01009 Vertical asymptote located and the one sided infinite limits stated",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "read_minutes": {
  "full": 4.88,
  "brief": 2.99
 },
 "word_count": {
  "full": 731,
  "brief": 448
 }
}
```
