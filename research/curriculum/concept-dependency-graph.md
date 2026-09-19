---
title: Concept Dependency Graph
research_date: 2026-09-19
status: draft
purpose: The unit-level dependency matrix, the concept-level adjacency listing derived from the skill edges, forward and backward traversal rules, and the machine-readable pointers into data/prereq_edges.csv.
---

# Concept Dependency Graph

Every statement here is derived from `../../data/prereq_edges.csv` by `../../tools/graph_check.py`. The CSV carries five columns, `from`, `to`, `type`, `evidence_tag`, `note`, and an edge reads as "from is a prerequisite of to". Two types are in use: `hard_prerequisite`, meaning the downstream skill cannot be performed without the upstream one, and `supporting`, meaning the upstream skill makes the downstream one easier or supplies a representation it uses. Rows whose endpoint is still a BC-TOP id are cross-unit edges written before the other unit's skills existed; their notes end with the word `unmapped` and `../../tools/remap_edges.py` rewrites them to a BC-SKL id as soon as one name matches.

## Graph summary [inferred]

The graph holds 945 edges over 541 BC-SKL nodes, 77 BC-PRQ nodes, and 25 BC-TOP placeholder nodes. Of those edges 376 are typed `hard_prerequisite` and 569 are typed `supporting`. The hard_prerequisite subgraph is acyclic: `tools/graph_check.py` reports 0 cycles. It has 280 root skills, meaning skills with no incoming hard prerequisite from another skill, and 351 leaf skills, meaning skills that no other skill depends on. Roots are entry points rather than easy skills: a skill is a root whenever its only recorded prerequisites are BC-PRQ records or supporting edges.

## Unit-level dependency matrix [inferred]

Cell values are the number of edges of any type running from a skill or topic of the row unit into a skill or topic of the column unit, that is, the row unit is the prerequisite side. Read a row as what this unit feeds; read a column as what this unit rests on. The diagonal is omitted because within-unit edges are not cross-unit dependencies.

| prerequisite unit / dependent unit | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | feeds total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BC-UNIT-01 Limits and Continuity | - | 23 |  | 5 | 6 | 8 |  |  |  | 2 | 44 |
| BC-UNIT-02 Differentiation: Definition and Fundamental Properties | 1 | - | 11 | 8 | 4 | 6 | 2 | 1 | 1 | 1 | 35 |
| BC-UNIT-03 Differentiation: Composite, Implicit, and Inverse Functions |  |  | - | 5 | 3 | 3 | 1 |  | 1 |  | 13 |
| BC-UNIT-04 Contextual Applications of Differentiation |  |  |  | - | 2 |  | 2 | 1 |  |  | 5 |
| BC-UNIT-05 Applying Derivatives to Analyze Functions |  |  |  | 1 | - | 3 | 4 | 2 | 1 |  | 11 |
| BC-UNIT-06 Integration and Accumulation of Change |  |  |  |  | 4 | - | 7 | 13 | 4 | 2 | 30 |
| BC-UNIT-07 Differential Equations |  |  |  |  |  |  | - | 1 | 1 | 1 | 3 |
| BC-UNIT-08 Applications of Integration |  |  |  |  |  |  |  | - | 7 |  | 7 |
| BC-UNIT-09 Parametric Equations, Polar Coordinates, and Vector-Valued Functions |  |  |  |  |  |  |  |  | - |  | 0 |
| BC-UNIT-10 Infinite Sequences and Series |  |  |  |  |  |  |  |  |  | - | 0 |
| rests-on total | 1 | 23 | 11 | 19 | 19 | 20 | 16 | 18 | 15 | 6 |  |

Three pairs are mutually dependent at unit level while the skill graph stays acyclic: BC-UNIT-01 and BC-UNIT-02, BC-UNIT-04 and BC-UNIT-05, BC-UNIT-05 and BC-UNIT-06. In each pair the two directions run between different skills, so no skill lies on a cycle. BC-UNIT-09 and BC-UNIT-10 feed nothing, which is the terminal position of the parametric, polar, vector unit and the series unit in the CED ordering.

