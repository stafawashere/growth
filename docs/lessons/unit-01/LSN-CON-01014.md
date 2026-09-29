---
title: LSN-CON-01014 Continuity on an interval
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01014, continuity on an interval, built from authoring_bundle("BC-CON-01014") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01014 Continuity on an interval

Concept BC-CON-01014 (skills BC-SKL-01046, BC-SKL-01047, BC-SKL-01048, BC-SKL-01049), topic 1.12 of Unit 1 (BC-TOP-0112), loaded by one archetype, BC-QA-01015 (primary). The archetype carries no `point_types`, so the lesson says nothing about points.

## Orientation

Served text (32 words), from BC-CON-01014 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-01-limits-continuity.md#1.12 Confirming Continuity over an Interval): a response lists the maximal intervals on which a rule is continuous, found by removing every input where the rule is undefined, and names the function family whose continuity on its domain gives the reason.

## Key ideas

Two BC-EK map to the four skills, BC-EK-LIM-2B1 (BC-SKL-01046, 01048, 01049) and BC-EK-LIM-2B2 (BC-SKL-01046, 01047), both on ced:49, so two blocks: ki-2 core (both bands), ki-1 extended (low band), which keeps the brief form under its 450-word cap.

- ki-1 (extended), BC-EK-LIM-2B1. Paraphrase of the topic's Interval continuity paragraph: continuity on an interval is continuity at every point of it, and at the endpoint of a closed interval the condition is one sided. Anchor quote (18 words) from ced:49. Notation line: continuous on an interval.
- ki-2 (core), BC-EK-LIM-2B2. Paraphrase of the Families paragraph: the six named families are continuous at every point of their domains, and the domain restriction is the working part of the statement, so the answer is the domain cut at the excluded inputs, open there and closed at an included endpoint such as a radicand's zero. Anchor quote (16 words) from ced:49.

## Recognition

