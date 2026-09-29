---
title: LSN-CON-01016 Infinite limits and vertical asymptotes
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01016, infinite limits and vertical asymptotes, built from authoring_bundle("BC-CON-01016") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01016 Infinite limits and vertical asymptotes

Concept BC-CON-01016 (skills BC-SKL-01054, BC-SKL-01055, BC-SKL-01056, BC-SKL-01057), topic 1.14 of Unit 1 (BC-TOP-0114), loaded by BC-QA-01009 (primary, three of the four skills) and BC-QA-01007 (through BC-SKL-01057). Neither archetype carries `point_types`, so the lesson says nothing about points.

## Orientation

Served text, from BC-CON-01016 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-01-limits-continuity.md#1.14 Connecting Infinite Limits and Vertical Asymptotes): a response simplifies first, locates the vertical asymptotes at the zeros of the denominator that survive, and states the behaviour on each side as a one sided infinite limit.

## Key ideas

Two BC-EK map to the skills, both on ced:51: BC-EK-LIM-2D1 (BC-SKL-01054, 01055) and BC-EK-LIM-2D2 (BC-SKL-01055, 01056, 01057). Two core blocks, both bands.

- ki-1 (core), BC-EK-LIM-2D1. Paraphrase of the Infinite limits and What the notation claims paragraphs: a limit written as infinite records unbounded growth and is not a claim that a real limit exists; each side is treated separately when the sign differs across the input. Anchor quote (12 words) from ced:51. Notation line: vertical asymptote.
- ki-2 (core), BC-EK-LIM-2D2. Paraphrase of the Locating asymptotes paragraph (research/units/unit-01-limits-continuity.md#1.14 Connecting Infinite Limits and Vertical Asymptotes, cited inline in place of ced:51): simplify first; a factor that divides out gives a removable break, not an asymptote. Anchor quote (13 words) from ced:51.

## Recognition

- BC-QA-01009 (family infinite-limit-asymptote, MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-01009 Vertical asymptote located and the one sided infinite limits stated): `typical_wording` "Find the vertical asymptotes of the graph of the given function and describe the behaviour of the function near each one"; `asked_to_produce` the locations of the vertical asymptotes and one sided infinite limit statements; `common_givens` empty. The signal is "vertical asymptote" or "behaviour near" with a rational rule.
- BC-QA-01007 (family discontinuity-classification, MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-01007 Discontinuity classified from a rule or a graph): `typical_wording` "Classify each discontinuity of the given function and give a reason for each classification"; `asked_to_produce` a classification as removable, jump or vertical asymptote with a reason; `common_givens` empty. The signal is "classify" with a break.

What says "not this concept": the infinity symbol under the arrow rather than in the value (BC-CON-01017, the BC-MIS-01018 probe named in docs/lessons/unit-01/README.md section 3); substitution giving zero over zero with a factor that cancels everywhere (BC-CON-01008); a named constant to solve for (BC-CON-01015). No official example is recorded for either archetype.

## Method choice

Two strategy blocks, low band both, mid band the first. Both archetypes have empty `common_givens`, so both blocks carry `evidence_tag: inferred` and their cues rest on `typical_wording` and `asked_to_produce`.

- st-1, BC-QA-01009. Cue: a rational rule, and the stem asks where the vertical asymptotes are and how the function behaves near each. Method, `expected_solution_path[0]`: factor numerator and denominator. Rival, `wrong_approaches`: one two sided infinite limit written where the sides differ in sign (BC-ERR-01019). Separating feature: the sign of the simplified quotient on each side of the surviving zero.
- st-2, BC-QA-01007. Cue: a function with breaks, and the stem asks to classify each with a reason. Method: locate the inputs where the function is undefined or the rule changes. Rival: a vertical asymptote named at a factor that divides out (BC-ERR-01018). Separating feature: whether the factor survives cancellation.

## Solution path

- ex-1, BC-QA-01009, both bands, no calculator. Draw: coefficient 2, cancelled_root 1, pole \(-2\), zero 3, form factored, giving \(f(x)=\frac{2(x-1)(x-3)}{(x-1)(x+2)}\). Constraints hold (\(1\ne-2\), \(3\ne-2\), \(3\ne1\)). Steps follow `expected_solution_path`: factored form read (no value), the expression (valued, new), the simplified form (valued, equivalent), the surviving zero (no value), the right-hand limit (valued, limit from the right), the left-hand limit (valued, new then limit from the left). A fluent solver writes the simplified form, the location and the two one sided statements, and holds the sign arithmetic in the head.

Each infinite value carries relation `limit` with its side (`dir`), so the checker recomputes it. The answer and the check keys are statements, because the response is a location with two one sided limits, not one value.

## Scoring

None. Neither BC-QA-01009 nor BC-QA-01007 lists `point_types`, so under plan 15 R14 the lesson carries no scoring checklist and names no points.

## Traps

Three active errors meet the concept's skills, in the bundle's order (all linked BC-MIS high, so by id). Low band all three, mid band the first two.

- err-BC-ERR-01018 (BC-MIS-01011, BC-MIS-01012). Wrong step on ex-1's draw: asymptotes at \(x=-2\) and \(x=1\). Right step: at \(x=-2\) only; \(x=1\) is removable. Distinct. Possible reason, words from BC-MIS-01011.
- err-BC-ERR-01019 (BC-MIS-01012, BC-MIS-01011). Wrong step: \(\lim_{x\to-2}f(x)=-\infty\). Right step: \(+\infty\) from the left, \(-\infty\) from the right. Distinct. Possible reason, words from BC-MIS-01012.
- err-BC-ERR-01020 (BC-MIS-01012, BC-MIS-99008). Wrong step: \(\infty\) read as a real value, "so the limit exists". Right step: \(\frac{1}{f(x)}=\frac{x+2}{2(x-3)}\to0\), so \(f\) passes every bound and no real limit exists. Distinct. Possible reason, words from BC-MIS-01012.

## Representations

None as a separate block. The topic's Representations paragraph names BC-REP-01 and BC-REP-02 and a conversion from one sided statements to a described graph; the orientation figure and the ki-1 motion carry it under Delivery.

## Prerequisite bridge

Two BC-PRQ parents reach the skills through `supporting` edges: BC-PRQ-01001 (factoring and dividing out, to BC-SKL-01056, 01057) and BC-PRQ-01009 (sign of a quotient near a zero of the denominator, to BC-SKL-01054, 01055). One bridge each, gated by state.

## Time

Both archetypes are `no_calculator` and "Typically a single multiple choice item", so the part is Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout; plan 15, Fluency). On an MCQ nothing is required in writing; the factoring and the sign on each side are the work, and the minutes go to the factoring when the form is expanded (BC-DF-02 on the `form` parameter).

