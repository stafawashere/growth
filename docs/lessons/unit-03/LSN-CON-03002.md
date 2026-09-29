---
title: LSN-CON-03002 Chain rule as a product of rates
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-03002, the chain rule as a product of rates, built from authoring_bundle("BC-CON-03002") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-03002 Chain rule as a product of rates

Concept BC-CON-03002 (skills BC-SKL-03002, BC-SKL-03004, BC-SKL-03005, BC-SKL-03006), topic 3.1 of Unit 3. Six archetypes load its skills: BC-QA-03001, BC-QA-03002, BC-QA-03003, BC-QA-03009, BC-QA-03010 and BC-QA-99001. The last three are primary to other concepts or units (BC-QA-03009 to BC-CON-03008, BC-QA-03010 to BC-CON-03006 and 03007, BC-QA-99001 to Unit 9; docs/lessons/unit-03/README.md, section 2), so this lesson draws from the first three, one per family.

## Orientation

Served text, from BC-CON-03002 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-03-differentiation-composite-implicit-inverse.md#3.1 The Chain Rule): a response multiplies the outer rate, read at the inner output, by the inner rate, read at the input. Stems give a formula, a table of values or two graphs. No count, no frequency.

## Key ideas

All four skills map to one BC-EK, BC-EK-FUN-3C1 (ced:75), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Chain rule, Leibniz form): dy/dx is dy/du times du/dx; f'(g(a)) is read at the inner output g(a), g'(a) at the input; from a table or graphs the same two readings are taken in sequence. No anchor quote is served, to keep the brief band under its cap. Notation line from the concept record: dy/dx equals dy/du times du/dx.

## Recognition

