---
title: LSN-CON-02003 The derivative as a function defined by a limit
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02003, the derivative as a function defined by a limit, built from authoring_bundle("BC-CON-02003") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02003 The derivative as a function defined by a limit

Concept BC-CON-02003 (skills BC-SKL-02008, BC-SKL-02009), topic 2.2 of Unit 2, loaded by BC-QA-02002 only. Its hard parent is BC-CON-02002 (unit README section 1); BC-CON-02006 holds it as a supporting parent.

## Prediction

One multiple choice question on worked example 1's own function, \(f(x)=-x^2+5x+4\), asked before the rule is shown: what the limit of the difference quotient produces as \(h\to0\) with \(x\) left a letter. The key is \(-2x+5\), a function of \(x\) (ex-1's third valued step); the distractors are the value 0, from the numerator vanishing, and the simplified quotient \(-2x-h+5\) with \(h\) still in it. The resolution, shown on the key idea screen beside the student's choice, names the result as the derivative function and gives its value at 3. No verdict word. Sources: BC-CON-02003 and the topic 2.2 section the key idea cites.

## Orientation

Served text (43 words), from BC-CON-02003 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation): the response writes the limit of the difference quotient at a general input, expands, divides out the increment with the limit carried, and takes the limit. No count, no frequency.

## Key ideas

BC-SKL-02008 maps BC-EK-CHA-2B2 and BC-SKL-02009 maps BC-EK-CHA-2B1 and BC-EK-CHA-2B2, so two blocks.

- ki-1 (core, BC-EK-CHA-2B2, ced:61). The derivative as the function whose value at \(x\) is the limit of the quotient; the result is a rule in \(x\); the Method paragraph of topic 2.2 (divide out the increment before the limit). Anchor quote (9 words) from ced:61. Notation line: f prime of x.
- ki-2 (extended, BC-EK-CHA-2B1). The same limit at one input gives a number, in either form; the function evaluated at \(a\) and the limit at \(a\) agree. No quote: the EK's page, ced:60, is not in this bundle's `ced_pages`.

## Recognition

