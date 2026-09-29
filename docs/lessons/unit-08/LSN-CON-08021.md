---
title: LSN-CON-08021 Arc length of a curve given by a function
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08021, the length of the graph of a function written as the integral of the square root of one plus the squared derivative over the stated interval, evaluated with a calculator or named with its interval, built from authoring_bundle("BC-CON-08021") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08021 Arc length of a curve given by a function

Concept BC-CON-08021 (skills BC-SKL-08056, BC-SKL-08057, BC-SKL-08058, BC-SKL-08059), topic 8.13 of Unit 8, BC only (ced:164), loaded by one archetype, BC-QA-08014 (family arc-length). No Unit 8 hard parent (docs/lessons/unit-08/README.md, section 1); the outside hard parents are BC-SKL-02021, 06034 and 06057, so differentiation by the product rule and a definite integral are assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers with the core claim that a small piece of the graph has length sqrt of one plus the squared slope, times dx. The question is the length of the piece over a run dx at x = 1, where f'(1) = 1. Key B, sqrt 2 dx. The distractors are dx (the run alone) and 2 dx (the run plus the rise added). The piece is the hypotenuse of a right triangle with legs dx and dy, which the Pythagorean theorem gives before any method is taught. The resolution states the hypotenuse and the general form, with no verdict. Source: BC-CON-08021 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-08021 `description_plain` ("the integral of the square root of one plus the square of the slope") and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.13 The Arc Length of a Smooth, Planar Curve and Distance Traveled): the MCQ asks which integral gives the length, the calculator FRQ asks for the length of a described curve with the setup, and the no calculator FRQ asks for the setup or for what a displayed integral tells about the graph. The orientation states what a response shows in each: the integral with the interval's limits, the value, or the length and the interval named. No count, no frequency.

## Key ideas

All four skills map to one essential knowledge statement, BC-EK-CHA-6A1 (ced:164): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs Arc length (hypothesis: f has a continuous derivative on [a, b]; conclusion: the length is the integral of the square root of one plus f prime squared, with respect to x), Notation ("The derivative is squared inside the radical; the radical covers the whole sum.") and Identification (a response names both the quantity and the interval, sg-24:16). Notation line: the concept's `notation`, "arc length integral". No anchor quote: the CHA-6.A.1 sentence on ced:164 adds no content the paraphrase lacks and costs 16 words in the brief band (Band plan).

## Recognition