## Checks

- chk-1, completion of ex-1, both bands: the right-hand limit \(-\infty\) is given, the student states the left-hand limit. Key: \(\lim_{x\to-2^-}f(x)=\infty\), as a statement.
- chk-2, isomorph on BC-QA-01009, both bands: coefficient \(-1\), cancelled_root \(-3\), pole 2, zero 0, \(g(x)=\frac{-x(x+3)}{(x+3)(x-2)}\). Key: asymptote \(x=2\) only, \(\lim_{x\to2^+}g(x)=-\infty\).
- chk-3, MCQ on BC-QA-01009, low band: coefficient 3, cancelled_root 2, pole \(-1\), zero 4, \(h(x)=\frac{3(x-2)(x-4)}{(x-2)(x+1)}\). Statement key: asymptote at \(x=-1\) only, \(+\infty\) from the left and \(-\infty\) from the right. Distractors: asymptotes at \(-1\) and 2 (BC-ERR-01018); \(\lim_{x\to-1}h(x)=-\infty\) (BC-ERR-01019); "the limit at \(-1\) exists and equals \(\infty\)" (BC-ERR-01020).

No draw equals a published BC-QA-01009 `parameter_draw` (content/items_gen_unit01, content/items_p1_agent).

## Delivery

- orientation: figure. Rule 3, BC-REP-02 on BC-SKL-01056 and 01057: the graph of ex-1 with the dashed line \(x=-2\) and the open circle at \((1,-\frac43)\).
- ki-1: motion. Rule 2, a limit being taken: the input steps toward \(-2\) from each side and the output grows without bound, with opposite signs (docs/lessons/unit-01/README.md, section 6).
- ki-2: figure. Rule 3, BC-REP-02 on BC-SKL-01057: the removable hole and the asymptote on one graph, each labelled by whether its factor survives.
- ex-1 and the three error blocks: step_reveal. Rule 1.

