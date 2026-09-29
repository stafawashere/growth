---
title: LSN-CON-01013 Continuity at a point as three conditions
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01013, continuity at a point as three conditions, built from authoring_bundle("BC-CON-01013") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01013 Continuity at a point as three conditions

Concept BC-CON-01013 (skills BC-SKL-01043, BC-SKL-01044, BC-SKL-01045), topic 1.11 of Unit 1, loaded by BC-QA-01006 (primary). The unit attack map places it thirteenth, after BC-CON-01004 and BC-CON-01006, and its delivery map picks interactive for the key idea.

## Prediction

Served first, both bands, on ex-1's rule and value. Form: `short_answer`, numeric key 3, which is ex-1's valued limit step, so the blind re-solve of the example covers it. The question asks for the concept's core claim, that the value must agree with the limit, before the three conditions are stated. The resolution gives the three demands and the number they produce. Sources: BC-CON-01013 and the topic section the key idea cites. Delivery: text.

## Orientation

Served text, from BC-CON-01013 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-01-limits-continuity.md#1.11 Defining Continuity at a Point): MCQ forms ask whether a piecewise function is continuous at a boundary; FRQ forms require continuity statements with reasons, where the reason carries its own point (sg-25:12). Stated as what a response shows. Delivered as a figure.

## Key ideas

All three skills map to BC-EK-LIM-2A2 (ced:48): one core block, both bands.

- ki-1 (core). Paraphrase of the topic's Required mathematical knowledge paragraph (Definition; Justification standard, sg-25:12). Anchor quote (15 words) from ced:48, in the page's spoken form. Notation line from the concept record and the topic.

## Recognition

- BC-QA-01006 (family continuity-at-a-point, one FRQ part or a single MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-01006 Continuity at a point tested against the three conditions). `typical_wording`: "Determine whether the given function is continuous at the named input. Justify your answer." `asked_to_produce`: the function value, the one sided limits, a conclusion naming the condition that fails. `common_givens` is empty. Official example BC-MCQ-PE2012-036 (a calculator item, though the archetype is `no_calculator`; unit-01 README, Library gaps). The signal is the word "continuous" with a named input, usually a piecewise boundary or a separately defined point.

What says "not this concept": the stem asks only for a limit, the approached value (BC-CON-01002, 01004; unit-01 README row, Limit exists against continuity); continuity on an interval (BC-CON-01014); a parameter to make the function continuous (BC-CON-01015).

The near miss for st-1 comes from the unit-01 README row, Limit exists against continuity: the same rule with the same hole, but the stem asks only for the approached value (BC-CON-01002, 01004). A limit stem needs one number; a continuity stem also gives a value to compare.

## Method choice

- st-1, BC-QA-01006, low and mid bands, `evidence_tag: inferred` (no `common_givens`). Method, `expected_solution_path[0]`: evaluate the function at the named input. Rival, `wrong_approaches`: concluding continuity from matching one sided limits without the value (BC-ERR-01015). Separating feature: agreeing limits settle condition two only; condition three still compares them with the value.

## Solution path

- ex-1, BC-QA-01006, both bands: boundary 2, break_kind value, left_limit 3, left_slope 2, point_value \(-1\); \(f(x)=\frac{2x^2-5x+2}{x-2}\) for \(x\ne2\), \(f(2)=-1\) [inferred shape from the notes]. Steps follow `expected_solution_path`: the value (`new`, \(-1\)); the quotient (`new`), rewritten (`equivalent`), the limit (`limit`, 3), which covers both one sided limits because one rule holds on both sides; the comparison and the named failed condition. Answer form statement. No published draw matches.

A fluent solver writes the value, the reduced form, the limit and the comparison; the zero over zero observation is held in the head [inferred].

## Scoring