## Unit dependency listing [inferred]

- BC-UNIT-01 Limits and Continuity. Depends on: BC-UNIT-02. Depended on by: BC-UNIT-02, BC-UNIT-04, BC-UNIT-05, BC-UNIT-06, BC-UNIT-10.
- BC-UNIT-02 Differentiation: Definition and Fundamental Properties. Depends on: BC-UNIT-01. Depended on by: BC-UNIT-01, BC-UNIT-03, BC-UNIT-04, BC-UNIT-05, BC-UNIT-06, BC-UNIT-07, BC-UNIT-08, BC-UNIT-09, BC-UNIT-10.
- BC-UNIT-03 Differentiation: Composite, Implicit, and Inverse Functions. Depends on: BC-UNIT-02. Depended on by: BC-UNIT-04, BC-UNIT-05, BC-UNIT-06, BC-UNIT-07, BC-UNIT-09.
- BC-UNIT-04 Contextual Applications of Differentiation. Depends on: BC-UNIT-01, BC-UNIT-02, BC-UNIT-03, BC-UNIT-05. Depended on by: BC-UNIT-05, BC-UNIT-07, BC-UNIT-08.
- BC-UNIT-05 Applying Derivatives to Analyze Functions. Depends on: BC-UNIT-01, BC-UNIT-02, BC-UNIT-03, BC-UNIT-04, BC-UNIT-06. Depended on by: BC-UNIT-04, BC-UNIT-06, BC-UNIT-07, BC-UNIT-08, BC-UNIT-09.
- BC-UNIT-06 Integration and Accumulation of Change. Depends on: BC-UNIT-01, BC-UNIT-02, BC-UNIT-03, BC-UNIT-05. Depended on by: BC-UNIT-05, BC-UNIT-07, BC-UNIT-08, BC-UNIT-09, BC-UNIT-10.
- BC-UNIT-07 Differential Equations. Depends on: BC-UNIT-02, BC-UNIT-03, BC-UNIT-04, BC-UNIT-05, BC-UNIT-06. Depended on by: BC-UNIT-08, BC-UNIT-09, BC-UNIT-10.
- BC-UNIT-08 Applications of Integration. Depends on: BC-UNIT-02, BC-UNIT-04, BC-UNIT-05, BC-UNIT-06, BC-UNIT-07. Depended on by: BC-UNIT-09.
- BC-UNIT-09 Parametric Equations, Polar Coordinates, and Vector-Valued Functions. Depends on: BC-UNIT-02, BC-UNIT-03, BC-UNIT-05, BC-UNIT-06, BC-UNIT-07, BC-UNIT-08. Depended on by: none.
- BC-UNIT-10 Infinite Sequences and Series. Depends on: BC-UNIT-01, BC-UNIT-02, BC-UNIT-06, BC-UNIT-07. Depended on by: none.

## Concept-level adjacency [inferred]

A BC-CON to BC-CON edge exists when at least one BC-SKL edge runs from a skill of the first concept to a skill of the second. The count in brackets is the number of skill edges that project onto that concept edge. Concepts with no outgoing edge are omitted; their skills are leaves or feed only skills inside the same concept.

