---
title: LSN-CON-05015 Critical points and behaviour of an implicit relation
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05015, locating the critical points of a relation in x and y and classifying them from a second derivative found implicitly, built from authoring_bundle("BC-CON-05015") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05015 Critical points and behaviour of an implicit relation

Concept BC-CON-05015 (skills BC-SKL-05058 to BC-SKL-05063), topic 5.12 of Unit 5. One archetype loads its skills, BC-QA-05012 (family implicit-differentiation). Unit parent BC-CON-05009; outside parents BC-CON-03004 and 03005 (docs/lessons/unit-05/README.md, section 1). BC-SKL-05058 against BC-SKL-05059 is the unit's confusable set, served by LSN-DEC-05-01 (README, section 3).

## Orientation

Served text, from BC-CON-05015 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.12 Exploring Behaviors of Implicit Relations): a response finds dy/dx implicitly, keeps only points that satisfy both the relation and the condition on dy/dx, and classifies from the sign of the second derivative after substituting dy/dx. No count, no frequency.

## Key ideas

Three BC-EK ids: two core blocks for both bands, one extended block for the low band.

- ki-1 (core, BC-EK-FUN-4D1, skills BC-SKL-05058, 05059, 05060). Paraphrase of Critical points of a relation and Two conditions at once: numerator zero with denominator nonzero, or denominator zero; the point satisfies both equations. Anchor quote from ced:110, 22 words.
- ki-2 (core, BC-EK-FUN-4E2, skills BC-SKL-05061, 05062). Paraphrase of Second derivative form: the second derivative is a relation in x, y and dy/dx, and the value of dy/dx is substituted before a number results; the differentiation and the substitution are scored separately (sg-25:21).
- ki-3 (extended, BC-EK-FUN-4E1, skill BC-SKL-05063). The second derivative test carried over to a relation. Anchor quote from ced:110, 10 words.

## Recognition

