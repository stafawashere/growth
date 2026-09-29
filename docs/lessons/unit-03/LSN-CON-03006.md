---
title: LSN-CON-03006 Derivative of an inverse function
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-03006, the derivative of an inverse function at a point, built from authoring_bundle("BC-CON-03006") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-03006 Derivative of an inverse function

Concept BC-CON-03006 (skills BC-SKL-03015 to BC-SKL-03020), topic 3.3 of Unit 3, loaded by two archetypes of the family inverse-function-derivative: BC-QA-03006 (primary, the value at a point) and BC-QA-03010 (the derivation from f(g(x)) = x, through BC-SKL-03020). Its hard parent concept is BC-CON-03002 (docs/lessons/unit-03/README.md, section 1).

## Orientation

Served text, from BC-CON-03006 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-03-differentiation-composite-implicit-inverse.md#3.3 Differentiating Inverse Functions): a response names the input of f whose output is the given value, reads f prime there, checks it is not zero and reports the reciprocal. No count, no frequency.

## Key ideas

All six skills map to BC-EK-FUN-3E1 (ced:77), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs (Derivative of an inverse, Derivation, Matched pairs): f(c) = b is the same statement as g(b) = c, so the slope of g at b is one over the slope of f at c, provided f'(c) is not zero; differentiating f(g(x)) = x by the chain rule gives it. No anchor quote, to keep the brief band under 450 words; FUN-3.E.1 on ced:77 is paraphrased. Notation line from the concept record.

## Recognition

BC-QA-03006 (research/question-analysis/question-archetypes.md#BC-QA-03006 Derivative of an inverse function at a point): `typical_wording` "the function g is the inverse of f; find the derivative of g at the stated value"; `common_givens` a function by formula, table or graph and a value that is an output of f; `asked_to_produce` the derivative of the inverse at the stated value. The signal: the word inverse beside a letter for the second function, and a number that sits in the output column of f. Shape: one MCQ, or one part of a multi-representation FRQ; no `official_examples`.

BC-QA-03010 (research/question-analysis/question-archetypes.md#BC-QA-03010 Inverse trigonometric derivative derived from the identity f(g(x)) = x): the stem supplies the identity and says differentiate both sides, and asks for g' as an expression in x.

What says "not this concept": a stem asking for the derivative of 1/f (the reciprocal function, a quotient rule question), or an arcsin or arctan of an inner expression with no identity supplied (BC-CON-03007).

## Method choice

Two strategy blocks, one per archetype; st-1 serves both bands.

- st-1, BC-QA-03006. Method, `expected_solution_path[0]`: identify the input whose output is the stated value. Rival, `wrong_approaches`: the reciprocal of f' at the stated value (BC-ERR-03015). Separating feature: the stated value is an output of f, never the input f' is read at. Both `asked_to_produce` and `common_givens` are present, so verified.
- st-2, BC-QA-03010. Method: differentiate both sides of the identity with the chain rule on the left. Rival, `wrong_approaches`: a remembered formula quoted without the inner factor. Separating feature: the stem supplies the identity and asks for the derivation.

## Solution path

- ex-1, BC-QA-03006, both bands, no calculator. Draw from `parameter_spec`: values [-1, 3, 4, 8], slopes [2, 5, 6, 3], at 2, names f,g; derived target = values[at - 1] = 3. Constraints hold: target 3 is in 1 to 4 and differs from at; values[2] = 4 is nonzero; 1/5, 1/6, 1/3, 1/4 are distinct. No published BC-QA-03006 item carries this draw.
- Steps follow `expected_solution_path`: the matching input (new); f' read at it (new); the nonzero check (no value); the reciprocal (new). A fluent solver writes g(3) = 2 and the reciprocal; the nonzero check is one clause, written when the stem asks why the rule applies (the Assessment behaviour's justification variant).

## Scoring

BC-QA-03006 and BC-QA-03010 list no `point_types`, so no what_a_reader_scores entry and no point tag; the served text says nothing about points beyond the error records' scoring_consequence. For the author: the archetype's scoring pattern says the matching input has to be visible in free response for the method to be communicated.

## Traps

Three active errors meet the skills, in the bundle's order: BC-ERR-03014, BC-ERR-03015, BC-ERR-03016. Low band all three; mid band the first two. All on ex-1's draw.

- err-BC-ERR-03014: 1/5 written with no condition, against 1/5 with f'(2) = 5 named nonzero; relation equivalent, the value is the same and the stated hypothesis differs. Possible reason, words from BC-MIS-03009.
- err-BC-ERR-03015: 1/f'(3) = 1/6 against 1/f'(2) = 1/5. Possible reason, words from BC-MIS-03008.
- err-BC-ERR-03016: 1/f(2) = 1/3 against 1/5. No possible reason line: neither linked description names the function column.

## Representations

The topic's Representations paragraph names the conversion of a table of values to the derivative of the inverse (BC-REP-03 to BC-REP-01) and of a graph to the slope of the inverse's graph (BC-REP-02 to BC-REP-01). The graph conversion is carried by ki-1's interactive; the table conversion is one low band block, served as a table of ex-1's draw with the matched row and the tempting row both inside it.

## Prerequisite bridge

- BC-PRQ-03003, from its `description_plain` and `failure_signature`.
- BC-PRQ-03006, from its `description_plain` and `failure_signature`.

## Time

BC-QA-03006 is `calculator_status` either, a single MCQ or one FRQ part. The design takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype placed in I-A; the table form keeps the numbers small]. The minutes go on locating the matching row; the reciprocal is one line. Written: steps 1, 2, 4. Held in the head on an MCQ: step 3.