- BC-CON-01001 (Instantaneous rate of change as a limit of average rates) -> BC-CON-02002 [3], BC-CON-02001 [2], BC-CON-02007 [2]
- BC-CON-01002 (The limit of a function at a point) -> BC-CON-01011 [1], BC-CON-06006 [1]
- BC-CON-01003 (Limit notation and its reading) -> BC-CON-02002 [1]
- BC-CON-01004 (One sided limits and two sided existence) -> BC-CON-01005 [1], BC-CON-01013 [1], BC-CON-02007 [1], BC-CON-02009 [1]
- BC-CON-01005 (Ways a limit can fail to exist) -> BC-CON-02009 [1]
- BC-CON-01006 (Estimation of a limit from a graph or a table) -> BC-CON-02007 [1], BC-CON-10001 [1]
- BC-CON-01007 (Limit theorems for combinations of functions) -> BC-CON-01009 [1], BC-CON-02011 [1]
- BC-CON-01008 (Indeterminate form handled by rewriting) -> BC-CON-02003 [1], BC-CON-04015 [1]
- BC-CON-01011 (Connecting graphical, numerical, analytical, and verbal limit statements) -> BC-CON-02004 [1]
- BC-CON-01012 (Classification of discontinuities) -> BC-CON-01015 [1], BC-CON-01016 [1], BC-CON-02008 [1], BC-CON-02009 [1]
- BC-CON-01013 (Continuity at a point as three conditions) -> BC-CON-02008 [3], BC-CON-01015 [1], BC-CON-01019 [1]
- BC-CON-01016 (Infinite limits and vertical asymptotes) -> BC-CON-06019 [1]
- BC-CON-01017 (Limits at infinity and horizontal asymptotes) -> BC-CON-04006 [1], BC-CON-04014 [1], BC-CON-05007 [1]
- BC-CON-01019 (The Intermediate Value Theorem) -> BC-CON-02008 [1], BC-CON-05001 [1]
- BC-CON-02001 (Average rate of change as a difference quotient) -> BC-CON-02002 [2], BC-CON-04001 [1]
- BC-CON-02002 (Instantaneous rate of change as the limit of a difference quotient) -> BC-CON-02003 [1], BC-CON-02006 [1]
- BC-CON-02003 (The derivative as a function defined by a limit) -> BC-CON-02006 [1], BC-CON-02010 [1], BC-CON-10016 [1]
- BC-CON-02005 (The derivative at a point as the slope of the tangent line) -> BC-CON-04012 [1], BC-CON-07003 [1]
- BC-CON-02006 (Recognising a limit as a derivative of a known function) -> BC-CON-06014 [1]
- BC-CON-02008 (Differentiability implies continuity) -> BC-CON-05001 [1]
- BC-CON-02009 (Ways a derivative fails to exist at a point of continuity) -> BC-CON-03002 [1], BC-CON-08021 [1]
- BC-CON-02010 (The power rule) -> BC-CON-02011 [1], BC-CON-03002 [1], BC-CON-05004 [1], BC-CON-06014 [1]
- BC-CON-02011 (Linearity of differentiation) -> BC-CON-02013 [2], BC-CON-02014 [1]
- BC-CON-02012 (Derivatives of the basic transcendental functions) -> BC-CON-02015 [1]
- BC-CON-02013 (The product rule) -> BC-CON-02014 [1], BC-CON-03002 [1], BC-CON-09014 [1]
- BC-CON-02014 (The quotient rule) -> BC-CON-02015 [2], BC-CON-03006 [1]
- BC-CON-02015 (Derivatives of the remaining trigonometric functions by rewriting) -> BC-CON-03008 [1]
- BC-CON-03001 (Composite function structure) -> BC-CON-03002 [1]
- BC-CON-03002 (Chain rule as a product of rates) -> BC-CON-03001 [1], BC-CON-03003 [1], BC-CON-03006 [1], BC-CON-03007 [1], BC-CON-06008 [1], BC-CON-06015 [1], BC-CON-09013 [1]
- BC-CON-03003 (A dependent variable inside an equation) -> BC-CON-03004 [1], BC-CON-03007 [1], BC-CON-03009 [1]
- BC-CON-03004 (Solving a differentiated relation for dy/dx) -> BC-CON-03005 [2], BC-CON-05015 [2], BC-CON-03009 [1]
- BC-CON-03007 (Derivatives of inverse trigonometric functions) -> BC-CON-06014 [1]
- BC-CON-03008 (Classification of an expression before differentiating) -> BC-CON-04015 [1]
- BC-CON-04002 (Units of a derivative) -> BC-CON-04001 [1], BC-CON-04006 [1]
- BC-CON-04003 (Position, velocity, and acceleration on a line) -> BC-CON-04004 [1], BC-CON-04005 [1]
- BC-CON-04004 (Velocity, speed, and direction) -> BC-CON-04005 [3]
- BC-CON-04006 (The common structure of contextual rate problems) -> BC-CON-04002 [1]
- BC-CON-04007 (Variables in a related rates problem as functions of time) -> BC-CON-04008 [2], BC-CON-04009 [1]
- BC-CON-04008 (The relating equation) -> BC-CON-04007 [1], BC-CON-04009 [1]
- BC-CON-04009 (Substitution after differentiation) -> BC-CON-04010 [2]
- BC-CON-04011 (The tangent line as a local linear approximation) -> BC-CON-04012 [1]
- BC-CON-04012 (Direction of the approximation error) -> BC-CON-07006 [2], BC-CON-05012 [1]
- BC-CON-04013 (Indeterminate form) -> BC-CON-04014 [1], BC-CON-04015 [1]
- BC-CON-04014 (The hypothesis of L'Hospital's rule) -> BC-CON-04013 [1], BC-CON-04015 [1]
- BC-CON-05003 (Critical points and the local versus global distinction) -> BC-CON-05005 [2], BC-CON-05006 [2], BC-CON-05009 [1], BC-CON-05013 [1]
- BC-CON-05004 (Monotonicity read from the sign of the first derivative) -> BC-CON-05011 [2], BC-CON-05005 [1], BC-CON-05006 [1], BC-CON-05012 [1], BC-CON-07005 [1]
- BC-CON-05005 (First derivative test for relative extrema) -> BC-CON-05009 [1], BC-CON-05010 [1], BC-CON-06009 [1], BC-CON-08008 [1]
- BC-CON-05006 (Candidates test for absolute extrema on a closed interval) -> BC-CON-05013 [1], BC-CON-05014 [1], BC-CON-06009 [1], BC-CON-08008 [1], BC-CON-09014 [1]
- BC-CON-05007 (Concavity as the monotonicity of the first derivative) -> BC-CON-05011 [2], BC-CON-05012 [2], BC-CON-05008 [1], BC-CON-05009 [1], BC-CON-07005 [1]
- BC-CON-05008 (Point of inflection as a change of concavity) -> BC-CON-05011 [1]
- BC-CON-05009 (Second derivative test at a critical point) -> BC-CON-05010 [1], BC-CON-05015 [1]
- BC-CON-05010 (A sole relative extremum as an absolute extremum) -> BC-CON-05013 [1]
- BC-CON-05011 (Graph of a function reconstructed from its derivative graphs) -> BC-CON-05012 [1]
- BC-CON-05012 (Simultaneous reading of a function and its first two derivatives) -> BC-CON-07006 [1]
- BC-CON-05013 (Optimisation model with an objective and a constraint) -> BC-CON-05014 [2], BC-CON-07012 [1]
- BC-CON-06003 (Riemann sum approximation of a definite integral) -> BC-CON-06004 [3]
- BC-CON-06005 (Summation notation and the Riemann sum as a sum of products) -> BC-CON-06006 [2]
- BC-CON-06007 (Accumulation function defined by a definite integral) -> BC-CON-06008 [1], BC-CON-06009 [1]
- BC-CON-06008 (Fundamental Theorem of Calculus part one) -> BC-CON-06009 [4], BC-CON-05003 [1]
- BC-CON-06009 (Behaviour of an accumulation function read from the integrand) -> BC-CON-05005 [1], BC-CON-05006 [1], BC-CON-05008 [1]
- BC-CON-06010 (Definite integral evaluated by geometry) -> BC-CON-06007 [1], BC-CON-08001 [1], BC-CON-08010 [1], BC-CON-09015 [1]
- BC-CON-06011 (Algebraic properties of the definite integral) -> BC-CON-06019 [1]
- BC-CON-06012 (Fundamental Theorem of Calculus part two and net change) -> BC-CON-08021 [2], BC-CON-06013 [1], BC-CON-06017 [1], BC-CON-06018 [1], BC-CON-06019 [1], BC-CON-07007 [1], BC-CON-08001 [1], BC-CON-08002 [1], BC-CON-08003 [1], BC-CON-08005 [1], BC-CON-08006 [1], BC-CON-08010 [1], BC-CON-09004 [1], BC-CON-09008 [1], BC-CON-09015 [1]
- BC-CON-06013 (Average value of a function) -> BC-CON-08001 [1]
- BC-CON-06014 (Antiderivative and indefinite integral) -> BC-CON-06016 [2], BC-CON-06017 [2], BC-CON-07008 [2], BC-CON-06012 [1], BC-CON-06020 [1]
- BC-CON-06015 (Substitution of variables) -> BC-CON-06016 [2], BC-CON-07007 [2], BC-CON-06018 [1], BC-CON-06020 [1], BC-CON-08014 [1], BC-CON-10025 [1]
- BC-CON-06016 (Rearrangement into an equivalent integrable form) -> BC-CON-06020 [1]
- BC-CON-06017 (Integration by parts) -> BC-CON-06020 [2]
- BC-CON-06018 (Linear partial fraction decomposition) -> BC-CON-06020 [2], BC-CON-07011 [1]
- BC-CON-06019 (Improper integral and convergence) -> BC-CON-06020 [1], BC-CON-10006 [1]
- BC-CON-07001 (Differential equation as a relation between a function and its derivatives) -> BC-CON-07008 [2], BC-CON-07010 [2], BC-CON-07011 [2]
- BC-CON-07002 (Verification of a proposed solution) -> BC-CON-07003 [1]
- BC-CON-07003 (Families of solutions) -> BC-CON-07008 [1]
- BC-CON-07004 (Slope field as a plot of derivative values) -> BC-CON-07005 [5], BC-CON-07006 [1]
- BC-CON-07005 (Solution curves read off a slope field) -> BC-CON-07006 [1], BC-CON-07012 [1], BC-CON-10016 [1]
- BC-CON-07007 (Separation of variables) -> BC-CON-07008 [1], BC-CON-07009 [1], BC-CON-07010 [1]
- BC-CON-07008 (Particular solution selected by an initial condition) -> BC-CON-07010 [3], BC-CON-09005 [1]
- BC-CON-07011 (Logistic differential equation) -> BC-CON-07012 [1]
- BC-CON-07012 (Carrying capacity and the point of fastest change) -> BC-CON-07011 [2]
- BC-CON-08003 (Displacement as the definite integral of velocity) -> BC-CON-09007 [1]
- BC-CON-08004 (Total distance as the definite integral of speed) -> BC-CON-09010 [1]
- BC-CON-08005 (Position and velocity recovered from an initial value) -> BC-CON-09010 [1]
- BC-CON-08010 (Area between two curves integrated in x) -> BC-CON-09016 [1]
- BC-CON-08019 (Washer method for a region held away from the axis) -> BC-CON-09016 [1]
- BC-CON-08021 (Arc length of a curve given by a function) -> BC-CON-09004 [2]

