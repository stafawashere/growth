---
title: LSN-DEC-06-01 Writing an accumulation function against differentiating one
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the decision lesson on the confusable set BC-SKL-06017 and BC-SKL-06019, which teaches the student to name, from the stem's verb, whether the accumulation function is to be written as an integral or differentiated, before any execution.
---

# LSN-DEC-06-01 Writing an accumulation function against differentiating one

Set from `confusable_sets`: BC-SKL-06017 (write an accumulation function as a definite integral with a variable upper limit) and BC-SKL-06019 (differentiate an accumulation function whose upper limit is a function of x), both on topic 6.4 (research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions), both loaded by BC-QA-06012. Each skill lists the other in `confusable_with`.

## Orientation

Served text (44 words). Two questions share the object \(F(x)=\int_a^{g(x)} f(t)\,dt\). One asks for \(F\) itself, as an integral with a variable upper limit; the other asks for \(F'\), the integrand at the upper limit times the derivative of that limit. A response names which before writing anything.

## Recognition

The selecting feature is the task verb, the one thing that changes between the stems: "Write \(F(x)\) as a definite integral" selects the first method; "Find \(F'(x)\)" selects the second. Everything else (integrand, lower limit, upper limit) is held fixed across the stems so the student cannot key on it. From BC-QA-06012: `asked_to_produce` the value of the derivative of the accumulation function at a stated input; `common_givens` a graph of the integrand. Stems on the writing side follow BC-SKL-06017's `adaptive.mastered_if` (the fixed starting input in the lower limit, \(x\) alone in the upper limit, a bound variable whose letter differs from \(x\)). MCQ and FRQ shapes: BC-QA-06012 is MCQ-shaped and no calculator.

## Method choice

The two strategy blocks side by side, the second is the BC-QA-06012 block, the first is the writing block built from BC-SKL-06017's `adaptive.mastered_if` and tagged inferred (the library holds no separate archetype for writing the accumulation).

- st-1 (write, BC-SKL-06017, inferred). Cue: the stem asks for the accumulation function itself, from a rate or integrand and a starting input. Method, first written line: \(F(x)=\int_a^{x} f(t)\,dt\) with the starting input in the lower limit and \(x\) alone in the upper limit. Rival: differentiating instead, or leaving the answer in terms of \(t\) (BC-ERR-06028). Separating feature: the verb is write, and the object asked for is a function of \(x\), not its rate.
- st-2 (differentiate, BC-SKL-06019, BC-QA-06012). Cue: the stem asks for the value of the derivative of the accumulation function at a stated input, from a graph of the integrand. Method, `expected_solution_path[0]`: state that the derivative of the accumulation equals the integrand at the upper limit. Rival, `wrong_approaches`: evaluating the integrand at the upper limit without the chain rule factor (BC-ERR-06027). Separating feature: the verb is find the derivative, and a composite upper limit adds the factor of its own derivative.

## Stems

Two stems, drawn on BC-QA-06012, differing in `task` only (integrand \(\cos t\), lower limit 0, upper limit \(x^2\) held fixed):

- stem-1 (task write): "Let \(F\) be the accumulation of \(\cos t\) from 0 to \(x^2\). Write \(F(x)\) as a definite integral." Method: write the accumulation as a definite integral with a variable upper limit.
- stem-2 (task differentiate): "Let \(F(x)=\int_0^{x^2}\cos t\,dt\). Find \(F'(x)\)." Method: differentiate the accumulation function with the chain rule.

## Traps

The errors held by the set's skills that a wrong method produces: BC-ERR-06027 (the derivative reported as the integrand at the limit with no extra factor: the differentiate method half done), BC-ERR-06028 (the answer left in terms of \(t\): the write method's bound variable leaking), BC-ERR-99032 (a statement that is not an integral expression when one was asked for). No execution is shown; the traps name the method that produced them.

## Time

BC-QA-06012 is `no_calculator` and MCQ-shaped: Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout). The decision itself takes no written line; the first written line is the method's own first step, so the whole budget stays for execution.

## Checks

Three discrimination checks, method-naming only, no execution. Options are the two methods plus the half-done differentiate method; distractors carry the error path the wrong method produces (BC-ERR-06027 for the missing factor, BC-ERR-06028 for the written integral offered where a derivative was asked, BC-ERR-99032 for a derivative offered where an integral expression was asked).