BC-QA-08014 (research/question-analysis/question-archetypes.md#BC-QA-08014 Arc length of a curve given by a function) is the only archetype loading the four skills.

- `common_givens`: "a function, sometimes only through a table of its derivative" and "a closed interval".
- `asked_to_produce`: "an integral expression, or a sentence naming arc length and the interval" and "a numerical length".
- `typical_wording`: "find the length of the curve on the stated interval and show the setup"; "what information does the displayed integral give about the graph of the function".
- The signal in the stem: the word length (of the graph, of the curve, of a wire bent along the graph) with an x interval; or a displayed integral whose integrand is a radical of one plus a squared derivative. The generator's context framing is "A wire is bent into the shape of the graph of" (app/generation/templates/qa_08014.py `CONTEXTS`).
- Shapes: an MCQ asking which integral gives the length, with area and volume forms as distractors (topic Assessment behaviour); a no calculator FRQ part, BC-FRQ-2014-Q5-C (the derivative by the product rule, then the integral), and BC-FRQ-2024-Q5-B (identify the displayed integral, two points, sg-24:16); a calculator setup and value part, BC-FRQ-2026-Q5-C; the MCQ BC-MCQ-PE2012-004. BC-QA-08014 `multipart_structure`: "One part of a multipart BC only no calculator question, or a calculator active setup and value part."

The near miss of the contrast pair is the area under the same curve on the same interval, the first `common_distractors` entry of BC-QA-08014, which belongs to the area concepts (BC-CON-08010): the two stems share a function and an interval and differ in what they ask for.

What says "not this concept": the stem asks for an area or a volume on the same region (BC-CON-08010, 08014, 08017; `common_distractors` "the area under the curve"); the curve is given as \(x(t), y(t)\) on a t interval, which is the parametric length (BC-SKL-09011, docs/lessons/unit-08/README.md, section 3); a particle on the x axis, which is total distance (`common_distractors`).

## Method choice

- st-1, BC-QA-08014. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]` "differentiate the function", then the next two entries, "square the derivative and add one" and "take the square root and integrate over the interval", written as one first line. Rival: `common_distractors` "the area under the curve", and `wrong_approaches` "omitting the square on the derivative". Separating feature: the stem asks for a length along the graph, not the region under it. Both cue fields exist, so the block is not inferred. The block also carries the contrast pair, a length stem beside an area stem on one function and interval, with the feature that separates them. No served field opens with the reader's own label, so the method reads as the step itself.

## Solution path

- ex-1, BC-QA-08014, both bands, no calculator. Draw: form log, scale 1, left 1, width 2 (right 3), units feet, framing bare, task setup. \(f(x)=x\ln x\) on \([1,3]\), \(f'(x)=\ln x+1\), key \(\int_1^3\sqrt{1+(\ln x+1)^2}\,dx\). No published item on BC-QA-08014 carries this draw (content/items_gen_unit08/ITM-GEN-08014-00 to 21; FRQ-AGT-08014-01 has none).
- ex-2, low band, calculator. Draw: form radical, scale 1, left 1, width 2 (right 3), units feet, framing context, task evaluate. \(f(x)=x\sqrt{x+1}\), \(f'(x)=\frac{3x+2}{2\sqrt{x+1}}\), length 5.00818 by SymPy, reported 5.008.
- ex-2 is faded from step 3: steps 1 and 2 (the function and its derivative) are shown, the student writes the answer, and steps 3 and 4 (the setup integral and the calculator value) then reveal. The fade falls there because the recognition and the product rule repeat ex-1's pattern, and the setup and the evaluation are what the student must produce.
- Steps follow `expected_solution_path`: the recognition with f (new), \(f'\) (differentiate), the radical (new), the integral with limits (new), and on ex-2 the value (evaluate, three places). A fluent solver writes \(f'\) and the integral, and on ex-2 the value; the recognition and the bare radical are held (Time).
- No productive-failure comparison: BC-CON-08021 is not in `PRODUCTIVE_FAILURE_TARGETS` (docs/lessons/unit-08/README.md, opening).

## Scoring

BC-QA-08014 lists BC-PT-99022, 99051, 99004, 99009, 99001. ex-1 tags BC-PT-99051 on the integral only, and its BC-PT-99022 tag on \(f'\) is dropped to fit the brief cap once the prediction and contrast pair are served (inferred array); ex-2 tags BC-PT-99022, 99051 and 99004. The lines are `reader_checks` output. BC-PT-99009 (arc length and interval named, sg-24:16) is taught in ki-1 and err-BC-ERR-08043 but tagged on no step, because the parameter_spec has no interpret task (library gap). BC-PT-99001 is untagged: BC-PT-99051 already scores the definite integral on this shape.

Point losses from research: the interval omitted from an arc length interpretation (research/scoring/common-point-losses.md#Interpretation points, cr-24:32); the interval point stays available after the arc length point is lost (research/scoring/point-taxonomy.md#BC-PT-99009 Interpretation of an integral as an arc length over an interval, sg-24:16); the form point needs numerical limits only, and the next point assesses the derivative (BC-PT-99051 `notation_requirements`, sg-26:19).

## Traps

Four errors meet the skills, in bundle order: BC-ERR-08019, BC-ERR-08041, BC-ERR-08042, BC-ERR-08043 (each linked to a high severity BC-MIS, then by id). BC-ERR-08044, 08045, 99019 and 99021 fall past the cap of 4. Low band all four, mid band the first two. All on ex-1's draw. All four carry `fix_prompt` true, since each pair is distinct.

- err-BC-ERR-08019: lower limit 0 in place of 1. No possible reason line (brief band words); the record links BC-MIS-08012 and 08014.
- err-BC-ERR-08041: the integral of \(f'\) with no radical, the record's first form. No possible reason line (brief band words); the record links BC-MIS-08024 and 08019.
- err-BC-ERR-08042: \(\sqrt{1+f'}\). Possible reason, BC-MIS-08024.
- err-BC-ERR-08043: the sentence names the length with no interval; the SymPy pair is the interval the sentence names, the empty set against \([1,3]\). Possible reason, BC-MIS-08009.

## Representations

None. The topic's Representations paragraph names BC-REP-01, 04 and 09 and the conversions symbolic to verbal and symbolic to calculator value; nothing figure-shaped (docs/lessons/unit-08/README.md, section 6).

## Prerequisite bridge

- BC-PRQ-06005, BC-PRQ-08006, BC-PRQ-08007, each from its `description_plain` and `failure_signature`.

## Time

ex-1 is the setup draw, `no_calculator` in the generator, the MCQ form "which integral gives the length": Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred for an either archetype]. As a free response part: 2 points, 3.33 minutes; 3 points with the product rule on BC-FRQ-2014-Q5-C, 5.0 minutes (docs/lessons/unit-08/README.md, section 5). A fluent solver writes \(f'\) and the integral with limits; the recognition and the radical before the limits are held. The minutes go on the product rule.

## Checks

- chk-1, completion of ex-1, both bands: \(f'\) given, the integral asked. Key \(\int_1^3\sqrt{1+(\ln x+1)^2}\,dx\).
- chk-2, isomorph, both bands, no calculator. Draw: form radical, scale 1/2, left 2, width 1, units inches, framing bare, task setup. \(f(x)=\frac12x\sqrt{x+1}\), \(f'(x)=\frac{3x+2}{4\sqrt{x+1}}\). Key \(\int_2^3\sqrt{1+\left(\frac{3x+2}{4\sqrt{x+1}}\right)^2}\,dx\).
- chk-3, MCQ, low band, calculator. Draw: form exponential, scale 1, left 2, width 2, units feet, framing bare, task evaluate. \(f(x)=xe^{x/4}\), \(f'(x)=\frac{(x+4)e^{x/4}}{4}\). Key 7.848 (SymPy 7.84769). Distractors: 4.359, \(\sqrt{1+f'}\) (BC-ERR-08042); 7.576, \(\int_2^4 f'\,dx=f(4)-f(2)\) (BC-ERR-08041); 11.730, lower limit 0 (BC-ERR-08019).

## Delivery

- orientation, ki-1: text. Rule 6: the skills carry BC-REP-01, 04, 05, 09, none figure-bearing (docs/lessons/unit-08/README.md, section 6). No block is drawn, so the record carries `no_figure_reason`: no skill has a figure-bearing representation and no key idea describes a process.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, the four error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 848 words, 5.7 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-08019, err-BC-ERR-08041, chk-2. 450 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-08021; BC-SKL-08056, BC-SKL-08057, BC-SKL-08058, BC-SKL-08059; BC-EK-CHA-6A1; ced:164
- BC-QA-08014; BC-PT-99022, BC-PT-99051, BC-PT-99004, BC-PT-99009
- BC-ERR-08019, BC-ERR-08041, BC-ERR-08042, BC-ERR-08043; BC-MIS-08012, BC-MIS-08024, BC-MIS-08009
- BC-PRQ-06005, BC-PRQ-08006, BC-PRQ-08007
- sg-24:16, sg-26:19, cr-24:32
- research/units/unit-08-applications-integration.md#8.13 The Arc Length of a Smooth, Planar Curve and Distance Traveled
- research/question-analysis/question-archetypes.md#BC-QA-08014 Arc length of a curve given by a function
- research/scoring/common-point-losses.md#Interpretation points
- research/scoring/point-taxonomy.md#BC-PT-99009 Interpretation of an integral as an arc length over an interval
- research/exam/exam-structure.md#Section and part layout
- [inferred] Part A for the setup draw of an either archetype; the interpret task missing from the parameter_spec; the held steps; ex-1's product rule point untagged. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-08021",
 "kind": "concept",
 "target_id": "BC-CON-08021",
 "unit": "08",
 "skills": ["BC-SKL-08056", "BC-SKL-08057", "BC-SKL-08058", "BC-SKL-08059"],
 "prediction": {
  "id": "pr-1",
  "stem": {"text": "Let \\(f(x)=x\\ln x\\), so \\(f'(1)=1\\). Predict the length of the graph over a small run \\(dx\\) at \\(x=1\\).", "command_verb": "predict"},
  "format": "mcq",
  "options": [{"id": "A", "label": "\\(dx\\)", "is_key": false}, {"id": "B", "label": "\\(\\sqrt{2}\\,dx\\)", "is_key": true}, {"id": "C", "label": "\\(2\\,dx\\)", "is_key": false}],
  "resolution": "The piece is the hypotenuse of legs \\(dx\\) and \\(f'(1)\\,dx\\), so its length is \\(\\sqrt{2}\\,dx\\), and \\(\\sqrt{1+(f'(x))^2}\\,dx\\) in general.",
  "sources": ["BC-CON-08021", "research/units/unit-08-applications-integration.md#8.13 The Arc Length of a Smooth, Planar Curve and Distance Traveled"]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (the topic names symbolic, verbal and calculator forms) and no key idea describes a process, since the length is a formula in the derivative.",
 "orientation": {
  "text": "Length of a graph: \\(\\int_a^b\\sqrt{1+(f'(x))^2}\\,dx\\) over the stated interval. A response writes it with limits, then the value, or names length and interval.",
  "sources": ["BC-CON-08021", "research/units/unit-08-applications-integration.md#8.13 The Arc Length of a Smooth, Planar Curve and Distance Traveled"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-6A1",
   "depth": "core",
   "text": "With \\(f'\\) continuous on \\([a,b]\\), the length of the graph is \\(\\int_a^b\\sqrt{1+(f'(x))^2}\\,dx\\). The derivative is squared and the radical covers the whole sum. A displayed integral of that form is named as a length over its interval.",
   "notation": "arc length integral",
   "quote": null,
   "sources": ["BC-EK-CHA-6A1", "ced:164", "sg-24:16", "research/units/unit-08-applications-integration.md#8.13 The Arc Length of a Smooth, Planar Curve and Distance Traveled"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08014",
   "cue": "A function, an interval, the word length.",
   "method": "\\(f'(x)\\), then \\(\\int_a^b\\sqrt{1+(f'(x))^2}\\,dx\\).",
   "rival": "Area under the curve, or \\(f'\\) unsquared.",
   "separating_feature": "Length along the graph, not the region under it.",
   "sources": ["BC-QA-08014"],
   "evidence_tag": "verified",
   "contrast": {
    "this": {"text": "Let \\(f(x)=e^{2x}\\). Find the length of the graph of f on \\([0,1]\\).", "archetype_id": "BC-QA-08014"},
    "not_this": {"text": "Let \\(f(x)=e^{2x}\\). Find the area under the graph of f on \\([0,1]\\).", "why_not": "It asks for the area under the graph, so the integrand is f."},
    "feature": "Length along the graph, not area beneath it."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08014",
   "bands": ["low", "mid"],
   "parameter_draw": {"form": "log", "scale": "1", "left": 1, "width": 2, "units": "feet", "framing": "bare", "task": "setup"},
   "problem": {"text": "Let \\(f(x)=x\\ln x\\). Write, but do not evaluate, an integral for the length of the graph of f from \\(x=1\\) to \\(x=3\\).", "command_verb": "write"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Length of the graph.", "why": "Length needs the slope.", "expr": "x*log(x)", "relation": "new"},
    {"cue": "f is a product.", "why": "Product rule.", "expr": "log(x) + 1", "relation": "differentiate", "variable": "x"},
    {"cue": "\\(f'\\) in hand: square, add one, root.", "why": "Radical over the whole sum.", "expr": "sqrt(1 + (log(x) + 1)**2)", "relation": "new"},
    {"cue": "Stem gives 1 to 3.", "why": "The integral is the answer.", "expr": "Integral(sqrt(1 + (log(x) + 1)**2), (x, 1, 3))", "relation": "new", "point_type_id": "BC-PT-99051"}
   ],
   "answer": {"form": "symbolic", "expr": "Integral(sqrt(1 + (log(x) + 1)**2), (x, 1, 3))"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-08014",
   "bands": ["low"],
   "parameter_draw": {"form": "radical", "scale": "1", "left": 1, "width": 2, "units": "feet", "framing": "context", "task": "evaluate"},
   "problem": {"text": "A wire is bent into the shape of the graph of \\(f(x)=x\\sqrt{x+1}\\) for \\(1\\le x\\le 3\\), in feet. Using a calculator, find the length of the wire. Show the setup.", "command_verb": "find"},
   "calculator_status": "calculator",
   "steps": [
    {"cue": "The wire lies along the graph: arc length.", "why": "Length, not area.", "expr": "x*sqrt(x + 1)", "relation": "new"},
    {"cue": "f is a product.", "why": "Product rule, chain rule on the root.", "expr": "(3*x + 2)/(2*sqrt(x + 1))", "relation": "differentiate", "variable": "x", "point_type_id": "BC-PT-99022"},
    {"cue": "Show the setup: the integral on paper.", "why": "It earns the setup point.", "expr": "Integral(sqrt(1 + ((3*x + 2)/(2*sqrt(x + 1)))**2), (x, 1, 3))", "relation": "new", "point_type_id": "BC-PT-99051"},
    {"cue": "Setup written, so the calculator evaluates it.", "why": "Three places, feet.", "expr": "5.008", "relation": "evaluate", "subs": {}, "approx": true, "point_type_id": "BC-PT-99004"}
   ],
   "answer": {"form": "numeric", "expr": "5.008"},
   "fade_from": 3
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": ["BC-PT-99051"],
   "lines": [
    {
     "point_type_id": "BC-PT-99051",
     "text": "Arc length or total distance integrand. Earned by: A definite integral whose integrand is the square root of one plus the square of the derivative, or the square root of the sum of the squares of the component derivatives (sg-26:19, sg-22:9). Not earned by: An unsupported value (sg-22:9); an integrand imported from an incorrect speed function, which sg-23:8 allows for this point but not for the answer point. Notation: sg-26:19 requires the limits to be numerical but not correct for this point, and assesses the derivative expression and the straight boundaries in the following point."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": ["BC-PT-99022", "BC-PT-99051", "BC-PT-99004"],
   "lines": [
    {
     "point_type_id": "BC-PT-99022",
     "text": "Product rule. Earned by: A differentiation that correctly applies the product rule to the given expression (sg-25:20, sg-22:16). Not earned by: A response that treats one factor as constant, which sg-22:16 states is eligible for the chain rule point but not this one."
    },
    {
     "point_type_id": "BC-PT-99051",
     "text": "Arc length or total distance integrand. Earned by: A definite integral whose integrand is the square root of one plus the square of the derivative, or the square root of the sum of the squares of the component derivatives (sg-26:19, sg-22:9). Not earned by: An unsupported value (sg-22:9); an integrand imported from an incorrect speed function, which sg-23:8 allows for this point but not for the answer point. Notation: sg-26:19 requires the limits to be numerical but not correct for this point, and assesses the derivative expression and the straight boundaries in the following point."
    },
    {
     "point_type_id": "BC-PT-99004",
     "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-08019",
   "observed_behavior": "The integral is set up with limits that are not the boundary of the region or the interval requested.",
   "scoring_consequence": "The answer point is lost, and in 2023 incorrect limits also made a response ineligible for the final area point (sg-23:16).",
   "wrong_step": {"text": "From 0.", "expr": "Integral(sqrt(1 + (log(x) + 1)**2), (x, 0, 3))"},
   "right_step": {"text": "From 1.", "expr": "Integral(sqrt(1 + (log(x) + 1)**2), (x, 1, 3))"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-08019"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08041",
   "observed_behavior": "The length integral is written as the integral of the derivative, or of the square root of the derivative squared alone.",
   "scoring_consequence": "The setup point is lost.",
   "wrong_step": {"text": "\\(\\int f'\\).", "expr": "Integral(log(x) + 1, (x, 1, 3))"},
   "right_step": {"text": "\\(\\int\\sqrt{1+(f')^2}\\).", "expr": "Integral(sqrt(1 + (log(x) + 1)**2), (x, 1, 3))"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-08041"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08042",
   "observed_behavior": "The integrand is the square root of one plus the derivative.",
   "scoring_consequence": "The setup point is lost.",
   "wrong_step": {"text": "\\(\\sqrt{1+f'}\\).", "expr": "Integral(sqrt(1 + (log(x) + 1)), (x, 1, 3))"},
   "right_step": {"text": "\\(\\sqrt{1+(f')^2}\\).", "expr": "Integral(sqrt(1 + (log(x) + 1)**2), (x, 1, 3))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08024", "text": "its own form is not examined"},
   "sources": ["BC-ERR-08042", "BC-MIS-08024"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08043",
   "observed_behavior": "The response says the integral gives the length of the curve but does not say on which interval.",
   "scoring_consequence": "The interval point is lost while the arc length point stands (sg-24:16).",
   "wrong_step": {"text": "The length of the graph of f.", "expr": "EmptySet"},
   "right_step": {"text": "The length of the graph of f from \\(x=1\\) to \\(x=3\\).", "expr": "Interval(1, 3)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08009", "text": "treats the sentence as a label for the integral"},
   "sources": ["BC-ERR-08043", "BC-MIS-08009"],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [{"prq_id": "BC-PRQ-06005", "text": "The radical needs \\(f'(x)\\), not f."}, {"prq_id": "BC-PRQ-08006", "text": "Three places after the decimal point."}, {"prq_id": "BC-PRQ-08007", "text": "Components combine as a root of squares."}],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 4]}, "skipped_steps": {"ex-1": [1, 3]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08014",
   "parameter_draw": {"form": "log", "scale": "1", "left": 1, "width": 2, "units": "feet", "framing": "bare", "task": "setup"},
   "completes": "ex-1",
   "stem": {"text": "\\(f'(x)=\\ln x+1\\). Write the length integral from \\(x=1\\) to \\(x=3\\).", "command_verb": "write"},
   "key": {"form": "symbolic", "expr": "Integral(sqrt(1 + (log(x) + 1)**2), (x, 1, 3))"},
   "steps": [{"text": "Square, add one, root.", "expr": "sqrt(1 + (log(x) + 1)**2)", "relation": "new"}, {"text": "Limits 1 and 3.", "expr": "Integral(sqrt(1 + (log(x) + 1)**2), (x, 1, 3))", "relation": "new"}],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08056"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08014",
   "parameter_draw": {"form": "radical", "scale": "1/2", "left": 2, "width": 1, "units": "inches", "framing": "bare", "task": "setup"},
   "stem": {"text": "Let \\(f(x)=\\frac{1}{2}x\\sqrt{x+1}\\). Write, but do not evaluate, an integral for the length of the graph of f from \\(x=2\\) to \\(x=3\\).", "command_verb": "write"},
   "key": {"form": "symbolic", "expr": "Integral(sqrt(1 + ((3*x + 2)/(4*sqrt(x + 1)))**2), (x, 2, 3))"},
   "steps": [
    {"text": "f.", "expr": "x*sqrt(x + 1)/2", "relation": "new"},
    {"text": "Product rule.", "expr": "(3*x + 2)/(4*sqrt(x + 1))", "relation": "differentiate", "variable": "x"},
    {"text": "Limits 2 and 3.", "expr": "Integral(sqrt(1 + ((3*x + 2)/(4*sqrt(x + 1)))**2), (x, 2, 3))", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08057"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-08014",
   "parameter_draw": {"form": "exponential", "scale": "1", "left": 2, "width": 2, "units": "feet", "framing": "bare", "task": "evaluate"},
   "stem": {"text": "Let \\(f(x)=xe^{x/4}\\). With a calculator, the length of the graph of f from \\(x=2\\) to \\(x=4\\) is", "command_verb": "identify"},
   "key": {"form": "numeric", "expr": "7.848"},
   "steps": [
    {"text": "f.", "expr": "x*exp(x/4)", "relation": "new"},
    {"text": "Product rule.", "expr": "(x + 4)*exp(x/4)/4", "relation": "differentiate", "variable": "x"},
    {"text": "Setup.", "expr": "Integral(sqrt(1 + ((x + 4)*exp(x/4)/4)**2), (x, 2, 4))", "relation": "new"},
    {"text": "Calculator.", "expr": "7.848", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "4.359", "error_path": "BC-ERR-08042", "derivation": "the integral of the square root of 1 + f'(x), the derivative unsquared"},
    {"id": "B", "is_key": false, "expr": "7.576", "error_path": "BC-ERR-08041", "derivation": "the integral of f'(x) from 2 to 4, which is f(4) - f(2)"},
    {"id": "C", "is_key": true, "expr": "7.848", "error_path": null},
    {"id": "D", "is_key": false, "expr": "11.730", "error_path": "BC-ERR-08019", "derivation": "the arc length integrand integrated from 0 to 4"}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-08059"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response shows", "sources": ["BC-CON-08021"]},
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-01, 04, 05, 09 on BC-SKL-08056 to 08059, none figure-bearing; the idea is a formula and a sentence, not a process",
   "sources": ["BC-SKL-08056", "BC-SKL-08057", "BC-SKL-08058", "BC-SKL-08059"]
  },
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08019", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08041", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08042", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08043", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-08019", "err-BC-ERR-08041", "err-BC-ERR-08042", "err-BC-ERR-08043", "ex-1"],
 "read_minutes": {"full": 5.7, "brief": 3.0},
 "word_count": {"full": 848, "brief": 450},
 "research_lines": [{"file": "research/units/unit-08-applications-integration.md", "line": "The derivative is squared inside the radical; the radical covers the whole sum."}],
 "inferred": [
  {"claim": "BC-QA-08014 is calculator status either; the setup draw, which the generator marks no_calculator, is timed against Section I Part A at 2.14 minutes.", "settles": "Timing data on arc length items split by exam part."},
  {
   "claim": "BC-PT-99009, the identification point, is taught in ki-1 and in the BC-ERR-08043 block but tagged on no worked step, because BC-QA-08014's parameter_spec has no interpret task.",
   "settles": "A parameter_spec task value that displays the integral and asks what it gives about the graph."
  },
  {"claim": "A fluent solver writes the derivative and the integral and holds the recognition and the bare radical.", "settles": "Timing data per step once the fluency telemetry exists."},
  {
   "claim": "ex-1's product rule point (BC-PT-99022) is earned but not tagged, because the prediction and contrast pair take the words its reader line needs in the brief band; ex-2 carries the tag.",
   "settles": "A brief cap that admits the reader line, or a shorter prediction and contrast."
  }
 ],
 "sources": [
  "BC-CON-08021",
  "BC-SKL-08056",
  "BC-SKL-08057",
  "BC-SKL-08058",
  "BC-SKL-08059",
  "BC-EK-CHA-6A1",
  "ced:164",
  "BC-QA-08014",
  "BC-PT-99022",
  "BC-PT-99051",
  "BC-PT-99004",
  "BC-PT-99009",
  "BC-ERR-08019",
  "BC-ERR-08041",
  "BC-ERR-08042",
  "BC-ERR-08043",
  "BC-MIS-08024",
  "BC-MIS-08009",
  "BC-PRQ-06005",
  "BC-PRQ-08006",
  "BC-PRQ-08007",
  "sg-24:16",
  "sg-26:19",
  "cr-24:32",
  "research/units/unit-08-applications-integration.md#8.13 The Arc Length of a Smooth, Planar Curve and Distance Traveled",
  "research/question-analysis/question-archetypes.md#BC-QA-08014 Arc length of a curve given by a function",
  "research/scoring/common-point-losses.md#Interpretation points",
  "research/scoring/point-taxonomy.md#BC-PT-99009 Interpretation of an integral as an arc length over an interval",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