The projection yields 192 concept edges over 85 source concepts, out of 170 concepts registered.

## Traversal forward [inferred]

Walking forward from a skill along `hard_prerequisite` edges gives the set of skills that cannot be performed while that skill is missing. The reachable set below is the full transitive closure, not just the direct dependents, and it is computed over hard edges only. These are the fifteen skills with the largest direct fan-out.

| Skill | Name | Direct dependents | Transitively unreachable | Units reached |
|---|---|---|---|---|
| BC-SKL-06034 | Evaluate a definite integral by antidifferentiation and endpoint substitution | 13 | 32 | 06, 07, 08, 09 |
| BC-SKL-03002 | Differentiate a two layer composite function with the chain rule | 8 | 53 | 03, 05, 06, 07, 09, 10 |
| BC-SKL-06047 | Select a substitution by identifying an inner function whose derivative appears | 7 | 28 | 06, 07, 10 |
| BC-SKL-02036 | Apply the product rule to a product of two differentiable functions | 6 | 13 | 02, 03, 04, 06, 09 |
| BC-SKL-05020 | Classify a critical point from the sign change of the first derivative | 6 | 10 | 05, 08 |
| BC-SKL-07010 | Compute the slope the equation assigns to a given point | 6 | 13 | 07 |
| BC-SKL-01028 | Recognise an indeterminate form as a signal that rewriting is needed | 5 | 13 | 01, 02, 03, 04 |
| BC-SKL-02039 | Apply the quotient rule to a quotient of two differentiable functions | 5 | 5 | 02, 03 |
| BC-SKL-05010 | Determine critical points where the first derivative equals zero | 5 | 27 | 05, 07, 08, 09 |
| BC-SKL-05016 | Build a sign chart on critical points and domain boundaries | 5 | 16 | 05, 08 |
| BC-SKL-06018 | Differentiate an accumulation function with a variable upper limit | 5 | 7 | 06 |
| BC-SKL-01058 | Evaluate the limit of a rational function at infinity by comparing degrees | 4 | 6 | 01, 04, 06 |
| BC-SKL-03010 | Solve the differentiated equation for dy/dx | 4 | 10 | 03, 05 |
| BC-SKL-05028 | Write a global justification covering every candidate | 4 | 7 | 05, 08, 09 |
| BC-SKL-05031 | Determine concavity from whether the derivative graph rises or falls | 4 | 9 | 05 |

