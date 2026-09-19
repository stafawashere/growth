---
title: Official Sample Question Index
research_date: 2026-09-19
status: draft
purpose: One row per indexed official multiple-choice question across the three public sources, plus the sample free-response questions printed in the course and exam description with their official tags.
---

# Official Sample Question Index

Every row below resolves to a record in `../../data/mcq_records.json`. The analysis over these rows is in [mcq-analysis.md](../question-analysis/mcq-analysis.md) and the mechanism catalogue in [distractor-taxonomy.md](../question-analysis/distractor-taxonomy.md). Section and timing facts are in [exam-structure.md](../exam/exam-structure.md). Full free-response coverage across administered years is in [official-question-index.md](official-question-index.md), and the scored free-response records themselves are in `../../data/frq_records.json`.

## Indexed multiple-choice questions [verified]

Ninety-one rows: 22 from the course and exam description sample section, 24 from the standalone sample set, and 45 from the 2012 released BC practice exam. The page column is the page of the cached document, and the number column is the question number as the document prints it, which restarts for the BC half of the standalone set and which runs 1 to 28 then 76 to 92 on the 2012 exam. The unit and topic columns are the first topic each record carries; several records carry more than one. No source prints a rationale for any option, so the rationale column is `no` on every row.

The evidence column records how the question content was read. A row tagged `verified` was read from the primary text layer of the cached document. A row tagged `single-source` depends on the OCR transcription in the matching `page-NNN.ocr.txt` file, because the primary text layer dropped or garbled the stem, the options, or a key letter; OCR is a machine transcription and is not treated as a second independent source. Forty-nine rows are `verified` and 42 are `single-source`, split as 14 and 8 in the course and exam description, 2 and 22 in the standalone sample set, and 33 and 12 in the 2012 practice exam. Records whose sources list an entry ending in `#ocr` are the ones that rest on the transcription.