None. BC-QA-01006 lists no `point_types`, so no `what_a_reader_scores` entry and no point tag. Its `scoring_pattern` describes a value and limit point and a justification point naming the failed condition (research/question-analysis/question-archetypes.md#BC-QA-01006 Continuity at a point tested against the three conditions). For the author: a "justify" part needs an argument, a "give a reason" part one targeted sentence (research/scoring/justification-requirements.md#Justify, give a reason, and give reasons); a bare continuity statement does not earn the hypothesis point in sg-25:12 (research/scoring/justification-requirements.md#Theorem hypotheses). Vague referents in a reason are a notation loss (research/scoring/common-point-losses.md#Notation points) [inferred for this archetype in the unit-01 README].

## Traps

The bundle lists six errors; the first four in its order are served (linked BC-MIS severity high). Mid band the first two. All on ex-1's draw.

- err-BC-ERR-01001. Wrong: the limit reported as \(-1\). Right: 3. Distinct. Reason, words from BC-MIS-01001.
- err-BC-ERR-01014. Wrong: continuity from \(f(2)\) existing (\(-1\)). Right: the limit 3 also needed. Distinct. Reason, words from BC-MIS-01009.
- err-BC-ERR-01015. Wrong: sides compared, \(3-3\). Right: limit against value, \(3-(-1)\). Distinct. Reason, words from BC-MIS-01009.
- err-BC-ERR-01016. Wrong: the definition with no values (an unevaluated limit minus \(f(2)\)). Right: \(3-(-1)\). Distinct. Reason, words from BC-MIS-01010.

BC-ERR-01017 and BC-ERR-99001 fall beyond the cap.

All four blocks are distinct, so all four carry `fix_prompt` true.

## Representations

None as a separate block. The topic's Representations paragraph names rule to verdict and graph to verdict; the orientation figure and the ki-1 interactive carry the graph side.

## Prerequisite bridge

Two BC-PRQ parents, supporting edges, gated by state: BC-PRQ-01003 (piecewise rule) and BC-PRQ-06005 (function notation and evaluation). Each is one short line from `description_plain`, with the `failure_signature` kept, to stay under the brief cap.

## Time

BC-QA-01006 is `no_calculator`, one FRQ part or a single MCQ; the MCQ shape is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). On an FRQ part every named output is written (value, limits, comparison, failed condition; unit-01 README, Time budgets); on the MCQ the rewriting is the only written work [inferred].

## Checks

- chk-1, completion of ex-1, both bands: value and limit given; the student gives the verdict and names condition three. Key statement.
- chk-2, isomorph, both bands: jump at \(-1\), branches \(x+3\) and \(-2x-5\). Key statement: not continuous, the limit does not exist (2 against \(-3\)), condition two fails.
- chk-3, MCQ, low band: value break at 0, \(\frac{3x^2-2x}{x}\), \(f(0)=1\). Key: not continuous, limit \(-2\) against value 1. Distractors carry BC-ERR-01014, BC-ERR-01015, BC-ERR-01016.

## Delivery

- orientation: figure. Rule 3, BC-REP-02 on BC-SKL-01044 (README: figure). The ex-1 graph with the open circle at the limit and the filled point at the value.
- ki-1: interactive. Rule 3 promoted, as the README names: one slider on \(c=f(2)\), domain \(-4\) to 4, step 1; the question asks which condition fails at the setting. Keyboard: Tab to the slider, arrows by 1, Home and End. Fallback: the static figure with a table of two settings.
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full), in the served order of 2026-09-29: prediction, orientation, bridges when gated in, ki-1, st-1 (contrast pair on st-1), ex-1 and its scoring lines (none), chk-1, err-BC-ERR-01001, err-BC-ERR-01014, err-BC-ERR-01015, err-BC-ERR-01016 (each a fix prompt), chk-2, representations (none), chk-3. 630 words, 4.2 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, bridges when gated in, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-01001, err-BC-ERR-01014, chk-2. 448 words, 2.99 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-01013; BC-SKL-01043, BC-SKL-01044, BC-SKL-01045; BC-EK-LIM-2A2; ced:48; sg-25:12
- BC-QA-01006; BC-MCQ-PE2012-036
- BC-ERR-01001, BC-ERR-01014, BC-ERR-01015, BC-ERR-01016; BC-MIS-01001, BC-MIS-01009, BC-MIS-01010
- BC-PRQ-01003, BC-PRQ-06005
- research/units/unit-01-limits-continuity.md#1.11 Defining Continuity at a Point
- research/question-analysis/question-archetypes.md#BC-QA-01006 Continuity at a point tested against the three conditions
- research/exam/exam-structure.md#Section and part layout
- research/scoring/justification-requirements.md#Justify, give a reason, and give reasons
- research/scoring/justification-requirements.md#Theorem hypotheses
- research/scoring/common-point-losses.md#Notation points
- [inferred] Non-text delivery modes. Settled by the modality A/B.
- [inferred] st-1 on `typical_wording`. Settled by `common_givens` on BC-QA-01006.
- [inferred] The value-break rule shape. Settled by the BC-QA-01006 template.
- [inferred] sg-25:12 read onto a continuity-at-a-point reason. Settled by a guideline scoring such a reason.
- [inferred] One control per screen. Settled by the modality A/B.
- Prediction and contrast stems: written for this lesson, no published item shares them (content/items_* searched). Citations sit in each block's `sources` array, never in served text.