- From BC-SKL-06034: BC-SKL-06036, BC-SKL-06037, BC-SKL-06038, BC-SKL-06039, BC-SKL-06060, BC-SKL-06065, BC-SKL-06068, BC-SKL-07025, BC-SKL-07026, BC-SKL-07027, BC-SKL-07029, BC-SKL-07030, BC-SKL-07031, BC-SKL-07033, BC-SKL-07035, BC-SKL-07036, BC-SKL-07037, BC-SKL-07038, BC-SKL-08001, BC-SKL-08004, BC-SKL-08006, BC-SKL-08009, BC-SKL-08012, BC-SKL-08022, BC-SKL-08057, BC-SKL-09011, BC-SKL-09020, BC-SKL-09021, BC-SKL-09026, BC-SKL-09038, BC-TOP-0706, BC-TOP-0807.
- From BC-SKL-03002: BC-SKL-03003, BC-SKL-03004, BC-SKL-03006, BC-SKL-03007, BC-SKL-03008, BC-SKL-03009, BC-SKL-03010, BC-SKL-03011, BC-SKL-03012, BC-SKL-03013, BC-SKL-03014, BC-SKL-03020, BC-SKL-03022, BC-SKL-03023, BC-SKL-03025, BC-SKL-03033, BC-SKL-03034, BC-SKL-05058, BC-SKL-05060, BC-SKL-05061, BC-SKL-05062, BC-SKL-05063, BC-SKL-06019, BC-SKL-06047, BC-SKL-06048, BC-SKL-06049, BC-SKL-06050, BC-SKL-06051, BC-SKL-06052, BC-SKL-06054, BC-SKL-06056, BC-SKL-06064, BC-SKL-06065, BC-SKL-06071, BC-SKL-06072, BC-SKL-06073, BC-SKL-06074, BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07027, BC-SKL-07028, BC-SKL-07029, BC-SKL-07030, BC-SKL-07031, BC-SKL-07033, BC-SKL-07035, BC-SKL-07036, BC-SKL-07037, BC-SKL-07038, BC-SKL-07043, BC-SKL-09032, BC-SKL-10069.
- From BC-SKL-06047: BC-SKL-06048, BC-SKL-06049, BC-SKL-06050, BC-SKL-06051, BC-SKL-06052, BC-SKL-06054, BC-SKL-06056, BC-SKL-06064, BC-SKL-06065, BC-SKL-06071, BC-SKL-06072, BC-SKL-06073, BC-SKL-06074, BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07027, BC-SKL-07028, BC-SKL-07029, BC-SKL-07030, BC-SKL-07031, BC-SKL-07033, BC-SKL-07035, BC-SKL-07036, BC-SKL-07037, BC-SKL-07038, BC-SKL-07043, BC-SKL-10069.
- From BC-SKL-02036: BC-SKL-02037, BC-SKL-02039, BC-SKL-02040, BC-SKL-02041, BC-SKL-02044, BC-SKL-02045, BC-SKL-03006, BC-SKL-03020, BC-SKL-04022, BC-SKL-09032, BC-SKL-09033, BC-TOP-0302, BC-TOP-0611.
- From BC-SKL-05020: BC-SKL-05021, BC-SKL-05022, BC-SKL-05023, BC-SKL-05038, BC-SKL-05039, BC-SKL-05053, BC-SKL-05054, BC-SKL-05055, BC-SKL-05057, BC-SKL-08014.

