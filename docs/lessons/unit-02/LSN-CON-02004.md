---
title: LSN-CON-02004 Derivative notation and its equivalent forms
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02004, derivative notation and its equivalent forms, built from authoring_bundle("BC-CON-02004") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02004 Derivative notation and its equivalent forms

Concept BC-CON-02004 (skills BC-SKL-02010, BC-SKL-02011), topic 2.2 of Unit 2, loaded by BC-QA-02012 only. Its hard parent is BC-CON-02002 (unit README section 1). It sits in the confusable set of LSN-DEC-02-02 with BC-CON-02005 and BC-CON-02007.

## Prediction

One multiple choice question on worked example 1's own numbers, asked before the rule is shown: \(V'(4)=-6\) for the volume \(V(t)\) of a tank, and the student picks the Leibniz statement that says the same. The key is ex-1's answer; the distractors are the two notation slips the error blocks carry, the quotient \(\frac{V(4)}{4}\) (BC-ERR-02029) and the differential \(dV\) in place of the derivative (BC-ERR-03022). The resolution, shown on the key idea screen beside the student's choice, names the function, the variable and the input the prime form carries. No verdict word. Sources: BC-CON-02004 and the topic 2.2 section the key idea cites.

## Orientation

Served text (31 words), from BC-CON-02004 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation): conceptual variants ask what the notation denotes, so a response reads each form as naming a function, the variable of differentiation and, where shown, the input. No count, no frequency.

## Key ideas

BC-SKL-02010 maps BC-EK-CHA-2B3 and BC-EK-CHA-2B4; BC-SKL-02011 maps BC-EK-CHA-2B4. Two blocks.

- ki-1 (core, BC-EK-CHA-2B3, ced:61). The three notations for \(y=f(x)\); what each names; a value at an input carries the input in every form; the Leibniz form is one symbol (BC-MIS-02015's description names the fraction reading as the failure). No anchor quote for this block (the run in the EK's cached text is too short to serve). Notation line from the concept record.
- ki-2 (extended, BC-EK-CHA-2B4, ced:61). The four representations of one derivative value: a slope on a graph, a quotient from a table, a formula, a sentence with units. Anchor quote (10 words) from ced:61.

## Recognition

- BC-QA-02012 (family notation-translation, MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-02012 Derivative notation read or converted): `typical_wording` "Which of the given expressions denotes the same quantity as the expression shown?"; `common_givens` a derivative written in one notation; `asked_to_produce` an equivalent expression in the requested notation, or a statement of what the notation denotes. The signal is a derivative symbol in the stem and a request for "the same quantity" or "what it means". The archetype has no `official_examples`.

Contrast pair on st-1: this stem is on BC-QA-02012 and asks for the same quantity in another notation; not this stem is the BC-CON-02005 shape, the same function with a line asked at the point (a sibling concept in the LSN-DEC-02-02 set). The separating feature is a restatement of one quantity against a new quantity to produce.

What says "not this concept": a number is asked from a function rule (BC-CON-02002, BC-CON-02003); a line is asked (BC-CON-02005); an estimate from data (BC-CON-02007). The LSN-DEC-02-02 selector is what the stem asks to produce (unit README section 3).

## Method choice

- st-1, BC-QA-02012, low and mid bands. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: identify the function and the independent variable from the supplied notation. Rival, `wrong_approaches`: treating Leibniz notation as a fraction whose parts separate and cancel (BC-ERR-02029). Separating feature: a value at an input keeps the input in every notation.

The archetype carries `asked_to_produce` and `common_givens`, so the block is not tagged inferred. The `method` text carries no leading label; the rival's record id sits in the block's `sources`.

## Solution path

- ex-1, BC-QA-02012, both bands, no calculator. Draw: order first, framing context, supplied prime, setting 0 (the tank, liters, minutes, from the generation template's context list), at 4, value \(-6\), giving \(V'(4)=-6\). Steps follow `expected_solution_path`: identify function, variable and input (no value), write the equivalent Leibniz statement (valued, new), state what it denotes with units (no value). A fluent solver writes the Leibniz line and the sentence; the identification is read, not written.

One example only, so nothing is faded. The answer is a statement, so the valued step carries the Leibniz statement as a SymPy equation, and the answer key is `statement`.

## Scoring

