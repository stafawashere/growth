---
title: LSN-CON-08008 Extreme value of an accumulated amount from the sign of the net rate
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08008, the time at which an accumulated amount is greatest, found from the net rate and justified globally, built from authoring_bundle("BC-CON-08008") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08008 Extreme value of an accumulated amount from the sign of the net rate

Concept BC-CON-08008 (skill BC-SKL-08014), topic 8.3 of Unit 8, loaded by one archetype, BC-QA-08006 (family accumulation-extremum), which also loads BC-SKL-08012 of BC-CON-08006. Its hard parents are BC-CON-08006 and BC-CON-08007 in Unit 8 and the Unit 5 candidates and sign arguments (docs/lessons/unit-08/README.md, section 1).

## Orientation

Served text, from BC-CON-08008 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts): a response sets the net rate, the derivative of the amount, equal to zero, then compares the amount at every critical point and at both endpoints, or argues globally from the sign of the net rate. No count, no frequency.

## Key ideas

BC-SKL-08014 maps to BC-EK-CHA-4D1 (ced:154): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs (Accumulation; Maximum of an accumulated amount): an amount defined by an integral accumulates the net rate, so its derivative is the net rate; the absolute maximum on a closed interval is where the net rate changes from positive to negative or at an endpoint; a derivative test at one point is local, and in 2025 a local test alone did not earn the justification point (sg-25:5). No anchor quote: the brief band is at its cap. Notation line from the concept record.

## Recognition