## Traversal backward [inferred]

Walking backward from a failed skill gives the checklist of upstream records to test before concluding that the skill itself is the broken one. The backward walk has three layers, and the registry stores each layer in a different place.

1. Direct `hard_prerequisite` edges into the skill, read from the `prerequisites` field of the BC-SKL record in ../../data/skills.json, which `../../tools/sync_dependents.py` keeps equal to the incoming hard edges of ../../data/prereq_edges.csv.

2. `supporting` edges into the skill, which do not appear in the `prerequisites` field and must be read from the CSV by filtering on `to` and `type`.

3. The BC-PRQ record named by `adaptive.remediation_target` on the skill, which is the non-calculus prerequisite the decomposition holds responsible when the response fails before any calculus step. The `prerequisite_gap_if` sentence on the same record states the observable condition.

The skills with the deepest backward chains are the ones with the most incoming hard edges:

| Skill | Name | Direct hard prerequisites | Transitive upstream |
|---|---|---|---|
| BC-SKL-06071 | Classify an integrand to select an antidifferentiation technique | 5 | 17 |
| BC-SKL-07043 | Interpret a logistic model in context | 4 | 25 |
| BC-SKL-02031 | Differentiate a polynomial function | 3 | 3 |
| BC-SKL-03002 | Differentiate a two layer composite function with the chain rule | 3 | 4 |
| BC-SKL-03006 | Combine the chain rule with the product or quotient rule | 3 | 11 |
| BC-SKL-05053 | Verify that the critical point gives the required extremum on the domain | 3 | 19 |
| BC-SKL-06027 | Describe the graph of an accumulation function from the graph of the integrand | 3 | 5 |
| BC-SKL-06056 | Decide between rearrangement and substitution for a rational integrand | 3 | 9 |
| BC-SKL-06057 | Choose u and dv for an integration by parts | 3 | 8 |
| BC-SKL-06073 | Chain two antidifferentiation techniques in one problem | 3 | 23 |
| BC-SKL-07029 | Substitute the initial condition to evaluate the constant of integration | 3 | 13 |
| BC-SKL-07035 | Produce the exponential solution from the model and the initial value | 3 | 17 |
| BC-SKL-01044 | Test continuity at a point by checking the three conditions | 2 | 2 |
| BC-SKL-01065 | Verify the continuity hypothesis before applying the theorem | 2 | 2 |
| BC-SKL-01067 | State the conclusion of the theorem with the correct interval | 2 | 4 |

