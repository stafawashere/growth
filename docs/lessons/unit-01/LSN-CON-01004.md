---
title: LSN-CON-01004 One sided limits and two sided existence
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01004, one sided limits and the rule that a two sided limit exists only when they agree, built from authoring_bundle("BC-CON-01004") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01004 One sided limits and two sided existence

Concept BC-CON-01004 (skills BC-SKL-01010, BC-SKL-01016, BC-SKL-01023), topics 1.3 to 1.5 of Unit 1, loaded by BC-QA-01006 (continuity-at-a-point), BC-QA-01001 (limit-from-graph) and BC-QA-01002 (limit-from-table). Its hard parent is BC-CON-01006, and BC-CON-01005 and BC-CON-01013 hang from it (docs/lessons/unit-01/README.md, section 1).

## Orientation

Served text, from BC-CON-01004 `description_plain` and the Assessment behaviour paragraphs of topics 1.3 and 1.5, which ask for one sided limits at named inputs and combine limit work with a piecewise boundary so that one sided limits must be matched first (research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs; research/units/unit-01-limits-continuity.md#1.5 Determining Limits Using Algebraic Properties of Limits). No count, no frequency.

## Key ideas

The three skills map four BC-EK: BC-EK-LIM-1C1 (BC-SKL-01010, 01016; ced:40), BC-EK-LIM-1C2 (BC-SKL-01010; ced:40), BC-EK-LIM-1C5 (BC-SKL-01016; ced:41) and BC-EK-LIM-1D1 (BC-SKL-01023; ced:42). One core block serves both bands; the rest are extended.

- ki-1 (core, BC-EK-LIM-1C1). A limit can be taken from one side; the two sided limit exists exactly when both one sided limits exist and agree (topic 1.3 One sided limits paragraph). Notation: left hand limit; right hand limit.
- ki-2 (extended, BC-EK-LIM-1D1). One sided limits come from a rule or a graph; on a piecewise rule each side takes the branch whose condition holds there. Anchor quote from ced:42.
- ki-3 (extended, BC-EK-LIM-1C2). On a graph each side is read as the height approached from that side. Anchor quote from ced:40.
- ki-4 (extended, BC-EK-LIM-1C5). In a table, the rows on one side support that side's estimate only (topic 1.4 Numerical estimation paragraph). Anchor quote from ced:41.

## Recognition

- BC-QA-01006 (research/question-analysis/question-archetypes.md#BC-QA-01006 Continuity at a point tested against the three conditions): `typical_wording` "Determine whether the given function is continuous at the named input. Justify your answer"; `asked_to_produce` includes the one sided limits at the input. `common_givens` is empty, so the cue rests on the wording. The signal is a piecewise rule whose conditions split at a named boundary.
- BC-QA-01001 (research/question-analysis/question-archetypes.md#BC-QA-01001 Limit estimated from a graph including one sided values): a graph with breaks, one sided and two sided limits at named inputs. The signal is a superscript sign on the arrow, or two different heights at one input.
- BC-QA-01002 (research/question-analysis/question-archetypes.md#BC-QA-01002 Limit estimated from a table of values): rows approaching the target from both sides, sometimes one side only.

What says "not this concept": a stem asking whether f is continuous also needs the function value and its comparison with the limit (BC-CON-01013); a stem with outputs growing without bound or oscillating asks which failure mode applies (BC-CON-01005). Both from the unit README's neighbour table.

## Method choice

Three strategy blocks, low band all, mid band st-1.

- st-1, BC-QA-01006, `evidence_tag` inferred (no `common_givens`). Cue from `typical_wording`: a piecewise rule and a named boundary. Method, `expected_solution_path[0]`: evaluate the function at the named input, then each one sided limit from its own branch. Rival: the branch that does not apply on that side (BC-ERR-01017). Separating feature: each side takes the branch whose condition holds there.
- st-2, BC-QA-01001. Method: locate the input, then read each side. Rival: one side reported as the two sided limit (BC-ERR-01002). Separating feature: a two sided answer needs both sides read and compared.
- st-3, BC-QA-01002. Method: identify the rows approaching from the left. Rival: one side's rows reported as the limit (BC-ERR-01002). Separating feature: a one sided estimate uses only that side's rows.

## Solution path

- ex-1, BC-QA-01006, both bands, no calculator. Draw: boundary 1, left_limit 3, right_limit 4, point_value 4, left_slope 2, right_slope -1, closed_side right, break_kind jump, so \(f(x)=2x+1\) for \(x<1\) and \(f(x)=5-x\) for \(x\ge1\). The stem asks for the one sided limits and the existence of the two sided limit, the part of BC-QA-01006's `asked_to_produce` this concept owns; the continuity conclusion belongs to BC-CON-01013. Steps: left branch (valued, new), its limit from the left (valued), right branch (valued, new), its limit from the right (valued), the comparison (no value). Answer: a statement, the limit does not exist.

A fluent solver writes the two one sided values and the comparison; the branch choice is read from the conditions (docs/lessons/unit-01/README.md, section 5).

## Scoring

None. BC-QA-01006, BC-QA-01001 and BC-QA-01002 list no `point_types`, so the lesson carries no scoring entry and says nothing about points (plan 15, R14).

## Traps

Two active errors, in the bundle's order, both served in both bands.

- err-BC-ERR-01002 (BC-MIS-01002, BC-MIS-01001). Wrong step on ex-1's draw: the left value 3 reported as the limit. Right step: the sides give 3 and 4, so no limit (expr `DNE`). Distinct. Possible reason from BC-MIS-01002.
- err-BC-ERR-01017 (BC-MIS-01009, BC-MIS-01019). Wrong step: the right hand limit taken from \(2x+1\), giving 3. Right step: from \(5-x\), giving 4. Distinct. No possible reason: neither linked description names branch choice.

## Representations

None. The topic Representations paragraphs name graphs, tables and rules; each is carried by a key idea's delivery (interactive, figure, table).

## Prerequisite bridge

Two bridges, BC-PRQ-01003 (supporting parent of BC-SKL-01023) and BC-PRQ-06005 (supporting parent of BC-SKL-01010 and 01016), gated by state.

## Time

BC-QA-01006 is `no_calculator`, one part of a free response question or a single MCQ: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). The minutes go to the two one sided values; the branch choice is read, not written.

## Checks

- chk-1, completion of ex-1, both bands: the one sided limits 3 and 4 are given, the student states the two sided result. Key: the limit does not exist, ex-1's answer.
- chk-2, isomorph on BC-QA-01006, both bands: boundary 2, \(f(x)=3x-7\) for \(x\le2\) and \(-2x+7\) for \(x>2\); the right hand limit. Key 3.

Two checks: the two active errors give two wrong values on one draw at most (one side reported, the wrong branch), short of three distinct distractors. Listed under inferred.

## Delivery

- orientation: figure. Rule 3, BC-REP-02 on BC-SKL-01010 and 01023; the unit README picks figure. ex-1's graph: two rays, an open circle at \((1,3)\), a filled point at \((1,4)\).
- ki-1: interactive. Rule 3 promoted: BC-QA-01001 and BC-QA-01006 `difficulty_variables` vary "whether the one sided limits agree" and the stem asks for that reading. One slider moves a point along ex-1's graph toward \(x=1\) from either side; the question asks whether the two heights agree.
- ki-2: figure. Rule 3, BC-REP-02 on BC-SKL-01023: the piecewise graph with each branch labelled by its condition.
- ki-3: figure. Rule 3, BC-REP-02 on BC-SKL-01010: left and right arrows toward the break.
- ki-4: table. Rule 4, BC-REP-03 on BC-SKL-01016: rows from the right only.
- ex-1, err blocks: step_reveal, rule 1.

Every non-text choice is [inferred], settled by the modality A/B.

## Band plan

- Low (full): orientation, ki-1 to ki-4, st-1 to st-3, ex-1, both error blocks, chk-1, chk-2, bridges when gated.
- Mid (brief): orientation, ki-1, st-1, ex-1, both error blocks, chk-1, chk-2, bridges when gated.
- Totals: full 610 words, 4.1 minutes (cap 900 and 6); brief 440 words, 2.95 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-01002, err-BC-ERR-01017, ex-1.

## Sources

- BC-CON-01004; BC-SKL-01010, BC-SKL-01016, BC-SKL-01023; BC-EK-LIM-1C1, BC-EK-LIM-1C2, BC-EK-LIM-1C5, BC-EK-LIM-1D1; ced:40, ced:41, ced:42
- BC-QA-01006, BC-QA-01001, BC-QA-01002
- BC-ERR-01002, BC-ERR-01017; BC-MIS-01001, BC-MIS-01002, BC-MIS-01009, BC-MIS-01019
- BC-PRQ-01003, BC-PRQ-06005
- research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs
- research/units/unit-01-limits-continuity.md#1.4 Estimating Limit Values from Tables
- research/units/unit-01-limits-continuity.md#1.5 Determining Limits Using Algebraic Properties of Limits
- research/question-analysis/question-archetypes.md#BC-QA-01006 Continuity at a point tested against the three conditions
- research/question-analysis/question-archetypes.md#BC-QA-01001 Limit estimated from a graph including one sided values
- research/question-analysis/question-archetypes.md#BC-QA-01002 Limit estimated from a table of values
- research/exam/exam-structure.md#Section and part layout
- [inferred] st-1 rests on typical_wording because BC-QA-01006 has no common_givens. Settled by a library pass filling common_givens.
- [inferred] Two checks. Settled by a third active error on the concept's skills.
- [inferred] Interactive, figure and table modes. Settled by the modality A/B.
- Library gap: BC-QA-01006 `common_givens` is empty.

## Machine record

```json
{
 "id": "LSN-CON-01004",
 "kind": "concept",
 "target_id": "BC-CON-01004",
 "unit": "01",
 "skills": ["BC-SKL-01010", "BC-SKL-01016", "BC-SKL-01023"],
 "orientation": {
  "text": "A response finds the limit from the left and the limit from the right separately, then reports a two sided limit only when the two agree. Stems give a piecewise rule, a graph or a table, often at a boundary where the rule changes.",
  "sources": ["BC-CON-01004", "research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs", "research/units/unit-01-limits-continuity.md#1.5 Determining Limits Using Algebraic Properties of Limits"]
 },
 "key_ideas": [
  {"id": "ki-1", "ek_id": "BC-EK-LIM-1C1", "depth": "core", "text": "A limit can be taken from one side only (BC-EK-LIM-1C1, ced:40). The two sided limit exists exactly when both one sided limits exist and agree; different values mean it does not exist.", "notation": "left hand limit; right hand limit", "quote": null, "sources": ["BC-EK-LIM-1C1", "ced:40", "research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs"]},
  {"id": "ki-2", "ek_id": "BC-EK-LIM-1D1", "depth": "extended", "text": "On a piecewise rule, each side of a boundary takes the branch whose condition holds on that side (BC-EK-LIM-1D1, ced:42).", "notation": "", "quote": {"text": "One sided limits can be determined analytically or graphically.", "source": "ced:42"}, "sources": ["BC-EK-LIM-1D1", "ced:42"]},
  {"id": "ki-3", "ek_id": "BC-EK-LIM-1C2", "depth": "extended", "text": "On a graph, each side is read as the height approached from that side (BC-EK-LIM-1C2, ced:40).", "notation": "", "quote": {"text": "Graphical information about a function can be used to estimate limits.", "source": "ced:40"}, "sources": ["BC-EK-LIM-1C2", "ced:40"]},
  {"id": "ki-4", "ek_id": "BC-EK-LIM-1C5", "depth": "extended", "text": "In a table, the rows on one side support that side's estimate only (BC-EK-LIM-1C5, ced:41).", "notation": "", "quote": {"text": "Numerical information can be used to estimate limits.", "source": "ced:41"}, "sources": ["BC-EK-LIM-1C5", "ced:41", "research/units/unit-01-limits-continuity.md#1.4 Estimating Limit Values from Tables"]}
 ],
 "strategy": [
  {"id": "st-1", "archetype_id": "BC-QA-01006", "cue": "A piecewise rule with a named boundary, and a question about the limit or continuity there.", "method": "First line: f at the boundary, then each one sided limit from its own branch.", "rival": "Evaluating the branch that does not apply on that side (BC-ERR-01017).", "separating_feature": "Each side takes the branch whose condition holds there.", "sources": ["BC-QA-01006"], "evidence_tag": "inferred"},
  {"id": "st-2", "archetype_id": "BC-QA-01001", "cue": "A graph with a break, and one sided or two sided limits asked at a named input.", "method": "First line: locate the input, then read the left and right heights.", "rival": "One side reported as the two sided limit (BC-ERR-01002).", "separating_feature": "A two sided answer needs both sides read and compared.", "sources": ["BC-QA-01001"], "evidence_tag": "verified"},
  {"id": "st-3", "archetype_id": "BC-QA-01002", "cue": "A table approaching the target from both sides, and a one sided or two sided estimate asked.", "method": "First line: identify the rows approaching from the left.", "rival": "One side's rows reported as the limit (BC-ERR-01002).", "separating_feature": "A one sided estimate uses only that side's rows.", "sources": ["BC-QA-01002"], "evidence_tag": "verified"}
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01006",
   "bands": ["low", "mid"],
   "parameter_draw": {"boundary": 1, "left_limit": 3, "right_limit": 4, "point_value": 4, "left_slope": 2, "right_slope": -1, "closed_side": "right", "break_kind": "jump"},
   "problem": {"text": "Let f(x) = 2x + 1 for x < 1 and f(x) = 5 - x for x ≥ 1. Find both one sided limits of f at x = 1. Does the limit at x = 1 exist?", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Left of 1 the condition x < 1 holds.", "why": "So the left side uses 2x + 1.", "expr": "2*x + 1", "relation": "new"},
    {"cue": "Approach 1 from the left.", "why": "2x + 1 heads to 3.", "expr": "3", "relation": "limit", "variable": "x", "point": "1", "dir": "-"},
    {"cue": "Right of 1 the condition x ≥ 1 holds.", "why": "So the right side uses 5 - x.", "expr": "5 - x", "relation": "new"},
    {"cue": "Approach 1 from the right.", "why": "5 - x heads to 4.", "expr": "4", "relation": "limit", "variable": "x", "point": "1", "dir": "+"},
    {"cue": "The stem asks about existence: compare.", "why": "3 and 4 differ, so the limit does not exist."}
   ],
   "answer": {"form": "statement", "expr": "DNE", "text": "The left hand limit is 3, the right hand limit is 4, so the limit of f at x = 1 does not exist."}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {"error_id": "BC-ERR-01002", "observed_behavior": "The response reports the value approached from one side as the limit although the two sides differ.", "scoring_consequence": "The value point is lost because the correct response is that the limit does not exist.", "wrong_step": {"text": "The left value 3 reported as the limit.", "expr": "3"}, "right_step": {"text": "Sides 3 and 4 differ: no limit.", "expr": "DNE"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-01002", "text": "a single one sided approach as sufficient"}, "sources": ["BC-ERR-01002", "BC-MIS-01002"]},
  {"error_id": "BC-ERR-01017", "observed_behavior": "The response substitutes the boundary input into the branch that does not apply on that side.", "scoring_consequence": "The one sided limit is wrong and every point depending on it is lost.", "wrong_step": {"text": "Right hand limit from 2x + 1: 3.", "expr": "2*1 + 1"}, "right_step": {"text": "From 5 - x: 4.", "expr": "5 - 1"}, "relation": "distinct", "possible_reason": null, "sources": ["BC-ERR-01017"]}
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-01003", "text": "A piecewise rule is read by choosing the branch whose condition holds for the input. The failure: the wrong branch at a boundary."},
  {"prq_id": "BC-PRQ-06005", "text": "Reading f at a stated input from a graph or table. The failure: a value read at the wrong input."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 4, 5]}, "skipped_steps": {"ex-1": [1, 3]}},
 "checks": [
  {"id": "chk-1", "check_kind": "completion", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-01006",
   "parameter_draw": {"boundary": 1, "left_limit": 3, "right_limit": 4, "point_value": 4, "left_slope": 2, "right_slope": -1, "closed_side": "right", "break_kind": "jump"},
   "completes": "ex-1",
   "stem": {"text": "For ex-1's f, the one sided limits at x = 1 are 3 and 4. State the limit of f at x = 1.", "command_verb": "state"},
   "key": {"form": "statement", "expr": "DNE", "text": "The limit does not exist."},
   "steps": [{"text": "Left 3.", "expr": "3", "relation": "new"}, {"text": "Right 4, which differs.", "expr": "4", "relation": "new"}],
   "calculator_status": "no_calculator", "skills": ["BC-SKL-01023"]},
  {"id": "chk-2", "check_kind": "isomorph", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-01006",
   "parameter_draw": {"boundary": 2, "left_limit": -1, "right_limit": 3, "point_value": -1, "left_slope": 3, "right_slope": -2, "closed_side": "left", "break_kind": "jump"},
   "stem": {"text": "Let f(x) = 3x - 7 for x ≤ 2 and f(x) = -2x + 7 for x > 2. Find the right hand limit of f at x = 2.", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "3"},
   "steps": [{"text": "Right of 2 the branch is -2x + 7.", "expr": "-2*x + 7", "relation": "new"}, {"text": "It heads to 3.", "expr": "3", "relation": "limit", "variable": "x", "point": "2", "dir": "+"}],
   "calculator_status": "no_calculator", "skills": ["BC-SKL-01023"]}
 ],
 "delivery": [
  {"block": "orientation", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-01010 and BC-SKL-01023; unit README delivery map", "sources": ["BC-SKL-01010", "BC-SKL-01023"],
   "spec": {"kind": "graph", "window": {"x": [-1, 3], "y": [-1, 6]}, "curves": [{"expr": "2*x + 1", "domain": [-1, 1]}, {"expr": "5 - x", "domain": [1, 3]}], "points": [{"at": [1, 3], "style": "open"}, {"at": [1, 4], "style": "filled"}], "labels": [{"text": "from the left: 3", "placement": "inside"}, {"text": "from the right: 4", "placement": "inside"}]},
   "fallback": "the same graph static with both labels", "keyboard": "no control; the figure description is reached with Tab"},
  {"block": "ki-1", "mode": "interactive", "reason": "rule 3 promoted: BC-QA-01001 and BC-QA-01006 difficulty_variables vary whether the one sided limits agree, and the stem asks for that reading", "sources": ["BC-SKL-01010", "BC-QA-01001", "BC-QA-01006"],
   "spec": {"kind": "graph", "curves": [{"expr": "2*x + 1", "domain": [-1, 1]}, {"expr": "5 - x", "domain": [1, 3]}], "points": [{"at": [1, 3], "style": "open"}, {"at": [1, 4], "style": "filled"}], "controls": [{"type": "slider", "name": "x", "domain": [-1, 3], "step": 0.05, "exclude": [1], "readout": "f(x)"}], "question": "As x reaches 1 from each side, do the two heights agree?", "labels": [{"text": "moving point (x, f(x))", "placement": "inside"}, {"text": "x = 1", "placement": "inside"}]},
   "fallback": "two static frames, the point at x = 0.95 (height 2.9) and at x = 1.05 (height 3.95), with the question below",
   "keyboard": "Left and Right arrow keys move the point by 0.05; Home and End jump to the window edges"},
  {"block": "ki-2", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-01023", "sources": ["BC-SKL-01023"],
   "spec": {"kind": "graph", "curves": [{"expr": "2*x + 1", "domain": [-1, 1]}, {"expr": "5 - x", "domain": [1, 3]}], "labels": [{"text": "x < 1: 2x + 1", "placement": "inside"}, {"text": "x ≥ 1: 5 - x", "placement": "inside"}]},
   "fallback": "the static graph with both condition labels", "keyboard": "no control"},
  {"block": "ki-3", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-01010", "sources": ["BC-SKL-01010"],
   "spec": {"kind": "graph", "curves": [{"expr": "2*x + 1", "domain": [-1, 1]}, {"expr": "5 - x", "domain": [1, 3]}], "arrows": [{"along": "left branch", "toward": [1, 3]}, {"along": "right branch", "toward": [1, 4]}], "labels": [{"text": "left height 3", "placement": "inside"}, {"text": "right height 4", "placement": "inside"}]},
   "fallback": "the static graph with both arrows and labels", "keyboard": "no control"},
  {"block": "ki-4", "mode": "table", "reason": "rule 4: BC-REP-03 on BC-SKL-01016", "sources": ["BC-SKL-01016"],
   "spec": {"kind": "table", "columns": ["x", "f(x)"], "rows": [["1.1", "3.9"], ["1.01", "3.99"], ["1.001", "3.999"]], "labels": [{"text": "rows from the right only: right hand estimate 4", "placement": "inside"}]},
   "fallback": "the three rows as static text", "keyboard": "no control; cells reached in reading order with Tab"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01002", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01017", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-01002", "err-BC-ERR-01017", "ex-1"],
 "read_minutes": {"full": 4.1, "brief": 2.95},
 "word_count": {"full": 610, "brief": 440},
 "research_lines": [
  {"file": "research/units/unit-01-limits-continuity.md", "line": "the two sided limit exists exactly when both one sided limits exist and agree"}
 ],
 "inferred": [
  {"claim": "st-1 rests on typical_wording because BC-QA-01006 has no common_givens.", "settles": "A library pass filling common_givens on BC-QA-01006."},
  {"claim": "Two checks: the two active errors give at most two distinct wrong values on one draw, short of three distractors.", "settles": "A third active error on BC-SKL-01010, 01016 or 01023."},
  {"claim": "Interactive, figure and table modes serve these blocks better than text; one control per screen.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-01004", "BC-SKL-01010", "BC-SKL-01016", "BC-SKL-01023", "BC-EK-LIM-1C1", "BC-EK-LIM-1C2", "BC-EK-LIM-1C5", "BC-EK-LIM-1D1", "ced:40", "ced:41", "ced:42", "BC-QA-01006", "BC-QA-01001", "BC-QA-01002", "BC-ERR-01002", "BC-ERR-01017", "BC-MIS-01002", "BC-PRQ-01003", "BC-PRQ-06005", "research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs", "research/units/unit-01-limits-continuity.md#1.5 Determining Limits Using Algebraic Properties of Limits", "research/exam/exam-structure.md#Section and part layout"]
}
```