| Record | Source document | Page | Number | Calculator | Unit | Topic | Archetype | Correct option | Rationale available | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| BC-MCQ-CED-001 | ced | 208 | 1 | no | BC-UNIT-01 | 1.6 Determining Limits Using Algebraic Manipulation | BC-QA-01004 | D | no | verified |
| BC-MCQ-CED-002 | ced | 208 | 2 | no | BC-UNIT-02 | 2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist | BC-QA-02005 | B | no | verified |
| BC-MCQ-CED-003 | ced | 209 | 3 | no | BC-UNIT-02 | 2.8 The Product Rule | BC-QA-02009 | A | no | verified |
| BC-MCQ-CED-004 | ced | 209 | 4 | no | BC-UNIT-03 | 3.2 Implicit Differentiation | BC-QA-03004 | B | no | single-source |
| BC-MCQ-CED-005 | ced | 209 | 5 | no | BC-UNIT-04 | 4.5 Solving Related Rates Problems | BC-QA-04006 | C | no | verified |
| BC-MCQ-CED-006 | ced | 210 | 6 | no | BC-UNIT-06 | 6.3 Riemann Sums, Summation Notation, and Definite Integral Notation | BC-QA-06014 | C | no | single-source |
| BC-MCQ-CED-007 | ced | 210 | 7 | no | BC-UNIT-06 | 6.5 Interpreting the Behavior of Accumulation Functions Involving Area | BC-QA-06003 | C | no | verified |
| BC-MCQ-CED-008 | ced | 210 | 8 | no | BC-UNIT-06 | 6.9 Integrating Using Substitution | BC-QA-06008 | A | no | verified |
| BC-MCQ-CED-009 | ced | 211 | 9 | no | BC-UNIT-07 | 7.4 Reasoning Using Slope Fields | BC-QA-07002 | B | no | verified |
| BC-MCQ-CED-010 | ced | 211 | 10 | no | BC-UNIT-08 | 8.5 Finding the Area Between Curves Expressed as Functions of y | BC-QA-08009 | C | no | verified |
| BC-MCQ-CED-011 | ced | 212 | 11 | yes | BC-UNIT-01 | 1.3 Estimating Limit Values from Graphs | BC-QA-01001 | C | no | verified |
| BC-MCQ-CED-012 | ced | 212 | 12 | yes | BC-UNIT-04 | 4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration | BC-QA-04003 | C | no | verified |
| BC-MCQ-CED-013 | ced | 213 | 13 | yes | BC-UNIT-05 | 5.1 Using the Mean Value Theorem | BC-QA-05001 | D | no | single-source |
| BC-MCQ-CED-014 | ced | 213 | 14 | yes | BC-UNIT-05 | 5.6 Determining Concavity of Functions over Their Domains | BC-QA-05005 | D | no | single-source |
| BC-MCQ-CED-015 | ced | 213 | 15 | yes | BC-UNIT-08 | 8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts | BC-QA-08004 | D | no | single-source |
| BC-MCQ-CED-016 | ced | 214 | 16 | no | BC-UNIT-06 | 6.11 Integrating Using Integration by Parts | BC-QA-06009 | A | no | verified |
| BC-MCQ-CED-017 | ced | 214 | 17 | no | BC-UNIT-07 | 7.9 Logistic Models with Differential Equations | BC-QA-07009 | B | no | single-source |
| BC-MCQ-CED-018 | ced | 214 | 18 | no | BC-UNIT-09 | 9.2 Second Derivatives of Parametric Equations | BC-QA-09002 | A | no | single-source |
| BC-MCQ-CED-019 | ced | 214 | 19 | no | BC-UNIT-10 | 10.9 Determining Absolute or Conditional Convergence | BC-QA-10007 | B | no | single-source |
| BC-MCQ-CED-020 | ced | 215 | 20 | no | BC-UNIT-10 | 10.14 Finding Taylor or Maclaurin Series for a Function | BC-QA-10018 | D | no | verified |
| BC-MCQ-CED-021 | ced | 216 | 21 | yes | BC-UNIT-09 | 9.8 Find the Area of a Polar Region or the Area Bounded by a Single Polar Curve | BC-QA-09012 | A | no | verified |
| BC-MCQ-CED-022 | ced | 216 | 22 | yes | BC-UNIT-10 | 10.12 Lagrange Error Bound | BC-QA-10009 | A | no | verified |
| BC-MCQ-SAMPLE-001 | sample-questions | 5 | 1 | no | BC-UNIT-04 | 4.7 Using L’Hospital’s Rule for Determining Limits of Indeterminate Forms | BC-QA-04009 | B | no | single-source |
| BC-MCQ-SAMPLE-002 | sample-questions | 6 | 2 | no | BC-UNIT-01 | 1.6 Determining Limits Using Algebraic Manipulation | BC-QA-01004 | B | no | single-source |
| BC-MCQ-SAMPLE-003 | sample-questions | 7 | 3 | no | BC-UNIT-02 | 2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist | BC-QA-02005 | C | no | single-source |
| BC-MCQ-SAMPLE-004 | sample-questions | 8 | 4 | no | BC-UNIT-04 | 4.5 Solving Related Rates Problems | BC-QA-04006 | A | no | single-source |
| BC-MCQ-SAMPLE-005 | sample-questions | 9 | 5 | no | BC-UNIT-07 | 7.4 Reasoning Using Slope Fields | BC-QA-07002 | A | no | single-source |
| BC-MCQ-SAMPLE-006 | sample-questions | 10 | 6 | no | BC-UNIT-02 | 2.2 Defining the Derivative of a Function and Using Derivative Notation | BC-QA-02002 | B | no | single-source |
| BC-MCQ-SAMPLE-007 | sample-questions | 11 | 7 | no | BC-UNIT-06 | 6.4 The Fundamental Theorem of Calculus and Accumulation Functions | BC-QA-06012 | D | no | single-source |
| BC-MCQ-SAMPLE-008 | sample-questions | 12 | 8 | no | BC-UNIT-06 | 6.3 Riemann Sums, Summation Notation, and Definite Integral Notation | BC-QA-06014 | D | no | verified |
| BC-MCQ-SAMPLE-009 | sample-questions | 13 | 9 | no | BC-UNIT-08 | 8.1 Finding the Average Value of a Function on an Interval | BC-QA-08001 | B | no | single-source |
| BC-MCQ-SAMPLE-010 | sample-questions | 14 | 10 | no | BC-UNIT-07 | 7.8 Exponential Models with Differential Equations | BC-QA-07008 | A | no | single-source |
| BC-MCQ-SAMPLE-011 | sample-questions | 15 | 11 | yes | BC-UNIT-05 | 5.8 Sketching Graphs of Functions and Their Derivatives | BC-QA-05009 | A | no | verified |
| BC-MCQ-SAMPLE-012 | sample-questions | 17 | 12 | yes | BC-UNIT-05 | 5.3 Determining Intervals on Which a Function is Increasing or Decreasing | BC-QA-05008 | A | no | single-source |
| BC-MCQ-SAMPLE-013 | sample-questions | 18 | 13 | yes | BC-UNIT-04 | 4.1 Interpreting the Meaning of the Derivative in Context | BC-QA-04001 | D | no | single-source |
| BC-MCQ-SAMPLE-014 | sample-questions | 19 | 14 | yes | BC-UNIT-05 | 5.1 Using the Mean Value Theorem | BC-QA-05001 | C | no | single-source |
| BC-MCQ-SAMPLE-015 | sample-questions | 20 | 15 | yes | BC-UNIT-08 | 8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts | BC-QA-08004 | D | no | single-source |
| BC-MCQ-SAMPLE-016 | sample-questions | 21 | 16 | yes | BC-UNIT-08 | 8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals | BC-QA-08003 | B | no | single-source |
| BC-MCQ-SAMPLE-017 | sample-questions | 29 | 1 | no | BC-UNIT-09 | 9.1 Defining and Differentiating Parametric Equations | BC-QA-09001 | C | no | single-source |
| BC-MCQ-SAMPLE-018 | sample-questions | 30 | 2 | no | BC-UNIT-07 | 7.5 Approximating Solutions Using Euler’s Method | BC-QA-07004 | D | no | single-source |
| BC-MCQ-SAMPLE-019 | sample-questions | 31 | 3 | no | BC-UNIT-06 | 6.13 Evaluating Improper Integrals | BC-QA-06011 | C | no | single-source |
| BC-MCQ-SAMPLE-020 | sample-questions | 32 | 4 | no | BC-UNIT-10 | 10.10 Alternating Series Error Bound | BC-QA-10008 | C | no | single-source |
| BC-MCQ-SAMPLE-021 | sample-questions | 33 | 5 | no | BC-UNIT-10 | 10.11 Finding Taylor Polynomial Approximations of Functions | BC-QA-10011 | B | no | single-source |
| BC-MCQ-SAMPLE-022 | sample-questions | 34 | 6 | no | BC-UNIT-10 | 10.9 Determining Absolute or Conditional Convergence | BC-QA-10007 | B | no | single-source |
| BC-MCQ-SAMPLE-023 | sample-questions | 35 | 7 | yes | BC-UNIT-09 | 9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions | BC-QA-09007 | A | no | single-source |
| BC-MCQ-SAMPLE-024 | sample-questions | 36 | 8 | yes | BC-UNIT-10 | 10.4 Integral Test for Convergence | BC-QA-10005 | C | no | single-source |
| BC-MCQ-PE2012-001 | practice-exam-2012 | 22 | 1 | no | BC-UNIT-03 | 3.1 The Chain Rule | BC-QA-03001 | E | no | verified |
| BC-MCQ-PE2012-002 | practice-exam-2012 | 22 | 2 | no | BC-UNIT-09 | 9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions | BC-QA-09001 | A | no | verified |
| BC-MCQ-PE2012-003 | practice-exam-2012 | 23 | 3 | no | BC-UNIT-06 | 6.6 Applying Properties of Definite Integrals | BC-QA-06004 | B | no | verified |
| BC-MCQ-PE2012-004 | practice-exam-2012 | 24 | 4 | no | BC-UNIT-08 | 8.13 The Arc Length of a Smooth, Planar Curve and Distance Traveled | BC-QA-08014 | A | no | verified |
| BC-MCQ-PE2012-005 | practice-exam-2012 | 24 | 5 | no | BC-UNIT-10 | 10.2 Working with Geometric Series | BC-QA-10003 | C | no | verified |
| BC-MCQ-PE2012-006 | practice-exam-2012 | 25 | 6 | no | BC-UNIT-06 | 6.9 Integrating Using Substitution | BC-QA-06008 | C | no | verified |
| BC-MCQ-PE2012-007 | practice-exam-2012 | 25 | 7 | no | BC-UNIT-03 | 3.4 Differentiating Inverse Trigonometric Functions | BC-QA-03007 | A | no | verified |
| BC-MCQ-PE2012-008 | practice-exam-2012 | 26 | 8 | no | BC-UNIT-06 | 6.2 Approximating Areas with Riemann Sums | BC-QA-06001 | C | no | verified |
| BC-MCQ-PE2012-009 | practice-exam-2012 | 26 | 9 | no | BC-UNIT-10 | 10.8 Ratio Test for Convergence | BC-QA-10001 | D | no | verified |
| BC-MCQ-PE2012-010 | practice-exam-2012 | 27 | 10 | no | BC-UNIT-06 | 6.7 The Fundamental Theorem of Calculus and Definite Integrals | BC-QA-06008 | E | no | single-source |
| BC-MCQ-PE2012-011 | practice-exam-2012 | 27 | 11 | no | BC-UNIT-02 | 2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist | BC-QA-02005 | A | no | verified |
| BC-MCQ-PE2012-012 | practice-exam-2012 | 28 | 12 | no | BC-UNIT-07 | 7.2 Verifying Solutions for Differential Equations | BC-QA-07010 | C | no | verified |
| BC-MCQ-PE2012-013 | practice-exam-2012 | 28 | 13 | no | BC-UNIT-10 | 10.13 Radius and Interval of Convergence of Power Series | BC-QA-10014 | C | no | verified |
| BC-MCQ-PE2012-014 | practice-exam-2012 | 29 | 14 | no | BC-UNIT-07 | 7.9 Logistic Models with Differential Equations | BC-QA-07009 | E | no | verified |
| BC-MCQ-PE2012-015 | practice-exam-2012 | 30 | 15 | no | BC-UNIT-06 | 6.4 The Fundamental Theorem of Calculus and Accumulation Functions | BC-QA-06003 | A | no | single-source |
| BC-MCQ-PE2012-016 | practice-exam-2012 | 31 | 16 | no | BC-UNIT-07 | 7.5 Approximating Solutions Using Euler’s Method | BC-QA-07004 | C | no | verified |
| BC-MCQ-PE2012-017 | practice-exam-2012 | 31 | 17 | no | BC-UNIT-10 | 10.14 Finding Taylor or Maclaurin Series for a Function | BC-QA-10017 | C | no | verified |
| BC-MCQ-PE2012-018 | practice-exam-2012 | 32 | 18 | no | BC-UNIT-06 | 6.7 The Fundamental Theorem of Calculus and Definite Integrals | BC-QA-06003 | A | no | single-source |
| BC-MCQ-PE2012-019 | practice-exam-2012 | 33 | 19 | no | BC-UNIT-02 | 2.9 The Quotient Rule | BC-QA-02011 | C | no | verified |
| BC-MCQ-PE2012-020 | practice-exam-2012 | 33 | 20 | no | BC-UNIT-06 | 6.12 Integrating Using Linear Partial Fractions | BC-QA-06010 | C | no | verified |
| BC-MCQ-PE2012-021 | practice-exam-2012 | 34 | 21 | no | BC-UNIT-01 | 1.15 Connecting Limits at Infinity and Horizontal Asymptotes | BC-QA-01010 | E | no | single-source |
| BC-MCQ-PE2012-022 | practice-exam-2012 | 34 | 22 | no | BC-UNIT-10 | 10.13 Radius and Interval of Convergence of Power Series | BC-QA-10013 | D | no | verified |
| BC-MCQ-PE2012-023 | practice-exam-2012 | 35 | 23 | no | BC-UNIT-07 | 7.1 Modeling Situations with Differential Equations | BC-QA-07006 | A | no | verified |
| BC-MCQ-PE2012-024 | practice-exam-2012 | 35 | 24 | no | BC-UNIT-06 | 6.11 Integrating Using Integration by Parts | BC-QA-06009 | E | no | verified |
| BC-MCQ-PE2012-025 | practice-exam-2012 | 36 | 25 | no | BC-UNIT-06 | 6.13 Evaluating Improper Integrals | BC-QA-06011 | B | no | verified |
| BC-MCQ-PE2012-026 | practice-exam-2012 | 37 | 26 | no | BC-UNIT-09 | 9.7 Defining Polar Coordinates and Differentiating in Polar Form | BC-QA-09009 | B | no | verified |
| BC-MCQ-PE2012-027 | practice-exam-2012 | 38 | 27 | no | BC-UNIT-10 | 10.5 Harmonic Series and p-Series | BC-QA-10004 | C | no | verified |
| BC-MCQ-PE2012-028 | practice-exam-2012 | 39 | 28 | no | BC-UNIT-04 | 4.7 Using L’Hospital’s Rule for Determining Limits of Indeterminate Forms | BC-QA-04009 | D | no | verified |
| BC-MCQ-PE2012-029 | practice-exam-2012 | 41 | 76 | yes | BC-UNIT-02 | 2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist | BC-QA-05009 | B | no | verified |
| BC-MCQ-PE2012-030 | practice-exam-2012 | 41 | 77 | yes | BC-UNIT-05 | 5.3 Determining Intervals on Which a Function is Increasing or Decreasing | BC-QA-05008 | B | no | verified |
| BC-MCQ-PE2012-031 | practice-exam-2012 | 42 | 78 | yes | BC-UNIT-06 | 6.6 Applying Properties of Definite Integrals | BC-QA-06013 | C | no | single-source |
| BC-MCQ-PE2012-032 | practice-exam-2012 | 42 | 79 | yes | BC-UNIT-10 | 10.11 Finding Taylor Polynomial Approximations of Functions | BC-QA-10010 | E | no | single-source |
| BC-MCQ-PE2012-033 | practice-exam-2012 | 43 | 80 | yes | BC-UNIT-05 | 5.9 Connecting a Function, Its First Derivative, and Its Second Derivative | BC-QA-05009 | E | no | verified |
| BC-MCQ-PE2012-034 | practice-exam-2012 | 44 | 81 | yes | BC-UNIT-05 | 5.6 Determining Concavity of Functions over Their Domains | BC-QA-05005 | D | no | verified |
| BC-MCQ-PE2012-035 | practice-exam-2012 | 44 | 82 | yes | BC-UNIT-08 | 8.1 Finding the Average Value of a Function on an Interval | BC-QA-08001 | C | no | single-source |
| BC-MCQ-PE2012-036 | practice-exam-2012 | 45 | 83 | yes | BC-UNIT-01 | 1.11 Defining Continuity at a Point | BC-QA-01006 | C | no | verified |
| BC-MCQ-PE2012-037 | practice-exam-2012 | 45 | 84 | yes | BC-UNIT-05 | 5.6 Determining Concavity of Functions over Their Domains | BC-QA-05004 | D | no | single-source |
| BC-MCQ-PE2012-038 | practice-exam-2012 | 46 | 85 | yes | BC-UNIT-04 | 4.5 Solving Related Rates Problems | BC-QA-04006 | B | no | single-source |
| BC-MCQ-PE2012-039 | practice-exam-2012 | 47 | 86 | yes | BC-UNIT-06 | 6.7 The Fundamental Theorem of Calculus and Definite Integrals | BC-QA-06003 | B | no | verified |
| BC-MCQ-PE2012-040 | practice-exam-2012 | 48 | 87 | yes | BC-UNIT-08 | 8.7 Volumes with Cross Sections: Squares and Rectangles | BC-QA-08011 | B | no | single-source |
| BC-MCQ-PE2012-041 | practice-exam-2012 | 49 | 88 | yes | BC-UNIT-05 | 5.8 Sketching Graphs of Functions and Their Derivatives | BC-QA-05009 | E | no | verified |
| BC-MCQ-PE2012-042 | practice-exam-2012 | 50 | 89 | yes | BC-UNIT-08 | 8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals | BC-QA-08003 | E | no | single-source |
| BC-MCQ-PE2012-043 | practice-exam-2012 | 50 | 90 | yes | BC-UNIT-10 | 10.6 Comparison Tests for Convergence | BC-QA-10004 | E | no | verified |
| BC-MCQ-PE2012-044 | practice-exam-2012 | 51 | 91 | yes | BC-UNIT-09 | 9.9 Finding the Area of the Region Bounded by Two Polar Curves | BC-QA-09013 | D | no | single-source |
| BC-MCQ-PE2012-045 | practice-exam-2012 | 52 | 92 | yes | BC-UNIT-05 | 5.9 Connecting a Function, Its First Derivative, and Its Second Derivative | BC-QA-05009 | B | no | verified |