- BC-QA-01015 (family continuity-interval, MCQ shape, no calculator; research/question-analysis/question-archetypes.md#BC-QA-01015 Intervals of continuity determined from the domain of an expression): `typical_wording` "State the intervals on which the given function is continuous and give a reason for your answer"; `common_givens` a function given by a rule; `asked_to_produce` the intervals on which the function is continuous and a reason naming the function family and its domain. The signal is the word "intervals" beside "continuous" with a rule and no named point. No official example is recorded (`official_examples` empty).

What says "not this concept": a single named input with "is f continuous at" (BC-CON-01013, continuity at a point); a piecewise rule with an unknown constant (BC-CON-01015); a target value with "must there be" (BC-CON-01019, where interval continuity is the hypothesis, not the answer).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-01015. Cue, from `asked_to_produce` and `common_givens`: a rule is given and the stem asks for the intervals of continuity with a reason. Method, `expected_solution_path[0]`: identify every input at which the expression is undefined. First written line: the denominator set to zero (or the radicand set nonnegative) and solved. Rival: the domain written as one interval, from `common_distractors` ("writing the domain as a single interval when it has several pieces"), because the record carries no `wrong_approaches`. Separating feature: the answer is the whole domain cut at each undefined input, so a rational rule with two excluded inputs has three pieces. Evidence tag inferred, because the rival is not from `wrong_approaches` [inferred].

## Solution path

- ex-1, BC-QA-01015, both bands, no calculator. Draw: family rational, coefficient 2, zero 3, roots \(-2\) and 1, giving \(f(x)=\frac{2(x-3)}{x^2+x-2}\). Steps follow `expected_solution_path`: the denominator set to zero (valued, new), its roots (valued, solve), the family statement (no value), the maximal intervals (valued, new), the endpoint check (no value). A fluent solver writes the roots and the interval list and holds the family statement in the head on an MCQ; on a stem that demands a reason the family sentence is written [inferred: settled by an FRQ example of this archetype].

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

None. BC-QA-01015 lists no `point_types` (the record's `scoring_pattern` names an interval point and a reason point, but no BC-PT record carries them), so under plan 15 R14 the lesson carries no scoring checklist and names no points.

## Traps

Two active errors meet the concept's skills, in the bundle's order (BC-MIS-01019 medium on both, then id). Low band both, mid band both.

- err-BC-ERR-01031 (BC-MIS-01019, BC-MIS-01011). Wrong step on ex-1's draw: \((-\infty,-2)\cup(-2,\infty)\), with 1 left inside. Right step: \((-\infty,-2)\cup(-2,1)\cup(1,\infty)\). Distinct. Possible reason, words from BC-MIS-01019: without excluding the inputs outside that domain.
- err-BC-ERR-01032 (BC-MIS-01019, BC-MIS-01009). Wrong step: \((-2,1]\) written as the middle piece. Right step: \((-2,1)\). Distinct as sets, and the wrong piece contains 1, unlike err-BC-ERR-01031's wrong set. Possible reason null: neither linked description names a bracket.

## Representations

None. The topic's Representations paragraph names BC-REP-01 and BC-REP-04 and two conversions, an expression to a set of intervals and a family statement to a justification; neither is figure shaped.

## Prerequisite bridge

Three BC-PRQ parents reach the skills through `supporting` edges: BC-PRQ-01003 (reading a piecewise rule), BC-PRQ-01008 (domain of rational, radical, logarithmic and trigonometric expressions) and BC-PRQ-01010 (interval notation). One bridge each, from `description_plain` and `failure_signature`, gated by state.

## Time

BC-QA-01015 is `no_calculator` and "Typically a single multiple choice item", so the part is Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout; plan 15, Fluency). A fluent solver writes the roots of the denominator and the interval list and skips the family sentence and the endpoint check on an MCQ; nearly all of the budget goes to factoring the denominator.

## Checks

- chk-1, completion of ex-1, both bands: the excluded inputs \(-2\) and 1 are given, the student writes the intervals. Key \((-\infty,-2)\cup(-2,1)\cup(1,\infty)\), ex-1's answer.
- chk-2, isomorph on BC-QA-01015, both bands: radical family, coefficient 1, zero 0, roots \(-3\) and 2, \(g(x)=\frac{\sqrt{x+3}}{x-2}\). Key \([-3,2)\cup(2,\infty)\).
- chk-3, MCQ on BC-QA-01015, low band: rational family, coefficient 1, zero \(-1\), roots \(-3\) and 4, \(h(x)=\frac{x+1}{x^2-x-12}\). Key \((-\infty,-3)\cup(-3,4)\cup(4,\infty)\). Distractors: \((-\infty,-3)\cup(-3,\infty)\) (BC-ERR-01031, 4 left inside), \(\mathbb{R}\) written as \((-\infty,\infty)\) (BC-ERR-01031, both inputs left inside), \((-\infty,4)\cup(4,\infty)\) (BC-ERR-01032, the closed bracket \([-3,4)\), which puts \(-3\) back in the set).

No draw equals a published BC-QA-01015 `parameter_draw` (content/items_gen_unit01).

## Delivery

- orientation: text. Rule 5; BC-SKL-01046 to 01049 carry BC-REP-01 and BC-REP-04 only (docs/lessons/unit-01/README.md, section 6).
- ki-1, ki-2: text. Rule 5, same reason.
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-01031, err-BC-ERR-01032: step_reveal, wrong beside right. Rule 1.

No figure, motion, interactive or model mode applies: the skills carry no figure-bearing BC-REP and no process is taken [inferred; settled by the modality A/B in the build plan].

## Band plan

- Low (full): orientation, ki-1, ki-2, st-1, ex-1, err-01031, err-01032, chk-1, chk-2, chk-3, the three bridges. 528 words, 3.6 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-2, st-1, ex-1, err-01031, err-01032, chk-1, chk-2, the three bridges. 445 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-2, err-BC-ERR-01031, err-BC-ERR-01032, ex-1.

## Sources

- BC-CON-01014; BC-SKL-01046, BC-SKL-01047, BC-SKL-01048, BC-SKL-01049; BC-EK-LIM-2B1, BC-EK-LIM-2B2; ced:49
- BC-QA-01015
- BC-ERR-01031, BC-ERR-01032; BC-MIS-01019, BC-MIS-01011, BC-MIS-01009
- BC-PRQ-01003, BC-PRQ-01008, BC-PRQ-01010
- research/units/unit-01-limits-continuity.md#1.12 Confirming Continuity over an Interval
- research/question-analysis/question-archetypes.md#BC-QA-01015 Intervals of continuity determined from the domain of an expression
- research/exam/exam-structure.md#Section and part layout
- [inferred] The rival in st-1 comes from `common_distractors`, since BC-QA-01015 has no `wrong_approaches`. Settled by a library pass filling `wrong_approaches` on BC-QA-01015.
- [inferred] The family sentence is written only when a reason is demanded. Settled by an FRQ example of BC-QA-01015 with its scoring guideline.
- [inferred] No non-text delivery mode. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-01014",
 "kind": "concept",
 "target_id": "BC-CON-01014",
 "unit": "01",
 "skills": ["BC-SKL-01046", "BC-SKL-01047", "BC-SKL-01048", "BC-SKL-01049"],
 "orientation": {
  "text": "A response lists the largest intervals on which a rule is continuous: every input where the rule is undefined is removed, and the reason names the family, continuous on its domain.",
  "sources": ["BC-CON-01014", "research/units/unit-01-limits-continuity.md#1.12 Confirming Continuity over an Interval"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-2B1",
   "depth": "extended",
   "text": "A function is continuous on an interval when it is continuous at every point of that interval (BC-EK-LIM-2B1, ced:49). At an endpoint of a closed interval only one side lies in the interval, so the condition there is one sided: the value exists and matches the limit from inside.",
   "notation": "continuous on an interval",
   "quote": {"text": "A function is continuous on an interval if the function is continuous at each point in the interval.", "source": "ced:49"},
   "sources": ["BC-EK-LIM-2B1", "ced:49", "research/units/unit-01-limits-continuity.md#1.12 Confirming Continuity over an Interval"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-2B2",
   "depth": "core",
   "text": "The six standard families are continuous at every point of their domains (BC-EK-LIM-2B2, ced:49). The domain restriction does the work: the domain, cut at every undefined input, is the answer, open at each excluded input and closed at an endpoint the rule includes, such as a radicand's zero.",
   "notation": "open, closed and half open interval notation",
   "quote": {"text": "Polynomial, rational, power, exponential, logarithmic, and trigonometric functions are continuous on all points in their domains.", "source": "ced:49"},
   "sources": ["BC-EK-LIM-2B2", "ced:49", "research/units/unit-01-limits-continuity.md#1.12 Confirming Continuity over an Interval"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01015",
   "cue": "A rule is given and the stem asks for its intervals of continuity, with a reason naming its family.",
   "method": "First written line: identify every input at which the expression is undefined, by setting the denominator to zero or the radicand below zero.",
   "rival": "The rival writes the domain as a single interval when it has several pieces.",
   "separating_feature": "The answer is the whole domain cut at each undefined input, so a rational rule with two excluded inputs has three pieces.",
   "sources": ["BC-QA-01015"],
   "evidence_tag": "inferred"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01015",
   "bands": ["low", "mid"],
   "parameter_draw": {"coefficient": "2", "zero": "3", "roots": ["-2", "1"], "family": "rational"},
   "problem": {"text": "Let \\(f(x)=\\frac{2(x-3)}{x^2+x-2}\\). State the intervals on which \\(f\\) is continuous and give a reason.", "command_verb": "state"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "A rational rule is undefined only where its denominator is zero.", "why": "Those inputs are outside the domain.", "expr": "x**2 + x - 2 = 0", "relation": "new"},
    {"cue": "The quadratic factors as \\((x+2)(x-1)\\).", "why": "The excluded inputs are \\(-2\\) and \\(1\\).", "expr": "FiniteSet(-2, 1)", "relation": "solve", "variable": "x"},
    {"cue": "The stem asks for a reason, and \\(f\\) is a quotient of polynomials.", "why": "Rational functions are continuous on their domains: the family and its domain."},
    {"cue": "Two excluded inputs split the line into three pieces.", "why": "Each piece is open at an excluded input, since \\(f\\) has no value there.", "expr": "Union(Interval.open(-oo, -2), Interval.open(-2, 1), Interval.open(1, oo))", "relation": "new"},
    {"cue": "No piece has a closed endpoint.", "why": "No one sided check is needed."}
   ],
   "answer": {"form": "symbolic", "expr": "Union(Interval.open(-oo, -2), Interval.open(-2, 1), Interval.open(1, oo))"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01031",
   "observed_behavior": "The response reports an interval of continuity whose interior or endpoint contains a point where the function is undefined.",
   "scoring_consequence": "The interval point is lost.",
   "wrong_step": {"text": "\\((-\\infty,-2)\\cup(-2,\\infty)\\) keeps \\(1\\) inside.", "expr": "Union(Interval.open(-oo, -2), Interval.open(-2, oo))"},
   "right_step": {"text": "\\((-\\infty,-2)\\cup(-2,1)\\cup(1,\\infty)\\).", "expr": "Union(Interval.open(-oo, -2), Interval.open(-2, 1), Interval.open(1, oo))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-01019", "text": "without excluding the inputs outside that domain"},
   "sources": ["BC-ERR-01031", "BC-MIS-01019"]
  },
  {
   "error_id": "BC-ERR-01032",
   "observed_behavior": "The response writes a closed interval endpoint at an input that is not in the domain of the function.",
   "scoring_consequence": "The interval point is lost on notation.",
   "wrong_step": {"text": "\\((-2,1]\\) is closed where \\(f\\) has no value.", "expr": "Interval.Lopen(-2, 1)"},
   "right_step": {"text": "\\((-2,1)\\) is open at both ends.", "expr": "Interval.open(-2, 1)"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-01032"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-01003", "text": "A piecewise rule is read by choosing the branch whose condition holds for the input. The slip: the wrong branch evaluated at a boundary input."},
  {"prq_id": "BC-PRQ-01008", "text": "An expression is undefined where a denominator is zero or a logarithm has a nonpositive argument. The slip: intervals of continuity that include points outside the domain."},
  {"prq_id": "BC-PRQ-01010", "text": "A bracket is an inequality: \\((a,b]\\) means \\(a<x\\le b\\). The slip: a conclusion stated on a closed interval when the theorem gives an interior point."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 4]}, "skipped_steps": {"ex-1": [1, 3, 5]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-01015",
   "parameter_draw": {"coefficient": "2", "zero": "3", "roots": ["-2", "1"], "family": "rational"},
   "completes": "ex-1",
   "stem": {"text": "For \\(f(x)=\\frac{2(x-3)}{x^2+x-2}\\) the excluded inputs are \\(-2\\) and \\(1\\). Write the intervals on which \\(f\\) is continuous.", "command_verb": "write"},
   "key": {"form": "symbolic", "expr": "Union(Interval.open(-oo, -2), Interval.open(-2, 1), Interval.open(1, oo))"},
   "steps": [
    {"text": "The excluded inputs are the roots of the denominator.", "expr": "FiniteSet(-2, 1)", "relation": "new"},
    {"text": "Two excluded inputs give three open pieces.", "expr": "Union(Interval.open(-oo, -2), Interval.open(-2, 1), Interval.open(1, oo))", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-01046"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-01015",
   "parameter_draw": {"coefficient": "1", "zero": "0", "roots": ["-3", "2"], "family": "radical"},
   "stem": {"text": "Let \\(g(x)=\\frac{\\sqrt{x+3}}{x-2}\\). State the intervals on which \\(g\\) is continuous.", "command_verb": "state"},
   "key": {"form": "symbolic", "expr": "Union(Interval.Ropen(-3, 2), Interval.open(2, oo))"},
   "steps": [
    {"text": "The radicand needs \\(x\\ge -3\\) and the denominator excludes \\(2\\).", "expr": "Interval(-3, oo) - FiniteSet(2)", "relation": "new"},
    {"text": "Closed at \\(-3\\), where \\(g\\) has a value and the right-hand limit matches it; open at \\(2\\).", "expr": "Union(Interval.Ropen(-3, 2), Interval.open(2, oo))", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-01046", "BC-SKL-01049"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-01015",
   "parameter_draw": {"coefficient": "1", "zero": "-1", "roots": ["-3", "4"], "family": "rational"},
   "stem": {"text": "Let \\(h(x)=\\frac{x+1}{x^2-x-12}\\). On which set is \\(h\\) continuous?", "command_verb": "identify"},
   "key": {"form": "symbolic", "expr": "Union(Interval.open(-oo, -3), Interval.open(-3, 4), Interval.open(4, oo))"},
   "steps": [
    {"text": "The denominator is \\((x+3)(x-4)\\), zero at \\(-3\\) and \\(4\\).", "expr": "x**2 - x - 12 = 0", "relation": "new"},
    {"text": "The roots are \\(-3\\) and \\(4\\).", "expr": "FiniteSet(-3, 4)", "relation": "solve", "variable": "x"},
    {"text": "Three open pieces.", "expr": "Union(Interval.open(-oo, -3), Interval.open(-3, 4), Interval.open(4, oo))", "relation": "new"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "Union(Interval.open(-oo, -3), Interval.open(-3, oo))", "label": "\\((-\\infty,-3)\\cup(-3,\\infty)\\)", "error_path": "BC-ERR-01031", "derivation": "only -3 removed, so 4 stays inside"},
    {"id": "B", "is_key": false, "expr": "Interval(-oo, oo)", "label": "\\((-\\infty,\\infty)\\)", "error_path": "BC-ERR-01031", "derivation": "neither excluded input removed"},
    {"id": "C", "is_key": false, "expr": "Union(Interval.open(-oo, 4), Interval.open(4, oo))", "label": "\\((-\\infty,-3)\\cup[-3,4)\\cup(4,\\infty)\\)", "error_path": "BC-ERR-01032", "derivation": "closed bracket at -3 puts -3 back in the set"},
    {"id": "D", "is_key": true, "expr": "Union(Interval.open(-oo, -3), Interval.open(-3, 4), Interval.open(4, oo))", "label": "\\((-\\infty,-3)\\cup(-3,4)\\cup(4,\\infty)\\)", "error_path": null}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-01046", "BC-SKL-01049"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: BC-SKL-01046 to 01049 carry BC-REP-01 and BC-REP-04 only", "sources": ["BC-SKL-01046"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 5: a definition with no figure-bearing BC-REP on the skills", "sources": ["BC-SKL-01049"]},
  {"block": "ki-2", "mode": "text", "reason": "rule 5: a family statement, BC-REP-04 on BC-SKL-01047", "sources": ["BC-SKL-01047"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01031", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01032", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-2", "err-BC-ERR-01031", "err-BC-ERR-01032", "ex-1"],
 "read_minutes": {"full": 3.6, "brief": 3.0},
 "word_count": {"full": 528, "brief": 445},
 "research_lines": [
  {"file": "research/units/unit-01-limits-continuity.md", "line": "The restriction to the domain is the working part of the statement."}
 ],
 "inferred": [
  {"claim": "The rival in st-1 is taken from common_distractors because BC-QA-01015 carries no wrong_approaches.", "settles": "A library pass filling wrong_approaches on BC-QA-01015."},
  {"claim": "The family sentence is written only when the stem demands a reason; on an MCQ it is held in the head.", "settles": "An FRQ example of BC-QA-01015 with its scoring guideline."},
  {"claim": "No non-text delivery mode serves this concept better than text and step reveal.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-01014", "BC-SKL-01046", "BC-SKL-01047", "BC-SKL-01048", "BC-SKL-01049", "BC-EK-LIM-2B1", "BC-EK-LIM-2B2", "ced:49", "BC-QA-01015", "BC-ERR-01031", "BC-ERR-01032", "BC-MIS-01019", "BC-MIS-01011", "BC-MIS-01009", "BC-PRQ-01003", "BC-PRQ-01008", "BC-PRQ-01010", "research/units/unit-01-limits-continuity.md#1.12 Confirming Continuity over an Interval", "research/question-analysis/question-archetypes.md#BC-QA-01015 Intervals of continuity determined from the domain of an expression", "research/exam/exam-structure.md#Section and part layout"]
}
```