## Checks

- chk-1, completion of ex-1, both bands: g(3) = 2 and f'(2) = 5 are given, the student reports g'(3). Key 1/5.
- chk-2, isomorph, both bands. Draw: values [-2, 0, 1, 4], slopes [3, 4, 7, 2], at 3, names p,q; target 1. Key q'(1) = 1/p'(3) = 1/7.
- chk-3, MCQ, low band. Draw: values [-3, -1, 2, 5], slopes [4, 6, 3, 1], at 3, names h,k; target 2. Key k'(2) = 1/3. Distractors: 1/6 (BC-ERR-03015, f' read at the given value), 1/2 (BC-ERR-03016, reciprocal of h(3) = 2), -1 (BC-ERR-03016, reciprocal of h(2) = -1, the function value in the given value's row). BC-ERR-03014 produces the key value, so two distractors carry BC-ERR-03016; the parameter_spec's distinct list names both function-value reciprocals.

## Delivery

- orientation: text. Rule 5: a statement of what a response shows.
- ki-1: interactive. Rule 3 promoted: BC-SKL-03016 and BC-SKL-03019 carry BC-REP-02, and BC-QA-03006's `difficulty_variables` ("whether the original function is given only graphically") name a quantity that varies with the stem asking for a reading (docs/lessons/unit-03/README.md, section 6) [inferred; settled by the modality A/B].
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-03014, err-BC-ERR-03015, err-BC-ERR-03016: step_reveal. Rule 1.
- representations: table. Rule 4: BC-SKL-03018 rests on BC-REP-03 givens, and the parameter_spec binds BC-REP-03 to a table figure.

## Band plan

- Low (full): orientation, ki-1, st-1, st-2, ex-1, the three error blocks, chk-1 to chk-3, representations, the two bridges. 556 words, 3.8 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, err-BC-ERR-03014, err-BC-ERR-03015, chk-1, chk-2, the two bridges. 427 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-03014, err-BC-ERR-03015, err-BC-ERR-03016, ex-1.

## Sources

- BC-CON-03006; BC-SKL-03015, BC-SKL-03016, BC-SKL-03017, BC-SKL-03018, BC-SKL-03019, BC-SKL-03020; BC-EK-FUN-3E1; ced:77, ced:72
- BC-QA-03006, BC-QA-03010
- BC-ERR-03014, BC-ERR-03015, BC-ERR-03016; BC-MIS-03008, BC-MIS-03009
- BC-PRQ-03003, BC-PRQ-03006
- research/units/unit-03-differentiation-composite-implicit-inverse.md#3.3 Differentiating Inverse Functions
- research/question-analysis/question-archetypes.md#BC-QA-03006 Derivative of an inverse function at a point
- research/question-analysis/question-archetypes.md#BC-QA-03010 Inverse trigonometric derivative derived from the identity f(g(x)) = x
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-03006 is placed in Section I Part A although its calculator status is either. Settled by an official item on the archetype with its section recorded.
- [inferred] ki-1 as an interactive and the representations block as a table. Settled by the modality A/B.
- [inferred] The interactive's curve f(x) = x^3/4 + x is an illustration chosen for being increasing; no record supplies a curve. Settled by a graph-form BC-QA-03006 item whose curve the figure can reuse.

## Machine record

```json
{
 "id": "LSN-CON-03006",
 "kind": "concept",
 "target_id": "BC-CON-03006",
 "unit": "03",
 "skills": ["BC-SKL-03015", "BC-SKL-03016", "BC-SKL-03017", "BC-SKL-03018", "BC-SKL-03019", "BC-SKL-03020"],
 "orientation": {
  "text": "A response finds the input of f whose output is the given value, reads f' there, checks it is not zero, and reports its reciprocal.",
  "sources": ["BC-CON-03006", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.3 Differentiating Inverse Functions"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3E1",
   "depth": "core",
   "text": "For g the inverse of f, f(c) = b says the same as g(b) = c. Reflecting in y = x inverts slopes, so g'(b) = 1/f'(c), provided f'(c) is not zero. Differentiating f(g(x)) = x by the chain rule gives it.",
   "notation": "g prime of a equals one over f prime of g of a",
   "quote": null,
   "sources": ["BC-EK-FUN-3E1", "ced:77", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.3 Differentiating Inverse Functions"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-03006",
   "cue": "g is named the inverse of f, and the given value sits among the outputs of f.",
   "method": "First line: find c with f(c) equal to the given value, then write g' there as 1/f'(c).",
   "rival": "Rival: 1 over f' at the given value itself (BC-ERR-03015).",
   "separating_feature": "The given value is an output of f, so it is never where f' is read.",
   "sources": ["BC-QA-03006"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-03010",
   "cue": "An identity such as tan(g(x)) = u is supplied and g' is asked for as an expression in x.",
   "method": "First line: differentiate both sides of the identity, chain rule on the left.",
   "rival": "Rival: a remembered formula quoted without the inner factor.",
   "separating_feature": "The stem supplies the identity, so the derivation is the answer.",
   "sources": ["BC-QA-03010"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-03006",
   "bands": ["low", "mid"],
   "parameter_draw": {"values": [-1, 3, 4, 8], "slopes": [2, 5, 6, 3], "at": 2, "names": "f,g"},
   "problem": {"text": "g is the inverse of f. For x = 1, 2, 3, 4: f(x) = -1, 3, 4, 8 and f'(x) = 2, 5, 6, 3. Find g'(3).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "3 is an output of f: which input gives it?", "why": "f(2) = 3, so g(3) = 2.", "expr": "g(3) = 2", "relation": "new"},
    {"cue": "The slope of g at 3 comes from f at 2.", "why": "The f' column in the row x = 2.", "expr": "5", "relation": "new"},
    {"cue": "The rule divides by f'(2).", "why": "5 is not zero, so the rule applies."},
    {"cue": "Reciprocal of the matched slope.", "why": "g'(3) = 1/f'(g(3)) = 1/f'(2).", "expr": "1/5", "relation": "new"}
   ],
   "answer": {"form": "numeric", "expr": "1/5"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-03014",
   "observed_behavior": "The formula for the derivative of an inverse is written with no mention that the derivative of the original function at the matching input must not be zero.",
   "scoring_consequence": "A justification point that requires the hypothesis is not earned; the Chief Reader reports record unverified hypotheses as a recurring loss (BC-ERR-99008).",
   "wrong_step": {"text": "g'(3) = 1/5, no condition.", "expr": "1/5"},
   "right_step": {"text": "f'(2) = 5, not zero, so g'(3) = 1/5.", "expr": "1/5"},
   "relation": "equivalent",
   "possible_reason": {"misconception_id": "BC-MIS-03009", "text": "treats the reciprocal formula as unconditional"},
   "sources": ["BC-ERR-03014", "BC-MIS-03009"]
  },
  {
   "error_id": "BC-ERR-03015",
   "observed_behavior": "The response computes the reciprocal of the derivative of the original function at the value supplied, instead of at the input whose output is that value.",
   "scoring_consequence": "The reported value is wrong although the formula is correct.",
   "wrong_step": {"text": "1/f'(3) = 1/6.", "expr": "1/6"},
   "right_step": {"text": "1/f'(2) = 1/5.", "expr": "1/5"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-03008", "text": "treats the input of the inverse and the input of the original function as the same number"},
   "sources": ["BC-ERR-03015", "BC-MIS-03008"]
  },
  {
   "error_id": "BC-ERR-03016",
   "observed_behavior": "The response inverts the value of the original function rather than the value of its derivative.",
   "scoring_consequence": "The reported value is wrong.",
   "wrong_step": {"text": "1/f(2) = 1/3.", "expr": "1/3"},
   "right_step": {"text": "1/f'(2) = 1/5.", "expr": "1/5"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-03016"]
  }
 ],
 "representations": {
  "text": "In a table, find the given value in the f column; the f' entry in that row, inverted, is the answer.",
  "figure": {"kind": "table", "representations": ["BC-REP-03"], "columns": ["x", "f(x)", "f'(x)"], "rows": [[1, -1, 2], [2, 3, 5], [3, 4, 6], [4, 8, 3]],
   "labels": [{"text": "row x = 2: f(2) = 3, the matched row", "placement": "inside"}, {"text": "row x = 3: the tempting row", "placement": "inside"}]}
 },
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-03003", "text": "f(a) = b means g(b) = a. Without the matching input, the formula is evaluated at the given input."},
  {"prq_id": "BC-PRQ-03006", "text": "A wrong simplification after a correct reciprocal changes the value reported."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 4]}, "skipped_steps": {"ex-1": [3]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03006",
   "parameter_draw": {"values": [-1, 3, 4, 8], "slopes": [2, 5, 6, 3], "at": 2, "names": "f,g"},
   "completes": "ex-1",
   "stem": {"text": "From the table, g(3) = 2 and f'(2) = 5. Find g'(3).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "1/5"},
   "steps": [
    {"text": "f'(2) = 5, not zero.", "expr": "5", "relation": "new"},
    {"text": "The reciprocal.", "expr": "1/5", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03018"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03006",
   "parameter_draw": {"values": [-2, 0, 1, 4], "slopes": [3, 4, 7, 2], "at": 3, "names": "p,q"},
   "stem": {"text": "q is the inverse of p. For x = 1, 2, 3, 4: p(x) = -2, 0, 1, 4 and p'(x) = 3, 4, 7, 2. Find q'(1).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "1/7"},
   "steps": [
    {"text": "p(3) = 1, so q(1) = 3.", "expr": "q(1) = 3", "relation": "new"},
    {"text": "p'(3) = 7, not zero.", "expr": "7", "relation": "new"},
    {"text": "The reciprocal.", "expr": "1/7", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03018"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-03006",
   "parameter_draw": {"values": [-3, -1, 2, 5], "slopes": [4, 6, 3, 1], "at": 3, "names": "h,k"},
   "stem": {"text": "k is the inverse of h. For x = 1, 2, 3, 4: h(x) = -3, -1, 2, 5 and h'(x) = 4, 6, 3, 1. What is k'(2)?", "command_verb": "identify"},
   "key": {"form": "numeric", "expr": "1/3"},
   "steps": [
    {"text": "h(3) = 2, so k(2) = 3.", "expr": "k(2) = 3", "relation": "new"},
    {"text": "h'(3) = 3, not zero.", "expr": "3", "relation": "new"},
    {"text": "The reciprocal.", "expr": "1/3", "relation": "new"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "1/6", "error_path": "BC-ERR-03015", "derivation": "h' read at the given value 2: 1/h'(2) = 1/6"},
    {"id": "B", "is_key": false, "expr": "1/2", "error_path": "BC-ERR-03016", "derivation": "the function value inverted: 1/h(3) = 1/2"},
    {"id": "C", "is_key": true, "expr": "1/3", "error_path": null},
    {"id": "D", "is_key": false, "expr": "-1", "error_path": "BC-ERR-03016", "derivation": "the function value in the given value's row inverted: 1/h(2) = -1"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03018"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: a statement of what a response shows", "sources": ["BC-CON-03006"]},
  {"block": "ki-1", "mode": "interactive", "reason": "rule 3 promoted: BC-REP-02 on BC-SKL-03016 and BC-SKL-03019; BC-QA-03006 difficulty_variables name a graphically given function and the stem asks for a reading of the slope relationship", "sources": ["BC-SKL-03016", "BC-SKL-03019", "BC-QA-03006"],
   "spec": {
    "kind": "inverse_pair",
    "representations": [
     "BC-REP-02",
     "BC-REP-01"
    ],
    "curves": [
     "f(x) = x^3/4 + x",
     {
      "expr": "sign(2*x + sqrt(4*x**2 + 64/27))*Abs(2*x + sqrt(4*x**2 + 64/27))**(1/3) + sign(2*x - sqrt(4*x**2 + 64/27))*Abs(2*x - sqrt(4*x**2 + 64/27))**(1/3)"
     },
     "y = x, dashed",
     {
      "expr": "c**3/4 + c + (3*c**2/4 + 1)*(x - c)"
     },
     {
      "expr": "c + (x - (c**3/4 + c))/(3*c**2/4 + 1)"
     }
    ],
    "window": {
     "x": [
      -3,
      5
     ],
     "y": [
      -3,
      5
     ]
    },
    "controls": [
     {
      "type": "slider",
      "name": "c",
      "range": [
       -2,
       2
      ],
      "step": 0.25,
      "start": 1
     }
    ],
    "drawn": [
     "the point (c, f(c)) with the tangent line of f there",
     "the point (f(c), c) with the tangent line of the inverse there",
     "both slopes as numbers"
    ],
    "labels": [
     {
      "text": "slope of f at (c, f(c))",
      "placement": "inside"
     },
     {
      "text": "slope of the inverse at (f(c), c)",
      "placement": "inside"
     },
     {
      "text": "y = x",
      "placement": "inside"
     }
    ],
    "question": "As c moves, how does the slope of the inverse at (f(c), c) compare with the slope of f at (c, f(c))?",
    "points": [
     {
      "x": "c",
      "y": "c**3/4 + c"
     },
     {
      "x": "c**3/4 + c",
      "y": "c"
     }
    ]
   },
   "fallback": "a static figure at c = 1: the points (1, 1.25) and (1.25, 1) marked, slopes 1.75 and 4/7 written inside the figure beside their tangent lines",
   "keyboard": "Tab focuses the slider; left and right arrow keys move c by one step; Home and End jump to the ends of the range"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03014", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03015", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03016", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "representations", "mode": "table", "reason": "rule 4: BC-SKL-03018 rests on BC-REP-03 givens; the parameter_spec binds BC-REP-03 to a table", "sources": ["BC-SKL-03018", "BC-QA-03006"],
   "spec": {"kind": "table", "columns": ["x", "f(x)", "f'(x)"], "rows": [[1, -1, 2], [2, 3, 5], [3, 4, 6], [4, 8, 3]], "highlight_rows": [2, 3],
    "labels": [{"text": "matched row: f(2) = 3", "placement": "inside"}, {"text": "tempting row: x = 3", "placement": "inside"}]},
   "fallback": "the same table as plain text with the two rows named in a sentence below it",
   "keyboard": "arrow keys move between cells; the screen reader reads each row's label"}
 ],
 "refresher": ["ki-1", "err-BC-ERR-03014", "err-BC-ERR-03015", "err-BC-ERR-03016", "ex-1"],
 "read_minutes": {"full": 3.8, "brief": 3.0},
 "word_count": {"full": 556, "brief": 427},
 "research_lines": [
  {"file": "research/units/unit-03-differentiation-composite-implicit-inverse.md", "line": "so the derivative of the inverse at b is read from the behaviour of f at c, not at b"}
 ],
 "inferred": [
  {"claim": "BC-QA-03006 has calculator_status either and the lesson places it in Section I Part A at 2.14 minutes.", "settles": "An official BC-QA-03006 item with its exam section recorded."},
  {"claim": "ki-1 is served as an interactive slider and the representations block as a table rather than as static text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "The interactive's curve f(x) = x^3/4 + x is an illustration chosen for being increasing; no record supplies a curve.", "settles": "A graph-form BC-QA-03006 item whose curve the figure can reuse."},
  {"claim": "chk-3 carries BC-ERR-03016 on two distractors because BC-ERR-03014 produces the key value on every draw.", "settles": "A BC-ERR record for the derivative of f reported unchanged, a common_distractor on BC-QA-03006 with no error id."}
 ],
 "sources": ["BC-CON-03006", "BC-SKL-03015", "BC-SKL-03016", "BC-SKL-03017", "BC-SKL-03018", "BC-SKL-03019", "BC-SKL-03020", "BC-EK-FUN-3E1", "ced:77", "ced:72", "BC-QA-03006", "BC-QA-03010", "BC-ERR-03014", "BC-ERR-03015", "BC-ERR-03016", "BC-MIS-03008", "BC-MIS-03009", "BC-PRQ-03003", "BC-PRQ-03006", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.3 Differentiating Inverse Functions", "research/question-analysis/question-archetypes.md#BC-QA-03006 Derivative of an inverse function at a point", "research/question-analysis/question-archetypes.md#BC-QA-03010 Inverse trigonometric derivative derived from the identity f(g(x)) = x", "research/exam/exam-structure.md#Section and part layout"]
}
```
