---
title: LSN-CON-01015 Removing a discontinuity and matching a piecewise function
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01015, removing a discontinuity and matching a piecewise function, built from authoring_bundle("BC-CON-01015") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01015 Removing a discontinuity and matching a piecewise function

Concept BC-CON-01015 (skills BC-SKL-01050, BC-SKL-01051, BC-SKL-01052, BC-SKL-01053), topic 1.13 of Unit 1 (BC-TOP-0113), loaded by one archetype, BC-QA-01008 (primary). The archetype carries no `point_types`, so the lesson says nothing about points.

## Orientation

Served text, from BC-CON-01015 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-01-limits-continuity.md#1.13 Removing Discontinuities): a response shows one matching equation per boundary, built from the branch on each side and the value at the boundary, then solves for the constants; a removable break is repaired by setting the value equal to the limit.

## Key ideas

Two BC-EK map to the skills, both on ced:50: BC-EK-LIM-2C1 (BC-SKL-01050, 01053) and BC-EK-LIM-2C2 (BC-SKL-01051, 01052).

- ki-1 (extended, low band), BC-EK-LIM-2C1. Paraphrase of the topic's Removing a discontinuity and When removal is impossible paragraphs: when the limit exists at a break, defining the value as the limit repairs it; a jump or an infinite break has no limit and cannot be repaired. Anchor quote (19 words) from ced:50.
- ki-2 (core, both bands), BC-EK-LIM-2C2. Paraphrase of the Piecewise matching paragraph: at a boundary the left expression, the right expression and the function value must all agree, so each boundary gives exactly one equation. Anchor quote (11 words) from ced:50. The concept's `notation` field is empty, so the notation line is empty.

## Recognition

