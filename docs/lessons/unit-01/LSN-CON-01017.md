---
title: LSN-CON-01017 Limits at infinity and horizontal asymptotes
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01017, limits at infinity and horizontal asymptotes, built from authoring_bundle("BC-CON-01017") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01017 Limits at infinity and horizontal asymptotes

Concept BC-CON-01017 (skills BC-SKL-01058, BC-SKL-01059, BC-SKL-01060, BC-SKL-01061, BC-SKL-01063), topic 1.15 of Unit 1 (BC-TOP-0115), loaded by one archetype, BC-QA-01010 (primary), which lists BC-PT-99054 and BC-PT-99004. Official examples BC-FRQ-2025-Q1-C (sg-25:4) and BC-MCQ-PE2012-021.

## Prediction

Served first, both bands, on ex-1's own limit, \(\lim_{x\to-\infty}\frac{\sqrt{4x^2+5}}{3x+1}\). Form `mcq`, three value options, key "Negative \(\frac23\)". The three values are the ones the sign of the root and the ratio of the coefficients produce, so the student commits to the concept's core claim, that the dominant power under a root carries the sign of the end, before it is stated. Source: BC-CON-01017 and the topic's Limits at infinity paragraph (research/units/unit-01-limits-continuity.md#1.15 Connecting Limits at Infinity and Horizontal Asymptotes). The resolution shows the division and the sign of \(\frac{|x|}{x}\) and passes no verdict. Delivery: text.

## Orientation

Served text, from BC-CON-01017 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-01-limits-continuity.md#1.15 Connecting Limits at Infinity and Horizontal Asymptotes): a response writes the limit with the variable increasing or decreasing without bound, for the function the stem names, then its value; a finite value is a horizontal asymptote.

## Key ideas

Two BC-EK map to the skills, both on ced:52: BC-EK-LIM-2D3 (all five skills except BC-SKL-01060) and BC-EK-LIM-2D4 (BC-SKL-01058, 01059, 01060, 01063). Two core blocks, both bands.

- ki-1 (core), BC-EK-LIM-2D3. Paraphrase of the Limits at infinity and Method paragraphs: divide by the dominant power; under a square root the dominant power carries the sign of the end examined, so \(\sqrt{x^2}=|x|\), which is \(-x\) as \(x\to-\infty\). No anchor quote is served, because the brief form needs the room for the prediction and the contrast pair. Notation line: horizontal asymptote; end behaviour.
- ki-2 (core), BC-EK-LIM-2D4. Paraphrase of the Horizontal asymptotes paragraph: a finite limit \(L\) at either end gives \(y=L\), and the two ends are checked separately. No anchor quote is served, for the same reason. Both key ideas stay core.

## Recognition