BC-QA-08006 (research/question-analysis/question-archetypes.md#BC-QA-08006 Time at which an accumulated amount is maximal): `typical_wording` "at what time in the stated interval does the modelled amount attain its maximum value, and justify the answer"; `common_givens` an amount function defined with a definite integral, a closed interval; `asked_to_produce` an equation for the critical point, a global justification, the time of the maximum. The signal: "at what time" with "maximum" or "greatest", "justify", and a closed time interval. Shape: the closing part of the calculator free response question (BC-FRQ-2019-Q1-C, BC-FRQ-2013-Q1-D, BC-FRQ-2022-Q1-D, BC-FRQ-2015-Q1-C, BC-FRQ-2018-Q1-D), after the amount at a time (BC-CON-08006) and the net rate (BC-CON-08007) on the same context (research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions).

What says "not this concept": "how much at time t" (amount, BC-CON-08006); "is the amount increasing at time t" (the sign of the net rate at one time, one line).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-08006. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: differentiate the amount function, so A'(t) is the net rate, and set it to zero. Rival, `wrong_approaches`: a local argument for a global claim, or a candidates table missing an endpoint (BC-ERR-99004, BC-ERR-08016). Separating feature: a closed interval makes both endpoints candidates. Both fields are present, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-08006, both bands, calculator. Draw from `parameter_spec`: period 12, net 3, times 2, outflow 4, initial 100, context water, presentation net_rate; so swing 6, the net rate is 3 + 6cos(pi t/6) gallons per hour on [0, 12], it is zero at t = 4 and t = 8, and with times 2 (ratio 1/2, above a quarter) the right endpoint wins, as the spec's notes state. A(0) = 100, A(4) = 121.924, A(8) = 114.076, A(12) = 136. No published BC-QA-08006 item carries this draw.
- Steps follow `expected_solution_path`: the amount (new); its derivative (differentiate); the equation A'(t) = 0 (new); its solutions (solve, a calculator solve); the amount in closed form (new); A(4) (evaluate, approx); the largest candidate value (new, tagged BC-PT-99011); the time (new). A fluent solver writes the equation, the four labelled values and the conclusion; the closed form is typed into the calculator, not written [inferred].

## Scoring

BC-QA-08006 lists BC-PT-99013, 99004, 99010, 99011 and 99064. ex-1 tags BC-PT-99011, the candidates test, which is this concept's point; the reader line is `reader_checks(["BC-PT-99011"])` copied exactly. For the author: the archetype's scoring pattern is three points, considering the derivative equal to zero, a global justification and the answer, and a first or second derivative test alone leaves the answer point available but not the justification (sg-25:5). A local argument becomes global with a uniqueness clause (research/scoring/justification-requirements.md#Global versus local arguments), and the candidates test needs both endpoints (research/scoring/justification-requirements.md#The candidates test).

## Traps

Two active errors meet the skill, in the bundle's order: BC-ERR-08016, BC-ERR-99004. Both bands serve both. On ex-1's draw.

- err-BC-ERR-08016: only t = 4 evaluated, t = 4 reported, against t = 12. Possible reason, words from BC-MIS-99010.
- err-BC-ERR-99004: A' changes from positive to negative at t = 4, so t = 4 reported, against t = 12. No possible reason line: the brief band is at its 450 word cap.

## Representations

None. The topic's Representations paragraph names verbal to symbolic and symbolic to verbal conversions and a tabulated rate, none figure-shaped for this concept.

## Prerequisite bridge

- BC-PRQ-08001, from its `description_plain` and `failure_signature`.

## Time

BC-QA-08006 is `calculator`, the closing part of the calculator free response question, so Section II Part A, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout); its three points are a 5.0 minute share (docs/lessons/unit-08/README.md, section 5). The minutes go on the four candidate values typed into the calculator and the sentence naming the largest.

## Checks

- chk-1, completion of ex-1, both bands: the four candidate values given, the time. Key 12.
- chk-2, isomorph, both bands. Draw: period 24, net 2, times 2, outflow 5, initial 60, context sand, presentation net_rate; net rate 2 + 4cos(pi t/12) on [0, 24], zero at 8 and 16, A(24) = 108. Key 24.
- chk-3, MCQ, low band. Draw: period 8, net 1, times 2, outflow 3, initial 40, context oil, presentation net_rate; net rate 1 + 2cos(pi t/4) on [0, 8], A(8/3) = 44.872, A(16/3) = 43.128, A(8) = 48. Key statement: t = 8 by the candidates test. Distractors: t = 8/3 from the interior values only (BC-ERR-08016); t = 8/3 from the sign change (BC-ERR-99004); t = 8 from A' positive just before 8 (BC-ERR-99004).

## Delivery

- orientation: text. Rule 6: BC-REP-05 and BC-REP-09 on BC-SKL-08014 draw nothing; the unit README delivery map gives text.
- ki-1: text. Rule 6, the candidates argument is a sequence of written lines (docs/lessons/unit-08/README.md, section 6).
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-08016, err-BC-ERR-99004: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 with its reader line, both error blocks, chk-1 to chk-3, the bridge. 500 words, 3.4 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its reader line, both error blocks, chk-1, chk-2, the bridge. 450 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-08016, err-BC-ERR-99004, ex-1.

## Sources

- BC-CON-08008; BC-SKL-08014; BC-EK-CHA-4D1; ced:154
- BC-QA-08006; BC-PT-99011; sg-25:5; BC-FRQ-2019-Q1-C, BC-FRQ-2013-Q1-D, BC-FRQ-2022-Q1-D, BC-FRQ-2015-Q1-C, BC-FRQ-2018-Q1-D
- BC-ERR-08016, BC-ERR-99004; BC-MIS-06010, BC-MIS-99010
- BC-PRQ-08001
- research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts
- research/question-analysis/question-archetypes.md#BC-QA-08006 Time at which an accumulated amount is maximal
- research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions
- research/scoring/justification-requirements.md#Global versus local arguments
- research/scoring/justification-requirements.md#The candidates test
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-PT-99013 and BC-PT-99004 are earned on ex-1 steps 3 and 8 but not tagged: with their reader lines the brief band passes 450 words. Settled by a brief cap that exempts reader lines, or a shorter reader_checks form.
- [inferred] The gallons unit for the water context. Settled by a unit field in the parameter_spec.
- [inferred] Which lines are written and which are typed only. Settled by timing data per step from 10's fluency telemetry.

## Machine record

```json
{
 "id": "LSN-CON-08008",
 "kind": "concept",
 "target_id": "BC-CON-08008",
 "unit": "08",
 "skills": ["BC-SKL-08014"],
 "orientation": {
  "text": "A response sets the net rate, the derivative of the amount, equal to zero, then compares the amount at every critical point and both endpoints, or argues from the sign of the net rate over the whole interval.",
  "sources": ["BC-CON-08008", "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-4D1",
   "depth": "core",
   "text": "An amount defined by an integral accumulates the net rate, so its derivative is the net rate. On a closed interval its absolute maximum is where the net rate changes from positive to negative, or at an endpoint. A sign change at one point is local; alone it did not earn the justification (sg-25:5).",
   "notation": "candidates test on an accumulation function",
   "quote": null,
   "sources": ["BC-EK-CHA-4D1", "ced:154", "sg-25:5", "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08006",
   "cue": "The stem asks for the time of the maximum and a justification, from an amount defined by an integral on a closed interval.",
   "method": "First written line: \\(A'(t)=\\) net rate \\(=0\\).",
   "rival": "Rival: a local argument, or a table missing an endpoint (BC-ERR-99004).",
   "separating_feature": "A closed interval makes both endpoints candidates.",
   "sources": ["BC-QA-08006"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08006",
   "bands": ["low", "mid"],
   "parameter_draw": {"period": 12, "net": 3, "times": "2", "outflow": 4, "initial": 100, "context": "water", "presentation": "net_rate"},
   "problem": {"text": "A tank holds 100 gallons at \\(t=0\\); water changes at the net rate \\(3+6\\cos(\\pi t/6)\\) gallons per hour, \\(0\\le t\\le 12\\). When is the amount greatest? Justify.", "command_verb": "justify"},
   "calculator_status": "calculator",
   "steps": [
    {"cue": "Amount: initial value plus accumulated net rate.", "why": "\\(A(t)\\).", "expr": "100 + Integral(3 + 6*cos(pi*s/6), (s, 0, t))", "relation": "new"},
    {"cue": "A maximum is asked: differentiate.", "why": "Derivative of an accumulation.", "expr": "3 + 6*cos(pi*t/6)", "relation": "differentiate", "variable": "t"},
    {"cue": "Critical points.", "why": "The equation is written.", "expr": "3 + 6*cos(pi*t/6) = 0", "relation": "new"},
    {"cue": "Solve on \\([0,12]\\).", "why": "Calculator solve.", "expr": "FiniteSet(4, 8)", "relation": "solve", "variable": "t"},
    {"cue": "Closed interval: endpoints join the candidates.", "why": "\\(A(t)\\) in closed form.", "expr": "100 + 3*t + 36*sin(pi*t/6)/pi", "relation": "new"},
    {"cue": "Local maximum \\(t=4\\).", "why": "\\(A(4)\\).", "expr": "121.924", "relation": "evaluate", "subs": {"t": "4"}, "approx": true},
    {"cue": "Compare every candidate.", "why": "\\(A(0)=100\\), \\(A(8)=114.076\\), \\(A(12)=136\\): largest.", "expr": "136", "relation": "new", "point_type_id": "BC-PT-99011"},
    {"cue": "The stem asks when.", "why": "At the endpoint.", "expr": "12", "relation": "new"}
   ],
   "answer": {"form": "numeric", "expr": "12"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99011"], "lines": [{"point_type_id": "BC-PT-99011", "text": "Justification by candidates test. Earned by: A global argument that evaluates the function at every interior critical point and at both endpoints, with the evaluations correct to the stated precision (sg-25:5, sg-25:19). Not earned by: A candidates table missing an endpoint (sg-23:15), containing an evaluation error (sg-23:15), or listing extra x-values (sg-25:19). Precision: sg-25:5 and sg-25:9 require candidate evaluations correct to the first digit after the decimal, rounded or truncated; sg-22:5 allows up to three decimals or correctly rounded integers."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-08016",
   "observed_behavior": "The candidates test evaluates the amount only at the interior critical point.",
   "scoring_consequence": "The justification point is lost because the argument is not global (sg-25:5).",
   "wrong_step": {"text": "Only \\(A(4)\\): \\(t=4\\).", "expr": "4"},
   "right_step": {"text": "All four: \\(t=12\\).", "expr": "12"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-99010", "text": "endpoints and other critical points are never compared"},
   "sources": ["BC-ERR-08016", "BC-MIS-99010"]
  },
  {
   "error_id": "BC-ERR-99004",
   "observed_behavior": "Responses justify an absolute maximum or minimum on a closed interval by a sign change at one point, or run an incomplete candidates test that omits an endpoint or an interior critical point.",
   "scoring_consequence": "The justification point for the absolute extremum is not earned; the answer point may still be available.",
   "wrong_step": {"text": "\\(A'\\) turns negative at 4.", "expr": "4"},
   "right_step": {"text": "\\(A(12)\\) largest.", "expr": "12"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-99004"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-08001", "text": "Every solution in the interval found, on the calculator solver; a missed one drops a candidate."}
 ],
 "time": {"exam_part": "II-A", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3, 4, 7, 8]}, "skipped_steps": {"ex-1": [1, 5, 6]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08006",
   "parameter_draw": {"period": 12, "net": 3, "times": "2", "outflow": 4, "initial": 100, "context": "water", "presentation": "net_rate"},
   "completes": "ex-1",
   "stem": {"text": "\\(A(0)=100\\), \\(A(4)=121.924\\), \\(A(8)=114.076\\), \\(A(12)=136\\). When is \\(A\\) greatest?", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "12"},
   "steps": [
    {"text": "Largest value.", "expr": "Max(100, 121.924, 114.076, 136)", "relation": "new"},
    {"text": "It is \\(A(12)\\).", "expr": "12", "relation": "new"}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-08014"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08006",
   "parameter_draw": {"period": 24, "net": 2, "times": "2", "outflow": 5, "initial": 60, "context": "sand", "presentation": "net_rate"},
   "stem": {"text": "A pile holds 60 tons at \\(t=0\\); sand changes at \\(2+4\\cos(\\pi t/12)\\) tons per hour, \\(0\\le t\\le 24\\). When is it greatest?", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "24"},
   "steps": [
    {"text": "\\(A'(t)=0\\).", "expr": "2 + 4*cos(pi*t/12) = 0", "relation": "new", "point_type_id": "BC-PT-99013"},
    {"text": "\\(t=8, 16\\).", "expr": "FiniteSet(8, 16)", "relation": "solve", "variable": "t"},
    {"text": "The amount.", "expr": "60 + 2*t + 48*sin(pi*t/12)/pi", "relation": "new"},
    {"text": "\\(A(24)=108\\) beats \\(A(8)=89.232\\), \\(A(16)=78.768\\), \\(A(0)=60\\).", "expr": "108", "relation": "evaluate", "subs": {"t": "24"}},
    {"text": "At \\(t=24\\).", "expr": "24", "relation": "new"}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-08014"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-08006",
   "parameter_draw": {"period": 8, "net": 1, "times": "2", "outflow": 3, "initial": 40, "context": "oil", "presentation": "net_rate"},
   "stem": {"text": "A tank holds 40 gallons at \\(t=0\\); oil changes at \\(1+2\\cos(\\pi t/4)\\) gallons per hour, \\(0\\le t\\le 8\\). Which answer and reason earn full credit?", "command_verb": "justify"},
   "key": {"form": "statement", "expr": "t_8_by_candidates_test"},
   "options": [
    {"id": "A", "is_key": false, "label": "\\(t=8/3\\): \\(A(8/3)=44.872\\) exceeds \\(A(16/3)=43.128\\).", "error_path": "BC-ERR-08016", "derivation": "only the interior critical points evaluated"},
    {"id": "B", "is_key": false, "label": "\\(t=8/3\\): \\(A'\\) changes from positive to negative there.", "error_path": "BC-ERR-99004", "derivation": "a local sign change offered for the absolute maximum"},
    {"id": "C", "is_key": true, "label": "\\(t=8\\): \\(A(8)=48\\) exceeds \\(A(0)=40\\), \\(A(8/3)=44.872\\), \\(A(16/3)=43.128\\).", "error_path": null},
    {"id": "D", "is_key": false, "label": "\\(t=8\\): \\(A'\\) is positive just before \\(t=8\\).", "error_path": "BC-ERR-99004", "derivation": "a local argument at the endpoint"}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-08014"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: BC-REP-05 and BC-REP-09 on BC-SKL-08014 draw nothing; unit README delivery map", "sources": ["BC-SKL-08014"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 6: the candidates argument is a sequence of written lines", "sources": ["BC-SKL-08014"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08016", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99004", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-08016", "err-BC-ERR-99004", "ex-1"],
 "read_minutes": {"full": 3.4, "brief": 3.0},
 "word_count": {"full": 500, "brief": 450},
 "research_lines": [
  {"file": "research/scoring/justification-requirements.md", "line": "The sharpest recurring rule is that a local argument does not justify a global claim."}
 ],
 "inferred": [
  {"claim": "BC-PT-99013 and BC-PT-99004 are earned on ex-1 steps 3 and 8 but not tagged, because their reader lines push the brief band past 450 words.", "settles": "A brief word cap that exempts reader lines, or a shorter reader_checks form."},
  {"claim": "The water context is measured in gallons, the sand context in tons and the oil context in gallons.", "settles": "A unit field in BC-QA-08006's parameter_spec."},
  {"claim": "A fluent solver writes the equation, the labelled candidate values and the conclusion, and types the closed form into the calculator only.", "settles": "Timing data per step from 10's fluency telemetry."}
 ],
 "sources": ["BC-CON-08008", "BC-SKL-08014", "BC-EK-CHA-4D1", "ced:154", "BC-QA-08006", "BC-PT-99011", "BC-PT-99013", "sg-25:5", "BC-ERR-08016", "BC-ERR-99004", "BC-MIS-99010", "BC-MIS-06010", "BC-PRQ-08001", "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts", "research/question-analysis/question-archetypes.md#BC-QA-08006 Time at which an accumulated amount is maximal", "research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions", "research/scoring/justification-requirements.md#Global versus local arguments", "research/scoring/justification-requirements.md#The candidates test", "research/exam/exam-structure.md#Section and part layout"]
}
```