- BC-QA-01008 (family parameter-for-continuity, MCQ or one FRQ part, no calculator; research/question-analysis/question-archetypes.md#BC-QA-01008 Parameter solved so that a piecewise function is continuous): `typical_wording` "Find the value or values of the constants for which the given piecewise function is continuous"; `common_givens` a piecewise rule with one or two unknown constants; `asked_to_produce` a matching equation at each boundary and the values of the constants. The signal is a letter other than \(x\) inside a branch together with "continuous". No official example is recorded.

What says "not this concept": a piecewise rule with no unknown and "is f continuous at" (BC-CON-01013); a single rational expression with "vertical asymptote" (BC-CON-01016); a break with "classify" (BC-QA-01007).

The count of boundaries is the count of equations (`invariant_structure`), so two unknowns need two boundaries; a stem with two unknowns and one boundary is a different question (`common_distractors`: "solving one equation for two unknowns").

## Method choice

- st-1, BC-QA-01008, both bands. Cue, from `asked_to_produce` and `common_givens`: a piecewise rule with unknown constants, and the stem asks for their values. Method, `expected_solution_path[0]`: evaluate the one sided limit from each branch at the boundary. First written line: the left limit and the right limit at the first boundary, each from the branch that owns that side. Rival, `wrong_approaches`: matching the two one sided limits and ignoring the defined value (BC-ERR-01015). Separating feature: the branch whose condition carries the equals sign supplies the value, and the value enters the equation.

## Solution path

- ex-1, BC-QA-01008, both bands, no calculator. Draw: left_end 1, right_end 3, curvature 1, lift 3, check values, giving \(f(x)=\frac{x^2-1}{x-1}\) for \(x<1\), \(kx+m\) for \(1\le x\le3\), \(x^2+3\) for \(x>3\). Every constraint in `parameter_spec` holds: \((9+3-2)\) is divisible by 2, \(12\ne4\), \(4\ne2\). Steps: the left branch (valued, new), its limit at 1 (valued, limit from the left), the matching equation at 1 (valued, new), the matching equation at 3 (valued, new), the difference of the two (valued, new), \(k\) (valued, solve), the pair (valued, new). A fluent solver writes the two matching equations and the pair and holds the limit of the left branch in the head.

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

None. BC-QA-01008 lists no `point_types`; its `scoring_pattern` names a point per matching equation and one for the solution, but no BC-PT record carries them, so under plan 15 R14 the lesson carries no scoring checklist and names no points.

## Traps

Three active errors meet the concept's skills, in the bundle's order (all linked BC-MIS at severity high, so by id). Low band all three, mid band the first two.

- err-BC-ERR-01003 (BC-MIS-01001, BC-MIS-01009). Wrong step on ex-1's draw: the left branch is undefined at 1, so the left limit is declared nonexistent (\(\frac{0}{0}\) taken as the answer). Right step: the factor divides out and the left limit is 2. Distinct. Possible reason, words from BC-MIS-01001: a missing or displaced function value is read as a missing or displaced limit.
- err-BC-ERR-01015 (BC-MIS-01009, BC-MIS-01001). Wrong step, on ex-1's rule with the value at 1 set on its own line as \(f(1)=4\): the left and right limits both equal 2, so continuity at 1 is claimed. Right step: the value 4 is compared with the limit 2, and they differ, so \(f\) is not continuous at 1. Distinct: on ex-1's own draw the middle branch owns \(x=1\) and the two lines coincide, so the block sets the value apart to show the lost comparison. Possible reason, words from BC-MIS-01009: most often that the function is defined there or that the one sided limits agree.
- err-BC-ERR-01017 (BC-MIS-01009, BC-MIS-01019). Wrong step: the right branch \(x^2+3\) evaluated at 1, giving \(k+m=4\). Right step: \(k+m=2\). Distinct. Possible reason null: neither linked description names branch selection.

## Representations

None as a separate block. The topic's Representations paragraph names BC-REP-01 and BC-REP-02 and one conversion, a rule with an unknown constant to an equation in that constant; the graphical side is carried by the orientation figure and the ki-2 interactive under Delivery.

## Prerequisite bridge

Two BC-PRQ parents reach the skills through `supporting` edges: BC-PRQ-01001 (factoring and dividing out a common factor, to BC-SKL-01050) and BC-PRQ-01003 (reading a piecewise rule, to BC-SKL-01051, 01052, 01053). One bridge each, gated by state.

## Time

BC-QA-01008 is `no_calculator` and "Typically a single multiple choice item or one part of a larger question"; the MCQ shape sets the part, Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout; plan 15, Fluency). A fluent solver writes the two matching equations and the solved pair; the left limit, the elimination and the branch choice are held in the head. Most of the budget goes to the two boundary evaluations.

## Checks

- chk-1, completion of ex-1, both bands: the two matching equations are given, the student solves. Key \(k=5\), \(m=-3\), ex-1's answer.
- chk-2, isomorph on BC-QA-01008, both bands: left_end \(-1\), right_end 2, curvature 1, lift 0: \(\frac{x^2-1}{x+1}\) for \(x<-1\), \(kx+m\) on \([-1,2]\), \(x^2\) for \(x>2\). Key \(k=2\), \(m=0\).
- chk-3, MCQ on BC-QA-01008, low band: left_end 2, right_end 4, curvature 1, lift \(-2\): \(\frac{x^2-4}{x-2}\) for \(x<2\), \(kx+m\) on \([2,4]\), \(x^2-2\) for \(x>4\); find \(k\). Key 5. Distractors: 6 (BC-ERR-01017, \(x^2-2\) used at 2), 1 (BC-ERR-01017, \(x+2\) used at 4), 2 (BC-ERR-01017 at both boundaries). BC-ERR-01003 and BC-ERR-01015 give no distinct value on a draw of this `parameter_spec`, because the middle branch always owns both boundaries [inferred].

No draw equals a published BC-QA-01008 `parameter_draw` (content/items_gen_unit01, content/items_p1_agent).

## Delivery

