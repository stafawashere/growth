---
title: LSN-CON-03005 Tangent line behaviour on an implicit curve
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-03005, horizontal and vertical tangents on an implicitly defined curve, built from authoring_bundle("BC-CON-03005") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-03005 Tangent line behaviour on an implicit curve

Concept BC-CON-03005 (skills BC-SKL-03012, BC-SKL-03013), topic 3.2 of Unit 3, loaded by one archetype, BC-QA-03005 (family implicit-differentiation), which reuses the curve of the implicit differentiation question. Its hard parent concept is BC-CON-03004 (docs/lessons/unit-03/README.md, section 1).

## Prediction

One multiple choice question on worked example 1's own quotient, \(dy/dx=\frac{3(x-1)(x+1)}{2(y-2)}\), asked before the rule is shown: which part is zero where the tangent is horizontal. The key is the numerator, ex-1's first step. The distractors are the denominator (the BC-ERR-03012 path) and both parts at once. The resolution, shown on the key idea screen beside the choice, states that a quotient is zero where its numerator is zero and its denominator is not, and gives the candidates \(x=-1\) and \(x=1\). No verdict word. Sources: BC-CON-03005 and the topic 3.2 section the key idea cites.

## Orientation

Served text, from BC-CON-03005 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation): a response sets the numerator of dy/dx to zero for a horizontal tangent or the denominator for a vertical one, then substitutes into the curve equation and keeps only points of the curve. No count, no frequency.

## Key ideas

Both skills map to BC-EK-FUN-3D1 (ced:76), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Tangent conditions): with dy/dx a quotient, the tangent is horizontal where the numerator is zero and the denominator is not, vertical where the denominator is zero and the numerator is not, and a candidate meeting only the condition on dy/dx need not be a point of the curve (cr-23:22, cr-24:17). No anchor quote: the bundle's `ced_pages` for this concept are ced:63, ced:110 and ced:171, none of which carries BC-EK-FUN-3D1, so no quote can be checked against a bundle page (library gap). Notation line from the concept record.

## Recognition