- BC-QA-02002 (family derivative-definition-limit, MCQ or one part, no calculator; research/question-analysis/question-archetypes.md#BC-QA-02002 Derivative computed from the limit definition): `typical_wording` "Use the definition of the derivative to find the derivative of the given function, or its value at the named input"; `common_givens` a function rule; `asked_to_produce` a difference quotient inside a limit, and the derivative function or its value. The signal is the word definition with no input named, or with the function asked first. Official example BC-MCQ-SAMPLE-006.

Contrast pair on st-1: this stem is on BC-QA-02002 with the word definition and no input named; not this stem is the same function with no definition demanded, where a differentiation rule is allowed (the `wrong_approaches` entry of the power rule presented as the definition, and the rule concepts from BC-CON-02010). The separating feature is the word definition.

What says "not this concept": the stem names no definition (a rule is allowed, BC-CON-02010 onward); the limit is already written and asks to be evaluated (BC-CON-02006); one input and a rate asked in context (BC-CON-02002).

## Method choice

- st-1, BC-QA-02002, low and mid bands. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: write the difference quotient for the given rule, at a general \(x\). Rival, `wrong_approaches`: differentiating by the power rule and presenting it as the definition (BC-ERR-02008); the second entry, zero substituted for the increment before it is divided out (BC-ERR-02005), is a trap below. Separating feature: the word definition in the stem.

The archetype carries `asked_to_produce` and `common_givens`, so the block is not tagged inferred. The `method` text carries no leading label; the rival's record id sits in the block's `sources`.

## Solution path

- ex-1, BC-QA-02002, both bands, no calculator. Draw: leading \(-1\), linear 5, constant 4, point 3, degree 2, giving \(f(x)=-x^2+5x+4\), \(f'(x)\) and then \(f'(3)\). Steps follow `expected_solution_path`: the quotient at \(x\) (new), expanded and with \(h\) divided out (equivalent), the limit \(-2x+5\) (limit, \(h\to0\)), the value at 3 (evaluate). A fluent solver writes all four lines; the expansion of \((x+h)^2\) is held in the head only when it is short.

One example: the archetype has one shape, and ex-1 already carries both the function and a value, so nothing is faded. No productive-failure comparison (BC-CON-02002 is the unit's target).

## Scoring

None. BC-QA-02002 lists no `point_types`, so no step carries a point tag and the lesson says nothing about points beyond the error records' own scoring consequences. Its `scoring_pattern` (quotient, simplification, value) is drawn from the CED, since no 2023 to 2025 free response part asks for a derivative from the definition (research/units/unit-02-differentiation-definition-properties.md#Unresolved).

## Traps

Five active errors meet the concept's skills; the cap is 4, so the first four in the bundle's order are shown. Low band all four, mid band the first two.

- err-BC-ERR-02005 (BC-MIS-02002, BC-MIS-02003). Wrong step on ex-1's draw: \(h=0\) in the unsimplified quotient, \(\frac{0}{0}\). Right step: \(-2x-h+5\), then the limit \(-2x+5\). Distinct. Possible reason from BC-MIS-02002.
- err-BC-ERR-02006 (BC-MIS-02003, BC-MIS-02002). Wrong: \(f'(x)=-2x-h+5\) with no limit. Right: \(\lim_{h\to0}(-2x-h+5)=-2x+5\). Distinct. Possible reason from BC-MIS-02003.
- err-BC-ERR-02007 (BC-MIS-02003, BC-MIS-02011). Wrong: \(-(x+h)^2\) taken as \(-x^2-h^2\), quotient \(5-h\). Right: \(-2x-h+5\). Distinct. Possible reason null: neither linked description names the shifted term.
- err-BC-ERR-02008 (BC-MIS-02002, BC-MIS-02004). Wrong: the limit written, then \(-2x+5\) at once by the power rule, with no quotient line. Right: the simplified quotient \(-2x-h+5\) inside the limit, the line the lost points attach to. Distinct: the right step shows the missing work, while the final value may be right, which is the record's point. Possible reason from BC-MIS-02002.

BC-ERR-02030 is the fifth and is taught in LSN-CON-02002 and LSN-CON-02004.

## Representations

None. Topic 2.2's Representations paragraph names limit definition to a derivative value (BC-REP-01 to BC-REP-01), which is symbolic, and the concept's skills carry BC-REP-01 only.

## Prerequisite bridge

- BC-PRQ-02005 (supporting parent of BC-SKL-02008): \(f(x+h)\) is \(f\) at the shifted input, with \(x\) as the base.
- BC-PRQ-02001 (supporting parent of BC-SKL-02009): expand, subtract, divide out the common factor, from its `failure_signature` (a quotient written but not reduced).

## Time

BC-QA-02002 is `no_calculator` and MCQ shaped: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). A fluent solver writes four lines: the quotient inside the limit, the simplified quotient with the limit kept, the limit, the value.

## Checks

- chk-1, completion of ex-1, both bands: \(f'(x)=-2x+5\) is given, the value at 3 is asked. Key \(-1\), equal to ex-1's answer.
- chk-2, isomorph on BC-QA-02002, both bands: leading 1, linear \(-2\), constant 3, point \(-2\), degree 2. Key \(-6\).
- chk-3, MCQ on BC-QA-02002, low band: leading 3, linear \(-1\), constant 2, point 1, degree 2. Key 5. Distractors: \(-1\) (BC-ERR-02007, \((1+h)^2\) taken as \(1+h^2\), the slip the spec's notes name), \(\infty\) (BC-ERR-02007, \(f(1+h)\) taken as \(f(1)+f(h)\), so the quotient \(3h-1+\frac{2}{h}\) grows without bound), undefined (BC-ERR-02005, \(h\) set to 0 while still in the denominator, giving \(\frac00\)) [inferred: the record does not state the value reported].

No draw equals a published BC-QA-02002 `parameter_draw` (content/items_gen_unit02, content/items_unit02_agent).

## Delivery

- orientation, ki-1, ki-2: text. Rule 5; the skills carry BC-REP-01 only and the key ideas are the algebra of the quotient (unit README delivery map).
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-02005, err-BC-ERR-02006, err-BC-ERR-02007, err-BC-ERR-02008: step_reveal. Rule 1.

No drawn block: none of rules 2 to 5 applies. The skills carry BC-REP-01 only, so rules 4 and 5 do not select a figure or a table, and the key ideas describe algebra on a quotient, not a process to draw, so rules 2 and 3 do not select motion or an interactive. The machine record states `no_figure_reason`. The prediction is delivered as text.

## Band plan

- Low (full), in served order: prediction, orientation, the two bridges, ki-1, ki-2, st-1 with its contrast pair, ex-1, chk-1, the four error blocks, chk-2, chk-3. 589 words, 4.0 minutes (cap 900 and 6). There is no example 2, so nothing is faded.
- Mid (brief): prediction, orientation, the bridges, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-02005, err-02006, chk-2. 431 words, 2.9 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02005, err-BC-ERR-02006, err-BC-ERR-02007, err-BC-ERR-02008, ex-1.

## Sources

- BC-CON-02003; BC-SKL-02008, BC-SKL-02009; BC-EK-CHA-2B2, BC-EK-CHA-2B1; ced:61, ced:60
- BC-QA-02002; BC-MCQ-SAMPLE-006
- BC-ERR-02005, BC-ERR-02006, BC-ERR-02007, BC-ERR-02008, BC-ERR-02030; BC-MIS-02002, BC-MIS-02003, BC-MIS-02004, BC-MIS-02011
- BC-PRQ-02001, BC-PRQ-02005
- research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation
- research/units/unit-02-differentiation-definition-properties.md#Unresolved
- research/question-analysis/question-archetypes.md#BC-QA-02002 Derivative computed from the limit definition
- research/exam/exam-structure.md#Section and part layout
- [inferred] chk-3's distractor undefined for BC-ERR-02005: the record says the increment is set to zero while in the denominator, giving 0/0, not what is then reported. Settled by a `common_distractors` value on BC-QA-02002 for that error.

## Machine record

```json
{
 "id": "LSN-CON-02003",
 "kind": "concept",
 "target_id": "BC-CON-02003",
 "unit": "02",
 "skills": ["BC-SKL-02008", "BC-SKL-02009"],
 "prediction": {
  "id": "pr-1",
  "stem": {"text": "Predict. Let \\(f(x)=-x^2+5x+4\\) and let \\(h\\to0\\) in \\(\\frac{f(x+h)-f(x)}{h}\\), keeping \\(x\\) a letter. What is the limit?", "command_verb": "predict"},
  "format": "mcq",
  "options": [
   {"id": "A", "label": "\\(-2x+5\\), a function of \\(x\\)", "is_key": true},
   {"id": "B", "label": "\\(0\\), since the numerator vanishes", "is_key": false},
   {"id": "C", "label": "\\(-2x-h+5\\), which still holds \\(h\\)", "is_key": false}
  ],
  "resolution": "The limit is the derivative function, \\(f'(x)=-2x+5\\), a rule in \\(x\\). Its value at 3 is \\(-1\\).",
  "sources": ["BC-CON-02003", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation"]
 },
 "no_figure_reason": "The concept is the algebra of a difference quotient at a general input. Its skills carry only a symbolic representation and no key idea describes a process to draw, so no figure fits.",
 "orientation": {
  "text": "A response writes the derivative as a function: the limit as \\(h\\to0\\) of \\(\\frac{f(x+h)-f(x)}{h}\\), expanded, with \\(h\\) divided out and the limit carried on every line, then taken. When the stem says use the definition, the quotient and its simplification are the work.",
  "sources": ["BC-CON-02003", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-2B2",
   "depth": "core",
   "text": "The derivative of \\(f\\) is the function whose value at \\(x\\) is \\(\\lim_{h\\to0}\\frac{f(x+h)-f(x)}{h}\\), provided the limit exists. The input stays a letter, so the result is a rule, \\(f'(x)\\). At \\(h=0\\) the quotient is \\(\\frac{0}{0}\\): expand \\(f(x+h)\\), subtract, divide out \\(h\\), then let \\(h\\to0\\).",
   "notation": "f prime of x",
   "quote": {"text": "The derivative of f is the function whose value", "source": "ced:61"},
   "sources": ["BC-EK-CHA-2B2", "ced:61", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-2B1",
   "depth": "extended",
   "text": "At one input the same limit gives a number: \\(f'(a)=\\lim_{h\\to0}\\frac{f(a+h)-f(a)}{h}\\), or \\(\\lim_{x\\to a}\\frac{f(x)-f(a)}{x-a}\\). Substituting \\(a\\) into \\(f'(x)\\) gives the same number.",
   "notation": "f prime of a",
   "quote": null,
   "sources": ["BC-EK-CHA-2B1", "ced:60", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-02002",
   "cue": "A function rule; the stem says use the definition to find the derivative, or its value.",
   "method": "\\(\\lim_{h\\to0}\\frac{f(x+h)-f(x)}{h}\\) with the rule substituted.",
   "rival": "The power rule's result with the definition copied around it.",
   "separating_feature": "The word definition: the quotient and its simplification carry the work.",
   "contrast": {
    "this": {"text": "Let \\(g(x)=x^2+3x\\). Use the definition of the derivative to find \\(g'(x)\\).", "archetype_id": "BC-QA-02002"},
    "not_this": {"text": "Let \\(g(x)=x^2+3x\\). Find \\(g'(x)\\).", "why_not": "No definition is demanded, so a differentiation rule is allowed."},
    "feature": "The word definition in the stem."
   },
   "sources": ["BC-QA-02002", "BC-ERR-02008"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-02002",
   "bands": ["low", "mid"],
   "parameter_draw": {"leading": -1, "linear": 5, "constant": 4, "point": 3, "degree": 2},
   "problem": {"text": "Let \\(f(x)=-x^2+5x+4\\). Use the definition of the derivative to find \\(f'(x)\\), then \\(f'(3)\\).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "The stem says definition and asks for \\(f'(x)\\).", "why": "Keep \\(x\\) a letter: \\(\\lim_{h\\to0}\\frac{f(x+h)-f(x)}{h}\\).", "expr": "(-(x+h)**2 + 5*(x+h) + 4 - (-x**2 + 5*x + 4))/h", "relation": "new"},
    {"cue": "At \\(h=0\\) this is \\(\\frac{0}{0}\\): expand \\((x+h)^2\\) in full.", "why": "The numerator is \\(-2xh-h^2+5h\\); dividing out \\(h\\) leaves \\(-2x-h+5\\).", "expr": "-2*x - h + 5", "relation": "equivalent"},
    {"cue": "No \\(h\\) is left in a denominator, so let \\(h\\to0\\).", "why": "The limit is the derivative function.", "expr": "-2*x + 5", "relation": "limit", "variable": "h", "point": "0"},
    {"cue": "The stem then asks for \\(f'(3)\\).", "why": "Substitute into the function: \\(-6+5\\).", "expr": "-1", "relation": "evaluate", "subs": {"x": "3"}}
   ],
   "answer": {"form": "numeric", "expr": "-1"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-02005",
   "observed_behavior": "The response substitutes zero for the increment while it is still in the denominator.",
   "scoring_consequence": "The simplification point and the value point are both lost.",
   "wrong_step": {"text": "\\(h=0\\) in \\(\\frac{-2xh-h^2+5h}{h}\\) gives \\(\\frac{0}{0}\\).", "expr": "(-2*x*0 - 0**2 + 5*0)/0"},
   "right_step": {"text": "Divide out \\(h\\) first: \\(-2x-h+5\\), limit \\(-2x+5\\).", "expr": "-2*x + 5"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-02002", "text": "the increment is set to zero immediately"},
   "sources": ["BC-ERR-02005", "BC-MIS-02002"]
  },
  {
   "error_id": "BC-ERR-02006",
   "observed_behavior": "The response manipulates the difference quotient without carrying the limit symbol and attaches it only to the final line.",
   "scoring_consequence": "A notation point is lost where the definition itself is being assessed.",
   "wrong_step": {"text": "\\(f'(x)=-2x-h+5\\), no limit written.", "expr": "-2*x - h + 5"},
   "right_step": {"text": "\\(\\lim_{h\\to0}(-2x-h+5)=-2x+5\\).", "expr": "-2*x + 5"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-02003", "text": "intermediate lines assert equalities that are false before the limit is taken"},
   "sources": ["BC-ERR-02006", "BC-MIS-02003"]
  },
  {
   "error_id": "BC-ERR-02007",
   "observed_behavior": "The response expands the function evaluated at the shifted input as though the function distributed over the sum.",
   "scoring_consequence": "The simplification point and the value point are both lost.",
   "wrong_step": {"text": "\\(-(x+h)^2\\) taken as \\(-x^2-h^2\\); the quotient becomes \\(5-h\\).", "expr": "5 - h"},
   "right_step": {"text": "\\(-(x+h)^2=-x^2-2xh-h^2\\); the quotient is \\(-2x-h+5\\).", "expr": "-2*x - h + 5"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": ["BC-ERR-02007"]
  },
  {
   "error_id": "BC-ERR-02008",
   "observed_behavior": "The response differentiates with the power rule and presents the result as an application of the definition.",
   "scoring_consequence": "The points attached to the difference quotient and its simplification are lost although the final value may be right.",
   "wrong_step": {"text": "The limit is written, then \\(-2x+5\\) at once by the power rule, with no quotient line.", "expr": "-2*x + 5"},
   "right_step": {"text": "The quotient simplified to \\(-2x-h+5\\) inside the limit: the line the lost points attach to.", "expr": "-2*x - h + 5"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-02002", "text": "the answer is produced by a rule and the definition is copied around it"},
   "sources": ["BC-ERR-02008", "BC-MIS-02002"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-02005", "text": "\\(f(x+h)\\) is \\(f\\) at the shifted input \\(x+h\\); \\(x\\) is the base."},
  {"prq_id": "BC-PRQ-02001", "text": "Expand, subtract, divide out the common factor: a quotient not reduced cannot have \\(h\\) set to zero."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 3, 4]}, "skipped_steps": {"ex-1": []}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-02002",
   "parameter_draw": {"leading": -1, "linear": 5, "constant": 4, "point": 3, "degree": 2},
   "completes": "ex-1",
   "stem": {"text": "The definition gives \\(f'(x)=-2x+5\\). Find \\(f'(3)\\).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "-1"},
   "steps": [
    {"text": "\\(f'(x)=-2x+5\\).", "expr": "-2*x + 5", "relation": "new"},
    {"text": "At 3: \\(-1\\).", "expr": "-1", "relation": "evaluate", "subs": {"x": "3"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02009"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-02002",
   "parameter_draw": {"leading": 1, "linear": -2, "constant": 3, "point": -2, "degree": 2},
   "stem": {"text": "Let \\(f(x)=x^2-2x+3\\). Use the definition of the derivative to find \\(f'(x)\\), then \\(f'(-2)\\).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "-6"},
   "steps": [
    {"text": "The quotient at \\(x\\).", "expr": "((x+h)**2 - 2*(x+h) + 3 - (x**2 - 2*x + 3))/h", "relation": "new"},
    {"text": "Simplified: \\(2x+h-2\\).", "expr": "2*x + h - 2", "relation": "equivalent"},
    {"text": "Limit: \\(2x-2\\).", "expr": "2*x - 2", "relation": "limit", "variable": "h", "point": "0"},
    {"text": "At \\(-2\\): \\(-6\\).", "expr": "-6", "relation": "evaluate", "subs": {"x": "-2"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02008", "BC-SKL-02009"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-02002",
   "parameter_draw": {"leading": 3, "linear": -1, "constant": 2, "point": 1, "degree": 2},
   "stem": {"text": "Let \\(f(x)=3x^2-x+2\\). Using the definition of the derivative, what is \\(f'(1)\\)?", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "5"},
   "steps": [
    {"text": "The quotient at 1, with \\(f(1)=4\\).", "expr": "(3*(1+h)**2 - (1+h) + 2 - 4)/h", "relation": "new"},
    {"text": "Simplified: \\(3h+5\\).", "expr": "3*h + 5", "relation": "equivalent"},
    {"text": "Limit: 5.", "expr": "5", "relation": "limit", "variable": "h", "point": "0"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "-1", "error_path": "BC-ERR-02007", "derivation": "(1 + h)^2 taken as 1 + h^2: the quotient is 3h - 1, limit -1"},
    {"id": "B", "is_key": true, "expr": "5", "error_path": null},
    {"id": "C", "is_key": false, "expr": "oo", "error_path": "BC-ERR-02007", "derivation": "f(1 + h) taken as f(1) + f(h): the quotient is 3h - 1 + 2/h, which grows without bound as h shrinks to 0 from the right"},
    {"id": "D", "is_key": false, "expr": "nan", "error_path": "BC-ERR-02005", "derivation": "h set to 0 while still in the denominator: the quotient is 0/0, reported as undefined"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02009"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: skills BC-SKL-02008 and BC-SKL-02009 carry BC-REP-01 only", "sources": ["BC-SKL-02008"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 5: the key idea is the algebra of the difference quotient (unit README delivery map)", "sources": ["BC-SKL-02008"]},
  {"block": "ki-2", "mode": "text", "reason": "rule 5: BC-REP-01 only", "sources": ["BC-SKL-02009"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02005", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02006", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02007", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02008", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-02005", "err-BC-ERR-02006", "err-BC-ERR-02007", "err-BC-ERR-02008", "ex-1"],
 "read_minutes": {"full": 4.0, "brief": 2.9},
 "word_count": {"full": 589, "brief": 431},
 "research_lines": [
  {"file": "research/units/unit-02-differentiation-definition-properties.md", "line": "The derivative of f is the function whose value at x is the limit as h tends to zero of the quotient of f(x plus h) minus f(x) by h, provided this limit exists"}
 ],
 "inferred": [
  {"claim": "chk-3's distractor undefined for BC-ERR-02005: the record says the increment is set to zero while in the denominator, giving 0/0, not what is then reported.", "settles": "A common_distractors value on BC-QA-02002 tied to BC-ERR-02005."}
 ],
 "sources": ["BC-CON-02003", "BC-SKL-02008", "BC-SKL-02009", "BC-EK-CHA-2B2", "BC-EK-CHA-2B1", "ced:61", "ced:60", "BC-QA-02002", "BC-MCQ-SAMPLE-006", "BC-ERR-02005", "BC-ERR-02006", "BC-ERR-02007", "BC-ERR-02008", "BC-ERR-02030", "BC-MIS-02002", "BC-MIS-02003", "BC-MIS-02004", "BC-MIS-02011", "BC-PRQ-02001", "BC-PRQ-02005", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation", "research/units/unit-02-differentiation-definition-properties.md#Unresolved", "research/exam/exam-structure.md#Section and part layout"]
}
```