- orientation: figure. Rule 3, BC-REP-02 on BC-SKL-01050 and 01053; the three branches of ex-1 drawn at \(k=5\), \(m=-3\), joined at \((1,2)\) and \((3,12)\).
- ki-1: figure. Rule 3, BC-REP-02 on BC-SKL-01050; the graph of \(\frac{x^2-1}{x-1}\) with an open circle at \((1,2)\) and the repaired value placed in it.
- ki-2: interactive. Rule 3 promoted, because BC-QA-01008 `common_givens` name "a piecewise rule with one or two unknown constants" and the stem asks for the value that joins the pieces (docs/lessons/unit-01/README.md, section 6). One slider on \(k\), with \(m=2-k\) fixed by the left match, so the middle segment pivots about \((1,2)\); the reading asked is the \(k\) at which its right end meets \((3,12)\).
- ex-1, err-BC-ERR-01003, err-BC-ERR-01015, err-BC-ERR-01017: step_reveal. Rule 1.

Every non-text choice is [inferred], settled by the modality A/B in the build plan.

## Band plan

- Low (full): orientation, ki-1, ki-2, st-1, ex-1, the three error blocks, chk-1, chk-2, chk-3, the two bridges. 551 words, 3.7 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-2, st-1, ex-1, err-01003, err-01015, chk-1, chk-2, the two bridges. 441 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-2, err-BC-ERR-01003, err-BC-ERR-01015, err-BC-ERR-01017, ex-1.

## Sources

