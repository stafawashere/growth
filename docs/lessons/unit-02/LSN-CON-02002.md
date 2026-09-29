---
title: LSN-CON-02002 Instantaneous rate of change as the limit of a difference quotient
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02002, the instantaneous rate of change as the limit of a difference quotient, built from authoring_bundle("BC-CON-02002") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02002 Instantaneous rate of change as the limit of a difference quotient

Concept BC-CON-02002 (skills BC-SKL-02004, BC-SKL-02005, BC-SKL-02006, BC-SKL-02007), topics 2.1 and 2.2 of Unit 2, loaded by BC-QA-02002 (listed first), BC-QA-02014, BC-QA-02003 and BC-QA-02012. Its hard parent is BC-CON-02001 (unit README section 1). It is the unit's productive-failure target: BC-QA-02014 carries BC-DF-15 in its `dial_bindings`.

## Orientation

Served text (50 words), from BC-CON-02002 `description_plain` and the Assessment behaviour paragraphs of topics 2.1 and 2.2 (research/units/unit-02-differentiation-definition-properties.md#2.1 Defining Average and Instantaneous Rates of Change at a Point; research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation): a response writes the difference quotient at the point inside a limit, simplifies it with the limit kept, and evaluates. No count, no frequency.

## Key ideas

All four skills map BC-EK-CHA-2B1 (ced:60), so one core block, both bands.

- ki-1 (core). The two limit forms at a point and that they name one number, paraphrased from the topic's Required mathematical knowledge paragraph; the secant-to-tangent reading of the limit; the Method paragraph of topic 2.2 (divide out the increment before the limit). Anchor quote (10 words) from ced:60. Notation line from the concept record: f prime of a.

## Recognition

- BC-QA-02002 (family derivative-definition-limit, MCQ or one part, no calculator; research/question-analysis/question-archetypes.md#BC-QA-02002 Derivative computed from the limit definition): `typical_wording` "Use the definition of the derivative to find the derivative of the given function, or its value at the named input"; `common_givens` a function rule; `asked_to_produce` a difference quotient inside a limit and the derivative value. The signal is the word definition. Official example BC-MCQ-SAMPLE-006.
- BC-QA-02014 (same family; research/question-analysis/question-archetypes.md#BC-QA-02014 Rate at an instant found before the derivative is defined, as a limit of average rates): `typical_wording` "at what rate is the quantity changing at the instant t equal to a named time"; `common_givens` a polynomial model in context and a named instant. The signal is one instant with no interval.
- BC-QA-02003 (same family): a limit already in difference quotient form, which BC-CON-02006 teaches; this concept supplies the reading of the quotient.
- BC-QA-02012 (family notation-translation; research/question-analysis/question-archetypes.md#BC-QA-02012 Derivative notation read or converted): a derivative in one notation, the same quantity asked in another; this concept supplies \(f'(a)\) as one number.

What says "not this concept": two endpoints named (an average, BC-CON-02001); the derivative asked as a function of \(x\) (BC-CON-02003); a rule named or no definition demanded (the rules, BC-CON-02010 onward).

## Method choice

One block per archetype family: derivative-definition-limit (BC-QA-02002 stands for the family; BC-QA-02014 and BC-QA-02003 share its first line shape) and notation-translation (BC-QA-02012). Low and mid bands, the first only in mid.

- st-1, BC-QA-02002. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: write the difference quotient for the given rule, here inside the limit at the named input. Rival, `wrong_approaches`: the power rule presented as the definition (BC-ERR-02008). Separating feature: the stem says definition.
- st-2, BC-QA-02012. Method, `expected_solution_path[0]`: identify the function and the independent variable from the supplied notation. Rival, `wrong_approaches`: Leibniz notation separated and cancelled as a fraction (BC-ERR-02029). Separating feature: \(f'(a)\) names one number at one input.

Both archetypes carry `asked_to_produce` and `common_givens`, so neither block is tagged inferred.

## Solution path

- ex-1, BC-QA-02002, both bands, no calculator. Draw: leading 2, linear \(-3\), constant 1, point 2, degree 2, giving \(f(x)=2x^2-3x+1\) and \(f'(2)\). Valued chain as the template fixes it for a limit definition: the difference quotient (new), its simplified form \(2h+5\) (equivalent), the limit 5 (limit, \(h\to0\)).
- ex-2, BC-QA-02014, low band only, no calculator. Draw: degree 2, leading 3, linear \(-4\), constant 6, instant 2, context position, giving \(s(t)=3t^2-4t+6\) and the rate at \(t=2\). Same chain: quotient over \([2,2+h]\), \(8+3h\), limit 8. This is the opener archetype's canonical path.

A fluent solver writes all three lines of each, and holds the expansion of the shifted term in the head when it is short (unit README section 5). Comparison gap for the productive-failure target: when the BC-QA-02014 opener preceded the lesson, ex-1 opens with a comparison callout naming the gap between the opener attempt and the canonical method, the average over the whole interval from the start against the limit of averages over \([t_0,t_0+h]\) (BC-QA-02014 `wrong_approaches`, BC-ERR-02033; docs/plan/15-lessons.md Within a concept, step 2).

## Scoring

None. BC-QA-02002, BC-QA-02014, BC-QA-02003 and BC-QA-02012 list no `point_types`, so no step carries a point tag and the lesson says nothing about points beyond the error records' own scoring consequences. BC-QA-02002's `scoring_pattern` is drawn from the CED because no 2023 to 2025 free response part asks for a derivative from the definition (research/units/unit-02-differentiation-definition-properties.md#Unresolved). The notation research makes limit notation a point in its own right only for improper integrals (research/scoring/notation-requirements.md#Limit notation), which is why the unit README tags the definition's notation point [inferred].

## Traps

Three active errors meet the concept's skills, in the bundle's order. Low band all three, mid band the first two.

- err-BC-ERR-02006 (BC-MIS-02003, BC-MIS-02002). Wrong step on ex-1's draw: \(f'(2)=2h+5\) with the limit dropped. Right step: \(\lim_{h\to0}(2h+5)=5\). Distinct. Possible reason, words from BC-MIS-02003.
- err-BC-ERR-02030 (BC-MIS-02015, BC-MIS-02014). Wrong step: \(4x-3\) reported where \(f'(2)\) is asked. Right step: 5. Distinct. Possible reason, words from BC-MIS-02015.
- err-BC-ERR-02033 (no linked BC-MIS). Wrong step on ex-2's draw: \(\frac{s(2)-s(0)}{2-0}=2\). Right step: 8. Distinct. Possible reason null.

## Representations

One block, low band, from the topic's Representations paragraph (contextual model to a difference quotient, BC-REP-05 to BC-REP-01): the difference quotients of ex-2's model at \(h=1, 0.1, 0.01, 0.001\), computed and shown as a table, served as a model under the unit README's delivery map.

## Prerequisite bridge

- BC-PRQ-02005 (supporting parent of BC-SKL-02006 and BC-SKL-02007), from `description_plain` and `failure_signature`: name the base point and the increment in \(f(a+h)\) before writing the quotient.

## Time

Every archetype here is `no_calculator` and MCQ shaped, so the part is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). In that budget a fluent solver writes three lines per example: the quotient inside the limit, the simplified quotient with the limit kept, the value.

## Checks

- chk-1, completion of ex-1, both bands: \(\lim_{h\to0}(2h+5)\) is given. Key 5, equal to ex-1's answer.
- chk-2, isomorph on BC-QA-02002, both bands: leading \(-1\), linear 4, constant \(-2\), point \(-1\), degree 2. Key 6.
- chk-3, MCQ on BC-QA-02014, low band: degree 2, leading 2, linear 1, constant 3, instant 3, context height. Key 13. Distractors: 7, 9 and 11 (BC-ERR-02033, the average over the whole interval \([0,3]\), \([1,3]\) and \([2,3]\)). The spec's other distractors, the value 24 (BC-ERR-02027) and the change 21 (BC-ERR-02001), are errors the lesson's skills do not hold.

No draw equals a published BC-QA-02002 or BC-QA-02014 `parameter_draw` (content/items_gen_unit02, content/items_unit02_agent).

## Delivery

- orientation: text. Rule 5.
- ki-1: motion. Rule 2: the key idea describes a limit being taken, and the unit README's delivery map names the secant closing to the tangent. Spec: the graph of ex-1's \(f\), the point \((2,3)\), the secant through \((2,f(2))\) and \((2+h,f(2+h))\) at frames \(h=1, 0.5, 0.25, 0.1, 0.01\), its slope \(2h+5\) labelled inside, the tangent of slope 5 on the last frame.
- ex-1, ex-2: step_reveal. Rule 1.
- err-BC-ERR-02006, err-BC-ERR-02030, err-BC-ERR-02033: step_reveal. Rule 1.
- representations: model. The template's model row: the meaning is the behaviour of a computed sequence of values, and the concept is a productive-failure target (BC-DF-15 on BC-QA-02014).

Every non-text choice is [inferred], settled by the modality A/B in the build plan.

## Band plan

- Low (full): orientation, ki-1, st-1, st-2, ex-1, err-02006, err-02030, err-02033, chk-1, ex-2, chk-2, representations, chk-3, the bridge. 555 words, 3.8 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, err-02006, err-02030, chk-1, chk-2, the bridge. 345 words, 2.4 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02006, err-BC-ERR-02030, err-BC-ERR-02033, ex-1.

## Sources

- BC-CON-02002; BC-SKL-02004, BC-SKL-02005, BC-SKL-02006, BC-SKL-02007; BC-EK-CHA-2B1; ced:60, ced:61
- BC-QA-02002, BC-QA-02014, BC-QA-02003, BC-QA-02012; BC-MCQ-SAMPLE-006; BC-DF-15
- BC-ERR-02006, BC-ERR-02030, BC-ERR-02033, BC-ERR-02008, BC-ERR-02029; BC-MIS-02002, BC-MIS-02003, BC-MIS-02014, BC-MIS-02015
- BC-PRQ-02005
- research/units/unit-02-differentiation-definition-properties.md#2.1 Defining Average and Instantaneous Rates of Change at a Point
- research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation
- research/units/unit-02-differentiation-definition-properties.md#Unresolved
- research/question-analysis/question-archetypes.md#BC-QA-02002 Derivative computed from the limit definition
- research/question-analysis/question-archetypes.md#BC-QA-02014 Rate at an instant found before the derivative is defined, as a limit of average rates
- research/question-analysis/question-archetypes.md#BC-QA-02012 Derivative notation read or converted
- research/scoring/notation-requirements.md#Limit notation
- research/exam/exam-structure.md#Section and part layout
- [inferred] The motion on ki-1 and the model on the representations block. Settled by the modality A/B.
- [inferred] One strategy block stands for the derivative-definition-limit family, on BC-QA-02002. Settled by a family-level cue record.

## Machine record

```json
{
 "id": "LSN-CON-02002",
 "kind": "concept",
 "target_id": "BC-CON-02002",
 "unit": "02",
 "skills": ["BC-SKL-02004", "BC-SKL-02005", "BC-SKL-02006", "BC-SKL-02007"],
 "orientation": {
  "text": "A response shows the rate at one instant as the value the average rates approach as the interval shrinks to nothing: the difference quotient at the point, inside a limit, simplified with the limit kept, then evaluated. An average over a whole interval is not the rate at an instant.",
  "sources": ["BC-CON-02002", "research/units/unit-02-differentiation-definition-properties.md#2.1 Defining Average and Instantaneous Rates of Change at a Point", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-2B1",
   "depth": "core",
   "text": "The rate of change of \\(f\\) at \\(x=a\\) is \\(\\lim_{h\\to0}\\frac{f(a+h)-f(a)}{h}\\) or \\(\\lim_{x\\to a}\\frac{f(x)-f(a)}{x-a}\\), provided the limit exists (BC-EK-CHA-2B1, ced:60). Both name one number, \\(f'(a)\\). Each quotient is a secant slope; as \\(h\\) shrinks the secants close on the tangent. At \\(h=0\\) the quotient is \\(\\frac{0}{0}\\), so \\(h\\) is divided out before the limit is taken.",
   "notation": "f prime of a",
   "quote": {"text": "These are equivalent forms of the definition of the derivative", "source": "ced:60"},
   "sources": ["BC-EK-CHA-2B1", "ced:60", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-02002",
   "cue": "A function rule, and the stem says use the definition of the derivative.",
   "method": "First line: the difference quotient for the rule at the named input, inside \\(\\lim_{h\\to0}\\).",
   "rival": "Rival: the power rule presented as the definition (BC-ERR-02008).",
   "separating_feature": "The word definition: the quotient must be on the page.",
   "sources": ["BC-QA-02002"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-02012",
   "cue": "A derivative written in one notation; the stem asks for the same quantity in another.",
   "method": "First line: name the function and the independent variable the notation carries.",
   "rival": "Rival: Leibniz notation split and cancelled as a fraction (BC-ERR-02029).",
   "separating_feature": "\\(f'(a)\\) names one number at one input.",
   "sources": ["BC-QA-02012"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-02002",
   "bands": ["low", "mid"],
   "parameter_draw": {"leading": 2, "linear": -3, "constant": 1, "point": 2, "degree": 2},
   "problem": {"text": "Let \\(f(x)=2x^2-3x+1\\). Use the definition of the derivative to find \\(f'(2)\\).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "The stem says definition, at the input 2.", "why": "\\(f'(2)=\\lim_{h\\to0}\\frac{f(2+h)-f(2)}{h}\\), with \\(f(2)=3\\).", "expr": "(2*(2+h)**2 - 3*(2+h) + 1 - 3)/h", "relation": "new"},
    {"cue": "At \\(h=0\\) the quotient is \\(\\frac{0}{0}\\), so expand and divide out \\(h\\).", "why": "The numerator is \\(2h^2+5h\\); the limit symbol stays on this line.", "expr": "2*h + 5", "relation": "equivalent"},
    {"cue": "Nothing divides by \\(h\\) now, so substitute \\(h=0\\).", "why": "The limit is the rate at 2.", "expr": "5", "relation": "limit", "variable": "h", "point": "0"}
   ],
   "answer": {"form": "numeric", "expr": "5"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-02014",
   "bands": ["low"],
   "parameter_draw": {"degree": 2, "leading": 3, "linear": -4, "constant": 6, "instant": 2, "context": "position"},
   "problem": {"text": "A particle's position at time \\(t\\) is \\(s(t)=3t^2-4t+6\\). At what rate is the position changing at the instant \\(t=2\\)?", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "One instant is named, so average over \\([2,2+h]\\).", "why": "The average rate is \\(\\frac{s(2+h)-s(2)}{h}\\), with \\(s(2)=10\\).", "expr": "(3*(2+h)**2 - 4*(2+h) + 6 - 10)/h", "relation": "new"},
    {"cue": "At \\(h=0\\) this is \\(\\frac{0}{0}\\): expand and divide out \\(h\\).", "why": "The average over \\([2,2+h]\\) is \\(8+3h\\).", "expr": "3*h + 8", "relation": "equivalent"},
    {"cue": "The instant is the interval shrunk to zero length.", "why": "The averages approach 8, the rate at \\(t=2\\).", "expr": "8", "relation": "limit", "variable": "h", "point": "0"}
   ],
   "answer": {"form": "numeric", "expr": "8"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-02006",
   "observed_behavior": "The response manipulates the difference quotient without carrying the limit symbol and attaches it only to the final line.",
   "scoring_consequence": "A notation point is lost where the definition itself is being assessed.",
   "wrong_step": {"text": "\\(f'(2)=\\frac{2h^2+5h}{h}=2h+5\\), with no limit written.", "expr": "2*h + 5"},
   "right_step": {"text": "\\(\\lim_{h\\to0}(2h+5)=5\\).", "expr": "5"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-02003", "text": "intermediate lines assert equalities that are false before the limit is taken"},
   "sources": ["BC-ERR-02006", "BC-MIS-02003"]
  },
  {
   "error_id": "BC-ERR-02030",
   "observed_behavior": "The response reports a function where a number is requested, or a number where the function is requested.",
   "scoring_consequence": "The conversion point is lost.",
   "wrong_step": {"text": "\\(4x-3\\), where \\(f'(2)\\) is asked.", "expr": "4*x - 3"},
   "right_step": {"text": "\\(f'(2)=5\\).", "expr": "5"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-02015", "text": "the derivative function is confused with its value"},
   "sources": ["BC-ERR-02030", "BC-MIS-02015"]
  },
  {
   "error_id": "BC-ERR-02033",
   "observed_behavior": "Asked for the rate of change at one instant, the response divides the change over a whole interval, usually from the starting time to that instant, by the length of the interval and reports that average.",
   "scoring_consequence": "The value reported is an average rate over an interval, so an answer point for the rate at the instant is not earned.",
   "wrong_step": {"text": "\\(\\frac{s(2)-s(0)}{2-0}=\\frac{10-6}{2}=2\\).", "expr": "(10 - 6)/(2 - 0)"},
   "right_step": {"text": "\\(\\lim_{h\\to0}(8+3h)=8\\).", "expr": "8"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-02033"]
  }
 ],
 "representations": {
  "text": "Average rates of \\(s(t)=3t^2-4t+6\\) over \\([2,2+h]\\) for \\(h=1, 0.1, 0.01, 0.001\\): 11, 8.3, 8.03, 8.003. They settle on 8.",
  "figure": {"kind": "numeric_experiment", "function": "3*t**2 - 4*t + 6", "at": 2, "h_values": [1, 0.1, 0.01, 0.001], "columns": ["h", "average rate over [2, 2 + h]"], "labels": [{"text": "averages approach 8", "placement": "inside", "at": "row below the last value"}]},
  "sources": ["research/units/unit-02-differentiation-definition-properties.md#2.1 Defining Average and Instantaneous Rates of Change at a Point"]
 },
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-02005", "text": "In \\(f(a+h)\\) the base point is \\(a\\) and the increment \\(h\\); name both before writing the quotient."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 3], "ex-2": [1, 2, 3]}, "skipped_steps": {"ex-1": [], "ex-2": []}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-02002",
   "parameter_draw": {"leading": 2, "linear": -3, "constant": 1, "point": 2, "degree": 2},
   "completes": "ex-1",
   "stem": {"text": "The definition gives \\(f'(2)=\\lim_{h\\to0}(2h+5)\\). Find \\(f'(2)\\).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "5"},
   "steps": [
    {"text": "The simplified quotient \\(2h+5\\).", "expr": "2*h + 5", "relation": "new"},
    {"text": "Its limit as \\(h\\to0\\) is 5.", "expr": "5", "relation": "limit", "variable": "h", "point": "0"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02006"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-02002",
   "parameter_draw": {"leading": -1, "linear": 4, "constant": -2, "point": -1, "degree": 2},
   "stem": {"text": "Let \\(f(x)=-x^2+4x-2\\). Use the definition of the derivative to find \\(f'(-1)\\).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "6"},
   "steps": [
    {"text": "\\(\\lim_{h\\to0}\\frac{f(-1+h)-f(-1)}{h}\\), with \\(f(-1)=-7\\).", "expr": "(-(-1+h)**2 + 4*(-1+h) - 2 + 7)/h", "relation": "new"},
    {"text": "Dividing out \\(h\\) leaves \\(6-h\\).", "expr": "6 - h", "relation": "equivalent"},
    {"text": "The limit is 6.", "expr": "6", "relation": "limit", "variable": "h", "point": "0"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02006"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-02014",
   "parameter_draw": {"degree": 2, "leading": 2, "linear": 1, "constant": 3, "instant": 3, "context": "height"},
   "stem": {"text": "A balloon's height at time \\(t\\) is \\(f(t)=2t^2+t+3\\). At what rate is the height changing at the instant \\(t=3\\)?", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "13"},
   "steps": [
    {"text": "The average over \\([3,3+h]\\), with \\(f(3)=24\\).", "expr": "(2*(3+h)**2 + (3+h) + 3 - 24)/h", "relation": "new"},
    {"text": "Dividing out \\(h\\) leaves \\(13+2h\\).", "expr": "2*h + 13", "relation": "equivalent"},
    {"text": "The limit is 13.", "expr": "13", "relation": "limit", "variable": "h", "point": "0"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "7", "error_path": "BC-ERR-02033", "derivation": "the average over [0, 3]: (24 - 3)/3"},
    {"id": "B", "is_key": false, "expr": "9", "error_path": "BC-ERR-02033", "derivation": "the average over the whole interval [1, 3]: (24 - 6)/2"},
    {"id": "C", "is_key": true, "expr": "13", "error_path": null},
    {"id": "D", "is_key": false, "expr": "11", "error_path": "BC-ERR-02033", "derivation": "the average over the whole interval [2, 3]: (24 - 13)/1"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02005", "BC-SKL-02004"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: a statement of what a response shows", "sources": ["BC-CON-02002"]},
  {"block": "ki-1", "mode": "motion", "reason": "rule 2: the key idea describes a limit being taken, a secant closing to a tangent (unit README delivery map)", "sources": ["BC-EK-CHA-2B1", "BC-SKL-02005"],
   "spec": {"kind": "graph_sweep", "representations": ["BC-REP-02"], "axes": {"x": [0, 3.5], "y": [-1, 16]},
    "curves": [{"expr": "2*x**2 - 3*x + 1", "domain": [0, 3.5]}],
    "points": [{"at": [2, 3], "label": {"text": "(2, 3)", "placement": "inside", "at": "just above the point"}}],
    "parameter": {"name": "h", "frames": [1, 0.5, 0.25, 0.1, 0.01]},
    "secant": {"through": ["(2, f(2))", "(2 + h, f(2 + h))"], "slope": "2*h + 5"},
    "tangent": {"slope": 5, "frames": "last only"},
    "labels": [{"text": "h = frame value", "placement": "inside", "at": "top left corner"}, {"text": "secant slope 2h + 5", "placement": "inside", "at": "along the secant"}, {"text": "tangent slope 5", "placement": "inside", "at": "along the tangent on the last frame"}]},
   "fallback": "the five frames as static small panels in one row, h decreasing left to right, the last showing the tangent",
   "keyboard": "left and right arrow keys step between frames; Home returns to h = 1; each frame announces h and the secant slope",
   "reduced_motion": "no auto-advance: each arrow key press cross-fades to the next frame"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02006", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02030", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02033", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "representations", "mode": "model", "reason": "template model row: the meaning is a computed sequence of difference quotients at shrinking h, and BC-QA-02014 carries BC-DF-15 (productive-failure target)", "sources": ["BC-QA-02014"],
   "spec": {"kind": "numeric_experiment", "representations": ["BC-REP-03"], "function": "3*t**2 - 4*t + 6", "at": 2, "h_values": [1, 0.1, 0.01, 0.001], "computed": "(s(2 + h) - s(2))/h", "columns": ["h", "average rate over [2, 2 + h]"],
    "labels": [{"text": "h", "placement": "inside", "at": "first column header"}, {"text": "averages approach 8", "placement": "inside", "at": "row below the last value"}]},
   "fallback": "the four computed rows printed as a static table with the closing label",
   "keyboard": "a Run control reached by Tab and pressed with Enter or Space adds one row per press; the table is read in row order"}
 ],
 "refresher": ["ki-1", "err-BC-ERR-02006", "err-BC-ERR-02030", "err-BC-ERR-02033", "ex-1"],
 "read_minutes": {"full": 3.8, "brief": 2.4},
 "word_count": {"full": 555, "brief": 345},
 "research_lines": [
  {"file": "research/units/unit-02-differentiation-definition-properties.md", "line": "justification variants ask why a limit is needed for the rate at an instant"},
  {"file": "research/units/unit-02-differentiation-definition-properties.md", "line": "The difference quotient is indeterminate at zero increment, so the increment is divided out of the numerator before the limit is taken."}
 ],
 "inferred": [
  {"claim": "The secant motion on ki-1 and the difference quotient model serve better than a static figure and text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "BC-QA-02002 stands for the derivative-definition-limit family in the strategy section, with BC-QA-02014 and BC-QA-02003 sharing its first-line shape.", "settles": "A family-level cue record, or strategy blocks per archetype."}
 ],
 "sources": ["BC-CON-02002", "BC-SKL-02004", "BC-SKL-02005", "BC-SKL-02006", "BC-SKL-02007", "BC-EK-CHA-2B1", "ced:60", "ced:61", "BC-QA-02002", "BC-QA-02014", "BC-QA-02003", "BC-QA-02012", "BC-MCQ-SAMPLE-006", "BC-DF-15", "BC-ERR-02006", "BC-ERR-02030", "BC-ERR-02033", "BC-ERR-02008", "BC-ERR-02029", "BC-MIS-02002", "BC-MIS-02003", "BC-MIS-02014", "BC-MIS-02015", "BC-PRQ-02005", "research/units/unit-02-differentiation-definition-properties.md#2.1 Defining Average and Instantaneous Rates of Change at a Point", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation", "research/units/unit-02-differentiation-definition-properties.md#Unresolved", "research/scoring/notation-requirements.md#Limit notation", "research/exam/exam-structure.md#Section and part layout"]
}
```
