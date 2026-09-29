---
title: LSN-CON-02006 Recognising a limit as a derivative of a known function
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02006, recognising a limit as the derivative of a known function, built from authoring_bundle("BC-CON-02006") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02006 Recognising a limit as a derivative of a known function

Concept BC-CON-02006 (skill BC-SKL-02035), topic 2.7 of Unit 2, loaded by BC-QA-02003 only. Its hard parent is BC-CON-02002 and its supporting parent BC-CON-02003 (unit README section 1).

## Prediction

Served first, both bands, on ex-1's numbers (source BC-CON-02006 and the topic's 2.7 section, research/units/unit-02-differentiation-definition-properties.md#2.7 Derivatives of cos x, sin x, e^x, and ln x). Form `mcq`, three options, key: the limit is the slope of \(y=4\sqrt{x}\) at \(x=9\). The distractors are the two readings the errors below record, a limit that does not exist and the function value 12. The resolution states what the reading gives and why, without a verdict word.

## Orientation

Served text (48 words), from BC-CON-02006 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.7 Derivatives of cos x, sin x, e^x, and ln x): justification variants identify the underlying function and base point of a recognised limit, so a response names both, states the limit as the derivative there, and evaluates by the rule. No count, no frequency.

## Key ideas

BC-SKL-02035 maps BC-EK-LIM-3A1 (ced:66), so one core block, both bands.

- ki-1 (core). The recognition, paraphrased from the topic's "Limit read as a derivative" paragraph, with the specific rules from its "Specific rules" paragraph (BC-EK-FUN-3A4, the EK of the neighbouring skills on the same page) supplying the derivative values for sine, cosine, the natural exponential and the natural logarithm only, the scope of that EK. Anchor quote (23 words) from ced:66. The concept's `notation` field is empty, so the notation line is empty.

## Recognition

- BC-QA-02003 (family derivative-definition-limit, MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-02003 Limit recognised as a derivative of a known function): `typical_wording` "Evaluate the given limit"; `common_givens` a limit in difference quotient form; `asked_to_produce` the value of the limit. The signal is the shape: substitution gives \(\frac{0}{0}\), and the numerator is a known function at a shifted input minus the same function at a base input, over the shift. The archetype has no `official_examples` (none in 2023 to 2025).

The contrast pair on st-1 takes its near miss from Unit 1: a limit that also gives \(\frac{0}{0}\) but whose numerator is not a difference of one function's values, so algebra resolves it (BC-SKL-01024 is `confusable_with` on BC-SKL-02035). The `this` stem is a fresh draw on BC-QA-02003, an exponential at base 2.

What says "not this concept": the numerator is not a difference of one function's values (a Unit 1 limit, rewritten by algebra); the stem says use the definition on a rule (BC-CON-02003); a rate at an instant in context (BC-CON-02002).

## Method choice