- BC-CON-01015; BC-SKL-01050, BC-SKL-01051, BC-SKL-01052, BC-SKL-01053; BC-EK-LIM-2C1, BC-EK-LIM-2C2; ced:50
- BC-QA-01008
- BC-ERR-01003, BC-ERR-01015, BC-ERR-01017; BC-MIS-01001, BC-MIS-01009, BC-MIS-01019
- BC-PRQ-01001, BC-PRQ-01003
- research/units/unit-01-limits-continuity.md#1.13 Removing Discontinuities
- research/question-analysis/question-archetypes.md#BC-QA-01008 Parameter solved so that a piecewise function is continuous
- research/exam/exam-structure.md#Section and part layout
- [inferred] All three MCQ distractors carry BC-ERR-01017, because the other two errors give no distinct value on this `parameter_spec`. Settled by a spec variant with a separately defined boundary value.
- [inferred] Non-text delivery modes. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-01015",
 "kind": "concept",
 "target_id": "BC-CON-01015",
 "unit": "01",
 "skills": ["BC-SKL-01050", "BC-SKL-01051", "BC-SKL-01052", "BC-SKL-01053"],
 "orientation": {
  "text": "A response writes one matching equation per boundary, from both branches and the boundary value, then solves for the constants. A removable break is repaired by setting the value equal to the limit.",
  "sources": ["BC-CON-01015", "research/units/unit-01-limits-continuity.md#1.13 Removing Discontinuities"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-2C1",
   "depth": "extended",
   "text": "When the limit exists at a break, defining or redefining the value there as the limit removes the break (BC-EK-LIM-2C1, ced:50). A jump or an infinite break has no limit, so no value repairs it.",
   "notation": "",
   "quote": {"text": "it is possible to remove the discontinuity by defining or redefining the value of the function at that point", "source": "ced:50"},
   "sources": ["BC-EK-LIM-2C1", "ced:50", "research/units/unit-01-limits-continuity.md#1.13 Removing Discontinuities"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-2C2",
   "depth": "core",
   "text": "At a boundary of a piecewise rule, the left expression, the right expression and the function value must agree (BC-EK-LIM-2C2, ced:50). All three enter, so each boundary gives one equation, and two unknowns need two boundaries.",
   "notation": "",
   "quote": {"text": "as well as the value of the function at the boundary.", "source": "ced:50"},
   "sources": ["BC-EK-LIM-2C2", "ced:50", "research/units/unit-01-limits-continuity.md#1.13 Removing Discontinuities"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01008",
   "cue": "A piecewise rule with one or two unknown constants, and the stem asks for their values.",
   "method": "First written line: the one sided limit from each branch at the first boundary.",
   "rival": "The rival matches the one sided limits and ignores the value (BC-ERR-01015).",
   "separating_feature": "The branch whose condition holds the equals sign supplies the value, and the value enters the equation.",
   "sources": ["BC-QA-01008"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01008",
   "bands": ["low", "mid"],
   "parameter_draw": {"left_end": "1", "right_end": "3", "curvature": "1", "lift": "3", "check": "values"},
   "problem": {"text": "\\(f(x)=\\frac{x^2-1}{x-1}\\) for \\(x<1\\), \\(kx+m\\) for \\(1\\le x\\le3\\), \\(x^2+3\\) for \\(x>3\\). Find \\(k\\) and \\(m\\) so \\(f\\) is continuous.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Boundary \\(x=1\\): the first branch owns \\(x<1\\).", "why": "The left limit comes from the branch that holds just left of 1.", "expr": "(x**2 - 1)/(x - 1)", "relation": "new"},
    {"cue": "Substitution gives \\(\\frac00\\), so divide out \\(x-1\\).", "why": "The branch equals \\(x+1\\) away from 1.", "expr": "2", "relation": "limit", "variable": "x", "point": "1", "dir": "-"},
    {"cue": "\\(1\\le x\\) puts \\(x=1\\) in the middle branch.", "why": "\\(f(1)=k+m\\), the right limit is \\(k+m\\), and both must equal 2.", "expr": "k + m = 2", "relation": "new"},
    {"cue": "Boundary \\(x=3\\): \\(f(3)=3k+m\\); the right branch tends to \\(12\\).", "why": "The second boundary gives the second equation.", "expr": "3*k + m = 12", "relation": "new"},
    {"cue": "Two equations share \\(m\\).", "why": "Subtracting removes \\(m\\).", "expr": "3*k + m - (k + m) = 12 - 2", "relation": "new"},
    {"cue": "One unknown left.", "why": "\\(2k=10\\).", "expr": "5", "relation": "solve", "variable": "k"},
    {"cue": "The stem asks for both constants.", "why": "\\(m=2-k=-3\\).", "expr": "FiniteSet(Eq(k, 5), Eq(m, -3))", "relation": "new"}
   ],
   "answer": {"form": "symbolic", "expr": "FiniteSet(Eq(k, 5), Eq(m, -3))"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01003",
   "observed_behavior": "The response states that the limit does not exist on the grounds that the function has no value at the input.",
   "scoring_consequence": "Both the value point and any justification point are lost.",
   "wrong_step": {"text": "\\(\\frac{x^2-1}{x-1}\\) has no value at 1, so the left limit is called nonexistent.", "expr": "(1**2 - 1)/(1 - 1)"},
   "right_step": {"text": "The factor divides out: the left limit is 2.", "expr": "2"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-01001", "text": "a missing or displaced function value is read as a missing or displaced limit"},
   "sources": ["BC-ERR-01003", "BC-MIS-01001"]
  },
  {
   "error_id": "BC-ERR-01015",
   "observed_behavior": "The response concludes continuity because the two one sided limits agree, without comparing them with the function value.",
   "scoring_consequence": "The justification point is lost, and a parameter solved this way can be wrong when the defined value differs.",
   "wrong_step": {"text": "With \\(f(1)=4\\) set apart, both one sided limits are 2, so continuity is claimed.", "expr": "Eq(2, 2)"},
   "right_step": {"text": "\\(f(1)=4\\) differs from the limit 2: not continuous at 1.", "expr": "Eq(4, 2)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-01009", "text": "most often that the function is defined there or that the one sided limits agree"},
   "sources": ["BC-ERR-01015", "BC-MIS-01009"]
  },
  {
   "error_id": "BC-ERR-01017",
   "observed_behavior": "The response substitutes the boundary input into the branch that does not apply on that side.",
   "scoring_consequence": "The one sided limit is wrong and every point depending on it is lost.",
   "wrong_step": {"text": "\\(x^2+3\\) used at 1: \\(k+m=4\\).", "expr": "k + m = 1**2 + 3"},
   "right_step": {"text": "The left branch gives \\(k+m=2\\).", "expr": "k + m = 2"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-01017"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-01001", "text": "Factor and divide out a common factor: \\(\\frac{x^2-1}{x-1}=x+1\\) for \\(x\\ne1\\). The slip: stopping at \\(\\frac00\\) with no factoring tried."},
  {"prq_id": "BC-PRQ-01003", "text": "Read a piecewise rule by the branch whose condition holds. The slip: the wrong branch evaluated at a boundary."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [3, 4, 7]}, "skipped_steps": {"ex-1": [1, 2, 5, 6]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-01008",
   "parameter_draw": {"left_end": "1", "right_end": "3", "curvature": "1", "lift": "3", "check": "values"},
   "completes": "ex-1",
   "stem": {"text": "The matching equations are \\(k+m=2\\) and \\(3k+m=12\\). Find \\(k\\) and \\(m\\).", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "FiniteSet(Eq(k, 5), Eq(m, -3))"},
   "steps": [
    {"text": "Subtract: \\(2k=10\\).", "expr": "2*k = 10", "relation": "new"},
    {"text": "\\(k=5\\).", "expr": "5", "relation": "solve", "variable": "k"},
    {"text": "\\(m=2-5=-3\\).", "expr": "FiniteSet(Eq(k, 5), Eq(m, -3))", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-01052"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-01008",
   "parameter_draw": {"left_end": "-1", "right_end": "2", "curvature": "1", "lift": "0", "check": "values"},
   "stem": {"text": "\\(f(x)=\\frac{x^2-1}{x+1}\\) for \\(x<-1\\), \\(kx+m\\) for \\(-1\\le x\\le2\\), \\(x^2\\) for \\(x>2\\). Find \\(k\\) and \\(m\\).", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "FiniteSet(Eq(k, 2), Eq(m, 0))"},
   "steps": [
    {"text": "At \\(-1\\): the left branch tends to \\(-2\\), so \\(-k+m=-2\\).", "expr": "-k + m = -2", "relation": "new"},
    {"text": "At 2: \\(2k+m=4\\).", "expr": "2*k + m = 4", "relation": "new"},
    {"text": "Subtract: \\(3k=6\\).", "expr": "3*k = 6", "relation": "new"},
    {"text": "\\(k=2\\).", "expr": "2", "relation": "solve", "variable": "k"},
    {"text": "\\(m=0\\).", "expr": "FiniteSet(Eq(k, 2), Eq(m, 0))", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-01052"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-01008",
   "parameter_draw": {"left_end": "2", "right_end": "4", "curvature": "1", "lift": "-2", "check": "values"},
   "stem": {"text": "\\(f(x)=\\frac{x^2-4}{x-2}\\) for \\(x<2\\), \\(kx+m\\) for \\(2\\le x\\le4\\), \\(x^2-2\\) for \\(x>4\\). For which \\(k\\) is \\(f\\) continuous?", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "5"},
   "steps": [
    {"text": "At 2: \\(2k+m=4\\).", "expr": "2*k + m = 4", "relation": "new"},
    {"text": "At 4: \\(4k+m=14\\).", "expr": "4*k + m = 14", "relation": "new"},
    {"text": "Subtract: \\(2k=10\\).", "expr": "2*k = 10", "relation": "new"},
    {"text": "\\(k=5\\).", "expr": "5", "relation": "solve", "variable": "k"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "6", "error_path": "BC-ERR-01017", "derivation": "x^2-2 used at 2: 2k+m=2 with 4k+m=14"},
    {"id": "B", "is_key": false, "expr": "1", "error_path": "BC-ERR-01017", "derivation": "x+2 used at 4: 4k+m=6 with 2k+m=4"},
    {"id": "C", "is_key": true, "expr": "5", "error_path": null},
    {"id": "D", "is_key": false, "expr": "2", "error_path": "BC-ERR-01017", "derivation": "wrong branch at both boundaries: 2k+m=2 with 4k+m=6"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-01052"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-01050 and BC-SKL-01053", "sources": ["BC-SKL-01050", "BC-SKL-01053"],
   "spec": {"kind": "graph", "window": {"x": [-2, 5], "y": [-2, 20]},
    "curves": [{"expr": "x + 1", "domain": [-2, 1], "open_end": 1}, {"expr": "5*x - 3", "domain": [1, 3], "closed_ends": [1, 3]}, {"expr": "x**2 + 3", "domain": [3, 5], "open_end": 3}],
    "points": [{"x": 1, "y": 2, "style": "filled"}, {"x": 3, "y": 12, "style": "filled"}],
    "labels": [{"text": "(1, 2)", "placement": "inside"}, {"text": "(3, 12)", "placement": "inside"}, {"text": "k = 5, m = -3", "placement": "inside"}],
    "representations": ["BC-REP-02"]},
   "fallback": "the same graph as a static image with the two join points listed beneath in text", "keyboard": "none needed: the figure has no control"},
  {"block": "ki-1", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-01050", "sources": ["BC-SKL-01050"],
   "spec": {"kind": "graph", "window": {"x": [-2, 4], "y": [-1, 5]},
    "curves": [{"expr": "(x**2 - 1)/(x - 1)", "domain": [-2, 4]}],
    "points": [{"x": 1, "y": 2, "style": "open"}, {"x": 1, "y": 2, "style": "filled", "caption": "repaired value"}],
    "labels": [{"text": "limit 2 at x = 1", "placement": "inside"}, {"text": "f(1) defined as 2", "placement": "inside"}],
    "representations": ["BC-REP-02"]},
   "fallback": "the graph with the open circle, then the same graph with the filled point, as two static images", "keyboard": "none needed: the figure has no control"},
  {"block": "ki-2", "mode": "interactive", "reason": "rule 3 promoted: BC-QA-01008 common_givens name a piecewise rule with unknown constants and the stem asks for the joining value", "sources": ["BC-QA-01008", "BC-SKL-01051"],
   "spec": {"kind": "graph", "window": {"x": [-2, 5], "y": [-4, 24]},
    "curves": [{"expr": "x + 1", "domain": [-2, 1]}, {"expr": "k*x + 2 - k", "domain": [1, 3]}, {"expr": "x**2 + 3", "domain": [3, 5]}],
    "control": {"type": "slider", "parameter": "k", "domain": {"min": 0, "max": 8, "step": 1}, "initial": 1},
    "question": "At which k does the middle segment meet the right branch at x = 3?",
    "labels": [{"text": "pivot (1, 2)", "placement": "inside"}, {"text": "target (3, 12)", "placement": "inside"}, {"text": "k", "placement": "inside"}],
    "representations": ["BC-REP-02"]},
   "fallback": "the graph at k = 3, 5 and 7 as three static images with the right end height stated under each", "keyboard": "the slider takes focus with Tab; Left and Right arrows change k by 1; Home and End jump to 0 and 8"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01003", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01015", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01017", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-2", "err-BC-ERR-01003", "err-BC-ERR-01015", "err-BC-ERR-01017", "ex-1"],
 "read_minutes": {"full": 3.73, "brief": 3.0},
 "word_count": {"full": 560, "brief": 450},
 "research_lines": [
  {"file": "research/units/unit-01-limits-continuity.md", "line": "All three quantities enter the condition, not only the two one sided limits."}
 ],
 "inferred": [
  {"claim": "All three MCQ distractors carry BC-ERR-01017, because BC-ERR-01003 and BC-ERR-01015 give no distinct value on a draw of this parameter_spec, where the middle branch owns both boundaries.", "settles": "A parameter_spec variant with a separately defined boundary value."},
  {"claim": "The figure and interactive modes serve the orientation and key ideas better than text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-01015", "BC-SKL-01050", "BC-SKL-01051", "BC-SKL-01052", "BC-SKL-01053", "BC-EK-LIM-2C1", "BC-EK-LIM-2C2", "ced:50", "BC-QA-01008", "BC-ERR-01003", "BC-ERR-01015", "BC-ERR-01017", "BC-MIS-01001", "BC-MIS-01009", "BC-MIS-01019", "BC-PRQ-01001", "BC-PRQ-01003", "research/units/unit-01-limits-continuity.md#1.13 Removing Discontinuities", "research/question-analysis/question-archetypes.md#BC-QA-01008 Parameter solved so that a piecewise function is continuous", "research/exam/exam-structure.md#Section and part layout"]
}
```