None. BC-QA-02012 lists no `point_types`, so no step carries a point tag and the lesson says nothing about points beyond the error records' own scoring consequences. Loose derivative notation is accepted when intent is clear (research/scoring/notation-requirements.md#Derivative notation; sg-25:7, sg-24:8), which is why the archetype's single point is the conversion itself (`scoring_pattern`).

## Traps

Four active errors meet the concept's skills; all four are shown, in the bundle's order. Low band all four, mid band the first two. BC-ERR-04017 is held by BC-SKL-02010; its record is a relating equation differentiated with respect to a length and stopped before the chain rule. ex-1 has no relating equation, so the block draws one for itself: \(V=3h^2\) with \(\frac{dh}{dt}=-1\) at \(h=1\), chosen so the completed chain rule gives ex-1's \(-6\). The drawn relation is [inferred]; the move on it is the record's.

- err-BC-ERR-02030 (BC-MIS-02015, BC-MIS-02014). Wrong step on ex-1's draw: \(\frac{dV}{dt}=-6\), the input dropped. Right step: \(\left.\frac{dV}{dt}\right|_{t=4}=-6\). Distinct. Possible reason from BC-MIS-02015.
- err-BC-ERR-04017 (BC-MIS-04008, BC-MIS-99005). Wrong: \(\frac{dV}{dh}=6h\) from \(V=3h^2\), and the work stops. Right: \(\frac{dV}{dt}=6h\frac{dh}{dt}=6(1)(-1)=-6\). Distinct (SymPy: \(\frac{d}{dh}3h^2=6h\); \(\frac{d}{dt}3h(t)^2=6h\,h'(t)\), which is \(-6\) at \(h=1\), \(h'=-1\)). Possible reason from BC-MIS-99005.
- err-BC-ERR-02029 (BC-MIS-02015, BC-MIS-03003). Wrong: \(\frac{V(4)}{4}=-6\). Right: \(\left.\frac{dV}{dt}\right|_{t=4}=-6\). Distinct. Possible reason from BC-MIS-02015.
- err-BC-ERR-03022 (BC-MIS-03014, BC-MIS-03003). Wrong: \(dV=-6\). Right: \(\frac{dV}{dt}=-6\) at \(t=4\). Distinct. Possible reason from BC-MIS-03014.

All four relations are distinct, so all four blocks are fix prompts.

The wrong and right steps are SymPy equations over the symbols the notation names (dV, dt, V, t) and over `Derivative` and `Subs`, so the CAS separates them structurally.

## Representations

None as a separate block. The topic's Representations paragraph names BC-REP-02 and BC-REP-03 among four, and ki-2 carries a graph with a table (Delivery).

## Prerequisite bridge

- BC-PRQ-02004 (supporting parent of BC-SKL-02010), from `description_plain` and `failure_signature`: each form names the variable it differentiates with respect to, and one expression keeps one form.

## Time

BC-QA-02012 is `no_calculator` and MCQ shaped: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). A fluent solver writes one line, the equivalent expression, and holds the function and variable identification in the head (unit README section 5).

## Checks

- chk-1, completion of ex-1, both bands: the identification is given; the student writes the Leibniz statement. Key equal to ex-1's answer.
- chk-2, isomorph on BC-QA-02012, both bands: order first, framing bare, supplied leibniz, setting 1 (\(w=g(t)\)), at 7, value 3. Key \(g'(7)=3\).
- chk-3, MCQ on BC-QA-02012, low band: order first, framing context, supplied prime, setting 2 (the rod, \(T(x)\) degrees Celsius, \(x\) meters), at 3, value \(-4\). Statement options, as the published items on this archetype carry: the key; BC-ERR-02029 (\(\frac{T(3)}{3}\)); BC-ERR-03022 (\(dT=-4\), the differential in place of the derivative); BC-ERR-02030 (the input dropped).

No draw equals a published BC-QA-02012 `parameter_draw` (content/items_gen_unit02).

## Delivery

- orientation: text. Rule 5.
- ki-1: text. Rule 5; the block is the reading of symbols.
- ki-2: figure. Rule 3; BC-SKL-02011 lists BC-REP-02 and BC-REP-03, and the unit README's delivery map names a figure and a table. One screen, two representations: an illustrative curve with \(V'(4)=-6\) and its tangent, and a three-row table whose quotient gives \(-6\). The curve \(V(t)=100+2t-t^2\) is chosen for the figure only and is not part of the draw [inferred].
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-02030, err-BC-ERR-04017, err-BC-ERR-02029, err-BC-ERR-03022: step_reveal. Rule 1.