- st-1, BC-QA-02003, low and mid bands. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`, written without a leading label: the numerator compared with a difference of function values. The contrast pair rides on this block. Rival, `wrong_approaches`: treating the difference quotient form as unresolvable and reporting that the limit does not exist (BC-ERR-02009). Separating feature: the constant in the numerator is a value of the same function at the base point.

The archetype carries `asked_to_produce` and `common_givens`, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-02003, both bands, no calculator. Draw: family sqrt, base_index 1 (base 9 in the template's list), coefficient 4, increment h, shape increment, giving \(\lim_{h\to0}\frac{4\sqrt{9+h}-12}{h}\). Steps follow `expected_solution_path`: compare and identify \(f(x)=4\sqrt{x}\) (valued, new), state the limit as \(f'(9)\) with the rule's \(f'(x)\) (differentiate), evaluate at 9 (evaluate). A fluent solver writes the function with the base point and the value, and holds the numerator comparison in the head (unit README section 5).

## Scoring

None. BC-QA-02003 lists no `point_types`, so no step carries a point tag and the lesson says nothing about points beyond the error records' own scoring consequences.

## Traps

Three active errors meet the concept's skill and are shown, in the bundle's order: the first two in both bands, BC-ERR-02024 in the low band only. BC-ERR-02024 is held by BC-SKL-02035; its record places a function value in a product or quotient rule position that calls for a derivative value. On this draw the same swap shows as \(f(9)\) reported where \(f'(9)\) is the limit; that carry-over is [inferred].

- err-BC-ERR-02009 (BC-MIS-02004, BC-MIS-02002). Wrong step on ex-1's draw: \(\frac{0}{0}\) reported as a limit that does not exist. Right: \(f'(9)=\frac{2}{3}\). Distinct. Possible reason from BC-MIS-02004.
- err-BC-ERR-02010 (BC-MIS-02004, BC-MIS-02014). Wrong: the constant 12 taken as the base point, \(f'(12)=\frac{2}{\sqrt{12}}\). Right: \(\frac{2}{3}\). Distinct. Possible reason null: neither linked description names the misread base.
- err-BC-ERR-02024 (BC-MIS-02011, BC-MIS-02014). Wrong: \(f(9)=4\sqrt{9}=12\) reported as the limit. Right: \(f'(9)=\frac{2}{3}\). Distinct. Possible reason from BC-MIS-02014.

## Representations

None. The topic's Representations paragraph names BC-REP-01 only, a limit to a derivative value.

## Prerequisite bridge

- BC-PRQ-02005 (supporting parent of BC-SKL-02035), from `description_plain` and `failure_signature`: which input the limit is built around.

## Time

BC-QA-02003 is `no_calculator` and MCQ shaped: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). A fluent solver writes two lines, the function with its base point and the value.

## Checks

- chk-1, completion of ex-1, both bands: \(f\) and \(f'\) are given. Key \(\frac{2}{3}\), equal to ex-1's answer.
- chk-2, isomorph on BC-QA-02003, both bands: family ln, base_index 2 (base \(\frac{1}{2}\)), coefficient 3, increment t, shape increment. Key 6.
- chk-3, MCQ on BC-QA-02003, low band: family sin, base_index 1 (base \(\frac{\pi}{3}\)), coefficient 2, increment h, shape increment. Statement key "The limit is 1", as the archetype's `invariants` require ("'The limit is' in key"). Distractors: 2 (BC-ERR-02010, \(2\cos x\) evaluated at 0, the value the increment approaches), \(2\cos\sqrt{3}\) (BC-ERR-02010, the constant taken as the base), does not exist (BC-ERR-02009).

No draw equals a published BC-QA-02003 `parameter_draw` (content/items_gen_unit02, content/items_unit02_agent).

## Delivery

- orientation, ki-1: text. Rule 5; BC-SKL-02035 carries BC-REP-01 only (unit README delivery map).
- No drawn block: `no_figure_reason` states it. The skill carries BC-REP-01 only and no key idea describes a process.
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-02009, err-BC-ERR-02010: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, the bridge, ki-1, st-1 with the contrast pair, ex-1, chk-1, the three error blocks, chk-2, chk-3. 492 words, 3.3 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, the bridge, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-02009, err-02010, chk-2. 423 words, 2.9 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02009, err-BC-ERR-02010, err-BC-ERR-02024, ex-1.

## Sources

- BC-CON-02006; BC-SKL-02035; BC-EK-LIM-3A1, BC-EK-FUN-3A4; ced:66
- BC-QA-02003; BC-SKL-01024 (the contrast near miss)
- BC-ERR-02009, BC-ERR-02010, BC-ERR-02024; BC-MIS-02002, BC-MIS-02004, BC-MIS-02014
- BC-PRQ-02005
- research/units/unit-02-differentiation-definition-properties.md#2.7 Derivatives of cos x, sin x, e^x, and ln x
- research/question-analysis/question-archetypes.md#BC-QA-02003 Limit recognised as a derivative of a known function
- research/exam/exam-structure.md#Section and part layout
- [inferred] The base points behind base_index come from the generation template for BC-QA-02003, not from the parameter_spec. Settled by the base list in the spec.
- [inferred] BC-ERR-02024's function value in a derivative position shown as \(f(9)\) reported for the limit, outside a product or quotient rule. Settled by an error record scoped to difference quotient limits.

## Machine record

```json
{
 "id": "LSN-CON-02006",
 "kind": "concept",
 "target_id": "BC-CON-02006",
 "unit": "02",
 "skills": ["BC-SKL-02035"],
 "prediction": {
  "id": "pr-1",
  "stem": {"text": "Predict before the rule: \\(\\lim_{h\\to0}\\frac{4\\sqrt{9+h}-12}{h}\\) gives \\(\\frac{0}{0}\\) at \\(h=0\\). What is the limit?", "command_verb": "predict"},
  "format": "mcq",
  "options": [
   {"id": "A", "label": "It does not exist, because substitution gives \\(\\frac{0}{0}\\).", "is_key": false},
   {"id": "B", "label": "The slope of \\(y=4\\sqrt{x}\\) at \\(x=9\\).", "is_key": true},
   {"id": "C", "label": "The value 12, since \\(4\\sqrt{9}=12\\).", "is_key": false}
  ],
  "resolution": "The numerator is \\(f(9+h)-f(9)\\) for \\(f(x)=4\\sqrt{x}\\), so the limit is \\(f'(9)=\\frac{2}{3}\\), a slope. A \\(\\frac{0}{0}\\) form of this shape has a value.",
  "sources": ["BC-CON-02006", "research/units/unit-02-differentiation-definition-properties.md#2.7 Derivatives of cos x, sin x, e^x, and ln x"]
 },
 "no_figure_reason": "The concept is a symbolic reading of a limit. Its one skill carries BC-REP-01 only and no key idea describes a process, so no figure, table or motion fits.",
 "orientation": {
  "text": "A response reads a limit shaped like a difference quotient as a derivative already known: it names the function and the base point, states the limit as that derivative there, and evaluates by the rule. Substitution gives \\(\\frac{0}{0}\\); that form does not mean the limit fails to exist.",
  "sources": ["BC-CON-02006", "research/units/unit-02-differentiation-definition-properties.md#2.7 Derivatives of cos x, sin x, e^x, and ln x"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-3A1",
   "depth": "core",
   "text": "If the numerator is a known function at a shifted input minus the same function at the base, over the shift, the limit is that function's derivative at the base Match \\(\\frac{f(a+h)-f(a)}{h}\\) or \\(\\frac{f(x)-f(a)}{x-a}\\), name \\(f\\) and \\(a\\), then use the rule: \\((\\sin x)'=\\cos x\\), \\((\\cos x)'=-\\sin x\\), \\((e^x)'=e^x\\), \\((\\ln x)'=\\frac{1}{x}\\).",
   "notation": "",
   "quote": {"text": "recognizing an expression for the definition of the derivative of a function whose derivative is known offers a strategy for determining a limit", "source": "ced:66"},
   "sources": ["BC-EK-LIM-3A1", "BC-EK-FUN-3A4", "ced:66", "research/units/unit-02-differentiation-definition-properties.md#2.7 Derivatives of cos x, sin x, e^x, and ln x"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-02003",
   "cue": "A limit in difference quotient form; the stem asks for its value.",
   "method": "Compare the numerator with a difference of values of a known function.",
   "rival": "Rival: \\(\\frac{0}{0}\\) read as unresolvable, the limit reported as nonexistent.",
   "separating_feature": "The constant in the numerator is the same function's value at the base.",
   "sources": ["BC-QA-02003"],
   "evidence_tag": "verified",
   "contrast": {
    "this": {"text": "Find \\(\\lim_{h\\to0}\\frac{5e^{2+h}-5e^{2}}{h}\\).", "archetype_id": "BC-QA-02003"},
    "not_this": {"text": "Find \\(\\lim_{h\\to0}\\frac{h^2+5h}{h}\\).", "why_not": "The numerator is not a difference of one function's values, so factoring and cancelling \\(h\\) resolves it."},
    "feature": "A numerator that subtracts the same function's value at the base point."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-02003",
   "bands": ["low", "mid"],
   "parameter_draw": {"family": "sqrt", "base_index": 1, "coefficient": 4, "increment": "h", "shape": "increment"},
   "problem": {"text": "Find \\(\\lim_{h\\to0}\\frac{4\\sqrt{9+h}-12}{h}\\).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Substitution gives \\(\\frac{0}{0}\\), and the numerator holds a shifted and a base value.", "why": "\\(12=4\\sqrt{9}\\): the numerator is \\(f(9+h)-f(9)\\) for \\(f(x)=4\\sqrt{x}\\).", "expr": "4*sqrt(x)", "relation": "new"},
    {"cue": "That numerator over \\(h\\) is the definition of \\(f'(9)\\).", "why": "The rule gives \\(f'(x)=\\frac{2}{\\sqrt{x}}\\).", "expr": "2/sqrt(x)", "relation": "differentiate", "variable": "x"},
    {"cue": "The base point is 9, the input inside the root at \\(h=0\\).", "why": "\\(f'(9)=\\frac{2}{3}\\).", "expr": "2/3", "relation": "evaluate", "subs": {"x": "9"}}
   ],
   "answer": {"form": "numeric", "expr": "2/3"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-02009",
   "observed_behavior": "The response treats a limit having the shape of a difference quotient as indeterminate and unresolvable.",
   "scoring_consequence": "The value point is lost.",
   "wrong_step": {"text": "Substitution gives \\(\\frac{0}{0}\\), reported as: the limit does not exist.", "expr": "(4*sqrt(9+0) - 12)/0"},
   "right_step": {"text": "The limit is \\(f'(9)=\\frac{2}{3}\\).", "expr": "2/3"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-02004", "text": "a difference quotient whose underlying derivative is known is not recognised as such"},
   "sources": ["BC-ERR-02009", "BC-MIS-02004"]
  },
  {
   "error_id": "BC-ERR-02010",
   "observed_behavior": "The response identifies the underlying function correctly but evaluates its derivative at the wrong input.",
   "scoring_consequence": "The value point is lost.",
   "wrong_step": {"text": "The constant 12 taken as the base: \\(f'(12)=\\frac{2}{\\sqrt{12}}\\).", "expr": "2/sqrt(12)"},
   "right_step": {"text": "The base is 9: \\(f'(9)=\\frac{2}{3}\\).", "expr": "2/3"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": ["BC-ERR-02010"]
  },
  {
   "error_id": "BC-ERR-02024",
   "observed_behavior": "The response substitutes the value of a function into a position in the product or quotient rule that calls for the value of its derivative.",
   "scoring_consequence": "The value point is lost.",
   "wrong_step": {"text": "The height \\(f(9)=4\\sqrt{9}=12\\) reported as the limit.", "expr": "4*sqrt(9)"},
   "right_step": {"text": "The slope \\(f'(9)=\\frac{2}{3}\\) is the limit.", "expr": "2/3"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-02014", "text": "the height is used as a slope"},
   "sources": ["BC-ERR-02024", "BC-MIS-02014"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-02005", "text": "The base point is the input left when the increment is 0; the constant in the numerator is \\(f\\) there, a value, not an input."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 3]}, "skipped_steps": {"ex-1": [2]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-02003",
   "parameter_draw": {"family": "sqrt", "base_index": 1, "coefficient": 4, "increment": "h", "shape": "increment"},
   "completes": "ex-1",
   "stem": {"text": "The limit is \\(f'(9)\\) for \\(f(x)=4\\sqrt{x}\\), and \\(f'(x)=\\frac{2}{\\sqrt{x}}\\). Find the limit.", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "2/3"},
   "steps": [
    {"text": "\\(f'(x)=\\frac{2}{\\sqrt{x}}\\).", "expr": "2/sqrt(x)", "relation": "new"},
    {"text": "At 9: \\(\\frac{2}{3}\\).", "expr": "2/3", "relation": "evaluate", "subs": {"x": "9"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02035"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-02003",
   "parameter_draw": {"family": "ln", "base_index": 2, "coefficient": 3, "increment": "t", "shape": "increment"},
   "stem": {"text": "Find \\(\\lim_{t\\to0}\\frac{3\\ln(\\frac{1}{2}+t)-3\\ln\\frac{1}{2}}{t}\\).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "6"},
   "steps": [
    {"text": "\\(f(x)=3\\ln x\\), base \\(\\frac{1}{2}\\).", "expr": "3*log(x)", "relation": "new"},
    {"text": "\\(f'(x)=\\frac{3}{x}\\).", "expr": "3/x", "relation": "differentiate", "variable": "x"},
    {"text": "\\(f'(\\frac{1}{2})=6\\).", "expr": "6", "relation": "evaluate", "subs": {"x": "1/2"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02035"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-02003",
   "parameter_draw": {"family": "sin", "base_index": 1, "coefficient": 2, "increment": "h", "shape": "increment"},
   "stem": {"text": "Find \\(\\lim_{h\\to0}\\frac{2\\sin(\\frac{\\pi}{3}+h)-\\sqrt{3}}{h}\\).", "command_verb": "find"},
   "key": {"form": "statement", "expr": "1", "label": "The limit is 1."},
   "steps": [
    {"text": "\\(f(x)=2\\sin x\\), base \\(\\frac{\\pi}{3}\\).", "expr": "2*sin(x)", "relation": "new"},
    {"text": "\\(f'(x)=2\\cos x\\).", "expr": "2*cos(x)", "relation": "differentiate", "variable": "x"},
    {"text": "\\(f'(\\frac{\\pi}{3})=1\\).", "expr": "1", "relation": "evaluate", "subs": {"x": "pi/3"}}
   ],
   "options": [
    {"id": "A", "is_key": false, "label": "The limit is 2.", "error_path": "BC-ERR-02010", "derivation": "the derivative 2cos x evaluated at 0, the value the increment approaches, instead of at the base point pi/3"},
    {"id": "B", "is_key": false, "label": "The limit is \\(2\\cos\\sqrt{3}\\).", "error_path": "BC-ERR-02010", "derivation": "the constant in the numerator, f at the base point, taken as the base point"},
    {"id": "C", "is_key": true, "label": "The limit is 1.", "error_path": null},
    {"id": "D", "is_key": false, "label": "The limit does not exist.", "error_path": "BC-ERR-02009", "derivation": "the zero over zero form taken to mean the limit does not exist"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02035"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: BC-SKL-02035 carries BC-REP-01 only", "sources": ["BC-SKL-02035"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 5: BC-REP-01 only (unit README delivery map)", "sources": ["BC-SKL-02035"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02009", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02010", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02024", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-02009", "err-BC-ERR-02010", "err-BC-ERR-02024", "ex-1"],
 "read_minutes": {"full": 3.3, "brief": 2.9},
 "word_count": {"full": 492, "brief": 423},
 "research_lines": [
  {"file": "research/units/unit-02-differentiation-definition-properties.md", "line": "justification variants identify the underlying function and base point of a recognised limit"}
 ],
 "inferred": [
  {"claim": "The base points behind base_index (9, 1/2, pi/3 here) come from the generation template for BC-QA-02003, not from the parameter_spec.", "settles": "The base list written into the BC-QA-02003 parameter_spec."},
  {"claim": "BC-ERR-02024 records a function value in a product or quotient rule position; on this draw the same swap is shown as f(9) reported for the limit.", "settles": "An error record scoped to limits recognised as difference quotients."}
 ],
 "sources": ["BC-CON-02006", "BC-SKL-02035", "BC-EK-LIM-3A1", "BC-EK-FUN-3A4", "ced:66", "BC-QA-02003", "BC-ERR-02009", "BC-ERR-02010", "BC-ERR-02024", "BC-MIS-02002", "BC-MIS-02004", "BC-MIS-02014", "BC-PRQ-02005", "research/units/unit-02-differentiation-definition-properties.md#2.7 Derivatives of cos x, sin x, e^x, and ln x", "research/exam/exam-structure.md#Section and part layout"]
}
```