## Machine-readable pointers [inferred]

- Edge list: `../../data/prereq_edges.csv`, columns `from,to,type,evidence_tag,note`, one row per edge, sorted by `(from, to, type)`.
- Edge sources: `../../data/staging/unit-01.edges.csv` through `../../data/staging/unit-10.edges.csv`, merged by `../../tools/merge_edges.py`, which de-duplicates on `(from, to, type)` and is the only writer of the merged file.
- Cross-unit placeholder rewriting: `../../tools/remap_edges.py`, which rewrites a BC-TOP endpoint to the BC-SKL its note names and otherwise appends `unmapped` to the note.
- Registry reverse links: `../../tools/sync_dependents.py`, which writes `../../data/staging/sync-dependents.json` for `../../tools/merge_staging.py` to merge, so `prerequisites` and `dependents` in `../../data/skills.json` stay equal to the hard edges.
- Structural report: `../../tools/graph_check.py`, which prints cycles, root skills, leaf skills, the unit dependency listing, and the fan-out ranking used above.
- Node attributes: `../../data/skills.json` under `skills`, `concepts`, and `prerequisites`; `../../data/curriculum.json` under `units` and `topics` for BC-TOP endpoints.
- Selecting hard edges only: filter `type == "hard_prerequisite"`. Selecting cross-unit edges: compare characters 8 and 9 of the two ids.
