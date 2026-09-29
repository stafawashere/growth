---
title: LSN-CON-07003 Families of solutions
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-07003, a differential equation satisfied by a whole family of functions from which an initial condition selects one, built from authoring_bundle("BC-CON-07003") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-07003 Families of solutions

Concept BC-CON-07003 (skill BC-SKL-07009), topic 7.2 of Unit 7, loaded by BC-QA-07007 (family de-verification). Its hard parent is BC-CON-07002 through BC-SKL-07006 (docs/lessons/unit-07/README.md, section 1).

## Prediction

One `mcq`, both bands, on ex-1's equation: y = 4 + e^x satisfies dy/dx = y - 4, and the question is how many functions satisfy it. Key B, infinitely many. The distractors are one (the printed function only) and exactly two. The student can settle it from the fact that adding a constant changes no derivative, before any rule is taught. The resolution shows that every 4 + Ce^x gives the same right side and that a stated point fixes one C. Sources: BC-CON-07003 and the topic 7.2 section the key idea cites.

## Orientation

Served text, from BC-CON-07003 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-07-differential-equations.md#7.2 Verifying Solutions for Differential Equations): a response shows that a formula with a constant satisfies the equation for every value of the constant, then lets the initial condition select one member. No count, no frequency.

## Key ideas

BC-SKL-07009 maps to BC-EK-FUN-7B2 (ced:138), one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Multiplicity of solutions): one equation has infinitely many solutions; a constant in the formula indexes them; a condition picks one. Anchor quote, the full EK sentence on ced:138 (10 words), in its clarified wording. Notation line from the concept record.

## Recognition

