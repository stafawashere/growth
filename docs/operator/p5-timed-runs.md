---
title: P5 timed sessions, 20 logged runs
research_date: 2026-09-24
status: measured
purpose: The 20 runs 11 P5's exit criterion names, showing no skills_state row changed during any timed session, run by Claude on the operator's delegation.
---

# P5 timed sessions: 20 logged runs [verified]

Run on 2026-09-24 by claude-opus-5-5 on the operator's delegation, not by a person. The application
was the real one (`app/main.py` `build_application` over a fresh scratch database, the worktree's
code at stage 6), served by uvicorn on localhost and driven over HTTP by a scratch script through
the same routes the client calls: register, open, start each part, save every question (answer,
visit time, mark for review, eliminated options), submit, capture each free-response question by
typed entry (the question's own worked solution, so deterministic points have something to decide),
wait for grading, and finish each mock. The one double was the passkey verifier. The AI backend
was off (`GROWTH_AI_BACKEND=none`), so model-judged points stayed provisional and only
deterministic points were decided; the full mock with the live grader and a photographed booklet
page is recorded separately in docs/operator/p5-full-mock.md. The item bank was the real one,
ingested with every check on the first query (108.3 seconds on this machine).

The measurement: every column of every skills_state row of the student (618 rows) was read
from the database file before and after each run and hashed (first 16 hex digits of a SHA-256 over
the rows in skill order); a row count compared column by column gives rows changed. The positive
control is two untimed unit checks run through the same routes, one before run 1 and one before
run 11, each of which changed the digest, so the measurement sees a change when one happens.

| control | session | digest before | digest after |
| --- | --- | --- | --- |
| 1 | unit check (`10d4779d`) | `2fbfd31cd44c5386` | `a95cfb511b7e159f` |
| 2 | unit check (`563ea7a6`) | `a95cfb511b7e159f` | `b554ca305b3885c1` |

| run | kind | multiple choice answered | attempts written | correct | diagnoses written | free-response points decided | band | skills_state before | skills_state after | rows changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | drill I-A | 26 | 26 | 17 | 26 | 0 | none (drill) | `a95cfb511b7e159f` | `a95cfb511b7e159f` | 0 |
| 2 | drill I-A | 19 | 19 | 10 | 19 | 0 | none (drill) | `a95cfb511b7e159f` | `a95cfb511b7e159f` | 0 |
| 3 | drill I-A | 29 | 29 | 17 | 29 | 0 | none (drill) | `a95cfb511b7e159f` | `a95cfb511b7e159f` | 0 |
| 4 | drill I-A | 28 | 28 | 21 | 28 | 0 | none (drill) | `a95cfb511b7e159f` | `a95cfb511b7e159f` | 0 |
| 5 | drill I-B | 4 | 4 | 3 | 4 | 0 | none (drill) | `a95cfb511b7e159f` | `a95cfb511b7e159f` | 0 |
| 6 | drill I-B | 13 | 13 | 13 | 13 | 0 | none (drill) | `a95cfb511b7e159f` | `a95cfb511b7e159f` | 0 |
| 7 | drill I-B | 13 | 13 | 6 | 13 | 0 | none (drill) | `a95cfb511b7e159f` | `a95cfb511b7e159f` | 0 |
| 8 | drill I-B | 7 | 7 | 4 | 7 | 0 | none (drill) | `a95cfb511b7e159f` | `a95cfb511b7e159f` | 0 |
| 9 | drill II-A | 0 | 2 | 0 | 2 | 2 | none (drill) | `a95cfb511b7e159f` | `a95cfb511b7e159f` | 0 |
| 10 | drill II-A | 0 | 2 | 0 | 2 | 0 | none (drill) | `a95cfb511b7e159f` | `a95cfb511b7e159f` | 0 |
| 11 | drill II-A | 0 | 2 | 0 | 2 | 4 | none (drill) | `b554ca305b3885c1` | `b554ca305b3885c1` | 0 |
| 12 | drill II-A | 0 | 2 | 0 | 2 | 0 | none (drill) | `b554ca305b3885c1` | `b554ca305b3885c1` | 0 |
| 13 | drill II-B | 0 | 4 | 0 | 4 | 5 | none (drill) | `b554ca305b3885c1` | `b554ca305b3885c1` | 0 |
| 14 | drill II-B | 0 | 4 | 0 | 4 | 15 | none (drill) | `b554ca305b3885c1` | `b554ca305b3885c1` | 0 |
| 15 | drill II-B | 0 | 4 | 0 | 4 | 3 | none (drill) | `b554ca305b3885c1` | `b554ca305b3885c1` | 0 |
| 16 | drill II-B | 0 | 4 | 0 | 4 | 18 | none (drill) | `b554ca305b3885c1` | `b554ca305b3885c1` | 0 |
| 17 | full mock | 42 | 48 | 35 | 48 | 9 | 3 to 5 | `b554ca305b3885c1` | `b554ca305b3885c1` | 0 |
| 18 | full mock | 38 | 44 | 12 | 44 | 7 | 1 to 5 | `b554ca305b3885c1` | `b554ca305b3885c1` | 0 |
| 19 | full mock | 31 | 37 | 19 | 37 | 10 | 1 to 5 | `b554ca305b3885c1` | `b554ca305b3885c1` | 0 |
| 20 | full mock | 29 | 35 | 3 | 35 | 11 | 1 to 5 | `b554ca305b3885c1` | `b554ca305b3885c1` | 0 |

Result: 20 timed runs (4 drills of each of the four parts and 4 full mocks at the documented
shape), 327 attempts graded and 327 diagnoses written by them, and
0 skills_state rows changed in any of them. The two unit-check controls each changed the
digest. The bands are wide because the model-judged free-response points stayed provisional with
the grader off, and the band covers every way a provisional point could fall.

## Runs 9 to 12 again, grader off, 2026-09-27 [verified]

Stage 13 gave the calculator free-response checks two readings they lacked: a line written with
the stem's own function names (E(t), L(t), C(t)) is read through each name's definition in the
question's `functions` record, and a setup whose limit or unknown is a numeric root is checked
against the root (`roots`, `bounds_match` with a named root, and the new `equation_setup` check).
A capital letter called like a function that the question does not define is refused, and the
point stays provisional. The four Section II Part A drills were driven again by claude-opus-5-5,
not by a person, through the real routes (`tools/frq_scenarios.py` build, `GROWTH_AI_BACKEND`
none, `GROWTH_RNG_SEED` 7, typed entry of each question's own worked solution), once on the tree
before the change and once after, both over the same six calculator questions.

| run | before: questions, decided | after: questions, decided |
| --- | --- | --- |
| 9 | 06006-01 0, 99008-01 4 | 06006-01 5, 09013-01 0 |
| 10 | 08012-01 0, 08001-01 2 | 99008-01 6, 08001-01 4 |
| 11 | 09005-01 0, 09013-01 0 | 08012-01 2, 09005-01 4 |
| 12 | 08012-01 0, 06006-01 0 | 09005-01 4, 09013-01 0 |
| total of 72 points | 6 decided, 66 provisional | 25 decided, 47 provisional |

Which questions a run draws depends on the attempts already stored, so the two columns pair
different questions per run; per question, grader off, the decided points went from 0 to 5
(06006-01), 2 to 4 (08001-01), 0 to 2 (08012-01), 0 to 4 (09005-01), 0 to 0 (09013-01) and 4
to 6 (99008-01). What stays provisional is model-required (justifications, BC-PT-99068), an
integrand-only point with a constant factor outside the integral (BC-PT-99048, 99058, 99002),
which no check reads, and every point whose eligibility waits on one of those; 09013-01 decides
its limits and setup equation but all six are gated on its three integrand points.