## Sample free-response questions in the course and exam description [verified]

The same sample section prints four free-response questions with scoring guidelines, tagged in the answer key table on `ced:221` with lists of practice skills, lists of learning objectives, and the units involved. These are illustrative questions rather than administered ones, so they are not scored-FRQ records; scored free-response parts from administered examinations live in `../../data/frq_records.json` with one record per scored free-response part.

| Question | Part | Calculator | Practice skills | Learning objectives | Units | Question page | Scoring guideline pages |
|---|---|---|---|---|---|---|---|
| 1 | Part A, AB or BC | yes | 1.D, 1.E, 2.B, 3.F | CHA-2.D, CHA-3.A, CHA-3.C, CHA-3.F, CHA-4.B, LIM-5.A | 2, 4, 6, 8 | `ced:217` | `ced:222` to `ced:223` |
| 2 | Part B, AB or BC | no | 1.C, 1.E, 2.B, 2.E, 3.B, 3.E | FUN-3.B, FUN-4.A, FUN-5.A, FUN-6.D | 2, 5, 6 | `ced:218` | `ced:224` to `ced:225` |
| 3 | Part A, BC only | yes | 1.C, 1.D, 1.E, 2.B | CHA-3.G, FUN-8.B | 9 | `ced:219` | `ced:226` to `ced:227` |
| 4 | Part B, BC only | no | 1.D, 1.E, 3.B, 3.D, 3.E | LIM-7.A, LIM-7.B, LIM-8.D, LIM-8.G | 10 | `ced:220` | `ced:228` to `ced:229` |

The practice skill codes in that table map onto BC-MPS ids by removing the dot, so 1.D is BC-MPS-1D and 3.F is BC-MPS-3F. The learning objective codes map onto BC-LO ids the same way, so CHA-3.G is BC-LO-CHA-3G. Questions 1 and 2 are the ones both AB and BC candidates would answer; questions 3 and 4 cover BC-only content, which the tags place in BC-UNIT-09 and BC-UNIT-10.

## Source registry entries [verified]

| Source id | Document | Tier | Cached pages used |
|---|---|---|---|
| BC-SRC-ced | Course and exam description | live | 202 to 230 |
| BC-SRC-sample-questions | Sample questions, AP Calculus AB and BC exams | live | 1 to 45 |
| BC-SRC-practice-exam-2012 | Calculus BC practice exam from the 2012 administration | live | 1 to 85, excluding the quarantined pages |

The 2012 document lists pages 12, 18, 70, 80, and 84 as quarantined in `../../cache/quarantine.json`. None of them falls in the multiple-choice question range, which runs from page 21 to page 52, or on the answer key pages 71 and 72, so no indexed row depends on a quarantined page. Full source metadata is in [source-registry.md](../evidence/source-registry.md).