## Machine record

```json
{
 "id": "LSN-CON-01013",
 "kind": "concept",
 "target_id": "BC-CON-01013",
 "unit": "01",
 "skills": [
  "BC-SKL-01043",
  "BC-SKL-01044",
  "BC-SKL-01045"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Before the rule: \\(f(x)=\\frac{2x^2-5x+2}{x-2}\\) for \\(x\\ne2\\), \\(f(2)=-1\\). What must \\(f(2)\\) be for \\(f\\) to be continuous at 2?",
   "command_verb": "predict"
  },
  "format": "short_answer",
  "key": {
   "form": "numeric",
   "expr": "3"
  },
  "resolution": "Continuity at 2 needs \\(f(2)\\) to exist, the limit to exist, and the two to agree. The quotient reduces to \\(2x-1\\), so the limit is 3.",
  "sources": [
   "BC-CON-01013",
   "research/units/unit-01-limits-continuity.md#1.11 Defining Continuity at a Point"
  ]
 },
 "orientation": {
  "text": "A response checks three conditions at the named input, the value, the limit and their agreement, and names the failed condition with its values.",
  "sources": [
   "BC-CON-01013",
   "research/units/unit-01-limits-continuity.md#1.11 Defining Continuity at a Point"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-2A2",
   "depth": "core",
   "text": "\\(f\\) is continuous at \\(x=c\\) when \\(f(c)\\) exists, \\(\\lim_{x\\to c}f(x)\\) exists, and the two are equal. A reason names the failed condition with its values, not the definition; a bare continuity statement earns no credit in the scoring guideline.",
   "notation": "continuous at a point",
   "quote": {
    "text": "A function f is continuous at x equals c provided that f of c exists",
    "source": "ced:48"
   },
   "sources": [
    "BC-EK-LIM-2A2",
    "ced:48",
    "sg-25:12",
    "research/units/unit-01-limits-continuity.md#1.11 Defining Continuity at a Point"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01006",
   "cue": "Is the function continuous at the named input? Justify.",
   "method": "Evaluate the function at the named input.",
   "rival": "Continuity from matching one sided limits alone.",
   "separating_feature": "Agreeing limits settle condition two only.",
   "sources": [
    "BC-QA-01006"
   ],
   "evidence_tag": "inferred",
   "contrast": {
    "this": {
     "text": "Let \\(f(x)=\\frac{x^2-9}{x-3}\\) for \\(x\\ne3\\), \\(f(3)=5\\). Is \\(f\\) continuous at \\(x=3\\)? Justify.",
     "archetype_id": "BC-QA-01006"
    },
    "not_this": {
     "text": "Let \\(f(x)=\\frac{x^2-9}{x-3}\\) for \\(x\\ne3\\). Find \\(\\lim_{x\\to3}f(x)\\).",
     "why_not": "It asks only for the approached value."
    },
    "feature": "The word continuous, with a value given at the input."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01006",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "boundary": 2,
    "break_kind": "value",
    "closed_side": "right",
    "left_limit": 3,
    "right_limit": 3,
    "point_value": -1,
    "left_slope": 2,
    "right_slope": 2
   },
   "problem": {
    "text": "Let \\(f(x)=\\frac{2x^2-5x+2}{x-2}\\) for \\(x\\ne2\\), \\(f(2)=-1\\). Is \\(f\\) continuous at \\(x=2\\)? Justify.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The stem names \\(x=2\\): evaluate \\(f(2)\\) first.",
     "why": "The second line gives \\(f(2)=-1\\): condition one holds.",
     "expr": "-1",
     "relation": "new"
    },
    {
     "cue": "For \\(x\\ne2\\) the quotient gives zero over zero at 2.",
     "why": "Rewrite before taking the limit.",
     "expr": "(2*x**2-5*x+2)/(x-2)",
     "relation": "new"
    },
    {
     "cue": "\\(2x^2-5x+2=(x-2)(2x-1)\\): a common factor.",
     "why": "Dividing out \\(x-2\\) is valid for \\(x\\ne2\\).",
     "expr": "2*x - 1",
     "relation": "equivalent"
    },
    {
     "cue": "The same rule holds on both sides of 2.",
     "why": "Both one sided limits are 3: condition two holds.",
     "expr": "3",
     "relation": "limit",
     "variable": "x",
     "point": "2"
    },
    {
     "cue": "Compare the limit with the value.",
     "why": "\\(3\\ne-1\\): condition three fails, so \\(f\\) is not continuous at 2."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "x = 2"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01001",
   "observed_behavior": "The response gives the plotted or defined value of the function at the input in place of the value the function approaches there.",
   "scoring_consequence": "The reading point is lost, and in a continuity part the comparison of limit with value collapses.",
   "wrong_step": {
    "text": "The limit at 2 is reported as \\(f(2)=-1\\).",
    "expr": "-1"
   },
   "right_step": {
    "text": "The limit is 3, from \\(2x-1\\).",
    "expr": "3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01001",
    "text": "treats the limit as another name for evaluation"
   },
   "sources": [
    "BC-ERR-01001",
    "BC-MIS-01001"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01014",
   "observed_behavior": "The response concludes continuity at a point because the function is defined there.",
   "scoring_consequence": "The justification point is lost because the limit condition is never addressed.",
   "wrong_step": {
    "text": "\\(f(2)=-1\\) exists, so \\(f\\) is called continuous.",
    "expr": "-1"
   },
   "right_step": {
    "text": "The limit, 3, is also needed, and it differs.",
    "expr": "3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01009",
    "text": "holds one of the three conditions as the whole definition"
   },
   "sources": [
    "BC-ERR-01014",
    "BC-MIS-01009"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01015",
   "observed_behavior": "The response concludes continuity because the two one sided limits agree, without comparing them with the function value.",
   "scoring_consequence": "The justification point is lost, and a parameter solved this way can be wrong when the defined value differs.",
   "wrong_step": {
    "text": "The sides are compared: \\(3-3=0\\), so \\(f\\) is called continuous.",
    "expr": "3 - 3"
   },
   "right_step": {
    "text": "Limit against value: \\(3-(-1)=4\\ne0\\).",
    "expr": "3 - (-1)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01009",
    "text": "most often that the function is defined there or that the one sided limits agree"
   },
   "sources": [
    "BC-ERR-01015",
    "BC-MIS-01009"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-01016",
   "observed_behavior": "The response asserts that the function is or is not continuous because of the definition of continuity, without naming the condition that fails or the values that show it.",
   "scoring_consequence": "The justification point is lost; a scoring guideline requires the reason rather than the assertion (sg-25:12).",
   "wrong_step": {
    "text": "Not continuous, by the definition: \\(\\lim_{x\\to2}f(x)\\ne f(2)\\) with no values.",
    "expr": "Limit(f(x), x, 2) - f(2)"
   },
   "right_step": {
    "text": "\\(\\lim_{x\\to2}f(x)=3\\) and \\(f(2)=-1\\) differ.",
    "expr": "3 - (-1)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01010",
    "text": "treats naming the definition or the theorem as the argument"
   },
   "sources": [
    "BC-ERR-01016",
    "BC-MIS-01010"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-01003",
   "text": "Pick the piecewise branch for an input; the wrong branch at a boundary marks this gap."
  },
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Tell \\(f\\) from \\(f(c)\\); values read for the wrong input mark this gap."
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
    4,
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
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
   "archetype_id": "BC-QA-01006",
   "parameter_draw": {
    "boundary": 2,
    "break_kind": "value",
    "closed_side": "right",
    "left_limit": 3,
    "right_limit": 3,
    "point_value": -1,
    "left_slope": 2,
    "right_slope": 2
   },
   "completes": "ex-1",
   "stem": {
    "text": "For the \\(f\\) above, \\(f(2)=-1\\) and \\(\\lim_{x\\to2}f(x)=3\\). Is \\(f\\) continuous at 2? Name the failed condition.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "x = 2"
   },
   "steps": [
    {
     "text": "Limit minus value is 4, not 0: condition three fails.",
     "expr": "3 - (-1)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01045"
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
   "archetype_id": "BC-QA-01006",
   "parameter_draw": {
    "boundary": -1,
    "break_kind": "jump",
    "closed_side": "left",
    "left_limit": 2,
    "right_limit": -3,
    "left_slope": 1,
    "right_slope": -2,
    "point_value": 0
   },
   "stem": {
    "text": "Let \\(f(x)=x+3\\) for \\(x\\le-1\\), \\(f(x)=-2x-5\\) for \\(x>-1\\). Is \\(f\\) continuous at \\(-1\\)? Justify.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "x = -1"
   },
   "steps": [
    {
     "text": "Left branch.",
     "expr": "x + 3",
     "relation": "new"
    },
    {
     "text": "Left limit 2.",
     "expr": "2",
     "relation": "limit",
     "variable": "x",
     "point": "-1",
     "dir": "-"
    },
    {
     "text": "Right branch.",
     "expr": "-2*x - 5",
     "relation": "new"
    },
    {
     "text": "Right limit \\(-3\\): no limit, condition two fails.",
     "expr": "-3",
     "relation": "limit",
     "variable": "x",
     "point": "-1",
     "dir": "+"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01044",
    "BC-SKL-01045"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-01006",
   "parameter_draw": {
    "boundary": 0,
    "break_kind": "value",
    "closed_side": "left",
    "left_limit": -2,
    "right_limit": -2,
    "point_value": 1,
    "left_slope": 3,
    "right_slope": 3
   },
   "stem": {
    "text": "Let \\(f(x)=\\frac{3x^2-2x}{x}\\) for \\(x\\ne0\\), \\(f(0)=1\\). Which response gives a correct verdict with its reason?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "x = 0"
   },
   "steps": [
    {
     "text": "The quotient.",
     "expr": "(3*x**2-2*x)/x",
     "relation": "new"
    },
    {
     "text": "Divide out \\(x\\).",
     "expr": "3*x - 2",
     "relation": "equivalent"
    },
    {
     "text": "Limit \\(-2\\), against \\(f(0)=1\\).",
     "expr": "-2",
     "relation": "limit",
     "variable": "x",
     "point": "0"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "Continuous at 0, because \\(f(0)=1\\) is defined.",
     "error_path": "BC-ERR-01014",
     "derivation": "the value alone"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "Continuous at 0, because both one sided limits equal \\(-2\\).",
     "error_path": "BC-ERR-01015",
     "derivation": "matching limits alone"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "Not continuous at 0: \\(\\lim_{x\\to0}f(x)=-2\\) but \\(f(0)=1\\).",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "label": "Not continuous at 0, by the definition of continuity.",
     "error_path": "BC-ERR-01016",
     "derivation": "definition restated without values"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01044",
    "BC-SKL-01045"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-01044 (unit-01 README delivery map)",
   "sources": [
    "BC-SKL-01044"
   ],
   "spec": {
    "kind": "graph",
    "window": {
     "x": [
      0,
      4
     ],
     "y": [
      -2,
      7
     ]
    },
    "curves": [
     {
      "expr": "2*x - 1",
      "label": {
       "text": "f",
       "placement": "inside"
      }
     }
    ],
    "points": [
     {
      "x": 2,
      "y": 3,
      "style": "open",
      "label": {
       "text": "limit 3",
       "placement": "inside"
      }
     },
     {
      "x": 2,
      "y": -1,
      "style": "closed",
      "label": {
       "text": "f(2) = -1",
       "placement": "inside"
      }
     }
    ],
    "labels": [
     {
      "text": "value, limit, agreement",
      "placement": "inside"
     }
    ],
    "representations": [
     "graph"
    ]
   },
   "fallback": "Alt text: the line \\(y=2x-1\\) with an open circle at \\((2,3)\\) and a filled point at \\((2,-1)\\).",
   "keyboard": "none needed: a static figure"
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 3 promoted: BC-REP-02 on BC-SKL-01044, and BC-QA-01006 difficulty_variables vary whether the function value is defined at the boundary and whether the one sided limits agree; the stem asks for a reading of which condition fails",
   "sources": [
    "BC-SKL-01044",
    "BC-QA-01006"
   ],
   "spec": {
    "kind": "graph",
    "window": {
     "x": [
      0,
      4
     ],
     "y": [
      -5,
      7
     ]
    },
    "curves": [
     {
      "expr": "2*x - 1",
      "label": {
       "text": "f for x not 2",
       "placement": "inside"
      }
     }
    ],
    "points": [
     {
      "x": 2,
      "y": 3,
      "style": "open",
      "label": {
       "text": "limit 3",
       "placement": "inside"
      }
     },
     {
      "x": 2,
      "y": "c",
      "style": "closed",
      "draggable": false,
      "label": {
       "text": "f(2) = c",
       "placement": "inside"
      }
     }
    ],
    "controls": [
     {
      "type": "slider",
      "parameter": "c",
      "domain": {
       "min": -4,
       "max": 4,
       "step": 1
      },
      "initial": -1,
      "label": {
       "text": "f(2)",
       "placement": "inside"
      }
     }
    ],
    "question": {
     "text": "At this setting, which of the three conditions fails, if any?",
     "placement": "inside"
    },
    "labels": [
     {
      "text": "x = 2",
      "placement": "inside"
     }
    ],
    "representations": [
     "graph"
    ]
   },
   "fallback": "Static figure at \\(c=-1\\) with a table of the settings \\(c=-1\\) and \\(c=3\\) and the verdict for each.",
   "keyboard": "Tab focuses the slider; left and right arrow keys move c by 1; Home and End jump to -4 and 4."
  },
  {
   "block": "ex-1",
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
   "block": "err-BC-ERR-01014",
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
   "block": "err-BC-ERR-01016",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-01001",
  "err-BC-ERR-01014",
  "err-BC-ERR-01015",
  "err-BC-ERR-01016",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/justification-requirements.md",
   "line": "a response simply stating the function is continuous without justification does not earn it"
  }
 ],
 "inferred": [
  {
   "claim": "The non-text delivery modes chosen here serve the content better than text and step reveal.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "BC-QA-01006 has no common_givens, so st-1 rests on typical_wording and asked_to_produce and carries evidence_tag inferred.",
   "settles": "A common_givens entry on BC-QA-01006 from an official item."
  },
  {
   "claim": "The value-break rule of ex-1 follows the BC-QA-01006 notes: a quotient that simplifies to the left branch away from the boundary, with point_value defined at the boundary; right_limit and right_slope are set equal to the left ones since the quotient governs both sides.",
   "settles": "The BC-QA-01006 item template."
  },
  {
   "claim": "The sg-25:12 rule (a bare continuity statement earns no credit) is read as applying to the reason in a continuity-at-a-point part; its guideline concerns an IVT hypothesis.",
   "settles": "A scoring guideline page scoring a continuity-at-a-point reason."
  },
  {
   "claim": "One control per screen on the interactive key idea.",
   "settles": "The template's interactive row ([inferred] there) and the modality A/B."
  }
 ],
 "sources": [
  "BC-CON-01013",
  "BC-SKL-01043",
  "BC-SKL-01044",
  "BC-SKL-01045",
  "BC-EK-LIM-2A2",
  "ced:48",
  "sg-25:12",
  "BC-QA-01006",
  "BC-MCQ-PE2012-036",
  "BC-ERR-01001",
  "BC-ERR-01014",
  "BC-ERR-01015",
  "BC-ERR-01016",
  "BC-MIS-01001",
  "BC-MIS-01009",
  "BC-MIS-01010",
  "BC-PRQ-01003",
  "BC-PRQ-06005",
  "research/units/unit-01-limits-continuity.md#1.11 Defining Continuity at a Point",
  "research/question-analysis/question-archetypes.md#BC-QA-01006 Continuity at a point tested against the three conditions",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/justification-requirements.md#Justify, give a reason, and give reasons",
  "research/scoring/justification-requirements.md#Theorem hypotheses"
 ],
 "read_minutes": {
  "full": 4.2,
  "brief": 2.99
 },
 "word_count": {
  "full": 629,
  "brief": 447
 }
}
```
