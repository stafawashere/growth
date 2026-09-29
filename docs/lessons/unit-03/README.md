---
title: Unit 3 attack map
research_date: 2026-09-29
status: draft
purpose: The map every designer of a Unit 3 concept lesson (Differentiation, Composite, Implicit, and Inverse Functions) reads first, giving the fringe order of the 10 BC-CON concepts, the exam shapes the unit feeds, the cross-concept recognition features and first lines, the recurring traps with their scoring consequences, the time budgets, the delivery mode per concept under TEMPLATE.md's selection rules, and the sources.
---

# Unit 3 attack map

BC-UNIT-03 holds six topics (BC-TOP-0301 to BC-TOP-0306), 10 concepts and 34 skills (BC-SKL-03001 to BC-SKL-03034), all shared with AB, carried by one enduring understanding, FUN-3 (research/units/unit-03-differentiation-composite-implicit-inverse.md#Unit 3, Differentiation: Composite, Implicit, and Inverse Functions; ced:72, ced:75, ced:79, ced:80). Every count and list below was computed on 2026-09-29 from `load_snapshot(DEFAULT_CONTENT_ROOT)` and data/prereq_edges.csv, data/errors.json and data/misconceptions.json. Nothing here is served to a student; it is input to the ten concept designs `LSN-CON-03001` to `LSN-CON-03010`.

## 1. Concept order along the prerequisite edges

Method: a topological order over the `hard_prerequisite` edges whose both ends are Unit 3 skills, ties broken by id, then each concept placed at the position of its first skill in that order (ties by concept id). The skill order the computation returns is BC-SKL-03001 to BC-SKL-03034 in id order, so the concept order equals id order. Parent concepts are the concepts holding a hard parent of any of the concept's skills; outside parents are hard parents from other units or BC-TOP stand-ins; supporting parents are listed separately.

Two facts a designer needs before reading the table:

- BC-CON-03001 and BC-CON-03002 are mutual parents at concept level: BC-SKL-03001 (in 03001) is a hard parent of BC-SKL-03002 (in 03002), and BC-SKL-03002 is a hard parent of BC-SKL-03003 (in 03001). The fringe reaches BC-CON-03001 first through BC-SKL-03001; its three-layer skill BC-SKL-03003 only opens after the two-layer chain rule.
- BC-SKL-03032, the only skill of BC-CON-03010, has no Unit 3 hard parent (its hard parent is BC-SKL-02010). Under the id tie rule it sorts last, but it can enter the fringe as soon as BC-SKL-02010 is mastered [inferred: the engine's actual fringe order depends on Unit 2 mastery state, settled by a fringe trace in app/engine/fringe.py on a student with Unit 2 placed].

| # | Concept | Name | Skills | Unit 3 parent concepts (hard) | Outside hard parents | Supporting parents |
|---|---|---|---|---|---|---|
| 1 | BC-CON-03001 | Composite function structure | BC-SKL-03001, BC-SKL-03003 | BC-CON-03002 (via BC-SKL-03002 to BC-SKL-03003) | BC-SKL-02032 | BC-PRQ-03001 |
| 2 | BC-CON-03002 | Chain rule as a product of rates | BC-SKL-03002, BC-SKL-03004, BC-SKL-03005, BC-SKL-03006 | BC-CON-03001 | BC-SKL-02027, BC-SKL-02036, BC-SKL-02037, BC-SKL-02039, BC-TOP-0207, BC-TOP-0209 | BC-PRQ-03001, BC-PRQ-03005, BC-PRQ-03006, BC-SKL-02021 |
| 3 | BC-CON-03003 | A dependent variable inside an equation | BC-SKL-03007, BC-SKL-03008, BC-SKL-03009 | BC-CON-03002 | BC-TOP-0208 | BC-PRQ-03005 |
| 4 | BC-CON-03004 | Solving a differentiated relation for dy/dx | BC-SKL-03010, BC-SKL-03011, BC-SKL-03014 | BC-CON-03003 | none | BC-PRQ-03002, BC-PRQ-03006 |
| 5 | BC-CON-03005 | Tangent line behaviour on an implicit curve | BC-SKL-03012, BC-SKL-03013 | BC-CON-03004 | none | BC-PRQ-03007 |
| 6 | BC-CON-03006 | Derivative of an inverse function | BC-SKL-03015, BC-SKL-03016, BC-SKL-03017, BC-SKL-03018, BC-SKL-03019, BC-SKL-03020 | BC-CON-03002 | BC-SKL-02039 | BC-PRQ-03003, BC-PRQ-03006 |
| 7 | BC-CON-03007 | Derivatives of inverse trigonometric functions | BC-SKL-03021, BC-SKL-03022, BC-SKL-03023, BC-SKL-03024, BC-SKL-03025 | BC-CON-03002, BC-CON-03003, BC-CON-03006 | none | BC-PRQ-03004, BC-PRQ-03006 |
| 8 | BC-CON-03008 | Classification of an expression before differentiating | BC-SKL-03026, BC-SKL-03027, BC-SKL-03028, BC-SKL-03029 | BC-CON-03002 (via BC-SKL-03004 to BC-SKL-03026) | BC-SKL-02025 | BC-PRQ-03001, BC-PRQ-03006, BC-SKL-02046 |
| 9 | BC-CON-03009 | Repeated differentiation | BC-SKL-03030, BC-SKL-03031, BC-SKL-03033, BC-SKL-03034 | BC-CON-03003, BC-CON-03004, BC-CON-03008 | BC-TOP-0202 | BC-PRQ-03002, BC-PRQ-03005, BC-PRQ-03006 |
| 10 | BC-CON-03010 | Notation for higher-order derivatives | BC-SKL-03032 | none | BC-SKL-02010 | BC-PRQ-03005 |

BC-PRQ parents, by name from the snapshot: BC-PRQ-03001 Decomposing a formula into an outer and an inner function; BC-PRQ-03002 Solving a linear equation for an embedded factor; BC-PRQ-03003 Definition of an inverse function and reading matched pairs; BC-PRQ-03004 Unit circle values, Pythagorean identities, and right triangle ratios; BC-PRQ-03005 Reading and writing prime and Leibniz derivative notation; BC-PRQ-03006 Simplifying rational and radical expressions; BC-PRQ-03007 Deciding when an expression is zero or undefined. All BC-PRQ edges are `supporting`.

Edges in data/prereq_edges.csv that differ from the research file's topic lists, and that a designer should trust over the research text: BC-SKL-03002 is a hard parent of BC-SKL-03015 and BC-SKL-03016 (not only BC-SKL-03020); BC-SKL-03015 is a hard parent of BC-SKL-03021; BC-SKL-03004 is a hard parent of BC-SKL-03026; BC-SKL-03026 is a hard parent of BC-SKL-03030. Several BC-TOP stand-ins named in research/units/unit-03-differentiation-composite-implicit-inverse.md#Cross-unit connections are now BC-SKL-02 ids in the CSV (for example BC-SKL-02036 for the product rule).

## 2. Exam question types the unit feeds

Twelve archetypes load a Unit 3 skill, in nine families. Exam part budgets from research/exam/exam-structure.md#Section and part layout: Section I Part A, 29 questions in 62 minutes, no calculator, 2.14 minutes per question; Part B, 13 in 38, calculator, 2.92; Section II, 2 in 30 (Part A, calculator) and 4 in 60 (Part B, no calculator), 15.0 per question, 9 points each (research/exam/exam-structure.md#Free-response point totals).

| Family | Archetype | Shape (research/question-analysis/question-archetypes.md) | Calculator status | Exam part | Point types | Official examples in the record |
|---|---|---|---|---|---|---|
| rule-manipulation | BC-QA-03001 Chain rule derivative of a composite given symbolically | usually one MCQ, or an opening step inside a multipart FRQ | no_calculator | I-A; II-B as a step | BC-PT-99023, BC-PT-99004 | BC-FRQ-2013-Q4-D, BC-FRQ-2014-Q3-D, BC-MCQ-PE2012-001 |
| rule-manipulation | BC-QA-03007 Inverse trigonometric derivative with an inner function | one MCQ, or a step inside a contextual FRQ | either | I-A or I-B; II-A contextual | none | BC-MCQ-PE2012-007 |
| derivative-from-table | BC-QA-03002 Composite derivative evaluated from a table of values | one MCQ, or one part of a table-based FRQ | either | I-A or I-B | none | none |
| derivative-from-graph | BC-QA-03003 Composite derivative read from graphs of the component functions | one MCQ | no_calculator | I-A | none | none |
| implicit-differentiation | BC-QA-03004 Implicit differentiation producing or verifying dy/dx | opening part of a multipart FRQ whose later parts reuse the curve | no_calculator | I-A; II-B | none | BC-MCQ-CED-004 |
| implicit-differentiation | BC-QA-03005 Horizontal or vertical tangent on an implicitly defined curve | one or two parts inside the implicit differentiation FRQ | no_calculator | II-B | none | none |
| inverse-function-derivative | BC-QA-03006 Derivative of an inverse function at a point | one MCQ, or one part of a multi-representation FRQ | either | I-A or I-B | none | none |
| inverse-function-derivative | BC-QA-03010 Inverse trigonometric derivative derived from the identity f(g(x)) = x | no multipart structure recorded | no_calculator | I-A [inferred: the record carries no shape field; settled by an official item on the archetype] | none | none |
| higher-order-derivative | BC-QA-03008 Higher-order derivative of a function or of a derivative expression | opening part of a Taylor polynomial or differential equation FRQ | no_calculator | II-B; I-A | BC-PT-99022, BC-PT-99023, BC-PT-99027 | BC-FRQ-2025-Q5-A |
| procedure-selection | BC-QA-03009 Selecting the differentiation procedure for a given expression | one MCQ, or a differentiation step inside a longer question | no_calculator | I-A | none | none |
| polar-calculus | BC-QA-99001 Polar tangent slope relation solved for the derivative of the horizontal coordinate | one part of a multipart polar FRQ, three points | calculator | II-A | BC-PT-99049, BC-PT-99005, BC-PT-99004 | BC-FRQ-2026-Q2-B |
| antidifferentiation-technique | BC-QA-06018 Antiderivative matched to an inverse trigonometric form | no multipart structure recorded | no_calculator | I-A [inferred, as for BC-QA-03010] | none | none |

BC-QA-99001 and BC-QA-06018 load a Unit 3 skill (BC-SKL-03002 and BC-SKL-03021) but are primary to Units 9 and 6; a Unit 3 lesson draws no example from them. BC-QA-03004 and BC-QA-03005 are grounded in the AB questions 2023 AB Q6, 2024 AB Q5 and 2025 AB Q6 as described in the Chief Reader reports (cr-23:22, cr-24:17), not in a BC scoring guideline, and the research file tags the BC equivalent [uncertain] (research/units/unit-03-differentiation-composite-implicit-inverse.md#Unresolved).

The research file's official evidence index also lists 22 FRQ parts with BC-UNIT-03 as primary or secondary unit; only three are primary to a Unit 3 archetype (BC-FRQ-2013-Q4-D, BC-FRQ-2014-Q3-D, BC-FRQ-2025-Q5-A). The rest use BC-SKL-03002 or BC-SKL-03030 inside Unit 4, 6, 7, 9 and 10 archetypes (research/units/unit-03-differentiation-composite-implicit-inverse.md#Official evidence index).

Point types, restated from the BC-PT records:

- BC-PT-99023 Chain rule. Earns: "Correct differentiation of the inner function, including the required differentials (sg-22:16, sg-25:21)." Does not earn: a product rule written without one or both differentials.
- BC-PT-99022 Product rule. Earns: a differentiation that correctly applies the product rule (sg-25:20, sg-22:16). Does not earn: a response that treats one factor as constant, which sg-22:16 states is eligible for the chain rule point but not this one.
- BC-PT-99027 Higher derivative expression evaluated at a point. Earns: a correct second or higher derivative evaluated at the requested point, consistent with earlier work (sg-25:20, sg-23:10). Does not earn: an expression left in terms of the first derivative where the prompt asked for the dependent variable (sg-23:11).
- BC-PT-99004 Answer with or without supporting work; BC-PT-99005 Answer with supporting work or setup shown; BC-PT-99049 Derivative of one variable with respect to another by the chain rule in polar or parametric form.

Nine of the twelve archetypes carry no `point_types`, so their lessons carry no scoring section (TEMPLATE.md reader_scores rule; docs/plan/15-lessons.md#The scoring checklist, `what_a_reader_scores`). This is the largest library gap for the unit (see Sources).

## 3. Cross-concept patterns

### Which concepts the stems combine

Computed from each archetype's `skills` mapped to concepts:

- BC-QA-03001: BC-CON-03001 and BC-CON-03002 (BC-SKL-03006 brings in the Unit 2 product and quotient rules).
- BC-QA-03002: BC-CON-03002 alone (BC-SKL-03004, BC-SKL-03006).
- BC-QA-03004: BC-CON-03003 and BC-CON-03004. BC-QA-03005: BC-CON-03005 and BC-CON-03004 (BC-SKL-03011).
- BC-QA-03006: BC-CON-03006 alone. BC-QA-03007: BC-CON-03007 alone. BC-QA-03010: BC-CON-03006, BC-CON-03007 and BC-CON-03002.
- BC-QA-03008: BC-CON-03009 and BC-CON-03010 (BC-SKL-03032). Its official example BC-FRQ-2025-Q5-A also loads BC-SKL-02036 and BC-SKL-07018.
- BC-QA-03009: BC-CON-03008 and BC-CON-03002 (BC-SKL-03006).

The implicit FRQ is built on one curve: derive or verify dy/dx, then reuse it for a tangent line, a horizontal or vertical tangent, and a related rate (research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation; cr-23:22, cr-24:17). BC-CON-03003, 03004 and 03005 therefore share one stem family, and an error in the opening part propagates (BC-ERR-03001 consequence text, section 4).

### Recognition features that separate neighbouring concepts

Each pair names the stem feature, from the archetype records and the topic Required mathematical knowledge paragraphs, that selects the method.

| Neighbours | Selecting feature | Source |
|---|---|---|
| Chain rule (BC-CON-03002) against product rule (Unit 2) | the operation applied last: a function evaluated at another function's output is a composition; two variable factors multiplied is a product. A composite that is one factor of a product needs both, outer structure first | BC-QA-03001 `common_givens`; BC-SKL-03006; research/units/unit-03-differentiation-composite-implicit-inverse.md#3.5 Selecting Procedures for Calculating Derivatives (Classification, Order of rules) |
| Implicit (BC-CON-03003) against explicit differentiation | an equation in x and y that is not solved for y; every y term then carries a dy/dx factor. An expression already solved for y is differentiated directly | BC-QA-03004 `common_givens`; BC-EK-FUN-3D1 (ced:76) |
| Inverse function derivative (BC-CON-03006) against the reciprocal of the function | the stem names g as the inverse of f and gives a value that is an output of f; the answer is one over f prime at the matching input, not one over f and not one over f prime at the given value | BC-QA-03006 `common_givens`, `wrong_approaches` (BC-ERR-03015, BC-ERR-03016) |
| Inverse trigonometric derivatives (BC-CON-03007) against the inverse function rule | arcsin, arccos or arctan of an inner expression selects the standard formula with the inner expression substituted and the inner derivative multiplied; the general inverse rule is the derivation route only (BC-QA-03010) | BC-QA-03007 `expected_solution_path`; BC-EK-FUN-3E2 (ced:78) |
| Higher-order derivatives (BC-CON-03009) against a first derivative | the stem asks for the second derivative or a value of it; when dy/dx is an expression in x and y, the second differentiation is implicit and dy/dx reappears | BC-QA-03008 `asked_to_produce`, `difficulty_variables`; sg-25:20 |
| Chain rule from a table (BC-SKL-03004) against the product rule from a table (BC-QA-02009) | the named combination is a composite f(g(a)), so the table is read twice in sequence (inner value, then outer derivative at that value); a product reads all four entries at the same input | BC-QA-03002 `expected_solution_path`, `difficulty_variables` ("whether a distractor row matches the input rather than the output") |
| Horizontal against vertical tangent (BC-CON-03005) | horizontal selects the numerator of dy/dx, vertical the denominator; either candidate is then checked against the curve equation | BC-QA-03005 `expected_solution_path`, BC-ERR-03012, BC-ERR-03013 |

The research file records BC-MIS-03012 (the differentiation rule follows from the look of the expression) across topics 3.1, 3.4 and 3.5, and the Chief Reader report records rule choice driven by the shape of an expression (cr-22:21). In the snapshot BC-MIS-03012 is linked only to the skills of BC-CON-03008, so the computed cross-concept list in section 4 does not show it.

### The first written line each method needs

From `expected_solution_path[0]`, the first step the record names:

- BC-QA-03001 chain rule, symbolic: identify the outer and inner functions. First line: inner u = ..., outer f(u) = ... [inferred as a written line: the record names the step, not its layout].
- BC-QA-03002 chain rule from a table: evaluate the inner function at the given input. First line: g(a) read from the table.
- BC-QA-03003 chain rule from graphs: read the inner function value at the given input.
- BC-QA-03004 implicit: differentiate every term of both sides with respect to x. First line: d/dx applied to both sides, with the right side kept (crabbc-25 notation note in research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation).
- BC-QA-03005 tangent condition: set the numerator or the denominator of dy/dx equal to zero as the direction requires.
- BC-QA-03006 inverse derivative: identify the input whose output is the stated value. First line: f(c) = b, so g(b) = c.
- BC-QA-03007 inverse trigonometric: write the standard derivative with the inner expression substituted.
- BC-QA-03008 higher order: differentiate the supplied expression with respect to the independent variable, product rule on mixed terms and chain rule on terms in the dependent variable.
- BC-QA-03009 selection: classify the outermost operation.
- BC-QA-03010 derivation: differentiate both sides of the identity, applying the chain rule to the composite on the left.

Every archetype above carries both `asked_to_produce` and `common_givens` in the snapshot, so no strategy block drawn from them needs `evidence_tag: inferred` on that ground.

## 4. Recurring traps

### BC-ERR and BC-MIS records that span two or more of the unit's concepts

Computed as records whose `skills` fall in two or more Unit 3 concepts. Consequence text is the record's `scoring_consequence`, verbatim.

| Record | Name | Concepts | Scoring consequence |
|---|---|---|---|
| BC-ERR-03001 | Inner derivative omitted from a chain rule application | 03001, 03002 | "The derivative is wrong, and in a multipart question the error propagates into every later part that uses it." |
| BC-ERR-03002 | One layer of a multi-layer composite left undifferentiated | 03001, 03002, 03008 | "The derivative is wrong; no credit is available for a partially applied rule in a single answer item." |
| BC-ERR-03006 | Product or quotient rule omitted when a composite is one factor | 03002, 03007, 03008 | "The derivative is wrong; in the 2025 implicit differentiation task the product rule carries its own scoring point (sg-25:20)." |
| BC-ERR-03008 | Product rule omitted on a term containing both variables | 03003, 03009 | "The differentiation loses the point for a completely correct implicit derivative, and the 2025 scoring guidelines award the product rule its own point (sg-25:20, crabbc-25:24)." |
| BC-ERR-03011 | Only one coordinate substituted into dy/dx | 03004, 03009 | "No numerical slope is produced, so the evaluation point is lost." |
| BC-MIS-03001 | Differentiation acts only on the outermost shell (severity high) | 03001, 03002 | not a scoring record |
| BC-MIS-03005 | A short mixed term is a single symbol (severity high) | 03003, 03009 | not a scoring record |
| BC-MIS-03006 | dy/dx is a number rather than an expression in both variables (severity medium) | 03004, 03009 | not a scoring record |

Three errors from other units are named in this unit's archetype `wrong_approaches`, and a designer anchoring distractors must check they are held by the lesson's skills before use: BC-ERR-05057 Horizontal tangent points found without checking the denominator (BC-QA-03005; "The reported points may have no tangent at all, so the critical point list is wrong."), BC-ERR-05060 Second derivative of a relation taken as though the second variable were constant (BC-QA-03008; "The differentiation point is lost, and the value point remains available only through a correct substitution."), BC-ERR-99036 Differentiation rule chosen by the shape of the expression (BC-QA-03009; "The derivative point is not earned, and every later part that uses the derivative inherits the error.").

The two high-severity clusters the research file names: y treated as an independent symbol with a mixed term read as one object (BC-MIS-03004, BC-MIS-03005), which lost the completely correct implicit differentiation point in 2023, 2024 and 2025 (cr-23:23, cr-24:18); and the tangent condition read apart from the curve (BC-MIS-03007; cr-23:23, cr-24:18) (research/units/unit-03-differentiation-composite-implicit-inverse.md#Misconception summary).

### Point losses research/scoring names for this unit's shapes

- Unnecessary simplification that introduces an error loses the answer point, BC-ERR-99022 (research/scoring/common-point-losses.md#Answer points; cr-24:19). Simplification is optional but must be correct if attempted (research/scoring/notation-requirements.md#Simplification; sg-23:16). Applies to every symbolic derivative in the unit, and BC-QA-03001 `expected_solution_path` ends with "simplify only as far as is safe".
- A variable expression equated to a numerical value, BC-ERR-99002 (research/scoring/common-point-losses.md#Notation points), and the general derivative expression equated to a number (research/scoring/notation-requirements.md#The equal sign; sg-23:6). Applies where dy/dx or the second derivative is evaluated at a point (BC-QA-03004, BC-QA-03008), and it is the BC-PT-99049 does-not-earn text on BC-QA-99001.
- Differentials and derivatives mixed, or the variable of differentiation unstated, BC-ERR-99013 (research/scoring/common-point-losses.md#Notation points). Loose derivative notation is otherwise accepted when intent is clear (research/scoring/notation-requirements.md#Derivative notation), which bounds how much notation BC-CON-03010 should insist on [inferred: whether a higher-order notation slip costs a point on its own is not stated; settled by a scoring guideline note on a higher-derivative part].
- Setup correct against value correct is scored separately (research/question-analysis/frq-analysis.md#The diagnostic value of an FRQ part), and the chain rule factor omitted is a named recurring distinction, 16 entries, including BC-FRQ-2013-Q4-D and BC-FRQ-2014-Q3-D.
- The 2025 second-derivative part awards product rule, chain rule and value separately, so the two rule points survive an arithmetic slip in the value (BC-QA-03008 scoring pattern; sg-25:20).

## 5. Time budgets

The budget is the exam's own per-question figure for the shape (docs/plan/15-lessons.md#Fluency, measured and never credited). For an FRQ part, the share of 15.0 minutes is the part's points over 9 [inferred: plan 15 names `scoring_pattern`'s share without fixing the rule as points over 9; settled by app/progress/fluency.py when built].

| Archetype | Shape | Budget | Steps a fluent solver writes (from `expected_solution_path`) |
|---|---|---|---|
| BC-QA-03001 | MCQ, I-A | 2.14 min | the derivative with the inner factor attached, one line per layer; decomposition held mentally [inferred] |
| BC-QA-03001 | FRQ step, II-B, 3 points on BC-FRQ-2013-Q4-D and BC-FRQ-2014-Q3-D | 5.0 min | the differentiation line showing the inner factor (the BC-PT-99023 point), then the value (BC-PT-99004) |
| BC-QA-03002 | MCQ, I-A or I-B | 2.14 or 2.92 min | g(a), f'(g(a)), g'(a), the product |
| BC-QA-03003 | MCQ, I-A | 2.14 min | inner value read, two slopes read, the product |
| BC-QA-03004 | MCQ, I-A | 2.14 min | the differentiated equation, the collected and factored line, dy/dx |
| BC-QA-03004 / 03005 | FRQ parts, II-B | not computable: no BC point record [inferred; settled by a BC-PT mapping for the AB parts in cr-23:22, cr-24:17] | the differentiated equation with every dy/dx and the product rule visible; for tangents, the zero condition, the substitution into the curve, the conclusion in words |
| BC-QA-03006 | MCQ, I-A or I-B | 2.14 or 2.92 min | f(c) = b, f'(c), the reciprocal; in FRQ the matching input must be visible (scoring pattern) |
| BC-QA-03007 | MCQ, I-A or I-B | 2.14 or 2.92 min | the formula with the inner expression substituted times the inner derivative |
| BC-QA-03008 | FRQ opening part, II-B, 3 points on BC-FRQ-2025-Q5-A | 5.0 min | the differentiated expression showing the product and chain rules, the substitution of the point and of dy/dx there, the value |
| BC-QA-03009 | MCQ, I-A | 2.14 min | the derivative, rules applied outside in; the classification is not written [inferred] |
| BC-QA-99001 | FRQ part, II-A, 3 points | 5.0 min | the chain relation, the substituted values, the value (sg-26:7) |

## 6. Delivery map

Rules from docs/lessons/TEMPLATE.md#Delivery, applied in order: (1) worked examples and error blocks are `step_reveal`; (2) a key idea describing a process is `motion`; (3) a figure-bearing BC-REP (02, 07, 08, 12, 13, 14) on the skills gives `figure`, promoted to `interactive` when `common_givens` or `difficulty_variables` name a varying quantity and the stem asks for a reading; (4) BC-REP-03 givens give `table`; (5) else `text`. The table below covers orientation and key ideas; every worked example and error block in all ten lessons is `step_reveal` by rule 1. Every non-text choice is [inferred], settled by the modality A/B in docs/lessons/BUILD-PLAN.md.

| Concept | Mode | Rule | Triggering field |
|---|---|---|---|
| BC-CON-03001 | text | 5 | skills' `representations` are BC-REP-01 and BC-REP-04 only |
| BC-CON-03002 | text for the rule; figure for the key idea on reading from graphs; table for the key idea on reading from a table | 5, 3, 4 | BC-SKL-03005 `representations` BC-REP-02; BC-SKL-03004 BC-REP-03; BC-QA-03002 `common_givens` "a table of values of f, f prime, g, and g prime". Static figure is enough: BC-QA-03003 `difficulty_variables` (corner, grid position) are properties of a fixed graph, not a varying parameter, so no promotion |
| BC-CON-03003 | text | 5 | BC-SKL-03007 to 03009 carry BC-REP-01 only; the dy/dx factor is an algebraic statement |
| BC-CON-03004 | text | 5 | BC-SKL-03010, 03011, 03014 carry BC-REP-01 only |
| BC-CON-03005 | interactive | 3, promoted | BC-SKL-03012 and 03013 `representations` include BC-REP-02; BC-QA-03005 `common_givens` "a stated horizontal line or a point on the curve" and `difficulty_variables` "whether more than one candidate value of the variable arises". Spec: one draggable point constrained to the implicit curve with its tangent drawn and dy/dx shown as numerator over denominator; the question asked is where the tangent is horizontal or vertical. Fallback: a static figure with the horizontal and vertical tangent points marked. Keyboard: arrow keys move the point along the curve |
| BC-CON-03006 | interactive for the key idea on the matched pair; table for the table key idea | 3, promoted; 4 | BC-SKL-03016 and 03019 `representations` include BC-REP-02; BC-SKL-03018 BC-REP-03; BC-QA-03006 `difficulty_variables` "whether a distractor input equal to the requested value exists". Spec: f and its inverse reflected across y = x, one slider for c, the points (c, f(c)) and (f(c), c) marked with both tangent slopes shown, the reading asked being that the second slope is the reciprocal of the first. Fallback: static figure at one c. Keyboard: arrow keys on the slider |
| BC-CON-03007 | text | 5 | skills carry BC-REP-01 and BC-REP-09; BC-REP-09 is not figure-bearing |
| BC-CON-03008 | text | 5 | BC-REP-01 and BC-REP-04; the stems of a decision lesson for this set would use `contrast`, which is outside concept lessons |
| BC-CON-03009 | text | 5 | BC-REP-01 only on the skills (BC-QA-03008 adds BC-REP-06, not figure-bearing). Repeated differentiation is not one of rule 2's processes (a limit, a partition, accumulation, a traced curve), so no motion |
| BC-CON-03010 | text | 5 | BC-SKL-03032 carries BC-REP-01 and BC-REP-04; a notation table (prime against Leibniz) is text layout, not rule 4, since no BC-REP-03 given |

No concept in the unit meets rule 2 or the `model` mode: no key idea is a limit process or a computed sequence of values, and no productive-failure target (BC-DF-13 or BC-DF-15 archetypes as productive-failure openers per TEMPLATE.md) is assigned here, although BC-QA-03002, 03004 and 03006 carry BC-DF-13 [inferred: whether BC-DF-13 on these archetypes makes them productive-failure targets is settled by the target list in docs/plan/15-lessons.md#Sequencing within and across concepts].

## 7. Sources

Library records: BC-CON-03001 to BC-CON-03010; BC-SKL-03001 to BC-SKL-03034; BC-SKL-02010, BC-SKL-02021, BC-SKL-02025, BC-SKL-02027, BC-SKL-02032, BC-SKL-02036, BC-SKL-02037, BC-SKL-02039, BC-SKL-02046; BC-TOP-0202, BC-TOP-0207, BC-TOP-0208, BC-TOP-0209; BC-PRQ-03001 to BC-PRQ-03007; BC-QA-03001 to BC-QA-03010, BC-QA-99001, BC-QA-06018, BC-QA-02009; BC-PT-99004, BC-PT-99005, BC-PT-99022, BC-PT-99023, BC-PT-99027, BC-PT-99049; BC-ERR-03001, 03002, 03006, 03008, 03011, 03012, 03013, 03015, 03016, BC-ERR-05057, BC-ERR-05060, BC-ERR-99002, BC-ERR-99013, BC-ERR-99022, BC-ERR-99036; BC-MIS-03001, 03004, 03005, 03006, 03007, 03012; BC-EK-FUN-3D1, BC-EK-FUN-3E2; BC-FRQ-2013-Q4-D, BC-FRQ-2014-Q3-D, BC-FRQ-2025-Q5-A, BC-FRQ-2026-Q2-B, BC-MCQ-PE2012-001, BC-MCQ-PE2012-007, BC-MCQ-CED-004; BC-REP-01 to 04, 06, 08, 09, 13.

Pages: ced:72, ced:75, ced:76, ced:77, ced:78, ced:79, ced:80; sg-22:16, sg-23:6, sg-23:16, sg-25:20, sg-26:7; cr-22:21, cr-23:22, cr-23:23, cr-24:17, cr-24:18, cr-24:19.

Research headings: research/units/unit-03-differentiation-composite-implicit-inverse.md#3.1 The Chain Rule, #3.2 Implicit Differentiation, #3.5 Selecting Procedures for Calculating Derivatives, #Cross-unit connections, #Misconception summary, #Unresolved, #Official evidence index; research/exam/exam-structure.md#Section and part layout, #Free-response point totals; research/scoring/common-point-losses.md#Answer points, #Notation points; research/scoring/notation-requirements.md#Simplification, #The equal sign, #Derivative notation; research/question-analysis/question-archetypes.md#BC-QA-03001 to #BC-QA-03009 and #BC-QA-99001; research/question-analysis/frq-analysis.md#The diagnostic value of an FRQ part; docs/lessons/TEMPLATE.md#Delivery; docs/plan/15-lessons.md#What a lesson is, and its granularity, #Methods, thought process and scoring habits, #Pacing to the exam date.

Library gaps met while building this map:

- Nine of twelve archetypes carry no `point_types` (BC-QA-03002 to 03007, 03009, 03010, 06018), so those lessons carry no scoring section.
- BC-QA-03002, 03003, 03005, 03006, 03009 and 03010 list no `official_examples`; BC-QA-03004 and 03005 rest on AB Chief Reader reports.
- BC-QA-03010 and BC-QA-06018 carry no multipart structure in research/question-analysis/question-archetypes.md, so their exam part is inferred.
- BC-MIS-03012 is linked in the snapshot only to BC-CON-03008's skills, while the research file places it in topics 3.1, 3.4 and 3.5.
- The 2025 implicit FRQ evidence sits on `crabbc-25` pages (cache/text/crabbc-25), which fall outside the checker's `cr-YY:` citation form; this map cites them only inside record or research text.