BC-QA-07007 (research/question-analysis/question-archetypes.md#BC-QA-07007 Verification that a function solves a differential equation), through its `difficulty_variables` "whether the candidate carries an arbitrary constant": a candidate with C beside the equation, and often a stated point. The topic names the conceptual variant "how many solutions an equation has" and the multi-concept variant where "only one member of the family survives" (research/units/unit-07-differential-equations.md#7.2 Verifying Solutions for Differential Equations).

The contrast pair sits on st-1. Its near miss is a BC-QA-07003 stem, whose `typical_wording` is "use separation of variables to find an expression for the particular solution to the differential equation with the given initial condition" (research/question-analysis/question-archetypes.md#BC-QA-07003 Particular solution by separation of variables): the same equation and point with no candidate printed, so the family is derived, not verified. The feature that separates them is a printed constant C. What says "not this concept": a candidate with no constant (BC-CON-07002), or "use separation of variables" (BC-CON-07007).

## Method choice

- st-1, BC-QA-07007. Method, `expected_solution_path[0]`: differentiate the candidate, with C held as a constant. Rival, `wrong_approaches`: solving the equation from scratch. Separating feature: the family is printed, so it is verified for every C, and C is then fixed by the point. Both fields present, so not tagged inferred. The block carries the contrast pair, and no strategy field opens with its own label, because the reader prints Cue, First line, Rival and Separating feature.

## Solution path

- ex-1, both bands. Draw: case solution, rate 1, level 4, initial 2, shift -1, so dy/dx = y - 4, y(0) = 2, family y = 4 + Ce^x. No published BC-QA-07007 item carries this draw.
- Steps: family (new); derivative (differentiate); right side (new); equal (equivalent); condition equation (new); C (solve); particular solution (new). A fluent solver writes all of them; the solve for C is one line.

## Scoring

BC-QA-07007 lists BC-PT-99005, 99068, 99004. ex-1 tags BC-PT-99068 on the comparison and BC-PT-99005 on the particular solution; the lines are reader_checks output. The pattern is scored by analogy with the separable family (sg-23:12).

## Traps

One active error meets the skill: BC-ERR-07009. Both bands. Its relation is `distinct`, so the block carries `fix_prompt: true`; neither text writes a decimal. On ex-1's draw: the family 4 + Ce^x reported as the one solution, with C never fixed by y(0) = 2. Possible reason, words from BC-MIS-07005.

## Representations

None. BC-REP-01, 04, 06 only.

## Prerequisite bridge

None.

## Time

BC-QA-07007 is `no_calculator` and its `multipart_structure` names a single MCQ first, so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). The minutes go on the derivative with C kept.

## Checks

- chk-1, completion of ex-1: the family is given as verified; the student fixes C. Key 4 - 2e^x.
- chk-2, isomorph. Draw: solution, rate -2, level 1, initial 3, shift 1; y = 1 + Ce^(-2x) for dy/dx = -2(y - 1), y(0) = 3. Key 1 + 2e^(-2x).
- No chk-3: the bundle holds one error, and an MCQ needs three error blocks for its distractors [inferred].

## Delivery

- prediction, orientation, ki-1: text. Rule 6: BC-REP-01, 04, 06 on BC-SKL-07009 (docs/lessons/unit-07/README.md, section 6).
- ex-1, err-BC-ERR-07009: step_reveal. Rule 1.
- No drawn block: `no_figure_reason` states that no skill carries a figure-bearing representation and no key idea describes a process, so none of rules 2 to 5 applies.

## Band plan

- Low (full), in served order: prediction, orientation, ki-1, st-1 with its contrast pair, ex-1 and its lines, chk-1, err-BC-ERR-07009, chk-2. 448 words, 2.99 minutes (cap 900 and 6). The lesson has one worked example, so nothing is faded.
- Mid (brief): the same blocks, in the same order. 448 words, 2.99 minutes (cap 450 and 3). Orientation, the key idea text, strategy fields, contrast texts, the prediction and step cues were shortened to fit; no anchor quote or scoring tag was dropped.
- Refresher: ki-1, err-BC-ERR-07009, ex-1.

## Sources

- BC-CON-07003; BC-SKL-07009; BC-EK-FUN-7B2; ced:138
- BC-QA-07007, BC-QA-07003; BC-PT-99005, BC-PT-99068; sg-23:12
- BC-ERR-07009; BC-MIS-07005
- research/units/unit-07-differential-equations.md#7.2 Verifying Solutions for Differential Equations
- research/question-analysis/question-archetypes.md#BC-QA-07007 Verification that a function solves a differential equation
- research/question-analysis/question-archetypes.md#BC-QA-07003 Particular solution by separation of variables
- research/exam/exam-structure.md#Section and part layout
- [inferred] Two checks, not three. Settled by a second and third error record on BC-SKL-07009.

## Machine record

```json
{
 "id": "LSN-CON-07003",
 "kind": "concept",
 "target_id": "BC-CON-07003",
 "unit": "07",
 "skills": ["BC-SKL-07009"],
 "prediction": {
  "id": "pr-1",
  "stem": {"text": "Y = 4 + e^x satisfies dy/dx = y - 4. How many functions satisfy this equation?", "command_verb": "predict"},
  "format": "mcq",
  "options": [
   {"id": "A", "label": "Only y = 4 + e^x.", "is_key": false},
   {"id": "B", "label": "Infinitely many.", "is_key": true},
   {"id": "C", "label": "Exactly two.", "is_key": false}
  ],
  "resolution": "Every y = 4 + Ce^x satisfies it; a stated point fixes one C.",
  "sources": ["BC-CON-07003", "research/units/unit-07-differential-equations.md#7.2 Verifying Solutions for Differential Equations"]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation and no key idea describes a process. The lesson verifies a formula with a constant and then solves for that constant, which is symbolic.",
 "orientation": {
  "text": "The equation holds for every C; the initial condition selects one member.",
  "sources": ["BC-CON-07003", "research/units/unit-07-differential-equations.md#7.2 Verifying Solutions for Differential Equations"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-7B2",
   "depth": "core",
   "text": "One equation, infinitely many functions. A constant C names them all; a stated point selects one.",
   "notation": "constant C",
   "quote": {"text": "There may be infinitely many solutions to a differential equation.", "source": "ced:138"},
   "sources": ["BC-EK-FUN-7B2", "ced:138", "research/units/unit-07-differential-equations.md#7.2 Verifying Solutions for Differential Equations"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-07007",
   "cue": "A candidate with a constant C.",
   "method": "Its derivative, C held constant.",
   "rival": "Solving the equation from scratch.",
   "separating_feature": "The family is supplied.",
   "sources": ["BC-QA-07007", "BC-QA-07003"],
   "evidence_tag": "verified",
   "contrast": {
    "this": {"text": "Show y = 1 + Ce^(2x) solves dy/dx = 2(y - 1); find the member with y(0) = 4.", "archetype_id": "BC-QA-07007"},
    "not_this": {"text": "Use separation of variables to solve dy/dx = 2(y - 1), y(0) = 4.", "why_not": "No candidate to verify."},
    "feature": "A printed C."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-07007",
   "bands": ["low", "mid"],
   "parameter_draw": {"case": "solution", "rate": 1, "level": 4, "initial": 2, "shift": -1},
   "problem": {"text": "Show that y = 4 + Ce^x solves dy/dx = y - 4 for every C, and find the solution with y(0) = 2.", "command_verb": "show"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "A family.", "why": "C stays a letter.", "expr": "4 + C*exp(x)", "relation": "new"},
    {"cue": "Left side.", "why": "C is constant.", "expr": "C*exp(x)", "relation": "differentiate", "variable": "x"},
    {"cue": "Right side.", "why": "(4 + Ce^x) - 4.", "expr": "(4 + C*exp(x)) - 4", "relation": "new"},
    {"cue": "Compare.", "why": "Equal for all C.", "expr": "C*exp(x)", "relation": "equivalent", "point_type_id": "BC-PT-99068"},
    {"cue": "The point.", "why": "It selects one member.", "expr": "4 + C = 2", "relation": "new"},
    {"cue": "Solve.", "why": "One curve.", "expr": "-2", "relation": "solve", "variable": "C"},
    {"cue": "Substitute.", "why": "The particular solution.", "expr": "4 - 2*exp(x)", "relation": "new", "point_type_id": "BC-PT-99005"}
   ],
   "answer": {"form": "symbolic", "expr": "4 - 2*exp(x)"}
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": ["BC-PT-99068", "BC-PT-99005"],
   "lines": [
    {
     "point_type_id": "BC-PT-99068",
     "text": "Verification for a show-that prompt. Earned by: An algebraic chain that lands on the stated target expression or inequality, closed with the target itself (sg-25:26). Not earned by: A chain that stops before the target, or that asserts equality where the prompt asked for a bound (sg-25:22, sg-22:21)."
    },
    {
     "point_type_id": "BC-PT-99005",
     "text": "Answer with supporting work or setup shown. Earned by: The correct value together with the setup the prompt demanded, such as a difference and a quotient from a table or an equation that produces the value (sg-26:2, sg-25:4). Not earned by: An unsupported value (sg-23:10, sg-22:9), or a setup with no value (sg-26:2). Notation: sg-22:6 withholds this point for an equation of the form function equals constant, such as a derivative expression set equal to a number without evaluation. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-07009",
   "observed_behavior": "The response treats the family with its constant as a single function.",
   "scoring_consequence": "The distinction the essential knowledge draws between a family and a particular solution is lost.",
   "wrong_step": {"text": "4 + Ce^x as the one solution.", "expr": "4 + C*exp(x)"},
   "right_step": {"text": "y(0) = 2 fixes C = -2.", "expr": "4 - 2*exp(x)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-07005", "text": "reads the equation as determining a single function"},
   "sources": ["BC-ERR-07009", "BC-MIS-07005"],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {"ex-1": [2, 3, 4, 5, 6, 7]},
  "skipped_steps": {"ex-1": [1]}
 },
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-07007",
   "parameter_draw": {"case": "solution", "rate": 1, "level": 4, "initial": 2, "shift": -1},
   "completes": "ex-1",
   "stem": {"text": "Every y = 4 + Ce^x solves dy/dx = y - 4. Find the one with y(0) = 2.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "4 - 2*exp(x)"},
   "steps": [
    {"text": "The point.", "expr": "4 + C = 2", "relation": "new"},
    {"text": "C.", "expr": "-2", "relation": "solve", "variable": "C"},
    {"text": "The member.", "expr": "4 - 2*exp(x)", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-07009"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-07007",
   "parameter_draw": {"case": "solution", "rate": -2, "level": 1, "initial": 3, "shift": 1},
   "stem": {"text": "y = 1 + Ce^(-2x) and dy/dx = -2(y - 1): verify, then find the member with y(0) = 3.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "1 + 2*exp(-2*x)"},
   "steps": [
    {"text": "Family.", "expr": "1 + C*exp(-2*x)", "relation": "new"},
    {"text": "Derivative.", "expr": "-2*C*exp(-2*x)", "relation": "differentiate", "variable": "x"},
    {"text": "Right side.", "expr": "-2*((1 + C*exp(-2*x)) - 1)", "relation": "new"},
    {"text": "Equal for every C.", "expr": "-2*C*exp(-2*x)", "relation": "equivalent"},
    {"text": "The point.", "expr": "1 + C = 3", "relation": "new"},
    {"text": "C.", "expr": "2", "relation": "solve", "variable": "C"},
    {"text": "The member.", "expr": "1 + 2*exp(-2*x)", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-07009"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: BC-REP-01, 04, 06 on BC-SKL-07009, none figure-bearing", "sources": ["BC-SKL-07009"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 6: a statement about how many solutions exist, no figure-bearing representation", "sources": ["BC-SKL-07009"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-07009", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-07009", "ex-1"],
 "read_minutes": {
  "full": 2.99,
  "brief": 2.99
 },
 "word_count": {
  "full": 447,
  "brief": 447
 },
 "research_lines": [
  {
   "file": "research/units/unit-07-differential-equations.md",
   "line": "multi-concept variants pair verification with an initial condition so that only one member of the family survives"
  }
 ],
 "inferred": [
  {
   "claim": "The lesson carries two checks, not three: the bundle holds one error record, and a four-option MCQ needs three error blocks for its distractors.",
   "settles": "Further active error records on BC-SKL-07009."
  },
  {
   "claim": "The particular solution after a verified family is tagged BC-PT-99005; the verification rubric is recorded by analogy.",
   "settles": "A scoring guideline for a family verification part."
  }
 ],
 "sources": ["BC-CON-07003", "BC-SKL-07009", "BC-EK-FUN-7B2", "ced:138", "BC-QA-07007", "BC-QA-07003", "BC-PT-99005", "BC-PT-99068", "sg-23:12", "BC-ERR-07009", "BC-MIS-07005", "research/units/unit-07-differential-equations.md#7.2 Verifying Solutions for Differential Equations", "research/question-analysis/question-archetypes.md#BC-QA-07007 Verification that a function solves a differential equation", "research/question-analysis/question-archetypes.md#BC-QA-07003 Particular solution by separation of variables", "research/exam/exam-structure.md#Section and part layout"]
}
```