Every non-text choice is [inferred], settled by the modality A/B in the build plan.

## Band plan

- Low (full): orientation, ki-1, ki-2, st-1, st-2, ex-1, the three error blocks, chk-1, chk-2, chk-3, the two bridges. 542 words, 3.7 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, ki-2, st-1, ex-1, err-01018, err-01019, chk-1, chk-2, the two bridges. 417 words, 2.8 minutes (cap 450 and 3).
- Refresher: ki-1, ki-2, err-BC-ERR-01018, err-BC-ERR-01019, err-BC-ERR-01020, ex-1.

## Sources

- BC-CON-01016; BC-SKL-01054, BC-SKL-01055, BC-SKL-01056, BC-SKL-01057; BC-EK-LIM-2D1, BC-EK-LIM-2D2; ced:51
- BC-QA-01009, BC-QA-01007
- BC-ERR-01018, BC-ERR-01019, BC-ERR-01020; BC-MIS-01011, BC-MIS-01012, BC-MIS-99008
- BC-PRQ-01001, BC-PRQ-01009
- research/units/unit-01-limits-continuity.md#1.14 Connecting Infinite Limits and Vertical Asymptotes
- research/question-analysis/question-archetypes.md#BC-QA-01009 Vertical asymptote located and the one sided infinite limits stated
- research/question-analysis/question-archetypes.md#BC-QA-01007 Discontinuity classified from a rule or a graph
- research/exam/exam-structure.md#Section and part layout
- [inferred] Strategy cues rest on `typical_wording` and `asked_to_produce`, because `common_givens` is empty on BC-QA-01009 and BC-QA-01007. Settled by a library pass filling `common_givens`.
- [inferred] Non-text delivery modes. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-01016",
 "kind": "concept",
 "target_id": "BC-CON-01016",
 "unit": "01",
 "skills": ["BC-SKL-01054", "BC-SKL-01055", "BC-SKL-01056", "BC-SKL-01057"],
 "orientation": {
  "text": "A response simplifies first, places a vertical asymptote at each zero of the denominator that survives, and states the behaviour on each side as a one sided infinite limit.",
  "sources": ["BC-CON-01016", "research/units/unit-01-limits-continuity.md#1.14 Connecting Infinite Limits and Vertical Asymptotes"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-2D1",
   "depth": "core",
   "text": "A limit written as \\(\\infty\\) records growth without bound; it does not say a real limit exists (BC-EK-LIM-2D1, ced:51). Each side is written separately whenever the sign differs across the input.",
   "notation": "vertical asymptote",
   "quote": {"text": "The concept of a limit can be extended to include infinite limits.", "source": "ced:51"},
   "sources": ["BC-EK-LIM-2D1", "ced:51", "research/units/unit-01-limits-continuity.md#1.14 Connecting Infinite Limits and Vertical Asymptotes"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-2D2",
   "depth": "core",
   "text": "Simplify first (research/units/unit-01-limits-continuity.md#1.14 Connecting Infinite Limits and Vertical Asymptotes). A factor that divides out leaves a removable break; only a zero of the simplified denominator is an asymptote.",
   "notation": "",
   "quote": {"text": "Asymptotic and unbounded behavior of functions can be described and explained using limits.", "source": "ced:51"},
   "sources": ["BC-EK-LIM-2D2", "ced:51", "research/units/unit-01-limits-continuity.md#1.14 Connecting Infinite Limits and Vertical Asymptotes"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01009",
   "cue": "A rational rule; the stem asks for the vertical asymptotes and the behaviour near each.",
   "method": "First written line: factor numerator and denominator.",
   "rival": "One two sided infinite limit where the sides differ in sign (BC-ERR-01019).",
   "separating_feature": "The sign of the simplified quotient on each side.",
   "sources": ["BC-QA-01009"],
   "evidence_tag": "inferred"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-01007",
   "cue": "A function with breaks; the stem asks to classify each and give a reason.",
   "method": "First written line: the inputs where the function is undefined or the rule changes.",
   "rival": "A vertical asymptote named at a factor that divides out (BC-ERR-01018).",
   "separating_feature": "Whether the factor survives cancellation.",
   "sources": ["BC-QA-01007"],
   "evidence_tag": "inferred"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01009",
   "bands": ["low", "mid"],
   "parameter_draw": {"coefficient": "2", "cancelled_root": "1", "pole": "-2", "zero": "3", "form": "factored"},
   "problem": {"text": "Let \\(f(x)=\\frac{2(x-1)(x-3)}{(x-1)(x+2)}\\). Find the vertical asymptotes and describe \\(f\\) near each.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Both parts arrive factored.", "why": "Factors are what cancel, so the factored form is read first."},
    {"cue": "\\(x-1\\) sits in both parts.", "why": "A shared factor divides out.", "expr": "2*(x-1)*(x-3)/((x-1)*(x+2))", "relation": "new"},
    {"cue": "Divide out \\(x-1\\), recording \\(x\\ne1\\).", "why": "At 1 the break is removable.", "expr": "2*(x-3)/(x+2)", "relation": "equivalent"},
    {"cue": "The simplified denominator is \\(x+2\\).", "why": "Only a surviving zero gives an asymptote: \\(x=-2\\)."},
    {"cue": "Just right of \\(-2\\): numerator near \\(-10\\), denominator small positive.", "why": "Negative over small positive.", "expr": "-oo", "relation": "limit", "variable": "x", "point": "-2", "dir": "+"},
    {"cue": "Left of \\(-2\\), the same simplified form.", "why": "Each side is taken on its own.", "expr": "2*(x-3)/(x+2)", "relation": "new"},
    {"cue": "Just left of \\(-2\\): the denominator is small negative.", "why": "Opposite sign, so each side gets its own statement.", "expr": "oo", "relation": "limit", "variable": "x", "point": "-2", "dir": "-"}
   ],
   "answer": {"form": "statement", "expr": "x = -2 only; left limit oo, right limit -oo"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01018",
   "observed_behavior": "The response names a vertical asymptote at an input where the factor divides out of the rational expression.",
   "scoring_consequence": "The location point is lost and the classification is wrong.",
   "wrong_step": {"text": "Asymptotes at \\(-2\\) and \\(1\\).", "expr": "FiniteSet(-2, 1)"},
   "right_step": {"text": "At \\(-2\\) only.", "expr": "FiniteSet(-2)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-01011", "text": "any zero of the original denominator as unbounded behaviour without simplifying first"},
   "sources": ["BC-ERR-01018", "BC-MIS-01011"]
  },
  {
   "error_id": "BC-ERR-01019",
   "observed_behavior": "The response writes a single infinite limit at an input where one side increases without bound and the other decreases without bound.",
   "scoring_consequence": "The behaviour point is lost because the notation asserts behaviour the function does not have.",
   "wrong_step": {"text": "\\(\\lim_{x\\to-2}f(x)=-\\infty\\).", "expr": "-oo"},
   "right_step": {"text": "From the left, \\(\\infty\\).", "expr": "oo"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-01012", "text": "writes one statement where the two sides carry opposite signs"},
   "sources": ["BC-ERR-01019", "BC-MIS-01012"]
  },
  {
   "error_id": "BC-ERR-01020",
   "observed_behavior": "The response writes that the limit equals infinity and then treats that statement as an existence claim for a real limit.",
   "scoring_consequence": "A point requiring a statement about existence is lost.",
   "wrong_step": {"text": "Left limit \\(\\infty\\) read as a real value, so it exists.", "expr": "oo"},
   "right_step": {"text": "\\(\\frac{1}{f(x)}=\\frac{x+2}{2(x-3)}\\to0\\): \\(f\\) passes every bound, no real limit.", "expr": "(x+2)/(2*(x-3))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-01012", "text": "reads the infinity symbol as a real value"},
   "sources": ["BC-ERR-01020", "BC-MIS-01012"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-01001", "text": "Factor and cancel a common factor. The slip: stopping at zero over zero with no factoring tried."},
  {"prq_id": "BC-PRQ-01009", "text": "Find the sign of a quotient on each side of a zero of its denominator. The slip: one two sided infinite limit where the signs differ."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [3, 4, 5, 7]}, "skipped_steps": {"ex-1": [1, 2, 6]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-01009",
   "parameter_draw": {"coefficient": "2", "cancelled_root": "1", "pole": "-2", "zero": "3", "form": "factored"},
   "completes": "ex-1",
   "stem": {"text": "For \\(f(x)=\\frac{2(x-3)}{x+2}\\), \\(x\\ne1\\), \\(\\lim_{x\\to-2^+}f(x)=-\\infty\\). State \\(\\lim_{x\\to-2^-}f(x)\\).", "command_verb": "state"},
   "key": {"form": "statement", "expr": "lim from the left at -2 is oo"},
   "steps": [
    {"text": "Left of \\(-2\\): negative over small negative.", "expr": "2*(x-3)/(x+2)", "relation": "new"},
    {"text": "Positive and unbounded.", "expr": "oo", "relation": "limit", "variable": "x", "point": "-2", "dir": "-"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-01055"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-01009",
   "parameter_draw": {"coefficient": "-1", "cancelled_root": "-3", "pole": "2", "zero": "0", "form": "factored"},
   "stem": {"text": "Let \\(g(x)=\\frac{-x(x+3)}{(x+3)(x-2)}\\). Locate the vertical asymptote and state \\(\\lim_{x\\to2^+}g(x)\\).", "command_verb": "state"},
   "key": {"form": "statement", "expr": "x = 2 only; right limit -oo"},
   "steps": [
    {"text": "Divide out \\(x+3\\).", "expr": "-x*(x+3)/((x+3)*(x-2))", "relation": "new"},
    {"text": "\\(g(x)=\\frac{-x}{x-2}\\), \\(x\\ne-3\\).", "expr": "-x/(x-2)", "relation": "equivalent"},
    {"text": "Right of 2: negative over small positive.", "expr": "-oo", "relation": "limit", "variable": "x", "point": "2", "dir": "+"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-01055", "BC-SKL-01056"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-01009",
   "parameter_draw": {"coefficient": "3", "cancelled_root": "2", "pole": "-1", "zero": "4", "form": "factored"},
   "stem": {"text": "Let \\(h(x)=\\frac{3(x-2)(x-4)}{(x-2)(x+1)}\\). Which statement is true?", "command_verb": "identify"},
   "key": {"form": "statement", "expr": "asymptote x = -1 only; left oo, right -oo"},
   "steps": [
    {"text": "Divide out \\(x-2\\).", "expr": "3*(x-2)*(x-4)/((x-2)*(x+1))", "relation": "new"},
    {"text": "\\(h(x)=\\frac{3(x-4)}{x+1}\\), \\(x\\ne2\\).", "expr": "3*(x-4)/(x+1)", "relation": "equivalent"}
   ],
   "options": [
    {"id": "A", "is_key": false, "label": "Asymptotes at \\(x=-1\\) and \\(x=2\\).", "error_path": "BC-ERR-01018", "derivation": "the cancelled factor x-2 kept as an asymptote"},
    {"id": "B", "is_key": false, "label": "\\(\\lim_{x\\to-1}h(x)=-\\infty\\).", "error_path": "BC-ERR-01019", "derivation": "the right side's sign written for both sides"},
    {"id": "C", "is_key": true, "label": "Only \\(x=-1\\); \\(\\infty\\) from the left, \\(-\\infty\\) from the right.", "error_path": null},
    {"id": "D", "is_key": false, "label": "The limit at \\(-1\\) exists and equals \\(\\infty\\).", "error_path": "BC-ERR-01020", "derivation": "an infinite limit read as an existing real limit"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-01054", "BC-SKL-01057"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-01056 and BC-SKL-01057", "sources": ["BC-SKL-01056", "BC-SKL-01057"],
   "spec": {"kind": "graph", "window": {"x": [-8, 6], "y": [-20, 20]},
    "curves": [{"expr": "2*(x-3)/(x+2)", "domain": [-8, 6], "break_at": [-2]}],
    "asymptotes": [{"type": "vertical", "x": -2, "style": "dashed"}],
    "points": [{"x": 1, "y": "-4/3", "style": "open"}],
    "labels": [{"text": "x = -2", "placement": "inside"}, {"text": "hole at (1, -4/3)", "placement": "inside"}],
    "representations": ["BC-REP-02"]},
   "fallback": "the same graph as a static image with its two labels", "keyboard": "none needed: the figure has no control"},
  {"block": "ki-1", "mode": "motion", "reason": "rule 2: a limit being taken; rule 3, BC-REP-02 on BC-SKL-01056", "sources": ["BC-SKL-01055", "BC-SKL-01056"],
   "spec": {"kind": "graph", "window": {"x": [-4, 0], "y": [-1000, 1000]},
    "curves": [{"expr": "2*(x-3)/(x+2)", "domain": [-4, 0], "break_at": [-2]}],
    "frames": [
     {"x": -2.5, "y": 22, "side": "left"}, {"x": -2.1, "y": 102, "side": "left"}, {"x": -2.01, "y": 1002, "side": "left"},
     {"x": -1.5, "y": -18, "side": "right"}, {"x": -1.9, "y": -98, "side": "right"}, {"x": -1.99, "y": -998, "side": "right"}],
    "labels": [{"text": "from the left: up without bound", "placement": "inside"}, {"text": "from the right: down without bound", "placement": "inside"}, {"text": "x = -2", "placement": "inside"}],
    "representations": ["BC-REP-02"]},
   "fallback": "the six frames as one static graph with the six points marked and their values in a two-row table beneath", "keyboard": "Right arrow steps to the next frame, Left arrow to the previous; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"},
  {"block": "ki-2", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-01057", "sources": ["BC-SKL-01057"],
   "spec": {"kind": "graph", "window": {"x": [-8, 6], "y": [-20, 20]},
    "curves": [{"expr": "2*(x-3)/(x+2)", "domain": [-8, 6], "break_at": [-2]}],
    "asymptotes": [{"type": "vertical", "x": -2, "style": "dashed"}],
    "points": [{"x": 1, "y": "-4/3", "style": "open"}],
    "labels": [{"text": "x - 1 cancels: removable", "placement": "inside"}, {"text": "x + 2 survives: asymptote", "placement": "inside"}],
    "representations": ["BC-REP-02"]},
   "fallback": "the same graph as a static image with its two labels", "keyboard": "none needed: the figure has no control"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01018", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01019", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01020", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "ki-2", "err-BC-ERR-01018", "err-BC-ERR-01019", "err-BC-ERR-01020", "ex-1"],
 "read_minutes": {"full": 3.7, "brief": 2.8},
 "word_count": {"full": 542, "brief": 417},
 "research_lines": [
  {"file": "research/units/unit-01-limits-continuity.md", "line": "A factor that divides out produces a removable discontinuity rather than a vertical asymptote."}
 ],
 "inferred": [
  {"claim": "Both strategy cues rest on typical_wording and asked_to_produce, because common_givens is empty on BC-QA-01009 and BC-QA-01007.", "settles": "A library pass filling common_givens on both archetypes."},
  {"claim": "The figure and motion modes serve the orientation and key ideas better than text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-01016", "BC-SKL-01054", "BC-SKL-01055", "BC-SKL-01056", "BC-SKL-01057", "BC-EK-LIM-2D1", "BC-EK-LIM-2D2", "ced:51", "BC-QA-01009", "BC-QA-01007", "BC-ERR-01018", "BC-ERR-01019", "BC-ERR-01020", "BC-MIS-01011", "BC-MIS-01012", "BC-MIS-99008", "BC-PRQ-01001", "BC-PRQ-01009", "research/units/unit-01-limits-continuity.md#1.14 Connecting Infinite Limits and Vertical Asymptotes", "research/question-analysis/question-archetypes.md#BC-QA-01009 Vertical asymptote located and the one sided infinite limits stated", "research/question-analysis/question-archetypes.md#BC-QA-01007 Discontinuity classified from a rule or a graph", "research/exam/exam-structure.md#Section and part layout"]
}
```