- BC-QA-03002 (family derivative-from-table; research/question-analysis/question-archetypes.md#BC-QA-03002 Composite derivative evaluated from a table of values): `typical_wording` "use the table of values to find the derivative of the composite function at the stated input"; `common_givens` a table of values of f, f prime, g and g prime at selected inputs, a composite of the tabulated functions. Signal: the named function is f(g(x)) and the table lists derivative columns. One MCQ, or one part of a table-based FRQ; no `official_examples`.
- BC-QA-03001 (family rule-manipulation; research/question-analysis/question-archetypes.md#BC-QA-03001 Chain rule derivative of a composite given symbolically): a formula built by composition, possibly one factor of a product. MCQ or an opening FRQ step (BC-FRQ-2013-Q4-D, BC-FRQ-2014-Q3-D, BC-MCQ-PE2012-001).
- BC-QA-03003 (family derivative-from-graph; research/question-analysis/question-archetypes.md#BC-QA-03003 Composite derivative read from graphs of the component functions): graphs of the two component functions and a stated input. One MCQ; no `official_examples`.

What says "not this one": a table stem whose named combination is a product f(x)g(x) reads all four entries at one input (BC-QA-02009, the product rule; docs/lessons/unit-03/README.md, section 3). A composite f(g(a)) reads the table twice in sequence.

## Method choice

Three strategy blocks, low band; st-1 only in the mid band. Each archetype carries `asked_to_produce` and `common_givens`, so none is tagged inferred.

- st-1, BC-QA-03002. Method, `expected_solution_path[0]`: evaluate the inner function at the given input. Rival, `wrong_approaches`: the outer derivative read at the stated input (BC-ERR-03003). Separating feature: the outer derivative's row is the inner output.
- st-2, BC-QA-03001. Method: identify the outer and inner functions. Rival: the composite factor differentiated without the enclosing product or quotient rule (BC-ERR-03006). Separating feature: the operation applied last picks the first rule.
- st-3, BC-QA-03003. Method: read the inner function value at the given input. Rival: a slope read at a corner of the graph (BC-ERR-03005). Separating feature: the outer slope is read on the piece that contains the inner output.

## Solution path

- ex-1, BC-QA-03002, both bands, no calculator. Draw: f_values 2, -1, 5, 4; f_slopes 4, -2, -3, 1; g_values 3, 1, 4, 2; g_slopes 2, -1, 3, 1; at 1; names f,g; direction forward. Derived: inner 3, outer_slope -3, inner_slope 2, chain -6; options -6, 8, -1, 10, distinct; every constraint holds. Steps: g(1) (no value), f'(3) (no value), the product (valued, new), the value (equivalent). A fluent solver writes g(1) = 3 beside the row it names, then the product; the other readings are held in the head.
- ex-2, BC-QA-03001, low band, no calculator. Draw: family root, exponent 2, inner_slope 2, at 1, outside_power 1, target 3, scale 1, so shift 7 and h(x) = x sqrt(2x^2 + 7). Options 11/3, 2/3, 19/6, 15, distinct. Steps: the composite factor (new), its derivative (differentiate, tagged BC-PT-99023), the product line (new), the value (evaluate). A fluent solver writes steps 2 to 4.

Neither draw equals a published `parameter_draw` on its archetype (content/items_gen_unit03, content/items_p1_agent). No productive-failure target is assigned in the unit, so no comparison callout.

## Scoring

ex-1's archetype, BC-QA-03002, lists no `point_types`, so ex-1 carries no scoring entry and the served text on it says nothing about points. ex-2's archetype, BC-QA-03001, lists BC-PT-99023 and BC-PT-99004; ex-2 tags BC-PT-99023 on the chain step, and its line is `reader_checks(["BC-PT-99023"])`:

Chain rule. Earned by: Correct differentiation of the inner function, including the required differentials (sg-22:16, sg-25:21). Not earned by: A product rule written without one or both differentials, which sg-22:16 states earns the product rule point but not this one. Notation: sg-22:16 treats a missing differential as the defining failure for this point.

Point losses for the symbolic form: an attempted simplification must be correct (research/scoring/notation-requirements.md#Simplification, sg-23:16); an unrequired simplification that introduces an error loses the answer point (research/scoring/common-point-losses.md#Answer points, BC-ERR-99022).

## Traps

Six active errors meet the skills; the first four in the bundle's order are served (cap 4): BC-ERR-03001, BC-ERR-03002, BC-ERR-03003, BC-ERR-03004. BC-ERR-03005 and BC-ERR-03006 are named in st-3 and st-2 only. Mid band shows the first two.

- err-BC-ERR-03001, on ex-1: f'(3) alone, -3, against -6. Possible reason, words from BC-MIS-03001.
- err-BC-ERR-03002, on ex-2: the inner derivative 4x omitted against the root differentiated. The record names the innermost layer of three; the spec draws two layers [inferred].
- err-BC-ERR-03003, on ex-1: f'(1)g'(1) = 8 against f'(3)g'(1) = -6. Possible reason, words from BC-MIS-03002.
- err-BC-ERR-03004, on ex-1: -3 + 2 = -1 against -6. No possible reason line: the linked descriptions do not name addition.

## Representations

None as a separate block. The topic's Representations paragraph names the graph-to-value conversion (BC-REP-02 to BC-REP-01), which ki-1's figure carries, and the table-to-value conversion (BC-REP-03 to BC-REP-01), which ex-1 carries as its given.

## Prerequisite bridge

Three supporting parents: BC-PRQ-03001, BC-PRQ-03005, BC-PRQ-03006, each from its `description_plain` and `failure_signature`, served by state.

## Time

BC-QA-03002 is `either` on calculator status and a single MCQ; this draw is integer arithmetic, so the part is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout); a calculator form sits in Part B at 2.92. A fluent solver writes g(1) = 3 and the product, and the MCQ budget goes on locating the right row. ex-2 fits the same Part A budget.

## Checks

- chk-1, completion of ex-1, both bands. Key -6.
- chk-2, isomorph on BC-QA-03002, both bands. Draw: f_values 1, 3, -2, 5; f_slopes 3, 2, -1, 4; g_values 2, 4, 1, 3; g_slopes 1, 5, 4, 3; at 3. Key f'(1)g'(3) = 12; the stem also lists f'(3) as the tempting row.
- chk-3, MCQ on BC-QA-03002, low band. Draw: f_values 3, -2, 6, 1; f_slopes 2, 5, 4, -1; g_values 4, 3, 1, 2; g_slopes 1, -2, 3, 2; at 2. Key -8. Distractors: -10 (BC-ERR-03003), 2 (BC-ERR-03004), 4 (BC-ERR-03001).

## Delivery

- orientation: text. Rule 5 for the orientation's statement; the figure-bearing representation is served once, on ki-1, to keep one new idea per screen.
- ki-1: figure. Rule 3: BC-SKL-03005 carries BC-REP-02. Not promoted: BC-QA-03003's `difficulty_variables` (a corner, a grid position) are properties of a fixed graph, not a varying quantity (docs/lessons/unit-03/README.md, section 6) [inferred; settled by the modality A/B].
- ex-1: step_reveal, the table rendered inside the problem (BC-REP-03 given). Rule 1.
- ex-2: step_reveal. Rule 1.
- err-BC-ERR-03001, 03002, 03003, 03004: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1 to st-3, ex-1, the four error blocks, the three checks, ex-2 with its scoring line, the three bridges. 753 words, 5.1 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, err-BC-ERR-03001, err-BC-ERR-03002, chk-1, chk-2, the bridges. 415 words, 2.8 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-03002; BC-SKL-03002, BC-SKL-03004, BC-SKL-03005, BC-SKL-03006; BC-EK-FUN-3C1; ced:75, ced:72, ced:79
- BC-QA-03001, BC-QA-03002, BC-QA-03003, BC-QA-03009, BC-QA-03010, BC-QA-99001, BC-QA-02009; BC-FRQ-2013-Q4-D, BC-FRQ-2014-Q3-D, BC-MCQ-PE2012-001
- BC-PT-99023, BC-PT-99004; sg-22:16, sg-25:21, sg-23:16
- BC-ERR-03001, BC-ERR-03002, BC-ERR-03003, BC-ERR-03004, BC-ERR-03005, BC-ERR-03006; BC-MIS-03001, BC-MIS-03002, BC-MIS-03012; BC-ERR-99022
- BC-PRQ-03001, BC-PRQ-03005, BC-PRQ-03006
- research/units/unit-03-differentiation-composite-implicit-inverse.md#3.1 The Chain Rule
- research/question-analysis/question-archetypes.md#BC-QA-03001 Chain rule derivative of a composite given symbolically
- research/question-analysis/question-archetypes.md#BC-QA-03002 Composite derivative evaluated from a table of values
- research/question-analysis/question-archetypes.md#BC-QA-03003 Composite derivative read from graphs of the component functions
- research/scoring/notation-requirements.md#Simplification
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-ERR-03002 shown on a two-layer draw. Settled by a layers parameter in the BC-QA-03001 spec.
- [inferred] ki-1 as a static figure. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-03002",
 "kind": "concept",
 "target_id": "BC-CON-03002",
 "unit": "03",
 "skills": ["BC-SKL-03002", "BC-SKL-03004", "BC-SKL-03005", "BC-SKL-03006"],
 "orientation": {
  "text": "A response multiplies two rates: the outer derivative, read at the inner output, times the inner derivative, read at the input. Stems give a formula, a table of values or two graphs.",
  "sources": ["BC-CON-03002", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.1 The Chain Rule"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3C1",
   "depth": "core",
   "text": "With y a function of u and u a function of x, dy/dx is dy/du times du/dx. For h = f(g(x)) at x = a, the outer rate f' is read at the inner output g(a), not at a; the inner rate g' is read at a. A table or two graphs give the same readings, taken in that order.",
   "notation": "dy/dx equals dy/du times du/dx",
   "quote": null,
   "sources": ["BC-EK-FUN-3C1", "ced:75", "ced:72", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.1 The Chain Rule"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-03002",
   "cue": "The stem asks for the derivative of the composite at the stated input, from a table of f, f', g and g'.",
   "method": "First written line: the inner function at the given input, g(a).",
   "rival": "Rival: the outer derivative read at the stated input (BC-ERR-03003).",
   "separating_feature": "The outer derivative's row is g(a).",
   "sources": ["BC-QA-03002"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-03001",
   "cue": "The stem asks for the derivative of the composite, from a formula built by composition, possibly one factor of a product.",
   "method": "First written line: identify the outer and inner functions.",
   "rival": "Rival: the composite factor differentiated without the enclosing product or quotient rule (BC-ERR-03006).",
   "separating_feature": "The operation applied last picks the first rule.",
   "sources": ["BC-QA-03001"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-3",
   "archetype_id": "BC-QA-03003",
   "cue": "The stem asks for the derivative of the composite at the stated input, from graphs of the two component functions.",
   "method": "First written line: the inner function value read at the given input.",
   "rival": "Rival: a slope read at a corner of the graph as though the derivative existed there (BC-ERR-03005).",
   "separating_feature": "The outer slope is read on the piece containing the inner output.",
   "sources": ["BC-QA-03003"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-03002",
   "bands": ["low", "mid"],
   "parameter_draw": {"f_values": [2, -1, 5, 4], "f_slopes": [4, -2, -3, 1], "g_values": [3, 1, 4, 2], "g_slopes": [2, -1, 3, 1], "at": 1, "names": "f,g", "direction": "forward"},
   "problem": {"text": "At x = 1, 2, 3, 4: f is 2, -1, 5, 4; f' is 4, -2, -3, 1; g is 3, 1, 4, 2; g' is 2, -1, 3, 1. h(x) = f(g(x)). Find h'(1).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "h is f of g: read the inner value first.", "why": "g(1) = 3 names the row for f'."},
    {"cue": "Outer rate at the inner output, row 3.", "why": "f'(3) = -3."},
    {"cue": "Inner rate at the input: g'(1) = 2.", "why": "The two rates multiply.", "expr": "(-3)*2", "relation": "new"},
    {"cue": "The stem asks for a value.", "why": "Product of the rates.", "expr": "-6", "relation": "equivalent"}
   ],
   "answer": {"form": "numeric", "expr": "-6"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-03001",
   "bands": ["low"],
   "parameter_draw": {"family": "root", "exponent": 2, "inner_slope": 2, "at": 1, "outside_power": 1, "target": 3, "scale": 1},
   "problem": {"text": "Let h(x) = x sqrt(2x^2 + 7). Find h'(1).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Last operation: x times a root. The root is a composite.", "why": "Product rule outside; inner u = 2x^2 + 7.", "expr": "sqrt(2*x**2 + 7)", "relation": "new"},
    {"cue": "Root derivative at the inner expression.", "why": "1/(2 sqrt(u)) times the inner rate 4x.", "expr": "4*x/(2*sqrt(2*x**2 + 7))", "relation": "differentiate", "variable": "x", "point_type_id": "BC-PT-99023"},
    {"cue": "Assemble the product rule.", "why": "Each term differentiates one factor.", "expr": "sqrt(2*x**2 + 7) + x*4*x/(2*sqrt(2*x**2 + 7))", "relation": "new"},
    {"cue": "The stem asks for h'(1).", "why": "The root is 3 at x = 1: 3 + 4/6.", "expr": "11/3", "relation": "evaluate", "subs": {"x": "1"}}
   ],
   "answer": {"form": "numeric", "expr": "11/3"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-2", "point_type_ids": ["BC-PT-99023"], "lines": [{"point_type_id": "BC-PT-99023", "text": "Chain rule. Earned by: Correct differentiation of the inner function, including the required differentials (sg-22:16, sg-25:21). Not earned by: A product rule written without one or both differentials, which sg-22:16 states earns the product rule point but not this one. Notation: sg-22:16 treats a missing differential as the defining failure for this point."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-03001",
   "observed_behavior": "The response differentiates the outer function correctly and stops, leaving the derivative of the inner function out of the product.",
   "scoring_consequence": "The derivative is wrong, and in a multipart question the error propagates into every later part that uses it.",
   "wrong_step": {"text": "f'(3) alone: -3.", "expr": "-3"},
   "right_step": {"text": "f'(3)g'(1): -6.", "expr": "(-3)*2"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-03001", "text": "whatever sits inside is copied across unchanged"},
   "sources": ["BC-ERR-03001", "BC-MIS-03001"]
  },
  {
   "error_id": "BC-ERR-03002",
   "observed_behavior": "A composition of three functions is differentiated through the first two layers and the innermost derivative is omitted.",
   "scoring_consequence": "The derivative is wrong; no credit is available for a partially applied rule in a single answer item.",
   "wrong_step": {"text": "ex-2, inner derivative 4x omitted: value 19/6.", "expr": "sqrt(2*x**2 + 7) + x/(2*sqrt(2*x**2 + 7))"},
   "right_step": {"text": "Root differentiated.", "expr": "sqrt(2*x**2 + 7) + x*4*x/(2*sqrt(2*x**2 + 7))"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-03002"]
  },
  {
   "error_id": "BC-ERR-03003",
   "observed_behavior": "In a table or graph based composite, the derivative of the outer function is read at the stated input instead of at the value the inner function produces.",
   "scoring_consequence": "The numerical answer is wrong even though the chain rule structure was written correctly.",
   "wrong_step": {"text": "f'(1)g'(1) = 4(2) = 8.", "expr": "4*2"},
   "right_step": {"text": "f'(3)g'(1) = -6.", "expr": "(-3)*2"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-03002", "text": "the inner output plays no part in where the outer derivative is read"},
   "sources": ["BC-ERR-03003", "BC-MIS-03002"]
  },
  {
   "error_id": "BC-ERR-03004",
   "observed_behavior": "The response adds the two tabulated derivatives instead of multiplying them.",
   "scoring_consequence": "The reported value is wrong.",
   "wrong_step": {"text": "f'(3) + g'(1) = -1.", "expr": "-3 + 2"},
   "right_step": {"text": "f'(3)g'(1) = -6.", "expr": "(-3)*2"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-03004"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-03001", "text": "Name the operation applied last and the one applied first. Without it the outer shell is differentiated and the work stops."},
  {"prq_id": "BC-PRQ-03005", "text": "f', dy/dx and dy/du name derivatives. Writing dy for dy/dx loses the meaning of the line."},
  {"prq_id": "BC-PRQ-03006", "text": "Rewrite radicals as powers without changing the value. A wrong simplification after a correct derivative changes the value."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 3], "ex-2": [2, 3, 4]}, "skipped_steps": {"ex-1": [2, 4], "ex-2": [1]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03002",
   "parameter_draw": {"f_values": [2, -1, 5, 4], "f_slopes": [4, -2, -3, 1], "g_values": [3, 1, 4, 2], "g_slopes": [2, -1, 3, 1], "at": 1, "names": "f,g", "direction": "forward"},
   "completes": "ex-1",
   "stem": {"text": "g(1) = 3, f'(3) = -3, g'(1) = 2. Find h'(1) for h(x) = f(g(x)).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "-6"},
   "steps": [
    {"text": "f'(g(1))g'(1).", "expr": "(-3)*2", "relation": "new"},
    {"text": "-6.", "expr": "-6", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03004"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03002",
   "parameter_draw": {"f_values": [1, 3, -2, 5], "f_slopes": [3, 2, -1, 4], "g_values": [2, 4, 1, 3], "g_slopes": [1, 5, 4, 3], "at": 3, "names": "f,g", "direction": "forward"},
   "stem": {"text": "g(3) = 1, g'(3) = 4, f'(1) = 3, f'(3) = -1. Find h'(3) for h(x) = f(g(x)).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "12"},
   "steps": [
    {"text": "f'(g(3))g'(3) = f'(1)g'(3).", "expr": "3*4", "relation": "new"},
    {"text": "12.", "expr": "12", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03004"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-03002",
   "parameter_draw": {"f_values": [3, -2, 6, 1], "f_slopes": [2, 5, 4, -1], "g_values": [4, 3, 1, 2], "g_slopes": [1, -2, 3, 2], "at": 2, "names": "f,g", "direction": "forward"},
   "stem": {"text": "g(2) = 3, g'(2) = -2, f'(2) = 5, f'(3) = 4. For h(x) = f(g(x)), what is h'(2)?", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "-8"},
   "steps": [
    {"text": "f'(g(2))g'(2) = f'(3)g'(2).", "expr": "4*(-2)", "relation": "new"},
    {"text": "-8.", "expr": "-8", "relation": "equivalent"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "-10", "error_path": "BC-ERR-03003", "derivation": "f'(2)g'(2): the outer derivative read at the input"},
    {"id": "B", "is_key": true, "expr": "-8", "error_path": null},
    {"id": "C", "is_key": false, "expr": "2", "error_path": "BC-ERR-03004", "derivation": "f'(3) + g'(2): the rates added"},
    {"id": "D", "is_key": false, "expr": "4", "error_path": "BC-ERR-03001", "derivation": "f'(3) alone: the inner derivative left out"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03004"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5 for a statement of what a response shows; the figure-bearing BC-REP-02 on BC-SKL-03005 is served once, on ki-1", "sources": ["BC-SKL-03002"]},
  {"block": "ki-1", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-03005; not promoted, since BC-QA-03003's difficulty_variables are properties of a fixed graph", "sources": ["BC-SKL-03005", "BC-QA-03003"],
   "spec": {"kind": "graph_pair", "representations": ["BC-REP-02"], "panels": [
     {"name": "g", "curve": "polygon through (0,1), (2,3), (4,2)", "marks": [{"at": [1, 2], "what": "point (a, g(a))"}], "labels": [{"text": "g(a) = u", "placement": "inside"}, {"text": "slope g'(a)", "placement": "inside"}]},
     {"name": "f", "curve": "polygon through (0,0), (2,2), (4,-1)", "marks": [{"at": [2, 2], "what": "the vertical line u = g(a)"}], "labels": [{"text": "read f' here, at u = g(a)", "placement": "inside"}, {"text": "not at x = a", "placement": "inside"}]}
    ]},
   "fallback": "the two panels as a static image with the same labels, and a text line: read g(a) first, then the slope of f at that value, then multiply by the slope of g at a",
   "keyboard": "none needed: the figure has no control"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1; the tabulated values render as a table inside the problem (BC-REP-03 given)", "sources": ["BC-SKL-03004"]},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03001", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03002", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03003", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03004", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-03001", "err-BC-ERR-03002", "err-BC-ERR-03003", "err-BC-ERR-03004", "ex-1"],
 "read_minutes": {"full": 5.1, "brief": 2.8},
 "word_count": {"full": 755, "brief": 417},
 "research_lines": [
  {"file": "research/units/unit-03-differentiation-composite-implicit-inverse.md", "line": "Look up the inner value first, then look up the outer derivative at that value."}
 ],
 "inferred": [
  {"claim": "BC-ERR-03002 describes the innermost layer of a three-layer composite, and the block shows a layer left undifferentiated on a two-layer draw.", "settles": "A layers parameter in the BC-QA-03001 parameter_spec, giving a three-layer draw."},
  {"claim": "ki-1 is served as a static figure rather than an interactive one.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-03002", "BC-SKL-03002", "BC-SKL-03004", "BC-SKL-03005", "BC-SKL-03006", "BC-EK-FUN-3C1", "ced:75", "ced:72", "ced:79", "BC-QA-03001", "BC-QA-03002", "BC-QA-03003", "BC-QA-03009", "BC-QA-03010", "BC-QA-99001", "BC-QA-02009", "BC-FRQ-2013-Q4-D", "BC-FRQ-2014-Q3-D", "BC-MCQ-PE2012-001", "BC-PT-99023", "BC-PT-99004", "sg-22:16", "sg-25:21", "sg-23:16", "BC-ERR-03001", "BC-ERR-03002", "BC-ERR-03003", "BC-ERR-03004", "BC-ERR-03005", "BC-ERR-03006", "BC-MIS-03001", "BC-MIS-03002", "BC-MIS-03012", "BC-ERR-99022", "BC-PRQ-03001", "BC-PRQ-03005", "BC-PRQ-03006", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.1 The Chain Rule", "research/question-analysis/question-archetypes.md#BC-QA-03002 Composite derivative evaluated from a table of values", "research/scoring/notation-requirements.md#Simplification", "research/scoring/common-point-losses.md#Answer points", "research/exam/exam-structure.md#Section and part layout"]
}
```