The lesson already carries a drawn block (the figure on ki-2), so it states no `no_figure_reason`. The prediction is delivered as text.

## Band plan

- Low (full), in served order: prediction, orientation, the bridge, ki-1, ki-2, st-1 with its contrast pair, ex-1, chk-1, the four error blocks, chk-2, chk-3. 659 words, 4.4 minutes (cap 900 and 6). There is no example 2, so nothing is faded.
- Mid (brief): prediction, orientation, the bridge, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-02030, err-04017, chk-2. 443 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02030, err-BC-ERR-04017, err-BC-ERR-02029, err-BC-ERR-03022, ex-1.

## Sources

- BC-CON-02004; BC-SKL-02010, BC-SKL-02011; BC-EK-CHA-2B3, BC-EK-CHA-2B4; ced:61
- BC-QA-02012
- BC-ERR-02030, BC-ERR-04017, BC-ERR-02029, BC-ERR-03022; BC-MIS-02014, BC-MIS-02015, BC-MIS-03003, BC-MIS-03014, BC-MIS-04008, BC-MIS-99005; crabbc-25:25, cr-24:18
- BC-PRQ-02004
- sg-25:7, sg-24:8
- research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation
- research/question-analysis/question-archetypes.md#BC-QA-02012 Derivative notation read or converted
- research/scoring/notation-requirements.md#Derivative notation
- research/exam/exam-structure.md#Section and part layout
- [inferred] The illustrative curve in ki-2's figure. Settled by a figure binding on BC-QA-02012's parameter_spec.
- [inferred] The figure delivery for ki-2. Settled by the modality A/B.
- [inferred] BC-ERR-04017 staged on a relating equation drawn for the block, since ex-1 has none. Settled by a notation-scoped error record or a published BC-QA-02012 item keyed on the variable of differentiation.

## Machine record