BC-QA-03005 (research/question-analysis/question-archetypes.md#BC-QA-03005 Horizontal or vertical tangent on an implicitly defined curve): `typical_wording` "find the coordinates of a point on the curve at which the tangent line is vertical, or explain why no such point exists", "determine whether the stated horizontal line is tangent to the curve"; `common_givens` an equation defining the curve, an expression for dy/dx supplied or found earlier, a stated horizontal line or a point on the curve; `asked_to_produce` coordinates, an explanation why no such point exists, a decision whether a stated line is tangent. The signal: the words horizontal or vertical beside tangent, with a quotient for dy/dx already on the page. Shape: one or two parts inside the no-calculator implicit FRQ (cr-23:22, cr-24:17); no `official_examples` in the record.

Contrast pair on st-1: this stem is on BC-QA-03005, a curve with its \(dy/dx\) supplied and a vertical tangent asked; not this stem is the same curve asking for the slope at a named point, the near miss from BC-CON-03004 (BC-QA-03004), which substitutes and sets nothing to zero. The separating feature is the words horizontal or vertical beside tangent.

What says "not this concept": a stem asking for the slope at a named point (BC-CON-03004), or for the tangent line equation there.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-03005. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: set the numerator or the denominator of dy/dx equal to zero as the direction requires. Rival, `wrong_approaches`: the conditions exchanged (BC-ERR-03012, cited in the block's `sources`, not in its text). Separating feature: horizontal means slope zero, so the numerator; vertical means slope undefined, so the denominator. The archetype carries both fields in the snapshot, so the block is not tagged inferred. The `method` text carries no leading label.

## Solution path

- ex-1, BC-QA-03005, both bands, no calculator. Draw from `parameter_spec`: stretch 1, spread 1, opening left, h 1, v 2, so shift = 3 and the curve is (y - 2)^2 = (x - 1)^2 (x + 2), with dy/dx = 3(x - 1)(x + 1)/(2(y - 2)) supplied (a `common_givens` form). The spec's notes: the singular point (h, v) = (1, 2) makes both parts vanish, and the numerator's other root gives two horizontal tangent points. No published BC-QA-03005 item carries this draw.
- Steps follow `expected_solution_path`: numerator zero (new); solve for x (solve); the curve equation (new); x = -1 substituted (evaluate); solve for y (solve); x = 1 discarded (no value); the points (new). A fluent solver writes all of them except the discard reasoning, which is one clause beside x = 1. One example, so nothing is faded.

## Scoring

BC-QA-03005 lists no `point_types`, so no what_a_reader_scores entry and no point tag; the served text names no point beyond the error records' scoring_consequence. For the author: the Chief Reader reports record responses that found the condition on dy/dx and failed to connect it to the defining equation (cr-23:23, cr-24:18), which is the substitution step ex-1 writes.

## Traps

Three active errors meet the skills, in the bundle's order: BC-ERR-03012, BC-ERR-03013 (both linked to BC-MIS-03007, severity high), BC-ERR-05057 (linked BC-MIS at severity medium). Low band all three; mid band the first two. All on ex-1's draw. All three are `distinct`, so each carries `fix_prompt` true.

- err-BC-ERR-03012: 2(y - 2) = 0 set for a horizontal tangent, against 3(x - 1)(x + 1) = 0. No possible reason line: the linked descriptions describe the numerator only for parametric slopes (BC-MIS-09003).
- err-BC-ERR-03013: x = -1 and x = 1 reported with no y, against the two points. Possible reason, words from BC-MIS-03007.
- err-BC-ERR-05057: (1, 2) kept although the denominator is zero there. Possible reason, words from BC-MIS-05031.

## Representations

None as a separate block. The topic's Representations paragraph names the conversion of a condition on dy/dx to a geometric statement about the tangent (BC-REP-01 to BC-REP-08); ki-1's interactive carries it.

## Prerequisite bridge

- BC-PRQ-03007, from its `description_plain` and `failure_signature`.

## Time

BC-QA-03005 is `no_calculator`, one or two parts inside the implicit FRQ, so Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), this part a share of it [inferred: no BC-PT record; docs/lessons/unit-03/README.md, section 5]. The minutes go on the substitution into the curve and the check of the other part of the quotient; the conclusion is written in words.

## Checks

- chk-1, completion of ex-1, both bands: x = -1 and x = 1 are given, the student substitutes and keeps the points. Key {(-1, 0), (-1, 4)}.
- chk-2, isomorph, both bands, the vertical direction. Draw: stretch 2, spread 1, opening left, h 0, v 1; curve 2(y - 1)^2 = x^2 (x + 6). Key {(-6, 1)}; (0, 1) is discarded because the numerator is zero there too.
- chk-3, MCQ, low band. Draw: stretch 1, spread 1, opening left, h 0, v 0; curve y^2 = x^2 (x + 3). Key {(-2, -2), (-2, 2)}. Distractors: {(0, 0), (-3, 0)} (BC-ERR-03012), {-2, 0} as x values only (BC-ERR-03013), {(0, 0), (-2, -2), (-2, 2)} (BC-ERR-05057).

## Delivery

- orientation: text. Rule 5 for a statement of what a response shows; the figure-bearing representation is served once, on ki-1.
- ki-1: interactive. Rule 3 promoted: BC-SKL-03012 and BC-SKL-03013 carry BC-REP-02, and BC-QA-03005's `common_givens` ("a stated horizontal line or a point on the curve") and `difficulty_variables` ("whether more than one candidate value of the variable arises") name a quantity that varies, with the stem asking for a reading (docs/lessons/unit-03/README.md, section 6) [inferred; settled by the modality A/B].
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-03012, err-BC-ERR-03013, err-BC-ERR-05057: step_reveal. Rule 1.

## Band plan

- Low (full), in served order: prediction, orientation, the bridge, ki-1, st-1 with its contrast pair, ex-1, chk-1, the three error blocks, chk-2, chk-3. 521 words, 3.5 minutes (cap 900 and 6). There is no example 2, so nothing is faded.
- Mid (brief): prediction, orientation, the bridge, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-03012, err-BC-ERR-03013, chk-2. 449 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-03012, err-BC-ERR-03013, err-BC-ERR-05057, ex-1.

## Sources

- BC-CON-03005; BC-SKL-03012, BC-SKL-03013; BC-EK-FUN-3D1; ced:76, ced:110
- BC-QA-03005; cr-23:22, cr-23:23, cr-24:17, cr-24:18
- BC-ERR-03012, BC-ERR-03013, BC-ERR-05057; BC-MIS-03007, BC-MIS-05031, BC-MIS-09003
- BC-PRQ-03007
- research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation
- research/question-analysis/question-archetypes.md#BC-QA-03005 Horizontal or vertical tangent on an implicitly defined curve
- research/exam/exam-structure.md#Section and part layout
- [inferred] The share of the 15.0 minutes. Settled by a BC-PT mapping for the tangent parts.
- [inferred] ki-1 as an interactive. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-03005",
 "kind": "concept",
 "target_id": "BC-CON-03005",
 "unit": "03",
 "skills": ["BC-SKL-03012", "BC-SKL-03013"],
 "prediction": {
  "id": "pr-1",
  "stem": {"text": "Predict. With \\(dy/dx=\\frac{3(x-1)(x+1)}{2(y-2)}\\), which part is zero at a horizontal tangent?", "command_verb": "predict"},
  "format": "mcq",
  "options": [
   {"id": "A", "label": "The numerator, \\(3(x-1)(x+1)\\)", "is_key": true},
   {"id": "B", "label": "The denominator, \\(2(y-2)\\)", "is_key": false},
   {"id": "C", "label": "Both parts at once", "is_key": false}
  ],
  "resolution": "A horizontal tangent has slope 0, and a quotient is 0 where its numerator is 0 and its denominator is not.",
  "sources": ["BC-CON-03005", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation"]
 },
 "orientation": {
  "text": "A response sets the numerator of dy/dx to zero for a horizontal tangent, or the denominator for a vertical one, then keeps only candidates on the curve.",
  "sources": ["BC-CON-03005", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3D1",
   "depth": "core",
   "text": "On an implicit curve dy/dx is a quotient. The tangent is horizontal where the numerator is zero and the denominator is not, vertical where the reverse holds. A value is a candidate until the curve gives the other coordinate.",
   "notation": "denominator of dy/dx equals zero",
   "quote": null,
   "sources": ["BC-EK-FUN-3D1", "ced:76", "cr-23:22", "cr-24:17", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-03005",
   "cue": "A horizontal or vertical tangent point, from a curve and its dy/dx.",
   "method": "Set the numerator or the denominator of dy/dx equal to zero as the direction requires.",
   "rival": "The denominator set to zero for a horizontal tangent.",
   "separating_feature": "Horizontal: slope zero, numerator. Vertical: slope undefined, denominator.",
   "contrast": {
    "this": {"text": "For \\(x^2+xy+y^2=3\\), \\(dy/dx=-\\frac{2x+y}{x+2y}\\). Find each vertical tangent point.", "archetype_id": "BC-QA-03005"},
    "not_this": {"text": "For \\(x^2+xy+y^2=3\\), find the tangent slope at \\((1,1)\\).", "why_not": "A named point gives the slope by substitution."},
    "feature": "The words horizontal or vertical beside tangent."
   },
   "sources": ["BC-QA-03005", "BC-ERR-03012"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-03005",
   "bands": ["low", "mid"],
   "parameter_draw": {"stretch": 1, "spread": 1, "opening": "left", "h": 1, "v": 2},
   "problem": {"text": "For (y - 2)^2 = (x - 1)^2 (x + 2), dy/dx = 3(x - 1)(x + 1)/(2(y - 2)). Find each point where the tangent line is horizontal.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Horizontal: slope zero, numerator.", "why": "The denominator stays nonzero.", "expr": "3*(x - 1)*(x + 1) = 0", "relation": "new"},
    {"cue": "The condition fixes x.", "why": "Two candidates.", "expr": "FiniteSet(-1, 1)", "relation": "solve", "variable": "x"},
    {"cue": "A candidate must lie on the curve.", "why": "The curve gives y.", "expr": "(y - 2)**2 = (x - 1)**2*(x + 2)", "relation": "new"},
    {"cue": "Candidate x = -1.", "why": "(-2)^2 (1) = 4.", "expr": "(y - 2)**2 = 4", "relation": "evaluate", "subs": {"x": "-1"}},
    {"cue": "Solve for y.", "why": "y - 2 is 2 or -2.", "expr": "FiniteSet(0, 4)", "relation": "solve", "variable": "y"},
    {"cue": "Candidate x = 1 gives y = 2.", "why": "Denominator zero: discarded."},
    {"cue": "Asked for points.", "why": "On the curve, denominator nonzero.", "expr": "FiniteSet(Tuple(-1, 0), Tuple(-1, 4))", "relation": "new"}
   ],
   "answer": {"form": "symbolic", "expr": "FiniteSet(Tuple(-1, 0), Tuple(-1, 4))"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-03012",
   "observed_behavior": "The denominator of dy/dx is set to zero when a horizontal tangent is requested, or the numerator when a vertical tangent is requested.",
   "scoring_consequence": "The reported point is wrong and the reasoning point is not available.",
   "wrong_step": {"text": "Denominator set to zero.", "expr": "2*(y - 2) = 0"},
   "right_step": {"text": "Numerator set to zero.", "expr": "3*(x - 1)*(x + 1) = 0"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": ["BC-ERR-03012"]
  },
  {
   "error_id": "BC-ERR-03013",
   "observed_behavior": "A coordinate satisfying the condition on dy/dx is reported as a point of the curve without substituting it into the defining equation.",
   "scoring_consequence": "The Chief Reader reports record responses failing to connect dy/dx with the defining equation, which costs the point for the coordinates (cr-23:23, cr-24:18).",
   "wrong_step": {"text": "x = -1 and x = 1 reported.", "expr": "FiniteSet(-1, 1)"},
   "right_step": {"text": "(-1, 0) and (-1, 4).", "expr": "FiniteSet(Tuple(-1, 0), Tuple(-1, 4))"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-03007", "text": "a value satisfying it is reported without checking that a point with that value lies on the curve"},
   "sources": ["BC-ERR-03013", "BC-MIS-03007"]
  },
  {
   "error_id": "BC-ERR-05057",
   "observed_behavior": "The response sets the numerator of the derivative to zero and reports points where the denominator also vanishes.",
   "scoring_consequence": "The reported points may have no tangent at all, so the critical point list is wrong.",
   "wrong_step": {"text": "(1, 2) kept.", "expr": "FiniteSet(Tuple(1, 2), Tuple(-1, 0), Tuple(-1, 4))"},
   "right_step": {"text": "(1, 2) discarded.", "expr": "FiniteSet(Tuple(-1, 0), Tuple(-1, 4))"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-05031", "text": "looks only at the numerator of the derivative expression and never at the denominator"},
   "sources": ["BC-ERR-05057", "BC-MIS-05031"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-03007", "text": "Set a numerator or denominator to zero and solve."}
 ],
 "time": {"exam_part": "II-B", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 3, 4, 5, 7]}, "skipped_steps": {"ex-1": [6]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03005",
   "parameter_draw": {"stretch": 1, "spread": 1, "opening": "left", "h": 1, "v": 2},
   "completes": "ex-1",
   "stem": {"text": "On (y - 2)^2 = (x - 1)^2 (x + 2), the numerator gives x = -1 or 1. Find the points.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "FiniteSet(Tuple(-1, 0), Tuple(-1, 4))"},
   "steps": [
    {"text": "The curve.", "expr": "(y - 2)**2 = (x - 1)**2*(x + 2)", "relation": "new"},
    {"text": "x = -1.", "expr": "(y - 2)**2 = 4", "relation": "evaluate", "subs": {"x": "-1"}},
    {"text": "y = 0 or 4.", "expr": "FiniteSet(0, 4)", "relation": "solve", "variable": "y"},
    {"text": "x = 1 gives (1, 2), where the denominator is zero.", "expr": "FiniteSet(Tuple(-1, 0), Tuple(-1, 4))", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03012"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03005",
   "parameter_draw": {"stretch": 2, "spread": 1, "opening": "left", "h": 0, "v": 1},
   "stem": {"text": "For 2(y - 1)^2 = x^2 (x + 6), dy/dx = 3x(x + 4)/(4(y - 1)). Find vertical tangent points.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "FiniteSet(Tuple(-6, 1))"},
   "steps": [
    {"text": "Denominator zero.", "expr": "4*(y - 1) = 0", "relation": "new"},
    {"text": "y = 1.", "expr": "1", "relation": "solve", "variable": "y"},
    {"text": "The curve.", "expr": "2*(y - 1)**2 = x**2*(x + 6)", "relation": "new"},
    {"text": "y = 1.", "expr": "0 = x**2*(x + 6)", "relation": "evaluate", "subs": {"y": "1"}},
    {"text": "x = -6 or 0.", "expr": "FiniteSet(-6, 0)", "relation": "solve", "variable": "x"},
    {"text": "At (0, 1) the numerator is zero too, so only (-6, 1).", "expr": "FiniteSet(Tuple(-6, 1))", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03013"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-03005",
   "parameter_draw": {"stretch": 1, "spread": 1, "opening": "left", "h": 0, "v": 0},
   "stem": {"text": "For y^2 = x^2 (x + 3), dy/dx = 3x(x + 2)/(2y). Which gives every horizontal tangent point?", "command_verb": "identify"},
   "key": {"form": "symbolic", "expr": "FiniteSet(Tuple(-2, -2), Tuple(-2, 2))"},
   "steps": [
    {"text": "Numerator zero.", "expr": "3*x*(x + 2) = 0", "relation": "new"},
    {"text": "x = -2 or 0.", "expr": "FiniteSet(-2, 0)", "relation": "solve", "variable": "x"},
    {"text": "The curve.", "expr": "y**2 = x**2*(x + 3)", "relation": "new"},
    {"text": "x = -2.", "expr": "y**2 = 4", "relation": "evaluate", "subs": {"x": "-2"}},
    {"text": "y = -2 or 2.", "expr": "FiniteSet(-2, 2)", "relation": "solve", "variable": "y"},
    {"text": "x = 0 gives (0, 0), where the denominator is zero.", "expr": "FiniteSet(Tuple(-2, -2), Tuple(-2, 2))", "relation": "new"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "FiniteSet(Tuple(0, 0), Tuple(-3, 0))", "error_path": "BC-ERR-03012", "derivation": "denominator 2y set to zero: y = 0, then x = 0 or -3"},
    {"id": "B", "is_key": true, "expr": "FiniteSet(Tuple(-2, -2), Tuple(-2, 2))", "error_path": null},
    {"id": "C", "is_key": false, "expr": "FiniteSet(-2, 0)", "error_path": "BC-ERR-03013", "derivation": "the x values from the numerator, never put into the curve"},
    {"id": "D", "is_key": false, "expr": "FiniteSet(Tuple(0, 0), Tuple(-2, -2), Tuple(-2, 2))", "error_path": "BC-ERR-05057", "derivation": "(0, 0) kept although the denominator is zero there"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03012"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5 for a statement of what a response shows; the figure-bearing BC-REP-02 is served once, on ki-1", "sources": ["BC-SKL-03012"]},
  {"block": "ki-1", "mode": "interactive", "reason": "rule 3 promoted: BC-REP-02 on BC-SKL-03012 and BC-SKL-03013; BC-QA-03005 common_givens and difficulty_variables name a varying point and the stem asks for a reading", "sources": ["BC-SKL-03012", "BC-SKL-03013", "BC-QA-03005"],
   "spec": {"kind": "implicit_curve", "representations": ["BC-REP-02", "BC-REP-01"], "curve": "(y - 2)^2 = (x - 1)^2 (x + 2)", "window": {"x": [-3, 3], "y": [-2, 6]},
    "controls": [{"type": "draggable_point", "constrained_to": "curve", "start": [-2, 2]}],
    "drawn": ["the tangent line at the point", "dy/dx at the point shown as numerator over denominator"],
    "labels": [{"text": "numerator 3(x - 1)(x + 1)", "placement": "inside"}, {"text": "denominator 2(y - 2)", "placement": "inside"}, {"text": "(1, 2): both zero", "placement": "inside"}],
    "question": "At which points of the curve is the tangent horizontal, and at which is it vertical?"},
   "fallback": "a static figure of the curve with (-1, 0) and (-1, 4) marked horizontal, (-2, 2) marked vertical and (1, 2) marked both zero, each label inside the figure",
   "keyboard": "Tab focuses the point; left and right arrow keys move it along the curve; Enter reads out dy/dx at the point"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03012", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03013", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05057", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-03012", "err-BC-ERR-03013", "err-BC-ERR-05057", "ex-1"],
 "read_minutes": {"full": 3.5, "brief": 3.0},
 "word_count": {"full": 521, "brief": 449},
 "research_lines": [
  {"file": "research/units/unit-03-differentiation-composite-implicit-inverse.md", "line": "a candidate satisfying only the condition on dy/dx need not correspond to a point of the curve"}
 ],
 "inferred": [
  {"claim": "The tangent part takes a share of the 15.0 minute Section II question that no record fixes.", "settles": "A BC-PT mapping for the tangent parts described in cr-23:22 and cr-24:17."},
  {"claim": "ki-1 is served as an interactive draggable point rather than a static figure.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-03005", "BC-SKL-03012", "BC-SKL-03013", "BC-EK-FUN-3D1", "ced:76", "ced:110", "BC-QA-03005", "cr-23:22", "cr-23:23", "cr-24:17", "cr-24:18", "BC-ERR-03012", "BC-ERR-03013", "BC-ERR-05057", "BC-MIS-03007", "BC-MIS-05031", "BC-MIS-09003", "BC-PRQ-03007", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation", "research/question-analysis/question-archetypes.md#BC-QA-03005 Horizontal or vertical tangent on an implicitly defined curve", "research/exam/exam-structure.md#Section and part layout"]
}
```