- chk-1: for \(F(x)=\int_0^{x^2}\cos t\,dt\), name the method that gives \(F'(x)\). Key: evaluate the integrand at the upper limit, then multiply by the derivative of the upper limit.
- chk-2: \(G\) is the accumulation of \(\sin t\) from 1 to \(3x\); name the method that gives \(G(x)\). Key: write the accumulation as a definite integral with a variable upper limit.
- chk-3: for \(H(x)=\int_1^{3x}\sin t\,dt\), name the method that gives \(H'(x)\). Key: evaluate the integrand at the upper limit, then multiply by the derivative of the upper limit.

## Delivery

- orientation: text. Rule 5.
- stems: contrast, the two stems on one screen with the task verb marked, per plan 15's side by side rule. The integrand graph is not drawn, because the selecting feature is the verb and a figure would add a representation the decision does not read [inferred; settled by the modality A/B].

## Band plan

The low band serves: orientation, the two stems, st-1, st-2, chk-1, chk-2, chk-3. 343 words in the full form (all three checks) and 237 in the brief form (checks 1 and 2, the first strategy block), 2.4 and 1.6 minutes. Refresher: st-1, st-2.

## Sources

- BC-SKL-06017, BC-SKL-06019; BC-EK-FUN-5A1, BC-EK-FUN-5A2; ced:121
- BC-QA-06012; BC-PT-99024, BC-PT-99004 (not tagged, no execution)
- BC-ERR-06027, BC-ERR-06028, BC-ERR-99032
- research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions
- research/exam/exam-structure.md#Section and part layout
- [inferred] st-1 rests on BC-SKL-06017's `adaptive.mastered_if`, because no active archetype asks only for the accumulation written as an integral. Settled by a library staging pass minting that archetype.

## Machine record

```json
{
 "id": "LSN-DEC-06-01",
 "kind": "decision",
 "target_id": "BC-UNIT-06",
 "unit": "06",
 "skills": ["BC-SKL-06017", "BC-SKL-06019"],
 "orientation": {
  "text": "Two questions share the object \\(F(x)=\\int_a^{g(x)} f(t)\\,dt\\). One asks for \\(F\\) itself, as an integral with a variable upper limit. The other asks for \\(F'\\), the integrand at the upper limit times the derivative of that limit. A response names which before writing anything.",
  "sources": ["BC-SKL-06017", "BC-SKL-06019", "research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions"]
 },
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06012",
   "cue": "The stem asks for the accumulation function itself, from a rate or integrand and a starting input.",
   "method": "First written line: \\(F(x)=\\int_a^{x} f(t)\\,dt\\), the starting input in the lower limit and \\(x\\) alone in the upper limit.",
   "rival": "The rival is differentiating instead, or leaving the answer in terms of \\(t\\).",
   "separating_feature": "The verb is write, and the object asked for is a function of \\(x\\), not its rate.",
   "sources": ["BC-SKL-06017"],
   "evidence_tag": "inferred"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-06012",
   "cue": "The stem asks for the accumulation function's derivative at a stated input, from a graph of the integrand.",
   "method": "First written line: state that the derivative of the accumulation equals the integrand at the upper limit.",
   "rival": "The rival is evaluating the integrand at the upper limit without the chain rule factor.",
   "separating_feature": "The verb is find the derivative, and a composite upper limit adds the factor of its own derivative.",
   "sources": ["BC-QA-06012"],
   "evidence_tag": "verified"
  }
 ],
 "decision": {
  "skills": ["BC-SKL-06017", "BC-SKL-06019"],
  "selecting_feature": "task",
  "stems": [
   {"id": "stem-1", "archetype_id": "BC-QA-06012", "method": "Write the accumulation as a definite integral with a variable upper limit", "parameter_draw": {"integrand": "cos(t)", "lower": 0, "upper_limit": "x^2", "task": "write"}, "text": "Let \\(F\\) be the accumulation of \\(\\cos t\\) from 0 to \\(x^2\\). Write \\(F(x)\\) as a definite integral."},
   {"id": "stem-2", "archetype_id": "BC-QA-06012", "method": "Differentiate the accumulation function with the chain rule", "parameter_draw": {"integrand": "cos(t)", "lower": 0, "upper_limit": "x^2", "task": "differentiate"}, "text": "Let \\(F(x)=\\int_0^{x^2}\\cos t\\,dt\\). Find \\(F'(x)\\)."}
  ]
 },
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout"},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "discrimination",
   "format": "mcq",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06012",
   "parameter_draw": {"integrand": "cos(t)", "lower": 0, "upper_limit": "x^2", "task": "name the method 1"},
   "stem": {"text": "For \\(F(x)=\\int_0^{x^2}\\cos t\\,dt\\), name the method that gives \\(F'(x)\\).", "command_verb": "name"},
   "key": {"form": "statement", "expr": "chain"},
   "options": [
    {"id": "A", "is_key": false, "label": "Evaluate the integrand at the upper limit and stop", "error_path": "BC-ERR-06027"},
    {"id": "B", "is_key": true, "label": "Differentiate the accumulation function with the chain rule", "error_path": null},
    {"id": "C", "is_key": false, "label": "Write the accumulation as a definite integral with a variable upper limit", "error_path": "BC-ERR-06028"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06019"]
  },
  {
   "id": "chk-2",
   "check_kind": "discrimination",
   "format": "mcq",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06012",
   "parameter_draw": {"integrand": "sin(t)", "lower": 1, "upper_limit": "3x", "task": "name the method 2"},
   "stem": {"text": "\\(G\\) is the accumulation of \\(\\sin t\\) from 1 to \\(3x\\). Name the method that gives \\(G(x)\\).", "command_verb": "name"},
   "key": {"form": "statement", "expr": "write"},
   "options": [
    {"id": "A", "is_key": true, "label": "Write the accumulation as a definite integral with a variable upper limit", "error_path": null},
    {"id": "B", "is_key": false, "label": "Differentiate the accumulation function with the chain rule", "error_path": "BC-ERR-99032"},
    {"id": "C", "is_key": false, "label": "Evaluate the integrand at the upper limit and stop", "error_path": "BC-ERR-06027"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06017"]
  },
  {
   "id": "chk-3",
   "check_kind": "discrimination",
   "format": "mcq",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06012",
   "parameter_draw": {"integrand": "sin(t)", "lower": 1, "upper_limit": "3x", "task": "name the method 3"},
   "stem": {"text": "For \\(H(x)=\\int_1^{3x}\\sin t\\,dt\\), name the method that gives \\(H'(x)\\).", "command_verb": "name"},
   "key": {"form": "statement", "expr": "chain"},
   "options": [
    {"id": "A", "is_key": false, "label": "Write the accumulation as a definite integral with a variable upper limit", "error_path": "BC-ERR-06028"},
    {"id": "B", "is_key": false, "label": "Evaluate the integrand at the upper limit and stop", "error_path": "BC-ERR-06027"},
    {"id": "C", "is_key": true, "label": "Differentiate the accumulation function with the chain rule", "error_path": null}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06019"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5", "sources": []},
  {"block": "stems", "mode": "contrast", "reason": "plan 15 decision lessons: the stems side by side with the selecting feature marked", "sources": ["BC-QA-06012"]}
 ],
 "refresher": ["st-1", "st-2"],
 "read_minutes": {"full": 2.4, "brief": 1.6},
 "word_count": {"full": 343, "brief": 237},
 "research_lines": [],
 "inferred": [
  {"claim": "st-1 rests on BC-SKL-06017's adaptive.mastered_if because no active archetype asks only for the accumulation written as an integral.", "settles": "A library staging pass minting that archetype."},
  {"claim": "The integrand graph is not drawn on the contrast screen.", "settles": "The modality A/B in the build plan."}
 ],
 "sources": ["BC-SKL-06017", "BC-SKL-06019", "BC-EK-FUN-5A1", "BC-EK-FUN-5A2", "ced:121", "BC-QA-06012", "BC-PT-99024", "BC-PT-99004", "BC-ERR-06027", "BC-ERR-06028", "BC-ERR-99032", "research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions", "research/exam/exam-structure.md#Section and part layout"]
}
```