BC-QA-05012 (research/question-analysis/question-archetypes.md#BC-QA-05012 Critical points and second derivative behaviour of an implicit relation): `typical_wording` "find the coordinates of every point on the curve at which the tangent line is horizontal", "find the value of the second derivative at the given point on the curve"; `common_givens` an implicit equation or a differential equation, a point on the curve; `asked_to_produce` the differentiated expression, the substitution of the first derivative, the numerical value or the coordinates. The signal: an equation in x and y that is not solved for y, with "points on the curve" or "second derivative at the point". Shape: one part of a no-calculator FRQ worth two or three points; no `official_examples` in the record (notes name 2025 Q5(A)).

What says "not this concept": y given explicitly (BC-CON-05009 on a function), or a parametric curve (Unit 9).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-05012. Method, `expected_solution_path[0]`: differentiate the relation implicitly. Rival, `wrong_approaches`: solving the relation explicitly when it is not solvable. Separating feature: the relation is not a function of x, so both variables stay and every candidate x is put back into the relation. Not tagged inferred.

## Solution path

- ex-1, BC-QA-05012, both bands. Draw from `parameter_spec`: across 0, up 1, loop q1s1, facing 1, derivative derive. The notes give (y - 1)^2 = x^2 (x + 3), horizontal tangents at u = -2q, that is x = -2, y = 1 plus or minus 2; the node (0, 1) has both parts zero. No published BC-QA-05012 item carries this draw.
- Steps: dy/dx (new); numerator zero (new); its roots (solve); the relation (new); x = -2 (evaluate); y values (solve); x = 0 discarded (no value); the points (new).
- ex-2, same draw, low band: the second derivative at (-2, 3). Steps: the first implicit derivative with p for dy/dx (new); the second, with q for the second derivative (new); p = 0 and the point substituted (evaluate); q = -3/2 (solve); the classification (no value). A fluent solver writes every line of both.

## Scoring

BC-QA-05012 lists no `point_types`, so no what_a_reader_scores entry and no point tag. For the author: the archetype's scoring pattern gives the differentiation and the substitution separate points, the value point reachable from either (sg-25:21).

## Traps

Seven active errors meet the skills; the first four in the bundle's order are served: BC-ERR-03012, BC-ERR-03023, BC-ERR-05060, BC-ERR-05062. BC-ERR-05057, 05058 and 05059 are left out by the cap of 4 and are taught in LSN-CON-03005 and LSN-DEC-05-01. Low band all four; mid band the first two.

- err-BC-ERR-03012 (ex-1): the denominator set to zero for a horizontal tangent. No possible reason line.
- err-BC-ERR-03023 (ex-2): the second derivative left with dy/dx in it. Possible reason, words from BC-MIS-05033.
- err-BC-ERR-05060 (ex-2's relation at (1, 3), where dy/dx = 9/4): the term 2(dy/dx)^2 lost by differentiating y - 1 as a constant, giving 3 in place of 15/32. Possible reason, words from BC-MIS-05033.
- err-BC-ERR-05062 (ex-2): relative minimum reported where the second derivative is -3/2. Statement-shaped. No possible reason line.

## Representations

None as a separate block. The topic's Representations paragraph names derivative expression plus relation to a point on the curve (BC-REP-01 to BC-REP-02); ki-1's figure carries it.

## Prerequisite bridge

- BC-PRQ-05001 and BC-PRQ-05007, from their `description_plain` and `failure_signature`.

## Time

BC-QA-05012 is `no_calculator` and one FRQ part worth two or three points, so Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), this part about 3.3 to 5.0 of them at 1.67 minutes a point (docs/lessons/unit-05/README.md, section 5). The minutes go on the second differentiation and the substitution.

## Checks

- chk-1, completion of ex-1, both bands: x = -2 and x = 0 given. Key {(-2, -1), (-2, 3)}.
- chk-2, isomorph, both bands. Draw: across 0, up 0, loop q2s1, facing -1, derivative given; y^2 = 2x^2 (6 - x). Key {(4, -8), (4, 8)}.
- chk-3, MCQ, low band. Draw: across 0, up 0, loop q1s2, facing 1, derivative derive; y^2 = 4x^2 (x + 3), second derivative -3 at (-2, 4). Key: relative maximum at (-2, 4). Distractors: relative minimum (BC-ERR-05062), no classification from an unsubstituted expression (BC-ERR-03023), tangents at (0, 0) and (-3, 0) (BC-ERR-03012).

## Delivery

- orientation: text. Rule 5.
- ki-1: figure, the curve with the two horizontal tangent points, the vertical tangent point and the node marked. Rule 3 on BC-REP-02 in BC-SKL-05060; not promoted, since BC-QA-05012 `difficulty_variables` name no varying quantity (docs/lessons/unit-05/README.md, section 6).
- ki-2: text. Rule 5: BC-SKL-05061, 05062 carry BC-REP-01, 06.
- ki-3: figure. Rule 3 on BC-REP-02 in BC-SKL-05063.
- ex-1, ex-2 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1 to ki-3, st-1, ex-1, the four error blocks, chk-1 to chk-3, ex-2, the two bridges. 629 words, 4.5 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, ki-2, st-1, ex-1, err-BC-ERR-03012, err-BC-ERR-03023, chk-1, chk-2, the two bridges. 404 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, ki-2, the four error blocks, ex-1.

## Sources

- BC-CON-05015; BC-SKL-05058, BC-SKL-05059, BC-SKL-05060, BC-SKL-05061, BC-SKL-05062, BC-SKL-05063; BC-EK-FUN-4D1, BC-EK-FUN-4E1, BC-EK-FUN-4E2; ced:110
- BC-QA-05012; sg-25:21
- BC-ERR-03012, BC-ERR-03023, BC-ERR-05060, BC-ERR-05062; BC-MIS-05033
- BC-PRQ-05001, BC-PRQ-05007
- research/units/unit-05-analytical-applications-differentiation.md#5.12 Exploring Behaviors of Implicit Relations
- research/question-analysis/question-archetypes.md#BC-QA-05012 Critical points and second derivative behaviour of an implicit relation
- research/exam/exam-structure.md#Section and part layout
- [inferred] The share of the 15.0 minutes. Settled by a BC-PT mapping for BC-QA-05012.
- [inferred] ki-1 and ki-3 as static figures. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-05015",
 "kind": "concept",
 "target_id": "BC-CON-05015",
 "unit": "05",
 "skills": ["BC-SKL-05058", "BC-SKL-05059", "BC-SKL-05060", "BC-SKL-05061", "BC-SKL-05062", "BC-SKL-05063"],
 "orientation": {
  "text": "A response finds \\(\\frac{dy}{dx}\\) implicitly, keeps only points that satisfy both the relation and the condition on \\(\\frac{dy}{dx}\\), and classifies from the sign of the second derivative after substituting the value of \\(\\frac{dy}{dx}\\).",
  "sources": ["BC-CON-05015", "research/units/unit-05-analytical-applications-differentiation.md#5.12 Exploring Behaviors of Implicit Relations"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-4D1",
   "depth": "core",
   "text": "On a relation, \\(\\frac{dy}{dx}\\) is a quotient. It is zero where the numerator is zero and the denominator is not; it fails to exist where the denominator is zero. A critical point is a point of the curve, so its coordinates satisfy both the relation and that condition.",
   "notation": "dy/dx",
   "quote": {"text": "A point on an implicit relation where the first derivative equals zero or does not exist is a critical point of the function.", "source": "ced:110"},
   "sources": ["BC-EK-FUN-4D1", "ced:110", "research/units/unit-05-analytical-applications-differentiation.md#5.12 Exploring Behaviors of Implicit Relations"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-4E2",
   "depth": "core",
   "text": "Differentiating again gives an expression in \\(x\\), \\(y\\) and \\(\\frac{dy}{dx}\\), with the chain rule on every \\(y\\). A number results only after the value of \\(\\frac{dy}{dx}\\) at the point is substituted.",
   "notation": "d2y/dx2",
   "quote": null,
   "sources": ["BC-EK-FUN-4E2", "ced:110", "sg-25:21", "research/units/unit-05-analytical-applications-differentiation.md#5.12 Exploring Behaviors of Implicit Relations"]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-FUN-4E1",
   "depth": "extended",
   "text": "The second derivative test carries over: where \\(\\frac{dy}{dx}=0\\) on the curve, a negative \\(\\frac{d^2y}{dx^2}\\) gives a relative maximum of \\(y\\), a positive one a relative minimum.",
   "notation": "d2y/dx2",
   "quote": {"text": "Applications of derivatives can be extended to implicitly defined functions.", "source": "ced:110"},
   "sources": ["BC-EK-FUN-4E1", "ced:110", "research/units/unit-05-analytical-applications-differentiation.md#5.12 Exploring Behaviors of Implicit Relations"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-05012",
   "cue": "The stem asks for coordinates or a second derivative value, from an implicit equation and a point on the curve.",
   "method": "First written line: differentiate the relation implicitly.",
   "rival": "Rival: solving the relation explicitly when it is not solvable.",
   "separating_feature": "Not solved for \\(y\\): both variables stay, and each candidate goes back into the relation.",
   "sources": ["BC-QA-05012"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-05012",
   "bands": ["low", "mid"],
   "parameter_draw": {"across": 0, "up": 1, "loop": "q1s1", "facing": 1, "derivative": "derive"},
   "problem": {"text": "Find every point on \\((y-1)^2=x^2(x+3)\\) where the tangent line is horizontal.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Not solved for \\(y\\): differentiate implicitly.", "why": "\\(2(y-1)y'=3x^2+6x\\).", "expr": "(3*x**2 + 6*x)/(2*(y - 1))", "relation": "new"},
    {"cue": "Horizontal: numerator zero.", "why": "The denominator must stay nonzero.", "expr": "3*x*(x + 2) = 0", "relation": "new"},
    {"cue": "Candidates.", "why": "\\(x=-2\\) or \\(x=0\\).", "expr": "FiniteSet(-2, 0)", "relation": "solve", "variable": "x"},
    {"cue": "Points must lie on the curve.", "why": "Back to the relation.", "expr": "(y - 1)**2 = x**2*(x + 3)", "relation": "new"},
    {"cue": "\\(x=-2\\).", "why": "\\(4\\cdot1=4\\).", "expr": "(y - 1)**2 = 4", "relation": "evaluate", "subs": {"x": "-2"}},
    {"cue": "Solve for \\(y\\).", "why": "\\(y-1=\\pm2\\); denominator nonzero.", "expr": "FiniteSet(-1, 3)", "relation": "solve", "variable": "y"},
    {"cue": "\\(x=0\\) gives \\(y=1\\).", "why": "Denominator zero too: discarded."},
    {"cue": "Points asked.", "why": "Both conditions hold.", "expr": "FiniteSet(Tuple(-2, -1), Tuple(-2, 3))", "relation": "new"}
   ],
   "answer": {"form": "symbolic", "expr": "FiniteSet(Tuple(-2, -1), Tuple(-2, 3))"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-05012",
   "bands": ["low"],
   "parameter_draw": {"across": 0, "up": 1, "loop": "q1s1", "facing": 1, "derivative": "derive"},
   "problem": {"text": "On \\((y-1)^2=x^2(x+3)\\), find \\(\\frac{d^2y}{dx^2}\\) at \\((-2,3)\\) and classify the point. Write \\(p=\\frac{dy}{dx}\\), \\(q=\\frac{d^2y}{dx^2}\\).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "First derivative, implicit.", "why": "Chain rule on \\(y\\).", "expr": "2*(y - 1)*p = 3*x**2 + 6*x", "relation": "new"},
    {"cue": "Differentiate again, keeping both variables.", "why": "Product rule: \\(2p\\cdot p+2(y-1)q\\).", "expr": "2*p**2 + 2*(y - 1)*q = 6*x + 6", "relation": "new"},
    {"cue": "Substitute \\(p=0\\) and the point.", "why": "\\(p\\) is zero at a horizontal tangent.", "expr": "4*q = -6", "relation": "evaluate", "subs": {"x": "-2", "y": "3", "p": "0"}},
    {"cue": "Solve for \\(q\\).", "why": "Negative.", "expr": "-3/2", "relation": "solve", "variable": "q"},
    {"cue": "Classify with a reason.", "why": "\\(\\frac{dy}{dx}=0\\) and \\(\\frac{d^2y}{dx^2}<0\\): relative maximum at \\((-2,3)\\)."}
   ],
   "answer": {"form": "symbolic", "expr": "-3/2"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-03012",
   "observed_behavior": "The denominator of dy/dx is set to zero when a horizontal tangent is requested, or the numerator when a vertical tangent is requested.",
   "scoring_consequence": "The reported point is wrong and the reasoning point is not available.",
   "wrong_step": {"text": "Denominator zero.", "expr": "2*(y - 1) = 0"},
   "right_step": {"text": "Numerator zero.", "expr": "3*x*(x + 2) = 0"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-03012"]
  },
  {
   "error_id": "BC-ERR-03023",
   "observed_behavior": "An expression for the second derivative containing dy/dx is evaluated without first computing the value of dy/dx at the point.",
   "scoring_consequence": "The numerical second derivative is wrong, although the product and chain rule points described in the 2025 scoring guidelines may still be earned (sg-25:20).",
   "wrong_step": {"text": "\\(q=\\frac{-6-2p^2}{4}\\) left with \\(p\\).", "expr": "(-6 - 2*p**2)/4"},
   "right_step": {"text": "\\(p=0\\): \\(q=-\\frac{3}{2}\\).", "expr": "-3/2"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-05033", "text": "leaves the derivative symbol unsubstituted"},
   "sources": ["BC-ERR-03023", "BC-MIS-05033"]
  },
  {
   "error_id": "BC-ERR-05060",
   "observed_behavior": "The response differentiates the derivative expression without applying the chain rule to the dependent variable.",
   "scoring_consequence": "The differentiation point is lost, and the value point remains available only through a correct substitution.",
   "wrong_step": {"text": "At \\((1,3)\\), \\(y-1\\) treated as constant: \\(2(y-1)q=6x+6\\) gives \\(4q=12\\), \\(q=3\\).", "expr": "3"},
   "right_step": {"text": "\\(2p^2+2(y-1)q=6x+6\\) with \\(p=\\frac{9}{4}\\) gives \\(q=\\frac{15}{32}\\).", "expr": "15/32"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-05033", "text": "differentiates expressions in the second variable without the chain rule"},
   "sources": ["BC-ERR-05060", "BC-MIS-05033"]
  },
  {
   "error_id": "BC-ERR-05062",
   "observed_behavior": "The response evaluates the second derivative on a relation correctly but classifies the point the wrong way round.",
   "scoring_consequence": "The classification is wrong although the computation was right.",
   "wrong_step": {"text": "\\(q=-\\frac{3}{2}\\), so a relative minimum.", "expr": "relative_minimum_at_minus2_3"},
   "right_step": {"text": "\\(q<0\\): relative maximum.", "expr": "relative_maximum_at_minus2_3"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-05062"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-05001", "text": "List the zeros of the numerator and of the denominator first; without them there are no candidate points."},
  {"prq_id": "BC-PRQ-05007", "text": "Solve the relation and the derived equation together; an input alone, with no matching output on the relation, is not a point."}
 ],
 "time": {"exam_part": "II-B", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 3, 4, 5, 6, 7, 8], "ex-2": [1, 2, 3, 4, 5]}, "skipped_steps": {"ex-1": [], "ex-2": []}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-05012",
   "parameter_draw": {"across": 0, "up": 1, "loop": "q1s1", "facing": 1, "derivative": "derive"},
   "completes": "ex-1",
   "stem": {"text": "On \\((y-1)^2=x^2(x+3)\\) the numerator gives \\(x=-2\\) or \\(0\\). Find the horizontal tangent points.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "FiniteSet(Tuple(-2, -1), Tuple(-2, 3))"},
   "steps": [
    {"text": "The relation.", "expr": "(y - 1)**2 = x**2*(x + 3)", "relation": "new"},
    {"text": "\\(x=-2\\).", "expr": "(y - 1)**2 = 4", "relation": "evaluate", "subs": {"x": "-2"}},
    {"text": "\\(y=-1\\) or \\(3\\).", "expr": "FiniteSet(-1, 3)", "relation": "solve", "variable": "y"},
    {"text": "\\(x=0\\) gives the node \\((0,1)\\), discarded.", "expr": "FiniteSet(Tuple(-2, -1), Tuple(-2, 3))", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-05060"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-05012",
   "parameter_draw": {"across": 0, "up": 0, "loop": "q2s1", "facing": -1, "derivative": "given"},
   "stem": {"text": "For \\(y^2=2x^2(6-x)\\), \\(\\frac{dy}{dx}=\\frac{3x(4-x)}{y}\\). Find every horizontal tangent point.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "FiniteSet(Tuple(4, -8), Tuple(4, 8))"},
   "steps": [
    {"text": "Numerator zero.", "expr": "3*x*(4 - x) = 0", "relation": "new"},
    {"text": "\\(x=0\\) or \\(4\\).", "expr": "FiniteSet(0, 4)", "relation": "solve", "variable": "x"},
    {"text": "The relation.", "expr": "y**2 = 2*x**2*(6 - x)", "relation": "new"},
    {"text": "\\(x=4\\).", "expr": "y**2 = 64", "relation": "evaluate", "subs": {"x": "4"}},
    {"text": "\\(y=\\pm8\\).", "expr": "FiniteSet(-8, 8)", "relation": "solve", "variable": "y"},
    {"text": "\\(x=0\\) gives \\(y=0\\), denominator zero: discarded.", "expr": "FiniteSet(Tuple(4, -8), Tuple(4, 8))", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-05058"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-05012",
   "parameter_draw": {"across": 0, "up": 0, "loop": "q1s2", "facing": 1, "derivative": "derive"},
   "stem": {"text": "On \\(y^2=4x^2(x+3)\\), \\(\\frac{dy}{dx}=0\\) at \\((-2,4)\\) and \\(2p^2+2yq=24x+24\\). Which is true?", "command_verb": "identify"},
   "key": {"form": "statement", "expr": "relative_maximum_at_minus2_4"},
   "steps": [
    {"text": "The second implicit derivative.", "expr": "2*p**2 + 2*y*q = 24*x + 24", "relation": "new"},
    {"text": "\\(p=0\\), \\((-2,4)\\).", "expr": "8*q = -24", "relation": "evaluate", "subs": {"x": "-2", "y": "4", "p": "0"}},
    {"text": "\\(q=-3\\).", "expr": "-3", "relation": "solve", "variable": "q"}
   ],
   "options": [
    {"id": "A", "is_key": false, "label": "\\(\\frac{d^2y}{dx^2}=-3\\), so a relative minimum at \\((-2,4)\\).", "error_path": "BC-ERR-05062", "derivation": "sign read the wrong way round"},
    {"id": "B", "is_key": true, "label": "\\(\\frac{d^2y}{dx^2}=-3\\), so a relative maximum at \\((-2,4)\\).", "error_path": null},
    {"id": "C", "is_key": false, "label": "\\(\\frac{d^2y}{dx^2}=-3-\\frac{p^2}{4}\\), so no sign can be read.", "error_path": "BC-ERR-03023", "derivation": "p left unsubstituted"},
    {"id": "D", "is_key": false, "label": "The horizontal tangents are at \\((0,0)\\) and \\((-3,0)\\), not \\((-2,4)\\).", "error_path": "BC-ERR-03012", "derivation": "denominator 2y set to zero for a horizontal tangent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-05063"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: a statement of what a response shows; the curve is drawn once, on ki-1", "sources": ["BC-SKL-05058"]},
  {"block": "ki-1", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-05060; not promoted, BC-QA-05012 difficulty_variables name no varying quantity", "sources": ["BC-SKL-05060", "BC-QA-05012"],
   "spec": {"kind": "implicit_curve", "representations": ["BC-REP-02", "BC-REP-01"], "curve": "(y - 1)^2 = x^2 (x + 3)", "window": {"x": [-4, 2], "y": [-3, 5]},
    "marks": ["(-2, -1)", "(-2, 3)", "(-3, 1)", "(0, 1)"],
    "labels": [{"text": "horizontal: numerator 0", "placement": "inside"}, {"text": "vertical: denominator 0", "placement": "inside"}, {"text": "(0, 1): both 0", "placement": "inside"}]},
   "fallback": "the same curve, static, with the four points marked and each label inside", "keyboard": "none needed; no control"},
  {"block": "ki-2", "mode": "text", "reason": "rule 5: BC-SKL-05061 and 05062 carry BC-REP-01, 06 only", "sources": ["BC-SKL-05061", "BC-SKL-05062"]},
  {"block": "ki-3", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-05063; a fixed feature, not promoted", "sources": ["BC-SKL-05063"],
   "spec": {"kind": "implicit_curve", "representations": ["BC-REP-02"], "curve": "(y - 1)^2 = x^2 (x + 3)", "window": {"x": [-4, 2], "y": [-3, 5]},
    "marks": ["(-2, 3)", "(-2, -1)"],
    "labels": [{"text": "(-2, 3): second derivative -3/2, maximum", "placement": "inside"}, {"text": "(-2, -1): second derivative 3/2, minimum", "placement": "inside"}]},
   "fallback": "the same curve, static, with the two points and labels inside", "keyboard": "none needed; no control"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03012", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03023", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05060", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05062", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "ki-2", "err-BC-ERR-03012", "err-BC-ERR-03023", "err-BC-ERR-05060", "err-BC-ERR-05062", "ex-1"],
 "read_minutes": {"full": 4.5, "brief": 3.0},
 "word_count": {"full": 629, "brief": 404},
 "research_lines": [
  {"file": "research/units/unit-05-analytical-applications-differentiation.md", "line": "so the coordinates must satisfy both the defining equation and the derived condition"}
 ],
 "inferred": [
  {"claim": "The second derivative part takes about 3.3 to 5.0 of the 15.0 Section II minutes, from its two or three points; no BC-PT record fixes it.", "settles": "A point_types mapping for BC-QA-05012."},
  {"claim": "ki-1 and ki-3 are served as static figures.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-05015", "BC-SKL-05058", "BC-SKL-05059", "BC-SKL-05060", "BC-SKL-05061", "BC-SKL-05062", "BC-SKL-05063", "BC-EK-FUN-4D1", "BC-EK-FUN-4E1", "BC-EK-FUN-4E2", "ced:110", "BC-QA-05012", "sg-25:21", "BC-ERR-03012", "BC-ERR-03023", "BC-ERR-05060", "BC-ERR-05062", "BC-MIS-05033", "BC-PRQ-05001", "BC-PRQ-05007", "research/units/unit-05-analytical-applications-differentiation.md#5.12 Exploring Behaviors of Implicit Relations", "research/question-analysis/question-archetypes.md#BC-QA-05012 Critical points and second derivative behaviour of an implicit relation", "research/exam/exam-structure.md#Section and part layout"]
}
```