- BC-QA-01010 (family end-behaviour-limit, one FRQ part, calculator either; research/question-analysis/question-archetypes.md#BC-QA-01010 End behaviour described by a limit at infinity): `typical_wording` "Write a limit expression that describes the long run behaviour of the given quantity and evaluate it"; `common_givens` a model function in a context, a formula for the rate of change of the model, candidate functions for a stated horizontal asymptote; `asked_to_produce` a limit expression for the end behaviour and its value. The signals are "long run", "end behaviour", "horizontal asymptote", or a variable "increasing without bound". In BC-FRQ-2025-Q1-C the stem names the rate, and the value point goes only to the rate's limit (sg-25:4).

What says "not this concept": the infinity symbol in the value with a finite input under the arrow (BC-CON-01016, the BC-MIS-01018 probe). The contrast pair's near miss comes from there: a one sided limit at \(-2\) of a rational rule, where the value, not the input, is infinite; a quotient of two growing quantities compared (BC-CON-01018, in the same topic).

## Method choice

- st-1, BC-QA-01010, both bands. Cue, from `asked_to_produce` and `common_givens`: a model or rule, and the stem asks for a limit expression for long run behaviour and its value. Method, `expected_solution_path[0]`: identify the function whose end behaviour is requested, then write the limit with the variable increasing without bound (no leading label is served). Rival, `wrong_approaches`: substituting infinity into the expression as a number (BC-ERR-01021). Separating feature: the infinity symbol sits under the arrow and never inside the expression. The block carries the contrast pair: `this` asks for a limit at \(-\infty\) of a radical quotient; `not_this` asks for a one sided limit at \(-2\) of a rational rule; the feature is where the infinity sits.

## Solution path

- ex-1, BC-QA-01010, both bands, no calculator. Draw: root_coef 2, linear_coef 3, linear_const 1, inner_const 5, radical_place numerator, giving \(\lim_{x\to-\infty}\frac{\sqrt{4x^2+5}}{3x+1}\). Constraints hold (\(3\ne2\), \(3\ne4\)). Chain: the expression (new, tagged BC-PT-99054), the form with \(|x|\) factored out (equivalent), the value \(-\frac23\) (limit at \(-\infty\)). A fluent solver writes all three lines; the value line is tagged BC-PT-99004.
- ex-2, BC-QA-01010, low band, no calculator, faded from step 3 (`fade_from: 3`): the student is shown \(A(t)\) and its derivative and writes the limit value, then sees the withheld step. The fade falls there because the two shown steps carry the choice the example teaches (the rate names \(A'\)) and the withheld step is the value line that ex-1 has already modelled. A contextual draw outside `parameter_spec`: amount \(A(t)=\frac{6t}{2t+1}\), stem asks for the long run rate. Chain: \(A\) (new), \(A'(t)\) (differentiate, tagged BC-PT-99054), 0 (limit at \(\infty\), tagged BC-PT-99004). The spec has no contextual or rate parameter, so the draw carries its own keys [inferred].

## Scoring

BC-QA-01010 lists BC-PT-99054 and BC-PT-99004. Both examples tag both: the limit expression line carries BC-PT-99054 and the value line BC-PT-99004. Lines generated by `reader_checks` and copied into the machine record:

Limit expression for end behaviour. Earned by: Writing the requested limit symbolically as the variable tends to infinity, for either the function or its derivative (sg-25:4). Not earned by: Setting up the limit so the variable tends to zero (crabbc-25:3); arithmetic with infinity in place of the value, which sg-25:4 treats as scratch work.

Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations.

Point losses the scoring research names for this shape: limit notation introduced then dropped, or arithmetic written with the infinity symbol, BC-ERR-99007 (research/scoring/common-point-losses.md#Notation points, cr-23:16); arithmetic with infinity is treated as scratch work for the value point (research/scoring/notation-requirements.md#Limit notation, sg-25:4); the expression and the value are separate points, and a limit taken on the amount blocks the value point (research/scoring/command-verbs.md#BC-CV-29 Write and evaluate a limit expression).

## Traps

All four served blocks are `distinct`, so each is a fix prompt: the student writes the right step before it appears. Five active errors meet the skills; the first four in the bundle's order are served (BC-ERR-01024, sign under a radical at negative infinity, falls fifth and is carried by ki-1 instead). Low band all four, mid band the first two.

- err-BC-ERR-01022 (BC-MIS-01014, BC-MIS-01018), on ex-2: wrong \(\lim A=3\), right \(\lim A'=0\). Distinct.
- err-BC-ERR-01023 (BC-MIS-99008, BC-MIS-01005), on ex-1: wrong \(\frac43\) (leading coefficients 4 and 3), right \(-\frac23\). Distinct. Possible reason null.
- err-BC-ERR-01033 (BC-MIS-01018, BC-MIS-01012), on ex-1: wrong \(x=-\frac13\) reported, right \(y=-\frac23\). Distinct.
- err-BC-ERR-01021 (BC-MIS-99008, BC-MIS-01018), on ex-1: wrong \(\frac{\sqrt{4\cdot\infty^2+5}}{3\cdot\infty+1}\), right \(-\frac23\). Distinct.

## Representations

None as a separate block. The topic's Representations paragraph names a limit at infinity turned into a horizontal asymptote on a graph (BC-REP-01 to BC-REP-02); the orientation figure, the ki-1 motion and the ki-2 figure carry it.

## Prerequisite bridge

Two BC-PRQ parents: BC-PRQ-01004 (end behaviour of a rational function by degrees) and BC-PRQ-06005 (function notation, to BC-SKL-01060). One bridge each, gated by state.

## Time

BC-QA-01010 has `calculator_status` either and is "Typically one part of a multipart free response question". Plan 15 has no rule for either, so the part is taken as Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]; as an FRQ part its 2 points of 9 are 3.33 of 15.0 minutes (docs/lessons/unit-01/README.md, section 5). A fluent solver writes the limit expression, the \(|x|\) line and the value; the choice of function is held in the head but decides the value point.

## Checks

- chk-1, completion of ex-1, both bands: the \(|x|\) form is given. Key \(-\frac23\).
- chk-2, isomorph, both bands: root_coef 3, linear_coef 4, linear_const \(-1\), inner_const 7, denominator: \(\lim_{x\to-\infty}\frac{4x-1}{\sqrt{9x^2+7}}\). Key \(-\frac43\).
- chk-3, MCQ, low band: root_coef 5, linear_coef \(-2\), linear_const 3, inner_const 2, numerator: \(\lim_{x\to-\infty}\frac{\sqrt{25x^2+2}}{-2x+3}\). Key \(\frac52\). Distractors \(-\frac{25}{2}\) (BC-ERR-01023), \(\frac32\) (BC-ERR-01033, the vertical asymptote input), \(-\frac52\) (BC-ERR-01021, \(\frac{5\infty}{-2\infty}\) cancelled as numbers).

No draw equals a published BC-QA-01010 `parameter_draw`.

## Delivery

- orientation: figure. Rule 3, BC-REP-02 on BC-SKL-01059 and 01063: ex-1's graph with \(y=\frac23\) and \(y=-\frac23\) dashed.
- ki-1: motion. Rule 2: the window widens as \(x\) decreases without bound and the curve settles on \(y=-\frac23\) (docs/lessons/unit-01/README.md, section 6).
- ki-2: figure. Rule 3: the two ends of one graph with different asymptotes.
- ex-1, ex-2 and the four error blocks: step_reveal. Rule 1.

Figure presence: three drawn blocks (two figures and a motion), so no `no_figure_reason` is needed.

Every non-text choice is [inferred], settled by the modality A/B.

## Band plan

- Low (full): pr-1, orientation, the two bridges when gated, ki-1, ki-2, st-1 with its contrast pair, ex-1 with its scoring lines, chk-1, the four error blocks, ex-2 faded from step 3 with its scoring lines, chk-2, chk-3. 739 words, 5.0 minutes (cap 900 and 6).
- Mid (brief): pr-1, orientation, the two bridges when gated, ki-1, ki-2, st-1 with its contrast pair, ex-1 with its scoring lines, chk-1, err-01022, err-01023, chk-2. 442 words, 3.0 minutes (cap 450 and 3). The brief sits near its cap, so no anchor quote is served.
- Refresher: ki-1, ki-2, err-BC-ERR-01022, err-BC-ERR-01023, err-BC-ERR-01033, err-BC-ERR-01021, ex-1.

## Sources

- BC-CON-01017; BC-SKL-01058, BC-SKL-01059, BC-SKL-01060, BC-SKL-01061, BC-SKL-01063; BC-EK-LIM-2D3, BC-EK-LIM-2D4; ced:52
- BC-QA-01010; BC-FRQ-2025-Q1-C, BC-MCQ-PE2012-021
- BC-PT-99054, BC-PT-99004; sg-25:4, sg-25:3, sg-26:4, sg-25:2, sg-26:2, crabbc-25:3, cr-23:16; BC-ERR-99007
- BC-ERR-01022, BC-ERR-01023, BC-ERR-01033, BC-ERR-01021, BC-ERR-01024; BC-MIS-01014, BC-MIS-01018, BC-MIS-99008, BC-MIS-01005, BC-MIS-01012
- BC-PRQ-01004, BC-PRQ-06005
- research/units/unit-01-limits-continuity.md#1.15 Connecting Limits at Infinity and Horizontal Asymptotes
- research/question-analysis/question-archetypes.md#BC-QA-01010 End behaviour described by a limit at infinity
- research/scoring/common-point-losses.md#Notation points
- research/scoring/notation-requirements.md#Limit notation
- research/scoring/command-verbs.md#BC-CV-29 Write and evaluate a limit expression
- research/exam/exam-structure.md#Section and part layout
- [inferred] Exam part I-A for a `calculator_status` of either. Settled by a plan 15 rule for either.
- [inferred] Ex-2's contextual draw lies outside `parameter_spec`. Settled by a spec parameter for a contextual rate draw.
- [inferred] Non-text delivery modes. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-01017",
 "kind": "concept",
 "target_id": "BC-CON-01017",
 "unit": "01",
 "skills": ["BC-SKL-01058", "BC-SKL-01059", "BC-SKL-01060", "BC-SKL-01061", "BC-SKL-01063"],
 "prediction": {
  "id": "pr-1",
  "stem": {"text": "Predict \\(\\lim_{x\\to-\\infty}\\frac{\\sqrt{4x^2+5}}{3x+1}\\).", "command_verb": "predict"},
  "format": "mcq",
  "options": [
   {"id": "A", "label": "Positive \\(\\frac23\\)", "is_key": false},
   {"id": "B", "label": "Negative \\(\\frac23\\)", "is_key": true},
   {"id": "C", "label": "\\(\\frac43\\)", "is_key": false}
  ],
  "resolution": "Dividing by the dominant power leaves \\(\\frac{|x|}{x}\\) times \\(\\frac23\\), and \\(\\frac{|x|}{x}=-1\\) when \\(x<0\\), so the limit is \\(-\\frac23\\).",
  "sources": ["BC-CON-01017", "research/units/unit-01-limits-continuity.md#1.15 Connecting Limits at Infinity and Horizontal Asymptotes"]
 },
 "orientation": {
  "text": "A response writes the limit as the variable grows without bound, for the function the stem names, then its value. A finite value is a horizontal asymptote.",
  "sources": ["BC-CON-01017", "research/units/unit-01-limits-continuity.md#1.15 Connecting Limits at Infinity and Horizontal Asymptotes"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-2D3",
   "depth": "core",
   "text": "Divide by the dominant power. Under a square root it carries the sign of the end: \\(\\sqrt{x^2}=|x|\\), which is \\(-x\\) as \\(x\\to-\\infty\\).",
   "notation": "horizontal asymptote; end behaviour",
   "quote": null,
   "sources": ["BC-EK-LIM-2D3", "ced:52", "research/units/unit-01-limits-continuity.md#1.15 Connecting Limits at Infinity and Horizontal Asymptotes"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-2D4",
   "depth": "core",
   "text": "A finite limit \\(L\\) at either end gives the horizontal asymptote \\(y=L\\). Each end is checked on its own.",
   "notation": "",
   "quote": null,
   "sources": ["BC-EK-LIM-2D4", "ced:52", "research/units/unit-01-limits-continuity.md#1.15 Connecting Limits at Infinity and Horizontal Asymptotes"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01010",
   "cue": "A rule; asks for long run behaviour and its value.",
   "method": "The limit of the named function as the variable grows without bound.",
   "rival": "Substituting infinity into the expression as a number.",
   "separating_feature": "Infinity under the arrow, never inside.",
   "contrast": {
    "this": {"text": "Find \\(\\lim_{x\\to-\\infty}\\frac{\\sqrt{9x^2+2}}{5x-4}\\).", "archetype_id": "BC-QA-01010"},
    "not_this": {"text": "Find \\(\\lim_{x\\to-2^+}\\frac{3x}{x+2}\\).", "why_not": "The input is finite and the value infinite: a vertical asymptote."},
    "feature": "Infinity under the arrow, not in the value."
   },
   "sources": ["BC-QA-01010", "BC-ERR-01021"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01010",
   "bands": ["low", "mid"],
   "parameter_draw": {"root_coef": "2", "linear_coef": "3", "linear_const": "1", "inner_const": "5", "radical_place": "numerator"},
   "problem": {"text": "Find \\(\\lim_{x\\to-\\infty}\\frac{\\sqrt{4x^2+5}}{3x+1}\\).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "The arrow points to \\(-\\infty\\).", "why": "Written first: the expression point.", "expr": "sqrt(4*x**2+5)/(3*x+1)", "relation": "new", "point_type_id": "BC-PT-99054"},
    {"cue": "Dominant power \\(x\\); under the root, \\(|x|\\).", "why": "\\(\\sqrt{x^2}=|x|\\).", "expr": "Abs(x)*sqrt(4+5/x**2)/(x*(3+1/x))", "relation": "equivalent"},
    {"cue": "\\(x<0\\), so \\(\\frac{|x|}{x}=-1\\).", "why": "The \\(\\frac1x\\) terms vanish: \\(-\\frac23\\).", "expr": "-2/3", "relation": "limit", "variable": "x", "point": "-oo", "point_type_id": "BC-PT-99004"}
   ],
   "answer": {"form": "numeric", "expr": "-2/3"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-01010",
   "bands": ["low"],
   "fade_from": 3,
   "parameter_draw": {"context": "amount_and_rate", "amount": "6*t/(2*t+1)", "subject": "rate"},
   "problem": {"text": "An amount is \\(A(t)=\\frac{6t}{2t+1}\\). Write a limit expression for the long run rate of change of \\(A\\) and evaluate it.", "command_verb": "write"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "\"Rate of change of \\(A\\)\" names \\(A'\\).", "why": "The value point goes to the rate's limit only.", "expr": "6*t/(2*t+1)", "relation": "new"},
    {"cue": "Quotient rule on \\(A\\).", "why": "The limit is written on this.", "expr": "6/(2*t+1)**2", "relation": "differentiate", "variable": "t", "point_type_id": "BC-PT-99054"},
    {"cue": "Denominator grows without bound.", "why": "The rate tends to 0.", "expr": "0", "relation": "limit", "variable": "t", "point": "oo", "point_type_id": "BC-PT-99004"}
   ],
   "answer": {"form": "numeric", "expr": "0"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99054", "BC-PT-99004"], "lines": [
   {"point_type_id": "BC-PT-99054", "text": "Limit expression for end behaviour. Earned by: Writing the requested limit symbolically as the variable tends to infinity, for either the function or its derivative (sg-25:4). Not earned by: Setting up the limit so the variable tends to zero (crabbc-25:3); arithmetic with infinity in place of the value, which sg-25:4 treats as scratch work."},
   {"point_type_id": "BC-PT-99004", "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."}]},
  {"example_id": "ex-2", "point_type_ids": ["BC-PT-99054", "BC-PT-99004"], "lines": [
   {"point_type_id": "BC-PT-99054", "text": "Limit expression for end behaviour. Earned by: Writing the requested limit symbolically as the variable tends to infinity, for either the function or its derivative (sg-25:4). Not earned by: Setting up the limit so the variable tends to zero (crabbc-25:3); arithmetic with infinity in place of the value, which sg-25:4 treats as scratch work."},
   {"point_type_id": "BC-PT-99004", "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-01022",
   "observed_behavior": "The response writes the end behaviour limit of the modelled quantity rather than of its rate of change.",
   "scoring_consequence": "The expression point may still be earned, but a response presenting the limit of the amount is not eligible for the value point (sg-25:4).",
   "wrong_step": {"text": "\\(\\lim_{t\\to\\infty}A(t)=3\\).", "expr": "3"},
   "right_step": {"text": "\\(\\lim_{t\\to\\infty}A'(t)=0\\).", "expr": "0"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-01014", "text": "treats a statement about the long run rate as a statement about the long run amount"},
   "sources": ["BC-ERR-01022", "BC-MIS-01014"]
  },
  {
   "error_id": "BC-ERR-01023",
   "observed_behavior": "The response reports the ratio of the leading coefficients as the limit at infinity although the degrees differ.",
   "scoring_consequence": "The value point is lost.",
   "wrong_step": {"text": "\\(\\frac43\\) from 4 and 3.", "expr": "4/3"},
   "right_step": {"text": "\\(\\sqrt{4x^2}=2|x|\\): \\(-\\frac23\\).", "expr": "-2/3"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": ["BC-ERR-01023"]
  },
  {
   "error_id": "BC-ERR-01033",
   "observed_behavior": "The response treats a vertical asymptote statement as an end behaviour statement or the reverse.",
   "scoring_consequence": "The conversion point is lost.",
   "wrong_step": {"text": "End behaviour given as \\(x=-\\frac13\\).", "expr": "x = -1/3"},
   "right_step": {"text": "End behaviour \\(y=-\\frac23\\).", "expr": "y = -2/3"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-01018", "text": "does not separate a limit whose value is infinite from a limit taken as the variable grows without bound"},
   "sources": ["BC-ERR-01033", "BC-MIS-01018"]
  },
  {
   "error_id": "BC-ERR-01021",
   "observed_behavior": "The response substitutes the infinity symbol into the expression and performs arithmetic with it.",
   "scoring_consequence": "Arithmetic performed with the infinity symbol is treated as scratch work and does not earn the value point (sg-25:4).",
   "wrong_step": {"text": "\\(\\frac{\\sqrt{4\\cdot\\infty^2+5}}{3\\cdot\\infty+1}\\).", "expr": "sqrt(4*oo**2+5)/(3*oo+1)"},
   "right_step": {"text": "The \\(|x|\\) form, then \\(-\\frac23\\).", "expr": "-2/3"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-99008", "text": "substitutes the infinity symbol for the variable and computes with the result"},
   "sources": ["BC-ERR-01021", "BC-MIS-99008"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-01004", "text": "Compare degrees for large inputs. Slip: computing values instead."},
  {"prq_id": "BC-PRQ-06005", "text": "\\(A\\) and \\(A'\\) differ. Slip: \\(f\\) and \\(f'\\) interchanged."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 3], "ex-2": [2, 3]}, "skipped_steps": {"ex-1": [], "ex-2": [1]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-01010",
   "parameter_draw": {"root_coef": "2", "linear_coef": "3", "linear_const": "1", "inner_const": "5", "radical_place": "numerator"},
   "completes": "ex-1",
   "stem": {"text": "\\(\\frac{\\sqrt{4x^2+5}}{3x+1}=\\frac{|x|\\sqrt{4+5/x^2}}{x(3+1/x)}\\). Evaluate the limit as \\(x\\to-\\infty\\).", "command_verb": "evaluate"},
   "key": {"form": "numeric", "expr": "-2/3"},
   "steps": [
    {"text": "The \\(|x|\\) form.", "expr": "Abs(x)*sqrt(4+5/x**2)/(x*(3+1/x))", "relation": "new"},
    {"text": "\\(\\frac{|x|}{x}=-1\\).", "expr": "-2/3", "relation": "limit", "variable": "x", "point": "-oo"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-01061", "BC-SKL-01063"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-01010",
   "parameter_draw": {"root_coef": "3", "linear_coef": "4", "linear_const": "-1", "inner_const": "7", "radical_place": "denominator"},
   "stem": {"text": "Find \\(\\lim_{x\\to-\\infty}\\frac{4x-1}{\\sqrt{9x^2+7}}\\).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "-4/3"},
   "steps": [
    {"text": "The limit.", "expr": "(4*x-1)/sqrt(9*x**2+7)", "relation": "new"},
    {"text": "Factor out \\(x\\) and \\(|x|\\).", "expr": "(4-1/x)*x/(Abs(x)*sqrt(9+7/x**2))", "relation": "equivalent"},
    {"text": "\\(\\frac{x}{|x|}=-1\\).", "expr": "-4/3", "relation": "limit", "variable": "x", "point": "-oo"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-01061", "BC-SKL-01063"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-01010",
   "parameter_draw": {"root_coef": "5", "linear_coef": "-2", "linear_const": "3", "inner_const": "2", "radical_place": "numerator"},
   "stem": {"text": "Find \\(\\lim_{x\\to-\\infty}\\frac{\\sqrt{25x^2+2}}{-2x+3}\\).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "5/2"},
   "steps": [
    {"text": "The limit.", "expr": "sqrt(25*x**2+2)/(-2*x+3)", "relation": "new"},
    {"text": "Factor out \\(|x|\\) and \\(x\\).", "expr": "Abs(x)*sqrt(25+2/x**2)/(x*(-2+3/x))", "relation": "equivalent"},
    {"text": "\\(\\frac{|x|}{x}=-1\\).", "expr": "5/2", "relation": "limit", "variable": "x", "point": "-oo"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "-25/2", "error_path": "BC-ERR-01023", "derivation": "leading coefficients 25 and -2 divided"},
    {"id": "B", "is_key": false, "expr": "3/2", "error_path": "BC-ERR-01033", "derivation": "the vertical asymptote input reported"},
    {"id": "C", "is_key": false, "expr": "-5/2", "error_path": "BC-ERR-01021", "derivation": "5 times infinity over -2 times infinity cancelled as numbers"},
    {"id": "D", "is_key": true, "expr": "5/2", "error_path": null}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-01058", "BC-SKL-01061"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-01059 and BC-SKL-01063", "sources": ["BC-SKL-01059", "BC-SKL-01063"],
   "spec": {"kind": "graph", "window": {"x": [-20, 20], "y": [-3, 3]},
    "curves": [{"expr": "sqrt(4*x**2+5)/(3*x+1)", "domain": [-20, 20], "break_at": [-0.3333]}],
    "asymptotes": [{"type": "horizontal", "y": "2/3", "style": "dashed"}, {"type": "horizontal", "y": "-2/3", "style": "dashed"}],
    "labels": [{"text": "y = 2/3 as x grows", "placement": "inside"}, {"text": "y = -2/3 as x falls", "placement": "inside"}],
    "representations": ["BC-REP-02"]},
   "fallback": "the same graph as a static image with its two labels", "keyboard": "none needed: the figure has no control"},
  {"block": "ki-1", "mode": "motion", "reason": "rule 2: a limit process, the window widening toward negative infinity; rule 3, BC-REP-02 on BC-SKL-01063", "sources": ["BC-SKL-01061", "BC-SKL-01063"],
   "spec": {"kind": "graph", "curves": [{"expr": "sqrt(4*x**2+5)/(3*x+1)"}],
    "frames": [{"window": {"x": [-10, 0], "y": [-2, 1]}}, {"window": {"x": [-100, 0], "y": [-2, 1]}}, {"window": {"x": [-1000, 0], "y": [-2, 1]}}],
    "asymptotes": [{"type": "horizontal", "y": "-2/3", "style": "dashed"}],
    "labels": [{"text": "y = -2/3", "placement": "inside"}, {"text": "sqrt(x^2) = -x here", "placement": "inside"}],
    "representations": ["BC-REP-02"]},
   "fallback": "the three windows side by side as static images", "keyboard": "Right arrow steps to the next window, Left arrow to the previous; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next window"},
  {"block": "ki-2", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-01059", "sources": ["BC-SKL-01059"],
   "spec": {"kind": "graph", "window": {"x": [-20, 20], "y": [-3, 3]},
    "curves": [{"expr": "sqrt(4*x**2+5)/(3*x+1)", "domain": [-20, 20], "break_at": [-0.3333]}],
    "asymptotes": [{"type": "horizontal", "y": "2/3", "style": "dashed"}, {"type": "horizontal", "y": "-2/3", "style": "dashed"}],
    "labels": [{"text": "right end", "placement": "inside"}, {"text": "left end", "placement": "inside"}],
    "representations": ["BC-REP-02"]},
   "fallback": "the same graph as a static image with its two labels", "keyboard": "none needed: the figure has no control"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01022", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01023", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01033", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01021", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "ki-2", "err-BC-ERR-01022", "err-BC-ERR-01023", "err-BC-ERR-01033", "err-BC-ERR-01021", "ex-1"],
 "read_minutes": {"full": 5.0, "brief": 3.0},
 "word_count": {"full": 739, "brief": 442},
 "research_lines": [
  {"file": "research/scoring/notation-requirements.md", "line": "sg-25:4 states that for the end-behaviour value point, arithmetic with infinity will be considered as scratch work and will not be considered in scoring."}
 ],
 "inferred": [
  {"claim": "BC-QA-01010 has calculator_status either, so the exam part is taken as I-A.", "settles": "A plan 15 budget rule for calculator_status either."},
  {"claim": "Ex-2's contextual amount and rate draw lies outside the parameter_spec, which draws only the radical quotient.", "settles": "A parameter_spec variant for a contextual rate draw."},
  {"claim": "The figure and motion modes serve the orientation and key ideas better than text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-01017", "BC-SKL-01058", "BC-SKL-01059", "BC-SKL-01060", "BC-SKL-01061", "BC-SKL-01063", "BC-EK-LIM-2D3", "BC-EK-LIM-2D4", "ced:52", "BC-QA-01010", "BC-FRQ-2025-Q1-C", "BC-MCQ-PE2012-021", "BC-PT-99054", "BC-PT-99004", "sg-25:4", "sg-25:3", "sg-26:4", "crabbc-25:3", "cr-23:16", "BC-ERR-99007", "BC-ERR-01022", "BC-ERR-01023", "BC-ERR-01033", "BC-ERR-01021", "BC-ERR-01024", "BC-MIS-01014", "BC-MIS-01018", "BC-MIS-99008", "BC-MIS-01005", "BC-MIS-01012", "BC-PRQ-01004", "BC-PRQ-06005", "research/units/unit-01-limits-continuity.md#1.15 Connecting Limits at Infinity and Horizontal Asymptotes", "research/question-analysis/question-archetypes.md#BC-QA-01010 End behaviour described by a limit at infinity", "research/scoring/common-point-losses.md#Notation points", "research/scoring/notation-requirements.md#Limit notation", "research/scoring/command-verbs.md#BC-CV-29 Write and evaluate a limit expression", "research/exam/exam-structure.md#Section and part layout"]
}
```