```json
{
 "id": "LSN-CON-02004",
 "kind": "concept",
 "target_id": "BC-CON-02004",
 "unit": "02",
 "skills": ["BC-SKL-02010", "BC-SKL-02011"],
 "prediction": {
  "id": "pr-1",
  "stem": {"text": "\\(V(t)\\) liters at \\(t\\) minutes, and \\(V'(4)=-6\\). Which is the same in Leibniz notation?", "command_verb": "predict"},
  "format": "mcq",
  "options": [
   {"id": "A", "label": "\\(\\frac{V(4)}{4}=-6\\)", "is_key": false},
   {"id": "B", "label": "\\(\\left.\\frac{dV}{dt}\\right|_{t=4}=-6\\)", "is_key": true},
   {"id": "C", "label": "\\(dV=-6\\)", "is_key": false}
  ],
  "resolution": "\\(V'(4)\\) names the function \\(V\\), the variable \\(t\\) and the input 4; the Leibniz form keeps all three.",
  "sources": ["BC-CON-02004", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation"]
 },
 "orientation": {
  "text": "A response reads derivative notation as naming a function, the variable it is differentiated with respect to, and, where shown, the input: \\(f'(a)\\), \\(\\left.\\frac{dy}{dx}\\right|_{x=a}\\) and \\(y'\\) at \\(a\\) are one number.",
  "sources": ["BC-CON-02004", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-2B3",
   "depth": "core",
   "text": "For \\(y=f(x)\\) the derivative is written \\(\\frac{dy}{dx}\\), \\(f'(x)\\) or \\(y'\\). Each names a function and the variable of differentiation. A value at one input carries the input: \\(f'(4)\\) is \\(\\left.\\frac{dy}{dx}\\right|_{x=4}\\). \\(\\frac{dy}{dx}\\) is one symbol, not a quotient.",
   "notation": "dy by dx; f prime of x; y prime",
   "quote": null,
   "sources": ["BC-EK-CHA-2B3", "ced:61", "BC-MIS-02015", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-2B4",
   "depth": "extended",
   "text": "One derivative value has four faces: a tangent slope on a graph, a quotient from a table, a formula, a sentence with units. \\(V'(4)=-6\\) reads: at \\(t=4\\) the volume is falling at 6 liters per minute.",
   "notation": "dy by dx",
   "quote": {"text": "The derivative can be represented graphically, numerically, analytically, and verbally.", "source": "ced:61"},
   "sources": ["BC-EK-CHA-2B4", "ced:61"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-02012",
   "cue": "A derivative in one notation; the same quantity is asked in another.",
   "method": "Name the function, the independent variable, and the input if shown.",
   "rival": "The Leibniz form split and cancelled as a fraction.",
   "separating_feature": "A value at an input keeps the input in every notation.",
   "contrast": {
    "this": {"text": "\\(P=h(x)\\) and \\(h'(5)=9\\). Which expression denotes the same quantity?", "archetype_id": "BC-QA-02012"},
    "not_this": {"text": "Let \\(h(x)=x^2\\). Write the tangent line to \\(h\\) at \\(x=5\\).", "why_not": "A line is asked, not the same derivative in another notation."},
    "feature": "The same quantity restated, not a new quantity produced."
   },
   "sources": ["BC-QA-02012", "BC-ERR-02029"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-02012",
   "bands": ["low", "mid"],
   "parameter_draw": {"order": "first", "framing": "context", "supplied": "prime", "setting": 0, "at": 4, "value": -6},
   "problem": {"text": "The volume of water in a tank is \\(V(t)\\) liters, \\(t\\) minutes after a valve opens, and \\(V'(4)=-6\\). Write this in Leibniz notation and state its meaning.", "command_verb": "write"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "\\(V'(4)\\) names the function \\(V\\), the variable \\(t\\), the input 4.", "why": "The statement is about one input, so the input stays in every form."},
    {"cue": "The stem asks for Leibniz notation.", "why": "\\(V\\) over \\(t\\), evaluated at 4: \\(\\left.\\frac{dV}{dt}\\right|_{t=4}=-6\\).", "expr": "Eq(Subs(Derivative(V(t), t), t, 4), -6)", "relation": "new"},
    {"cue": "The stem asks for its meaning; units are liters over minutes.", "why": "At \\(t=4\\) the volume is decreasing at 6 liters per minute."}
   ],
   "answer": {"form": "statement", "expr": "Eq(Subs(Derivative(V(t), t), t, 4), -6)", "label": "\\(\\left.\\frac{dV}{dt}\\right|_{t=4}=-6\\): at \\(t=4\\) the volume is decreasing at 6 liters per minute."}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-02030",
   "observed_behavior": "The response reports a function where a number is requested, or a number where the function is requested.",
   "scoring_consequence": "The conversion point is lost.",
   "wrong_step": {"text": "\\(\\frac{dV}{dt}=-6\\): the input is gone.", "expr": "Eq(Derivative(V(t), t), -6)"},
   "right_step": {"text": "\\(\\left.\\frac{dV}{dt}\\right|_{t=4}=-6\\).", "expr": "Eq(Subs(Derivative(V(t), t), t, 4), -6)"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-02015", "text": "the derivative function is confused with its value"},
   "sources": ["BC-ERR-02030", "BC-MIS-02015"]
  },
  {
   "error_id": "BC-ERR-04017",
   "observed_behavior": "The relating equation is differentiated with respect to a length or with respect to x, and the response stops there rather than continuing through the chain rule to a rate with respect to time.",
   "scoring_consequence": "The Chief Reader report for 2024 records that responses differentiating with respect to x needed to continue through the chain rule and that many provided no work beyond that step (cr-24:18); BC-ERR-99013 records the same family across years.",
   "wrong_step": {"text": "Given \\(V=3h^2\\) and \\(\\frac{dh}{dt}=-1\\) at \\(h=1\\): \\(\\frac{dV}{dh}=6h\\), and the work stops.", "expr": "Eq(Derivative(V(h), h), 6*h)"},
   "right_step": {"text": "Through the chain rule: \\(\\frac{dV}{dt}=6h\\frac{dh}{dt}=6(1)(-1)=-6\\).", "expr": "Eq(Derivative(V(t), t), 6*h(t)*Derivative(h(t), t))"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-99005", "text": "does not distinguish the variable of differentiation"},
   "sources": ["BC-ERR-04017", "BC-MIS-99005", "cr-24:18"]
  },
  {
   "error_id": "BC-ERR-02029",
   "observed_behavior": "The response treats the Leibniz form as a fraction whose parts can be separated and cancelled.",
   "scoring_consequence": "A notation point is lost where the meaning of the symbol is being assessed.",
   "wrong_step": {"text": "\\(\\frac{V(4)}{4}=-6\\): volume over time.", "expr": "Eq(V/t, -6)"},
   "right_step": {"text": "\\(\\frac{dV}{dt}=-6\\) at \\(t=4\\): a rate.", "expr": "Eq(dV/dt, -6)"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-02015", "text": "the Leibniz form is treated as a fraction"},
   "sources": ["BC-ERR-02029", "BC-MIS-02015"]
  },
  {
   "error_id": "BC-ERR-03022",
   "observed_behavior": "The response writes dy in place of dy/dx, or uses dy/dx where the operator d/dx is meant, or mixes the two notations inside one line.",
   "scoring_consequence": "The 2025 Chief Reader report lists this notation as a misconception seen in implicit differentiation responses, and poor notation cost points there (crabbc-25:25).",
   "wrong_step": {"text": "\\(dV=-6\\).", "expr": "Eq(dV, -6)"},
   "right_step": {"text": "\\(\\frac{dV}{dt}=-6\\) at \\(t=4\\).", "expr": "Eq(dV/dt, -6)"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-03014", "text": "notation is mixed within a line"},
   "sources": ["BC-ERR-03022", "BC-MIS-03014", "crabbc-25:25"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-02004", "text": "Each form names its variable of differentiation."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3]}, "skipped_steps": {"ex-1": [1]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-02012",
   "parameter_draw": {"order": "first", "framing": "context", "supplied": "prime", "setting": 0, "at": 4, "value": -6},
   "completes": "ex-1",
   "stem": {"text": "\\(V'(4)=-6\\) names \\(V\\), the variable \\(t\\) and the input 4. Write it in Leibniz notation.", "command_verb": "write"},
   "key": {"form": "statement", "expr": "Eq(Subs(Derivative(V(t), t), t, 4), -6)", "label": "\\(\\left.\\frac{dV}{dt}\\right|_{t=4}=-6\\)"},
   "steps": [
    {"text": "\\(\\left.\\frac{dV}{dt}\\right|_{t=4}=-6\\).", "expr": "Eq(Subs(Derivative(V(t), t), t, 4), -6)", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02010"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-02012",
   "parameter_draw": {"order": "first", "framing": "bare", "supplied": "leibniz", "setting": 1, "at": 7, "value": 3},
   "stem": {"text": "\\(w=g(t)\\) and \\(\\left.\\frac{dw}{dt}\\right|_{t=7}=3\\). Write this in prime notation.", "command_verb": "write"},
   "key": {"form": "statement", "expr": "Eq(Subs(Derivative(g(t), t), t, 7), 3)", "label": "\\(g'(7)=3\\)"},
   "steps": [
    {"text": "\\(g'(7)=3\\).", "expr": "Eq(Subs(Derivative(g(t), t), t, 7), 3)", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02010"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-02012",
   "parameter_draw": {"order": "first", "framing": "context", "supplied": "prime", "setting": 2, "at": 3, "value": -4},
   "stem": {"text": "A rod's temperature \\(x\\) meters from one end is \\(T(x)\\) degrees Celsius, and \\(T'(3)=-4\\). Which statement says the same?", "command_verb": "choose"},
   "key": {"form": "statement", "expr": "Eq(Subs(Derivative(T(x), x), x, 3), -4)", "label": "\\(\\left.\\frac{dT}{dx}\\right|_{x=3}=-4\\): at 3 meters the temperature is decreasing at 4 degrees Celsius per meter."},
   "steps": [
    {"text": "\\(\\left.\\frac{dT}{dx}\\right|_{x=3}=-4\\).", "expr": "Eq(Subs(Derivative(T(x), x), x, 3), -4)", "relation": "new"}
   ],
   "options": [
    {"id": "A", "is_key": false, "label": "\\(\\frac{T(3)}{3}=-4\\): temperature divided by distance is \\(-4\\).", "error_path": "BC-ERR-02029", "derivation": "the Leibniz fraction read as the quotient of the two quantities at the point"},
    {"id": "B", "is_key": true, "label": "\\(\\left.\\frac{dT}{dx}\\right|_{x=3}=-4\\): at 3 meters the temperature is decreasing at 4 degrees Celsius per meter.", "error_path": null},
    {"id": "C", "is_key": false, "label": "\\(dT=-4\\) at \\(x=3\\): the temperature changes by 4 degrees Celsius.", "error_path": "BC-ERR-03022", "derivation": "dT written in place of dT/dx, so the rate is read as a change in temperature"},
    {"id": "D", "is_key": false, "label": "\\(\\frac{dT}{dx}=-4\\): the temperature falls 4 degrees Celsius per meter at every point.", "error_path": "BC-ERR-02030", "derivation": "the input dropped, so a value at one point is read as the derivative function"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02010", "BC-SKL-02011"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: a statement of what a response shows", "sources": ["BC-CON-02004"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 5: the reading of symbols, BC-REP-01 and BC-REP-04 on BC-SKL-02010", "sources": ["BC-SKL-02010"]},
  {"block": "ki-2", "mode": "figure", "reason": "rule 3: BC-SKL-02011 lists BC-REP-02 (with BC-REP-03 carried as an inset table under rule 4); the unit README delivery map names a figure and a table", "sources": ["BC-SKL-02011"],
   "spec": {"kind": "graph_with_table", "representations": ["BC-REP-02", "BC-REP-03"], "axes": {"x": [0, 8], "y": [60, 110]},
    "curves": [{"expr": "100 + 2*t - t**2", "domain": [0, 8], "role": "illustrative V"}],
    "points": [{"at": [4, 92], "label": {"text": "(4, 92)", "placement": "inside", "at": "just right of the point"}}],
    "tangent": {"at": 4, "slope": -6},
    "table": {"columns": ["t", "V(t)"], "rows": [[3.9, 92.59], [4, 92], [4.1, 91.39]], "position": "upper right inset"},
    "labels": [{"text": "slope -6 = V'(4)", "placement": "inside", "at": "along the tangent"}, {"text": "(91.39 - 92.59)/0.2 = -6", "placement": "inside", "at": "last line of the inset table"}, {"text": "at t = 4, falling 6 liters per minute", "placement": "inside", "at": "lower left corner"}]},
   "fallback": "the same content as text: the tangent slope, the three table rows with their quotient, and the sentence",
   "keyboard": "none needed; the figure is static and its text alternative reads the slope, the table rows and the sentence in order"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02030", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-04017", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02029", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03022", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-02030", "err-BC-ERR-04017", "err-BC-ERR-02029", "err-BC-ERR-03022", "ex-1"],
 "read_minutes": {"full": 4.4, "brief": 3.0},
 "word_count": {"full": 658, "brief": 442},
 "research_lines": [
  {"file": "research/scoring/notation-requirements.md", "line": "Loose derivative notation is generally accepted when the intent is clear."},
  {"file": "research/units/unit-02-differentiation-definition-properties.md", "line": "Conceptual variants ask what the notation denotes"}
 ],
 "inferred": [
  {"claim": "The curve V(t) = 100 + 2t - t^2 in ki-2's figure is illustrative, chosen so that V'(4) = -6; the draw gives only the value.", "settles": "A figure binding on the BC-QA-02012 parameter_spec."},
  {"claim": "A static figure with an inset table serves ki-2 better than text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "BC-QA-02012 carries no relating equation, so BC-ERR-04017 is staged on a relation drawn for the block, V equal to 3 h squared with the depth falling at 1 per minute at depth 1, chosen to give ex-1's rate of negative 6.", "settles": "A notation-scoped error record, or a published BC-QA-02012 item keyed on the variable of differentiation."}
 ],
 "sources": ["BC-CON-02004", "BC-SKL-02010", "BC-SKL-02011", "BC-EK-CHA-2B3", "BC-EK-CHA-2B4", "ced:61", "BC-QA-02012", "BC-ERR-02030", "BC-ERR-04017", "BC-ERR-02029", "BC-ERR-03022", "BC-MIS-02014", "BC-MIS-02015", "BC-MIS-03003", "BC-MIS-03014", "BC-MIS-04008", "BC-MIS-99005", "crabbc-25:25", "cr-24:18", "BC-PRQ-02004", "sg-25:7", "sg-24:8", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation", "research/scoring/notation-requirements.md#Derivative notation", "research/exam/exam-structure.md#Section and part layout"]
}
```
