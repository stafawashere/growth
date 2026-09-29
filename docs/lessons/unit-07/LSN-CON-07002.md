---
title: LSN-CON-07002 Verification of a proposed solution
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-07002, verifying that a proposed function solves a differential equation and meets its initial condition, built from authoring_bundle("BC-CON-07002") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-07002 Verification of a proposed solution

Concept BC-CON-07002 (skills BC-SKL-07006, BC-SKL-07007, BC-SKL-07008), topic 7.2 of Unit 7, loaded by one archetype, BC-QA-07007 (family de-verification). No hard parent inside Unit 7 (docs/lessons/unit-07/README.md, section 1).

## Orientation

Served text, from BC-CON-07002 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-07-differential-equations.md#7.2 Verifying Solutions for Differential Equations): a response differentiates the candidate, substitutes candidate and derivative into both sides, compares, and checks the stated point before calling it the particular solution. No count, no frequency.

## Key ideas

All three skills map to BC-EK-FUN-7B1 (ced:138), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Verification, Refutation): differentiating the candidate and substituting both turns the equation into a true statement on an interval; one input where the sides disagree refutes it. Anchor quote from ced:138, 16 words. Notation line from the concept record.

## Recognition

BC-QA-07007 (research/question-analysis/question-archetypes.md#BC-QA-07007 Verification that a function solves a differential equation): `typical_wording` "show that the given function is a solution to the differential equation", "which of the following functions is a solution"; `common_givens` a differential equation, one or more candidate functions, sometimes an initial condition; `asked_to_produce` the derivative of the candidate, the substitution, a verdict. The signal: a function is printed beside the equation. Shapes: an MCQ with four candidates, or a short free-response part (BC-FRQ-2015-Q4-D).

What says "not this concept": "use separation of variables to find" supplies no candidate, which selects solving (BC-CON-07007; docs/lessons/unit-07/README.md, section 3).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-07007. Method, `expected_solution_path[0]`: differentiate the candidate. Rival, `wrong_approaches`: solving the equation from scratch. Separating feature: a candidate is printed, so it is tested, not derived. Both fields present, so not tagged inferred.

## Solution path

- ex-1, both bands. Draw: case solution, rate 2, level 3, initial 1, shift 1, so dy/dx = 2(y - 3), y(0) = 1, candidate y = 3 - 2e^(2x). Steps: candidate (new); derivative (differentiate); right side with the candidate (new); simplified (equivalent); candidate again (new); at x = 0 (evaluate).
- ex-2, low band. Draw: case wrong_initial_value, rate -1, level 2, initial 4, shift 1, so dy/dx = -(y - 2), y(0) = 4, candidate y = 2 + 3e^(-x), which solves the equation and gives 5 at x = 0.
- Neither draw equals a published BC-QA-07007 draw. A fluent solver writes every step: each is the demonstration.

## Scoring

BC-QA-07007 lists BC-PT-99005, 99068 and 99004. ex-1 tags BC-PT-99068 (the chain closed on the right side); ex-2 tags BC-PT-99068 and BC-PT-99005 (the value at the stated input as the supported verdict). The lines are reader_checks output. The BC-PT-99005 tag is dropped from ex-1 to keep the brief band under 450 words [inferred]. The archetype's `scoring_pattern` is recorded by analogy with the separable family (sg-23:12).

## Traps

Three active errors meet the skills, in the bundle's order: BC-ERR-07006, BC-ERR-07007, BC-ERR-07008. Low band all three; mid band the first two. BC-ERR-07006 and 07007 on ex-1's draw, BC-ERR-07008 on ex-2's draw, where a verdict of failure is the right answer.

- err-BC-ERR-07006: the candidate put where its derivative belongs. No possible reason: the linked descriptions do not name the step.
- err-BC-ERR-07007: verdict with no check at x = 0. Possible reason, words from BC-MIS-07005.
- err-BC-ERR-07008: "not the particular solution" with nothing shown. No possible reason.

## Representations

None. BC-REP-01 and BC-REP-06 only.

## Prerequisite bridge

- BC-PRQ-06005 and BC-PRQ-07002, from `description_plain` and `failure_signature`.

## Time

BC-QA-07007 is `no_calculator` and its `multipart_structure` names a single MCQ first, so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free-response part it carried 3 points on BC-FRQ-2015-Q4-D (docs/lessons/unit-07/README.md, section 5). The minutes go on the derivative and the substitution.

## Checks

- chk-1, completion of ex-1: both sides are shown equal; the student checks x = 0. Key the ex-1 statement.
- chk-2, isomorph. Draw: solution, rate -3, level -1, initial 2, shift 2; y = -1 + 3e^(-3x) for dy/dx = -3(y + 1), y(0) = 2. Key: the particular solution.
- chk-3, MCQ, low band. Draw: wrong_initial_value, rate 1, level -2, initial 0, shift 2; y = -2 + 4e^x for dy/dx = y + 2, y(0) = 0. Key: solves the equation, fails the condition. Distractors carry BC-ERR-07006, 07007, 07008.

## Delivery

- orientation, ki-1: text. Rule 6: BC-REP-01, 06 on all three skills (docs/lessons/unit-07/README.md, section 6).
- ex-1, ex-2 and the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 and its lines, ex-2 and its lines, three error blocks, chk-1 to chk-3, two bridges. 758 words, 5.1 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 and its lines, err-BC-ERR-07006, err-BC-ERR-07007, chk-1, chk-2, bridges. 433 words, 2.9 minutes (cap 450 and 3).
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-07002; BC-SKL-07006, BC-SKL-07007, BC-SKL-07008; BC-EK-FUN-7B1; ced:138
- BC-QA-07007; BC-FRQ-2015-Q4-D; BC-PT-99005, BC-PT-99068; sg-23:12
- BC-ERR-07006, BC-ERR-07007, BC-ERR-07008; BC-MIS-07005
- BC-PRQ-06005, BC-PRQ-07002
- research/units/unit-07-differential-equations.md#7.2 Verifying Solutions for Differential Equations
- research/question-analysis/question-archetypes.md#BC-QA-07007 Verification that a function solves a differential equation
- research/exam/exam-structure.md#Section and part layout
- [inferred] Which BC-PT the value check earns. Settled by a rubric for a verification part after 2015.

## Machine record

```json
{
 "id": "LSN-CON-07002",
 "kind": "concept",
 "target_id": "BC-CON-07002",
 "unit": "07",
 "skills": ["BC-SKL-07006", "BC-SKL-07007", "BC-SKL-07008"],
 "orientation": {
  "text": "Differentiate the candidate, put it and its derivative into both sides, compare, and check the stated point before calling it the particular solution.",
  "sources": ["BC-CON-07002", "research/units/unit-07-differential-equations.md#7.2 Verifying Solutions for Differential Equations"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-7B1",
   "depth": "core",
   "text": "A candidate solves the equation on an interval when its derivative, and the candidate itself, substituted into the two sides give a true statement there. One input where the sides differ shows it is not a solution. Meeting the initial condition is a separate test.",
   "notation": "substitution; satisfies the differential equation",
   "quote": {"text": "Derivatives can be used to verify that a function is a solution to a given differential equation.", "source": "ced:138"},
   "sources": ["BC-EK-FUN-7B1", "ced:138", "research/units/unit-07-differential-equations.md#7.2 Verifying Solutions for Differential Equations"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-07007",
   "cue": "A function is printed beside the equation: show that it is a solution, or pick which one is.",
   "method": "First line: the derivative of the candidate.",
   "rival": "Rival: solving the equation from scratch.",
   "separating_feature": "A candidate is supplied, so it is tested, not derived.",
   "sources": ["BC-QA-07007"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-07007",
   "bands": ["low", "mid"],
   "parameter_draw": {"case": "solution", "rate": 2, "level": 3, "initial": 1, "shift": 1},
   "problem": {"text": "Show that y = 3 - 2e^(2x) is the solution of dy/dx = 2(y - 3) with y(0) = 1.", "command_verb": "show"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "A printed candidate: start from it.", "why": "The candidate is tested, not derived.", "expr": "3 - 2*exp(2*x)", "relation": "new"},
    {"cue": "The left side is dy/dx.", "why": "Without the derivative the equation is never tested.", "expr": "-4*exp(2*x)", "relation": "differentiate", "variable": "x"},
    {"cue": "The right side takes the candidate for y.", "why": "2((3 - 2e^(2x)) - 3).", "expr": "2*((3 - 2*exp(2*x)) - 3)", "relation": "new"},
    {"cue": "Simplify and compare with the left side.", "why": "Both sides are -4e^(2x): the equation holds.", "expr": "-4*exp(2*x)", "relation": "equivalent", "point_type_id": "BC-PT-99068"},
    {"cue": "The stem names y(0) = 1.", "why": "Many functions solve the equation; the point selects one.", "expr": "3 - 2*exp(2*x)", "relation": "new"},
    {"cue": "Evaluate at x = 0.", "why": "3 - 2 = 1 matches, so it is the particular solution.", "expr": "1", "relation": "evaluate", "subs": {"x": "0"}}
   ],
   "answer": {"form": "statement", "expr": "y = 3 - 2*exp(2*x) solves dy/dx = 2*(y - 3) and y(0) = 1"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-07007",
   "bands": ["low"],
   "parameter_draw": {"case": "wrong_initial_value", "rate": -1, "level": 2, "initial": 4, "shift": 1},
   "problem": {"text": "Is y = 2 + 3e^(-x) the solution of dy/dx = -(y - 2) with y(0) = 4?", "command_verb": "determine"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "A candidate is printed.", "why": "Test it.", "expr": "2 + 3*exp(-x)", "relation": "new"},
    {"cue": "Left side first.", "why": "The derivative.", "expr": "-3*exp(-x)", "relation": "differentiate", "variable": "x"},
    {"cue": "Right side with the candidate.", "why": "-((2 + 3e^(-x)) - 2).", "expr": "-((2 + 3*exp(-x)) - 2)", "relation": "new"},
    {"cue": "Compare.", "why": "Both -3e^(-x): the equation holds.", "expr": "-3*exp(-x)", "relation": "equivalent", "point_type_id": "BC-PT-99068"},
    {"cue": "The condition y(0) = 4 remains.", "why": "The evidence for a no is a displayed value.", "expr": "2 + 3*exp(-x)", "relation": "new"},
    {"cue": "Evaluate at x = 0.", "why": "5, not 4: a solution, but not this one.", "expr": "5", "relation": "evaluate", "subs": {"x": "0"}, "point_type_id": "BC-PT-99005"}
   ],
   "answer": {"form": "statement", "expr": "solves the equation but y(0) = 5, not 4"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99068"], "lines": [
   {"point_type_id": "BC-PT-99068", "text": "Verification for a show-that prompt. Earned by: An algebraic chain that lands on the stated target expression or inequality, closed with the target itself (sg-25:26). Not earned by: A chain that stops before the target, or that asserts equality where the prompt asked for a bound (sg-25:22, sg-22:21)."}]},
  {"example_id": "ex-2", "point_type_ids": ["BC-PT-99068", "BC-PT-99005"], "lines": [
   {"point_type_id": "BC-PT-99068", "text": "Verification for a show-that prompt. Earned by: An algebraic chain that lands on the stated target expression or inequality, closed with the target itself (sg-25:26). Not earned by: A chain that stops before the target, or that asserts equality where the prompt asked for a bound (sg-25:22, sg-22:21)."},
   {"point_type_id": "BC-PT-99005", "text": "Answer with supporting work or setup shown. Earned by: The correct value together with the setup the prompt demanded, such as a difference and a quotient from a table or an equation that produces the value (sg-26:2, sg-25:4). Not earned by: An unsupported value (sg-23:10, sg-22:9), or a setup with no value (sg-26:2). Notation: sg-22:6 withholds this point for an equation of the form function equals constant, such as a derivative expression set equal to a number without evaluation. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2)."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-07006",
   "observed_behavior": "The verification puts the candidate into both sides and never produces its derivative.",
   "scoring_consequence": "The check does not test the equation, so the conclusion is unsupported.",
   "wrong_step": {"text": "Candidate as the left side.", "expr": "3 - 2*exp(2*x)"},
   "right_step": {"text": "Its derivative.", "expr": "-4*exp(2*x)"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-07006"]
  },
  {
   "error_id": "BC-ERR-07007",
   "observed_behavior": "The response verifies the equation and declares the candidate the particular solution without testing the stated point.",
   "scoring_consequence": "A member of the family is reported where a specific one was asked for.",
   "wrong_step": {"text": "Verdict with no value at 0.", "expr": "3 - 2*exp(2*x)"},
   "right_step": {"text": "Value at 0 is 1.", "expr": "3 - 2*exp(2*0)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-07005", "text": "reads the equation as determining a single function"},
   "sources": ["BC-ERR-07007", "BC-MIS-07005"]
  },
  {
   "error_id": "BC-ERR-07008",
   "observed_behavior": "The response says a candidate is not a solution and shows nothing that fails.",
   "scoring_consequence": "The verdict is unsupported even when correct.",
   "wrong_step": {"text": "No, with nothing shown.", "expr": "2 + 3*exp(-x)"},
   "right_step": {"text": "y(0) = 5, not 4.", "expr": "2 + 3*exp(-0)"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-07008"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "y(0) is the candidate's value at input 0; f and f' are different objects."},
  {"prq_id": "BC-PRQ-07002", "text": "dy/dx is the derivative of the candidate, the left side to compute."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3, 4, 6], "ex-2": [2, 3, 4, 6]}, "skipped_steps": {"ex-1": [1, 5], "ex-2": [1, 5]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-07007",
   "parameter_draw": {"case": "solution", "rate": 2, "level": 3, "initial": 1, "shift": 1},
   "completes": "ex-1",
   "stem": {"text": "y = 3 - 2e^(2x) makes both sides of dy/dx = 2(y - 3) equal. Finish: is it the solution with y(0) = 1?", "command_verb": "determine"},
   "key": {"form": "statement", "expr": "y = 3 - 2*exp(2*x) solves dy/dx = 2*(y - 3) and y(0) = 1"},
   "steps": [
    {"text": "The candidate.", "expr": "3 - 2*exp(2*x)", "relation": "new"},
    {"text": "At x = 0.", "expr": "1", "relation": "evaluate", "subs": {"x": "0"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-07007"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-07007",
   "parameter_draw": {"case": "solution", "rate": -3, "level": -1, "initial": 2, "shift": 2},
   "stem": {"text": "Is y = -1 + 3e^(-3x) the solution of dy/dx = -3(y + 1) with y(0) = 2?", "command_verb": "determine"},
   "key": {"form": "statement", "expr": "yes: both sides are -9*exp(-3*x) and y(0) = 2"},
   "steps": [
    {"text": "Candidate.", "expr": "-1 + 3*exp(-3*x)", "relation": "new"},
    {"text": "Derivative.", "expr": "-9*exp(-3*x)", "relation": "differentiate", "variable": "x"},
    {"text": "Right side.", "expr": "-3*((-1 + 3*exp(-3*x)) + 1)", "relation": "new"},
    {"text": "Equal.", "expr": "-9*exp(-3*x)", "relation": "equivalent"},
    {"text": "Candidate again.", "expr": "-1 + 3*exp(-3*x)", "relation": "new"},
    {"text": "At 0.", "expr": "2", "relation": "evaluate", "subs": {"x": "0"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-07006", "BC-SKL-07007"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-07007",
   "parameter_draw": {"case": "wrong_initial_value", "rate": 1, "level": -2, "initial": 0, "shift": 2},
   "stem": {"text": "For dy/dx = y + 2 with y(0) = 0, which verdict on y = -2 + 4e^x is supported?", "command_verb": "identify"},
   "key": {"form": "statement", "expr": "solves the equation; y(0) = 2, not 0"},
   "steps": [
    {"text": "Derivative 4e^x equals y + 2.", "expr": "-2 + 4*exp(x)", "relation": "new"},
    {"text": "At 0.", "expr": "2", "relation": "evaluate", "subs": {"x": "0"}}
   ],
   "options": [
    {"id": "A", "is_key": false, "label": "Not a solution: y put into both sides gives -2 + 4e^x against 4e^x.", "error_path": "BC-ERR-07006", "derivation": "the candidate used where its derivative belongs"},
    {"id": "B", "is_key": false, "label": "The particular solution: dy/dx = 4e^x equals y + 2.", "error_path": "BC-ERR-07007", "derivation": "the condition at 0 never tested"},
    {"id": "C", "is_key": false, "label": "Not a solution: it does not fit the equation.", "error_path": "BC-ERR-07008", "derivation": "a negative verdict with nothing exhibited"},
    {"id": "D", "is_key": true, "label": "It solves the equation, but y(0) = 2, not 0.", "error_path": null}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-07007"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: BC-REP-01, 06 on BC-SKL-07006 to 07008, none figure-bearing", "sources": ["BC-SKL-07006"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 6: a rule about substitution with no figure-bearing representation", "sources": ["BC-SKL-07006", "BC-SKL-07008"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-07006", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-07007", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-07008", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-07006", "err-BC-ERR-07007", "err-BC-ERR-07008", "ex-1"],
 "read_minutes": {"full": 5.1, "brief": 2.9},
 "word_count": {"full": 758, "brief": 433},
 "research_lines": [
  {"file": "research/units/unit-07-differential-equations.md", "line": "One input at which the two sides disagree is enough to show that a candidate is not a solution."}
 ],
 "inferred": [
  {"claim": "The BC-PT-99005 tag on the value check is dropped from ex-1 and kept on ex-2, because its reader line would take the brief band above 450 words.", "settles": "A band cap that excludes reader lines, or a shorter reader_checks line for BC-PT-99005."},
  {"claim": "The value check at the stated input is tagged BC-PT-99005; the only verification rubric (BC-FRQ-2015-Q4-D) predates the guidelines read and is scored by analogy.", "settles": "A scoring guideline for a verification part after 2015."}
 ],
 "sources": ["BC-CON-07002", "BC-SKL-07006", "BC-SKL-07007", "BC-SKL-07008", "BC-EK-FUN-7B1", "ced:138", "BC-QA-07007", "BC-FRQ-2015-Q4-D", "BC-PT-99005", "BC-PT-99068", "sg-23:12", "BC-ERR-07006", "BC-ERR-07007", "BC-ERR-07008", "BC-MIS-07005", "BC-PRQ-06005", "BC-PRQ-07002", "research/units/unit-07-differential-equations.md#7.2 Verifying Solutions for Differential Equations", "research/question-analysis/question-archetypes.md#BC-QA-07007 Verification that a function solves a differential equation", "research/exam/exam-structure.md#Section and part layout"]
}
```
