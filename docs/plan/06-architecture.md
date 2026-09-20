---
title: Architecture
research_date: 2026-09-19
status: draft
purpose: Fix the runtime shape of the adaptive AP Calculus BC tutor, name every component and table, and tie each one to the learning mechanic it exists to serve.
---

# Architecture

This document describes the system that runs the mechanics in `01-learning-model.md` under the rules in `02-adaptive-engine.md`. It is a planning document and contains no application code.

Every number carries its source URL or repository path and an evidence tag; numbers that follow from a decision rather than a source are tagged `[inferred]` and listed as tunables in `12-open-questions.md`. Unknown means unknown. The stack decision is D7 and is not reopened here; what this document adds is why each piece exists, what was rejected, and the seam at which each piece can be replaced.

## System diagram

The deployment is one machine, either the student's laptop or a small VPS the operator controls. The boundaries drawn are process boundaries chosen so that a later split onto two hosts changes configuration rather than code.

```
                        +------------------------------------------+
                        |            Browser client                |
                        |  React 18 + TypeScript + Vite            |
                        |  KaTeX render, MathLive input,           |
                        |  camera capture, SSE consumer            |
                        +---------------------+--------------------+
                                              |
                              HTTPS / HTTP on localhost
                              REST (JSON) + SSE (text/event-stream)
                                              |
      +---------------------------------------v----------------------------------------+
      |                          FastAPI application process                            |
      |                                                                                 |
      |  +------------------+   +------------------+   +--------------------------+     |
      |  |   API layer      |   |  Session loop    |   |   SSE hub                |     |
      |  |  routers, auth,  |-->|  orchestration   |-->|  per-connection queues,  |     |
      |  |  rate limits     |   |                  |   |  heartbeat, replay id    |     |
      |  +--------+---------+   +---------+--------+   +------------+-------------+     |
      |           |                       |                         |                   |
      |           v                       v                         |                   |
      |  +------------------+   +-------------------+               |                   |
      |  |  Engine          |   |  Grader           |               |                   |
      |  |  PFA + FSRS-7    |   |  per scoring      |               |                   |
      |  |  state, fringe,  |   |  point (BC-PT),   |               |                   |
      |  |  selection,      |   |  SymPy pre-checks |               |                   |
      |  |  interleave      |   +---------+---------+               |                   |
      |  +--------+---------+             |                         |                   |
      |           |                       v                         |                   |
      |           |             +-------------------+               |                   |
      |           |             |  Verifier         |               |                   |
      |           |             |  SymPy equivalence|               |                   |
      |           |             |  numeric probes,  |               |                   |
      |           |             |  Monte Carlo over |               |                   |
      |           |             |  parameter family |               |                   |
      |           |             +---------+---------+               |                   |
      |           |                       |                         |                   |
      |           v                       v                         |                   |
      |  +-------------------------------------------------+        |                   |
      |  |            Provider layer (07)                   |--------+                   |
      |  |  role router, fallback chain, budget guard,      |                            |
      |  |  prompt cache prefixes, usage accounting         |                            |
      |  +----+----------+----------+----------+------------+                            |
      |       |          |          |          |                                         |
      +-------|----------|----------|----------|-----------------------------------------+
              |          |          |          |
              v          v          v          v
        Anthropic   Gemini     OpenAI /    Ollama (optional, local)
        (default)   (tier 2)   OpenRouter  claudebox (off by default, 07)
              ^
              |
      +-------+------------------------------------------------------------------------+
      |                     Job worker process (single worker)                          |
      |  polls the jobs table, leases a row, runs one of:                                |
      |  generate | verify | monte_carlo | grade_batch | diagnose | snapshot_reload      |
      +--------------------------------+------------------------------------------------+
                                       |
      +--------------------------------v------------------------------------------------+
      |                          SQLite (SQLAlchemy)                                     |
      |  users, provider_configs, content_snapshots, skills_state, items,                |
      |  item_verifications, sessions, attempts, gradings, diagnoses,                    |
      |  review_queue, jobs, budgets, audit_log                                          |
      +---------------------------------------------------------------------------------+

      +---------------------------------------------------------------------------------+
      |             Content snapshot (immutable, in memory, loaded at startup)           |
      |  read-only projection of data/*.json and data/prereq_edges.csv,                  |
      |  validated against schemas/, keyed by BC-* IDs, versioned in content_snapshots   |
      +---------------------------------------------------------------------------------+
```

Three choices in that picture are deliberate. The engine, grader and verifier sit in one process with the provider layer rather than as services, because a wrong mastery update and a wrong scoring decision are the two failures that damage learning directly and both are cheaper to test when one test process can build a state, select, grade a synthetic response and assert the result without a network hop. The job worker is a separate process on the same SQLite file, because slow bursty generation must never make the student's next item wait, and it is a single worker because a second worker on one file buys throughput this workload does not need and costs a class of lease races. The content snapshot is not a content table; it is an immutable in-memory graph built at startup, with only its identity and version recorded in `content_snapshots`. Mastery rows store library IDs as strings and the graph gives those strings meaning.

## Stack decision with alternatives considered

The choice is D7: Python 3.12 with FastAPI on the server holding engine, grader, verifier, content loader and provider layer; React 18 with TypeScript and Vite on the client with KaTeX for rendering and MathLive for typed math input; SQLite through SQLAlchemy; a single job worker over a SQLite job table; SSE for streaming.

The ranking criterion is learning impact first, then cost, then convenience, and that ordering is what decides this table rather than developer taste.

| Criterion | D7: Python engine + React client | All TypeScript with a Python sidecar for SymPy | All Python with HTMX, no build step | All TypeScript, no symbolic checker |
| --- | --- | --- | --- | --- |
| Correctness of the verifier | SymPy in process with the verifier; symbolic equivalence, numeric probing and Monte Carlo over a parameter family all run against the same expression objects | Same SymPy, but every check is an RPC with a serialisation boundary where expressions become strings and get re-parsed | Same as D7 | No symbolic equivalence available; key checking falls back to numeric sampling and model agreement, which is exactly what track 3 says is insufficient |
| Learning-critical fit | Engine, grader and verifier are one testable unit; a mastery invariant and a scoring rule are asserted in one test | Engine in TypeScript, checker in Python; invariants that span both need integration tests to state at all | Good on the server; weak at the input surface, see below | Poor; the fidelity of generated items becomes model-trust |
| Math input ergonomics | MathLive is a web component with MathJSON export, which the verifier consumes as structure rather than as a display string. https://www.npmjs.com/package/mathlive [verified] | Same | HTMX has no natural home for a stateful web component that owns a virtual keyboard and a caret model; this is the reason to reject it | Same as D7 |
| Complexity | Two processes in development, two languages | Two processes and two languages, plus an RPC protocol that has to be versioned | One process, one language | One process, one language |
| Cost | No added provider cost; the deterministic checks are free compute and displace paid model calls | Same | Same | Higher: without SymPy, more verification falls to a second model call per item |
| Testability | Engine invariants from `10-quality-and-evaluation.md` run as plain unit tests against the real `data/` directory | Split across two runners | Good server side | Weakest |
| Migration cost | SQLAlchemy to Postgres; SQLite job table to Redis; both are named seams | Same database story, worse code story | Same database story | Same |

The choice follows from the first two rows. The verifier decides whether a generated item is safe to show a student, and track 3 is explicit that model agreement alone is not enough: solver-assisted architectures "substantially outperform" direct prediction on equation work (https://arxiv.org/pdf/2601.01774 [single-source]), and the recommended pipeline is independent re-solve plus SymPy equivalence plus numeric evaluation plus Monte Carlo over the parameter family, publishing only on unanimous agreement. That pipeline wants to live where SymPy lives, and `tools/` already reads `data/*.json` in Python.

What D7 trades away: one extra process and one extra language, so a change spanning the session loop and the session screen touches two toolchains; the single-language type sharing an all-TypeScript stack would give between API responses and the client, so the API contract is maintained deliberately rather than inherited; and the option of one static bundle.

All-Python with HTMX was rejected on learning impact. Typed math entry is secondary but load-bearing (D6: MathLive with MathJSON export for numeric answers, short answers and accessibility), and MathLive is a web component that wants a real client runtime. A weak input surface changes what the student is willing to enter, which changes what the engine can observe, which degrades the mastery estimate.

All-TypeScript with a Python sidecar was rejected on testability: it ends at two processes anyway, paying D7's cost without its benefit, and it puts engine invariants and verifier checks on opposite sides of an RPC.

SQLite rather than Postgres is a cost decision, not a learning one, and it is reversible through SQLAlchemy; the phase 8 migration in `11-phased-delivery.md` moves the same models. The requirement SQLite must meet is durability of attempts and mastery state across a crash, which write-ahead logging satisfies at this scale.

## Data model

One table per entity. Types are given in SQLite terms. Every table has `created_at` and `updated_at` as ISO 8601 text unless noted. The right-hand column names the plan document that owns the semantics of the table, meaning the document that gets to change the meaning of the fields; this document owns only their storage.

Library IDs are stored as TEXT holding the literal BC-* string (`BC-SKL-06017`, `BC-QA-06001`, `BC-PT-99007`, and so on, per `research/README.md`). They are never foreign keys to a content table, because content lives in the immutable snapshot, not in the database. Every write path that accepts a library ID validates it against the loaded snapshot first and rejects an ID the snapshot does not know. Every read path that resolves an ID and finds it retired consults the tombstone in `data/ids.json` and follows `superseded_by`. This is the single mechanism by which a library update and a student's history stay reconciled, and it is specified in the content loader section below.

### users

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | opaque |
| display_name | TEXT | |
| exam_date | TEXT | ISO date. Default 2027-05-10, Monday 10 May 2027, from `research/exam/exam-structure.md` [single-source] (the stored value is whatever the exam registry says, not a constant in code) (R19) |
| created_at | TEXT | |
| purge_after | TEXT | ISO date, default exam_date plus 30 days, owned by `09-security-and-privacy.md` |

Semantics owned by `09-security-and-privacy.md`. The single-user invariant lives here: the claudebox adapter in `07-ai-provider-layer.md` refuses to start when this table holds more than one row.

### provider_configs

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| user_id | TEXT | |
| provider | TEXT | anthropic, openai, gemini, openrouter, ollama, claudebox |
| enabled | INTEGER | 0 or 1; claudebox defaults to 0 |
| key_ciphertext | BLOB | libsodium secretbox output, passphrase-derived key |
| key_nonce | BLOB | |
| base_url | TEXT nullable | for ollama and claudebox |
| model_map | TEXT (JSON) | role to model id |
| options | TEXT (JSON) | provider-specific passthrough |
| last_verified_at | TEXT nullable | last successful call |

Semantics owned by `07-ai-provider-layer.md`. Storage rule: the plaintext key exists only inside a request-scoped buffer and is never written to any other table, log line or URL.

### content_snapshots

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| loaded_at | TEXT | |
| library_commit | TEXT nullable | if the library is under version control at load time |
| digest | TEXT | hash over the concatenated registry files and `prereq_edges.csv` |
| counts | TEXT (JSON) | active skills, concepts, prerequisites, edges by type, archetypes, variants, families, errors, misconceptions, signals, scoring points |
| status | TEXT | loading, active, superseded, rejected |
| rejection_reason | TEXT nullable | cycle or dangling ID detail |

Owned by this document. The counts recorded on a healthy load of the current library are 541 active BC-SKL, 170 BC-CON, 77 BC-PRQ, 1226 edges (602 hard_prerequisite, 622 supporting, 2 co_requisite, 0 cycles), 139 active BC-QA in 77 families, 395 BC-QV, 76 BC-PT, 390 active BC-ERR, 213 active BC-MIS, 711 BC-SIG, 249 FRQ parts and 91 MCQ records, all computed from `data/` on 2026-09-19 and recorded in the repository facts sheet [verified, `data/`].

### skills_state

One row per user per BC-SKL and one per BC-PRQ, seeded in full at account creation (R27). At current library size that is 541 plus 77, so 618 rows per user, in every phase including P1. The 54-skill P1 subgraph is a test fixture and a selection scope, never a row count: `tests/fixtures/graph_p1.json` is what the engine unit tests range over, while the live table holds all 618 rows from the first login. BC-TOP ids get no row at all, per R13.

| Field | Type | Notes |
| --- | --- | --- |
| user_id | TEXT | part of primary key |
| skill_id | TEXT | part of primary key, a BC-SKL or BC-PRQ string (R27) |
| snapshot_id | TEXT | the snapshot this row was last reconciled against |
| beta | REAL | declared difficulty logit, not learned |
| credited_successes | REAL | c_k, fractional because propagation credits fractions |
| credited_failures | REAL | f_k |
| stability | REAL | FSRS S_k |
| difficulty | REAL | FSRS D_k |
| last_practised_at | TEXT nullable | |
| fading_stage | TEXT | example, completion, unsupported |
| observation_count | INTEGER | |
| distinct_archetypes_succeeded | TEXT (JSON array) | BC-QA strings |
| success_days | TEXT (JSON array) | ISO dates |
| mastered | INTEGER | 0 or 1 |
| mastered_at | TEXT nullable | |
| hypercorrection_due | TEXT nullable | ISO date, set to tomorrow by a high-confidence error (R19) |
| consecutive_successes | INTEGER | credited successes in a row at the current fading stage (R19, R7) |
| consecutive_failures | INTEGER | credited failures in a row at the current fading stage (R19, R7) |
| concept_opener_done | INTEGER | 0 or 1, set on the concept's first skill once the productive-failure opener has been served (R19, R5) |

Rows are written at account creation, not lazily on first observation, because the seeded assumed-mastered parents need a stored state before the first selection runs. All 77 BC-PRQ rows are inserted mastered, per invariant 19. Per R15 the 19 BC-PRQ and 6 BC-SKL parents that the P1 subgraph actually depends on are inserted with `beta` 0.0, `credited_successes` and `credited_failures` 0, `stability` and `difficulty` null, `fading_stage` unsupported, and `mastered` 1 with `mastered_at` set to the account creation timestamp; they are flipped to 0 only by a diagnosed gap or a credited failure. The 4 BC-TOP parents get no row at all, because they are inert per R13.

Semantics owned by `02-adaptive-engine.md`. This document owns only the shape: every field in D2's state vector has a column, including the four added by R19 and R5 above, nothing is recomputed from an event log at read time, and the event log in `attempts` remains the source of truth for a rebuild.

### pending_probes

The discriminating probe the diagnostician recommends is a queue on the user rather than a field on a session, because every selection function drains it before its own scoring (R6).

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| user_id | TEXT | |
| archetype_id | TEXT | BC-QA string, the recommended probe |
| diagnosis_id | TEXT | the diagnosis that raised it |
| enqueued_at | TEXT | ISO timestamp |
| expires_at | TEXT | enqueued_at plus 7 days (R6) [inferred] |
| served_at | TEXT nullable | set when a selection function drains the entry |

Semantics owned by `02-adaptive-engine.md`. The queue holds at most 3 unserved entries per user and drops the oldest when a fourth arrives, and an entry past `expires_at` is never served (R6) [inferred]. Both the cap and the expiry are tunables in `12-open-questions.md`.

### items

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | app-minted, not a library ID |
| archetype_id | TEXT | BC-QA string |
| variant_id | TEXT nullable | BC-QV string |
| snapshot_id | TEXT | the snapshot the archetype was read from |
| parameter_draw | TEXT (JSON) | the substituted values |
| stem | TEXT | generated, never official text |
| figure_spec | TEXT (JSON) nullable | declarative, rendered client side |
| options | TEXT (JSON) nullable | MCQ options. Each option object carries `error_path`, which is a BC-ERR id or null (R26). The key's `error_path` is null; every distractor's is a BC-ERR id. In P1 the operator records it when authoring the 130 items, and from P4 the generator emits it as `generating_error_path`. `archetypes.common_distractors` is prose and is the operator's authoring guide, never machine input |
| answer_key | TEXT (JSON) | |
| worked_solution | TEXT (JSON) | steps tagged to BC-PT ids |
| calculator_status | TEXT | no_calculator, either, calculator |
| representation | TEXT | BC-REP string |
| difficulty_settings | TEXT (JSON) | per BC-DF |
| skills | TEXT (JSON array) | BC-SKL strings |
| provenance | TEXT (JSON) | keys `model`, `prompt_template_version`, `generation_job_id`, and for hand-authored items the authoring date and the archetype and variant ids. A P1 item sets `model` to the string `"operator"` and the other two to null (R30); there is no separate `provenance` string key |
| status | TEXT | draft, verified, rejected, retired |
| dedupe_minhash | TEXT | signature for the 5-gram MinHash gate |
| dedupe_embedding | BLOB nullable | for the cosine gate |

Semantics owned by `04-item-generation.md`.

### item_verifications

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| item_id | TEXT | |
| check_type | TEXT | independent_resolve, sympy_equivalence, numeric_probe, monte_carlo, distractor_distinct, calculator_boundary, dedupe_minhash, dedupe_embedding |
| outcome | TEXT | pass, fail, indeterminate |
| detail | TEXT (JSON) | e.g. failing parameter tuples, the count of draws, the Jaccard or cosine value |
| model_id | TEXT nullable | for independent_resolve |
| created_at | TEXT | |

Semantics owned by `04-item-generation.md`. The `indeterminate` outcome exists because SymPy equivalence is undecidable in general and returns unevaluated results on some expressions (track 3, section 5 [inferred]); an indeterminate symbolic check does not pass an item, it routes it to `review_queue`.

### sessions

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| user_id | TEXT | |
| mode | TEXT | diagnostic, learning, review, rehearsal |
| sub_mode | TEXT nullable | unit_check, timed_part_a1, timed_part_a2, timed_frq_a, timed_frq_b, full_mock |
| started_at, ended_at | TEXT | |
| queue | TEXT (JSON) | ordered item ids with the interleaving constraints recorded as satisfied |
| updates_mastery | INTEGER | 0 for rehearsal, per D6 |
| snapshot_id | TEXT | |

Semantics owned by `05-assessment-modes.md`. The `queue` column records the four blocks of the session-assembly rule in `02-adaptive-engine.md` (Session assembly) and the minute forecast computed for each, so a later reader can see what was assembled and what the student actually reached (R5).

### judgments

Metacognitive judgments of learning are collected in block 4 and had no storage before (review finding B3). One row per judgment.

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| user_id | TEXT | |
| session_id | TEXT | the session whose block 4 collected it |
| scope | TEXT | skill or concept |
| scope_id | TEXT | BC-SKL or BC-CON string |
| predicted_retention | REAL | the student's judgment, 0 to 1 |
| made_at | TEXT | ISO timestamp |
| outcome_attempt_id | TEXT nullable | the later attempt the judgment is scored against |
| outcome_correct | INTEGER nullable | filled when that attempt resolves |

Semantics owned by `01-learning-model.md` for the mechanic and `02-adaptive-engine.md` for when block 4 asks. The judgment never enters credit assignment; it exists so the calibration curve in `08-design-brief.md` has a source and so `10-quality-and-evaluation.md` can score it.

### attempts

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| session_id | TEXT | |
| item_id | TEXT | |
| started_at, submitted_at | TEXT | |
| response | TEXT (JSON) | MathJSON for typed input, option id for MCQ, image ids for photo capture |
| confidence | TEXT | guess, unsure, confident |
| elapsed_ms | INTEGER | |
| image_ids | TEXT (JSON array) nullable | |
| transcription | TEXT (JSON) nullable | model read-back |
| transcription_confirmed | INTEGER | 0 until the student confirms or corrects |
| correct | INTEGER nullable | deterministic for MCQ |
| served_stage | TEXT | example, completion, unsupported: the fading stage this attempt was actually served at (R27) |
| format | TEXT | mcq or short_answer (R27) |
| per_skill_states | TEXT (JSON) | the `mastery_state` assigned to each skill the item loaded, as an object keyed by BC-SKL string (R27) |
| error_note | TEXT nullable | the student's one-line error note (03) |
| self_explanation | TEXT nullable | the answer to the structured self-explanation prompt |
| snapshot_id | TEXT | the content snapshot the item was served under, so an attempt can be reinterpreted after a library update (P1 convention 2 in 11) |

Semantics owned by `03-diagnosis-and-feedback.md` for the confidence and feedback fields, `05-assessment-modes.md` for capture. The `transcription_confirmed` gate is a hard precondition on grading: no point is graded until it is 1, because the 2026 AIED study found roughly 87 percent of residual grading errors were transcription failures rather than rubric misapplication (https://arxiv.org/abs/2605.19043 [single-source]).

### gradings

One row per scoring point per attempt, not one row per attempt.

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| attempt_id | TEXT | |
| point_type_id | TEXT | BC-PT string |
| decided_by | TEXT | deterministic, model, escalated |
| earned | INTEGER nullable | null while escalated |
| samples | TEXT (JSON) | the 2 temperature-0 samples plus the strictness-varied sample |
| agreement | TEXT | unanimous, split |
| provisional | INTEGER | 1 while split or escalated |
| rationale | TEXT | the rule named and the scoring consequence |
| deterministic_check | TEXT (JSON) nullable | SymPy or numeric result that decided a mechanical point |

Semantics owned by `03-diagnosis-and-feedback.md`. The three-sample shape and the escalate-never-average rule are D4 and rest on track 3: best reported kappa 0.56 and question-level exact agreement at most 0.22 (https://arxiv.org/pdf/2603.00451 and https://arxiv.org/html/2607.01247, both [single-source]).

### diagnoses

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| attempt_id | TEXT | |
| observed_errors | TEXT (JSON) | BC-ERR ids or candidate text |
| misconception_hypotheses | TEXT (JSON) | BC-MIS id with probability, never a single cause at 1.0 |
| non_conceptual_causes | TEXT (JSON) | |
| prerequisite_gap | TEXT nullable | the named BC-SKL or BC-PRQ |
| mastery_states | TEXT (JSON) | one enum value per skill the item loaded |
| matched_signal | TEXT nullable | BC-SIG id when the output matched a signal record |
| probe_scheduled | TEXT nullable | the discriminating probe archetype, when the top two hypotheses are within 0.2 |

Semantics owned by `03-diagnosis-and-feedback.md`. The mastery_states values come from the controlled vocabulary in `research/README.md`: mastered, partial_procedural, partial_conceptual, partial_unspecified, prerequisite_gap, notation_only, not_mastered, not_attempted.

### review_queue

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| kind | TEXT | item_audit, item_verification_disagreement, grading_split, dispute, duplicate_gate_hit, transcription_rejected. `item_audit` is the operator's hand-audit verdict on a published item and is the only kind P1 writes (R27); the other five need `gradings` or `diagnoses` and arrive with those tables |
| ref_id | TEXT | item id, grading id or attempt id |
| opened_at, resolved_at | TEXT | |
| resolution | TEXT nullable | |
| visible_to_student | INTEGER | 1 for a dispute the student raised |

Semantics owned by `03-diagnosis-and-feedback.md` and `04-item-generation.md`.

### jobs

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| type | TEXT | generate, verify, monte_carlo, grade_batch, diagnose, snapshot_reload |
| payload | TEXT (JSON) | |
| idempotency_key | TEXT unique | |
| state | TEXT | queued, leased, done, failed, dead |
| attempts_made | INTEGER | |
| lease_expires_at | TEXT nullable | |
| not_before | TEXT | for backoff |
| last_error | TEXT nullable | |
| priority | INTEGER | lower runs first |

Owned by this document.

### budgets

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| user_id | TEXT | |
| role | TEXT | tutor, generator, verifier, grader, diagnostician, transcriber |
| day | TEXT | ISO date |
| tokens_in, tokens_out, tokens_cached_read, tokens_cached_write | INTEGER | |
| cost_usd | REAL | |
| cap_tokens, cap_usd | REAL | |
| hard_stopped | INTEGER | |

Semantics owned by `07-ai-provider-layer.md`.

### audit_log

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT primary key | |
| at | TEXT | |
| actor | TEXT | user id, worker, system |
| action | TEXT | controlled vocabulary |
| subject | TEXT | table and row id |
| detail | TEXT (JSON) | never contains a key, a passphrase or a raw provider response body |

Semantics owned by `09-security-and-privacy.md`.

## API surface

REST for everything with a request and a response. SSE for the two things that are genuinely progressive, namely tutor text and grading progress. Auth is a passkey-backed session cookie unless noted; `09-security-and-privacy.md` owns the auth mechanism. The role or job column says what the request causes behind the API.

| Method | Path | Purpose | Auth | Triggers |
| --- | --- | --- | --- | --- |
| POST | /auth/passkey/register/begin | WebAuthn registration challenge | none (first user only) | none |
| POST | /auth/passkey/register/finish | store the credential | none (first user only) | none |
| POST | /auth/passkey/login/begin | WebAuthn assertion challenge | none | none |
| POST | /auth/passkey/login/finish | establish the session | none | none |
| POST | /auth/logout | end the session | session | none |
| GET | /me | user, exam date, purge date | session | none |
| POST | /sessions | open a session in a mode; the response carries the four assembled blocks (due reviews, fringe learning, interleaved mixed review, calibration and error notes) and the minute forecast for each | session | engine: fringe computation and the Session assembly rule in `02-adaptive-engine.md` (R5) |
| GET | /sessions/{id} | session state and remaining queue | session | none |
| GET | /sessions/{id}/next | the next item, fully rendered | session | engine selection; may enqueue a generate job if the bank is short |
| POST | /sessions/{id}/attempts | submit a response | session | grader (deterministic path first) |
| GET | /sessions/{id}/attempts/{aid}/feedback | elaborated feedback after submission | session | diagnostician |
| POST | /sessions/{id}/attempts/{aid}/confidence | record the 3-point rating before feedback | session | engine (sets `hypercorrection_due`) |
| POST | /sessions/{id}/judgments | record a block 4 judgment of learning | session | `judgments` insert; never enters credit assignment (R5, B3) |
| POST | /sessions/{id}/close | end the session, write the summary | session | engine: FSRS scheduling for the next due dates |
| GET | /sessions/{id}/stream | SSE: tutor tokens, grading progress, queue events | session | provider layer, grader |
| POST | /attempts/{aid}/images | upload an FRQ photo | session | image quality gate, then transcriber role |
| GET | /attempts/{aid}/images/{iid} | fetch a stored image | session | none |
| DELETE | /attempts/{aid}/images/{iid} | delete an FRQ image | session | audit_log write |
| GET | /attempts/{aid}/transcription | the rendered read-back for confirmation | session | none |
| POST | /attempts/{aid}/transcription/confirm | student confirms or corrects the read-back | session | unlocks grading; enqueues grade_batch |
| GET | /attempts/{aid}/gradings | per-point results with provisional flags | session | none |
| POST | /gradings/{gid}/dispute | student disputes a point | session | review_queue insert |
| GET | /review-queue | operator view of open items | session, operator | none |
| POST | /review-queue/{id}/resolve | operator resolution | session, operator | may re-run a grading or retire an item |
| POST | /mocks | start a full mock on the 2027 form shape | session | engine: assembles the section structure |
| GET | /mocks/{id} | mock state, section and part timers | session | none |
| POST | /mocks/{id}/sections/{n}/start | start a timed part | session | rehearsal mode, pacing metrics only |
| POST | /mocks/{id}/sections/{n}/submit | submit a part | session | grade_batch job |
| POST | /mocks/{id}/finish | close the mock, produce the band | session | score estimate per `05-assessment-modes.md` |
| GET | /progress | mastery map, calibration, due counts | session | none |
| GET | /settings | app settings | session | none |
| PUT | /settings | update app settings | session | none |
| GET | /settings/providers | provider configs without key material | session | none |
| PUT | /settings/providers/{provider} | set or rotate a key, enable or disable | session, passphrase re-entry | provider layer reload |
| POST | /settings/providers/{provider}/test | one cheap call to confirm the key works | session | provider layer |
| GET | /settings/budgets | per-role caps and today's usage | session | none |
| PUT | /settings/budgets | change a cap | session | budget guard reload |
| POST | /export | produce a full data export | session | export job |
| GET | /export/{id} | download the export | session | none |
| POST | /purge | delete everything after an export | session, typed confirmation | purge, audit_log write |
| GET | /content/snapshot | active snapshot id, digest and counts | session | none |
| POST | /content/reload | reload the library into a new snapshot | session, operator | snapshot_reload job |
| GET | /healthz | liveness | none, localhost only | none |

Two entries deserve a note because they are where fidelity is won or lost.

`POST /attempts/{aid}/transcription/confirm` is the hinge of the whole FRQ path. Nothing is graded before it. The read-back is rendered math, not a LaTeX string, and the student can correct it. This is a deliberate rejection of the single-call design that folds transcription into grading; both designs appear in the literature and neither is settled (https://arxiv.org/abs/2605.19043 [single-source]), and the decision goes to the inspectable one because a rubric point lost to a misread exponent is the failure that destroys trust in the whole product.

`POST /gradings/{gid}/dispute` exists because per-point scores are presented as provisional. The published agreement numbers do not support autonomous scoring at a standard a student should be asked to accept without recourse (track 3, section 3).

## Streaming

Two things stream: tutor text and grading progress. Everything else is a request and a response, because a mastery update or a selection decision has no meaningful intermediate state a student should watch.

SSE is the transport, for three reasons in priority order. Learning impact: the only progressive content is the tutor's prose and the sequence of per-point grading decisions, both server to client only. A bidirectional channel would let the client send while the server streams, which is exactly the affordance D1 removes, since there is no chat box beside an unsolved problem. A one-way transport makes the wrong feature awkward to build. Cost and operations: SSE is plain HTTP and inherits the auth cookie, the rate limiter, the proxy and TLS with no second code path, where a WebSocket needs its own auth, heartbeat, reconnect semantics and CSP entry. Convenience: `Last-Event-ID` reconnection is part of the protocol, so a drop mid-grading resumes without inventing a resume protocol.

WebSockets would be right if the client had to push a continuous stream, for example live stroke data from a stylus canvas. D6 does not build the ink pipeline, so that requirement does not exist.

Normalising provider streams. Every adapter in `07-ai-provider-layer.md` emits the same internal event vocabulary regardless of what the provider sends:

```
{ "type": "start",     "role": "grader", "model": "...", "request_id": "..." }
{ "type": "text",      "delta": "..." }
{ "type": "reasoning", "delta": "..." }
{ "type": "json",      "delta": "..." }          partial structured output
{ "type": "progress",  "unit": "point", "done": 3, "total": 9 }
{ "type": "usage",     "input": 0, "output": 0, "cached_read": 0, "cached_write": 0 }
{ "type": "error",     "code": "...", "retryable": true }
{ "type": "end",       "reason": "stop" }
```

The mapping work per provider is mechanical but not uniform. Anthropic emits `message_start`, `content_block_start`, `content_block_delta` with delta types `text_delta`, `input_json_delta`, `thinking_delta` and `signature_delta`, `content_block_stop`, `message_delta`, `message_stop`, `ping` and `error` (https://platform.claude.com/docs/en/build-with-claude/streaming [verified]); the adapter maps `text_delta` to `text`, `thinking_delta` to `reasoning`, `input_json_delta` to `json`, and drops `ping`. OpenAI's Responses API emits typed semantic events including `response.created`, `response.output_text.delta`, `response.completed` and `error`, with the full catalogue not enumerated on the loaded page and therefore unknown (https://developers.openai.com/api/docs/guides/streaming-responses [verified, what is listed]); the adapter maps what it knows and treats an unrecognised event as ignorable rather than fatal. Gemini documents chunked streaming without a named event taxonomy on the loaded page (https://ai.google.dev/gemini-api/docs/text-generation [verified]). OpenRouter is SSE with two documented traps that the adapter must handle explicitly: keepalive comment lines reading `: OPENROUTER PROCESSING` that must be skipped before JSON parsing, and mid-stream errors that arrive as an SSE event carrying `finish_reason: "error"` underneath a 200 OK (https://openrouter.ai/docs/api-reference/streaming [verified]). The second one is why the internal vocabulary has an `error` event type that can arrive after `start`: a transport-level success is not a generation-level success.

Non-streaming providers degrade rather than fail. Ollama streams natively and on its OpenAI-compatible path (https://docs.ollama.com/api/openai-compatibility [verified]), so it is not the problem case. claudebox is: its server buffers the child process output and replies only after the process exits, with no SSE path at all (server.js, [verified]). The rule that follows is in D8 and is repeated here because it is an architectural constraint and not only a provider detail: the tutor role is not routable to claudebox. For any role that is routable to a non-streaming provider, the adapter wraps the single response in the same event sequence, emitting `start`, then one `text` or `json` event carrying the whole body, then `usage` if available and `end`. The client sees a valid stream that simply arrives at once. What the client must not do is present a typing animation over a buffered response, because that misrepresents latency; the session screen shows a determinate progress state for non-streaming roles instead.

Grading progress is not model streaming. It is the server emitting a `progress` event as each of the nine scoring points on an FRQ resolves, whether that point was decided by a SymPy pre-check in microseconds or by three model samples. The student watches the rubric fill in. This is worth building because it makes the per-point structure of the grade visible, which is the structure the dispute path operates on.

## Background jobs

A single worker process polls the `jobs` table. The queue is SQLite because the system already depends on SQLite for durability, and adding Redis to a single-user deployment would add a second thing that must be running for the app to work.

Job types. The `generate` and `verify` types exist in the schema from the start but are first enqueued in P4: P1 items are hand-authored by the operator and carry a provenance record with `model = "operator"` (R9).

| Type | What it does | Triggered by | Typical latency |
| --- | --- | --- | --- |
| generate | Produce n items from one archetype and a parameter draw | low item bank for a fringe skill; nightly top-up | seconds to minutes; batch API path up to 24h |
| verify | Independent re-solve, SymPy equivalence, numeric probes, distractor distinctness, calculator boundary | every new item | seconds |
| monte_carlo | A few hundred parameter draws against the archetype invariants | every new archetype family, and on any archetype record change | minutes |
| grade_batch | Per-point grading of a whole FRQ or a submitted mock section | transcription confirmed inside a unit check, part drill, mock or six-week checkpoint, or a mock section submitted; never a micro-session, whose grading is deterministic (R10) | seconds to minutes |
| diagnose | Error and misconception analysis over a graded point vector | grading complete | seconds |
| snapshot_reload | Rebuild the content snapshot and reconcile retired IDs | operator action; library file change | seconds |

Leasing and retry. A worker claims a row by a conditional update that sets `state = 'leased'` and `lease_expires_at` only where the row is still `queued`, which is atomic under SQLite's write lock. An expired lease is reclaimable, so a worker killed mid-job does not strand work. Retries back off with `not_before`, and the ladder is 1 minute, 5 minutes, 25 minutes, then dead, with a cap of 4 attempts [inferred; the schedule is a tunable in `12-open-questions.md`]. A job that goes dead writes to `review_queue` if a student is waiting on it and to `audit_log` always.

Idempotency. Every job carries a unique `idempotency_key` derived from its inputs: for generate it is the archetype id plus the parameter draw plus the prompt template version; for grade_batch it is the attempt id plus the confirmed transcription digest; for verify it is the item id plus the check set; for snapshot_reload it is the library digest. Enqueueing a duplicate key is a no-op that returns the existing job. This is what makes retry safe and what makes a crash during a batch harmless: the second run produces the same key and either finds the completed row or resumes it.

Batch API jobs are a special case because they are asynchronous at the provider. A `generate` or `grade_batch` job submitted to a batch endpoint records the provider batch id and moves to a polling state rather than holding a lease for hours. Anthropic's batch processing is 50 percent off both input and output, caps a batch at 100,000 requests or 256 MB, finishes most batches under an hour, expires all at 24 hours, and retains results 29 days (https://platform.claude.com/docs/en/build-with-claude/batch-processing [verified]). OpenAI's batch is 50 percent off with a 24 hour window only, 200 MB input file cap, 50,000 requests per batch and up to 2,000 batches created per hour (https://developers.openai.com/api/docs/guides/batch [verified]). Gemini's batch is 50 percent off; the size cap is unknown from the loaded pages (https://ai.google.dev/gemini-api/docs/pricing [verified]). Nothing on the student's interactive path is ever sent to a batch endpoint, because a 24 hour expiry is not a latency a session can absorb.

Redis migration path. The seam is the lease. The worker talks to a small queue interface with four operations: enqueue with an idempotency key, lease with a timeout, complete, and fail with a backoff. SQLite implements it with the conditional update above. A Redis implementation implements the same four operations with a sorted set for `not_before` and a processing list for leases, and the idempotency key becomes a `SETNX`. The job rows stay in the relational store either way, because the audit trail and the `review_queue` links must survive a queue flush. Nothing above the queue interface changes, and the trigger for the migration is a worker pool, which is a phase 8 concern per `11-phased-delivery.md`.

## Content loader for research/

The loader is the component that turns the research library into something the engine can traverse. It runs once at startup and again on a `snapshot_reload` job. It is the only component that reads `data/` from disk.

What it reads, by ID, at the paths named in `research/README.md`:

```
data/curriculum.json          units, topics, LOs, EKs, practices, practice skills
data/skills.json              BC-CON concepts, BC-SKL skills, BC-PRQ prerequisites
data/prereq_edges.csv         from, to, type, evidence_tag, note
data/archetypes.json          BC-QA archetypes and BC-QV variants
data/scoring_points.json      BC-PT scoring point types
data/errors.json              BC-ERR observed errors
data/misconceptions.json      BC-MIS misconceptions
data/diagnostic_signals.json  BC-SIG signals with mastery_state
data/taxonomies.json          BC-REP, BC-DF, BC-CV
data/frq_records.json         official FRQ part records (structure only)
data/mcq_records.json         official sample MCQ records (structure only)
data/sources.json             BC-SRC source registry
data/ids.json                 append-only ID registry with tombstones
```

Validation, in order, with the loader refusing to start on any failure:

1. Schema validation of each registry against its file in `schemas/` (`skills.schema.json`, `archetypes.schema.json`, `errors.schema.json`, `misconceptions.schema.json`, `diagnostic_signals.schema.json`, `scoring_points.schema.json`, `taxonomies.schema.json`, `curriculum.schema.json`, `frq_records.schema.json`, `mcq_records.schema.json`, `sources.schema.json`). The schemas already enforce the controlled vocabularies the engine depends on, including the `mastery_state` enum and the `scope` enum.
2. Referential integrity. Every BC-* string appearing in a cross-reference field must resolve to a record in the appropriate registry, or to a tombstone in `data/ids.json`. A dangling ID is a hard refusal with the offending record and field named.
3. Graph integrity on `prereq_edges.csv`. Build the typed edge set, accepting the 48 edges whose endpoints are BC-TOP ids (31 with a BC-TOP source, 17 with a BC-TOP target), which the loader resolves against `curriculum.json` and marks inert: an inert node does not gate, neither sends nor receives propagated credit, and is excluded from the outer fringe computation (R13). The remapping of those edges to BC-SKL ids is a library gap carried in `12-open-questions.md`. Then run the cycle detection, and run it over the whole loaded typed edge set rather than over the `hard_prerequisite` subgraph, which is the reading 02-adaptive-engine.md invariant 1 states and the one `test_graph_acyclic` asserts (C11): topological-sort the loaded graph over the union of BC-SKL, BC-PRQ and BC-TOP ids and assert the sort consumes all 1226 edges, including the 48 that touch a BC-TOP id. A cycle anywhere in that set, of any edge type, is a hard refusal. Checking only the hard edges would let a supporting or co_requisite cycle through, and the inert BC-TOP edges are still loaded, so they are still sorted. The current library has 0 cycles over 1226 edges [verified, `data/`], and the Prerequisite gating and the outer fringe rule in `02-adaptive-engine.md` rests on that, since the outer fringe is undefined on a cyclic graph.
4. Enum and range checks the engine specifically needs: `calculator_status` in the archetype set, `mastery_state` on every BC-SIG, every BC-DF reference in `difficulty_factors` resolving to a taxonomy record.

Refusing to start rather than degrading is a learning-impact decision. A dangling archetype reference means an item can be served whose skills are unknown, so a mastery update is attributed to the wrong skill and silently corrupts the state everything else reads. A cycle means the fringe computation either loops or silently excludes a region of the graph. Both failures are invisible in the interface and destructive in the model, so they must be loud at startup.

Immutability. The graph is built once and frozen for the process lifetime; the engine holds a reference, never mutates it and never writes back to `data/`. `02-adaptive-engine.md` computes the outer fringe on every selection under Prerequisite gating and the outer fringe, and a fringe computed against a graph that could change mid-session would make two items in one session incomparable.

Versioning. Each successful load writes a `content_snapshots` row with a digest over the registry files plus `prereq_edges.csv`, and the counts listed earlier. Every `sessions`, `items` and `skills_state` row records the `snapshot_id` it was created or last reconciled under. That is what makes it possible to say later that a mastery estimate was formed under a version of the graph that no longer exists.

Library updates and retired IDs. The research library is append-only by rule and retires IDs with a tombstone carrying `superseded_by` in `data/ids.json` (`research/README.md`). The reconciliation on `snapshot_reload` is:

```
for each skills_state row of each user:
    if row.skill_id is active in the new snapshot:
        keep, set snapshot_id
    else if ids.json has a tombstone with superseded_by = S and S is active:
        if a skills_state row for S already exists:
            merge: sum credited successes and failures,
                   take max stability, max observation_count,
                   union distinct_archetypes_succeeded and success_days,
                   mastered = mastered(old) or mastered(new),
                   recompute mastered flag against the D2 conditions afterwards
        else:
            rewrite skill_id to S
        write an audit_log entry naming both IDs
    else if tombstone has no superseded_by:
        mark the row orphaned, retain it, exclude it from selection and from
        the mastery map, and surface it in the operator's reload report
    else:
        refuse the reload: a tombstone pointing at an inactive ID is a
        library inconsistency, not something to guess about
```

Three details there are decisions, not mechanics. Merging rather than discarding, because discarding silently reduces demonstrated mastery when the library merely renamed a skill, and an unexplained mastery drop is worse than a slightly generous merge. Recomputing the `mastered` flag after a merge rather than trusting the union, because D2's declaration conditions (at least 3 credited unaided successes, at least 2 distinct archetypes, at least 3 distinct calendar days spanning at least 7 days) can be satisfied in appearance by a union without being satisfied in substance. Retaining orphaned rows rather than deleting them, because `attempts` still references them.

Items also reference the library, through `archetype_id`, `variant_id` and the BC-PT ids in `worked_solution`. An item whose archetype has been retired without a `superseded_by` is retired too, and its verification history is kept. An item whose archetype changed its `invariant_structure` is a harder case: the item was generated under a mould that no longer exists. The rule is that a change to `invariant_structure`, `safe_variables`, `difficulty_variables` or `point_types` on an archetype invalidates every item generated from it, moving those items to `status = 'retired'` and enqueueing a `monte_carlo` job for the new family. This is expensive and correct; the alternative, keeping items generated under an old structural definition, means serving items that no longer measure what the archetype says they measure.

A known library gap that the loader must tolerate rather than refuse over: 56 active archetypes carry no `point_types`, so their FRQ variants cannot be point-graded, and 36 carry no `official_examples`, so their difficulty priors rest on BC-DF factors alone [verified, `data/`, list in the repository facts sheet]. The loader records both counts on the snapshot and the Item selection algorithm in `02-adaptive-engine.md` avoids routing an FRQ-shaped request to a pointless archetype. `BC-SKL-02001` has no archetype at all and is therefore unservable; the loader records it rather than failing, and `12-open-questions.md` carries it as a library gap.

## Caching

Three caches, at three different layers, for three different reasons.

Prompt cache prefixes, per role. Anthropic's prompt caching has a minimum cacheable prefix of 512 tokens for Opus 5, 1,024 for Sonnet 5, and 4,096 for Haiku 4.5, and below the minimum the prompt is silently processed uncached with no error (https://platform.claude.com/docs/en/build-with-claude/prompt-caching [verified]). That silence is the design constraint: a prefix that falls under the minimum costs full price and reports nothing, so each role's prefix has a stated minimum length that a golden test asserts. Cache reads cost 0.1x base input; a 5 minute write costs 1.25x and a 1 hour write costs 2x, which for Opus 5 at $5 per MTok input works out to $0.50 per MTok read, $6.25 per MTok for a 5 minute write and $10 per MTok for a 1 hour write (same page [verified]). Up to 4 explicit breakpoints are available and automatic caching consumes one slot (same page [verified]). Cache reads do not count toward the input tokens per minute rate limit on current models (same page [verified]).

The 1 hour TTL is chosen for interactive roles during a session and the 5 minute default elsewhere. A 1 hour write at 2x against a 5 minute write at 1.25x is a 0.75x base-input premium on the write, and it pays back the moment a session has a gap longer than 5 minutes. The Session assembly rule in `02-adaptive-engine.md` (block 1 due reviews at most 5 items or 5 forecast minutes, block 2 fringe learning to 25 forecast minutes, block 3 interleaved mixed review at 10 to 15 forecast minutes, block 4 calibration prompts and error notes) produces those gaps repeatedly whenever the student is reading feedback or working an FRQ on paper.

Per-role prefix contents and minimum lengths:

| Role | Prefix contents | Minimum length target | TTL |
| --- | --- | --- | --- |
| tutor | Guardrail instructions, the never-give-the-answer rule, the student's persistent misconception list, the current unit's CED structure | above 1,024 tokens (Sonnet 5 minimum) | 1h during a session |
| grader | Scoring conventions, the BC-PT definitions in play, the earns and does_not_earn and eligibility_after_error language, the notation requirements | above 1,024 tokens | 1h during a session |
| generator | The archetype's invariant_structure and safe_variables, the BC-DF definitions, the generation contract, the no-official-text rule | above 512 tokens (Opus 5 minimum) | 1h during a generation batch |
| verifier | The re-solve instructions, the calculator-boundary rule, the output schema | above 512 tokens | 1h during a verification batch |
| diagnostician | The BC-ERR and BC-MIS vocabulary for the item's skills, the mastery_state enum, the never-a-single-cause rule | above 512 tokens | 1h during a session |
| transcriber | The read-back instructions, the notation conventions, the image quality expectations | above 4,096 tokens if routed to Haiku 4.5, otherwise above the routed model's minimum | 5m |

The transcriber row is the awkward one and it is stated honestly: routing transcription to Haiku 4.5 means a 4,096 token minimum prefix (same page [verified]), and the transcriber's genuine instructions are much shorter than that. Padding a prompt to reach a cache minimum is a real practice with a real cost in input tokens, and whether it pays depends on call volume. This is left as a measurement, not a decision, and is listed in `12-open-questions.md`.

Two provider-specific cache facts change the arithmetic if routing changes. Gemini's implicit caching is on by default with a 4,096 token minimum on the 3.x Flash line and on 3.1 Pro Preview, and 2,048 on the 2.5 line, with telemetry through `usage.total_cached_tokens` (https://ai.google.dev/gemini-api/docs/caching [verified]); explicit caches are available on `generateContent` but not on the Interactions path (same page [verified]). OpenAI's caching is automatic with a 1,024 token minimum on GPT-5.6 and later, reads at 0.1x, no write premium, and a prefix that stays reusable for 30 minutes after its last use on GPT-5.6 and later (https://developers.openai.com/api/docs/guides/prompt-caching [verified]).

Two things invalidate an Anthropic cache and both are relevant here: changing the structured output format invalidates the prompt cache, and changing `budget_tokens` on extended thinking invalidates cache breakpoints (https://platform.claude.com/docs/en/build-with-claude/structured-outputs and https://platform.claude.com/docs/en/build-with-claude/extended-thinking [verified]). The consequence for this architecture is that output schemas and thinking budgets are pinned per role and versioned with the prompt template, not tuned per call.

Item bank reuse. A verified item is a durable asset. It is reused across sessions and, later, across users, subject to the exposure rules in `04-item-generation.md`. This is the largest single cost lever in the system, because generation plus verification is several model calls per item while serving a cached item is zero. It is also a learning lever in the wrong direction if overdone, since serving the same item repeatedly turns retrieval practice into recognition; the interleaving and exploration constraints in D3 bound reuse.

Verification results cached by parameter draw. `item_verifications` is keyed by item, and items are keyed by archetype plus parameter draw. A re-generated item with an identical draw finds an existing verification record and skips the checks. The Monte Carlo result is cached per archetype family rather than per item, because it is a property of the family: a few hundred draws asserting the archetype's invariants hold across the parameter space (track 3, section 5). Re-running it is only required when the archetype record changes.

## Cost controls

Ordered by learning impact. A cost control that degrades what the student sees is a last resort; a cost control that changes only how work is scheduled is free.

Per-role daily budget caps, in tokens and dollars, stored in `budgets`. Caps are per role because stopping has different consequences per role: a stopped generator or verifier is invisible while the bank holds items, a stopped grader leaves an FRQ ungraded, a stopped tutor leaves a student mid-session without support. `07-ai-provider-layer.md` owns the stop behaviour. The architectural requirement is that the guard is checked before the call and lives inside the provider layer so no caller can bypass it.

Batch API for queues. Generation, verification and non-interactive grading go through batch endpoints at 50 percent off input and output on Anthropic (https://platform.claude.com/docs/en/build-with-claude/batch-processing [verified]), 50 percent on OpenAI (https://developers.openai.com/api/docs/guides/batch [verified]) and 50 percent on Gemini (https://ai.google.dev/gemini-api/docs/pricing [verified]). This is the single largest structural saving available and it costs nothing the student can perceive, because the work is asynchronous by nature. The constraint is the expiry: 24 hours on all three, so the job scheduler must not submit work whose result is needed sooner.

Cached items. Covered above; the point here is that the cost model should be stated as cost per new item, not cost per item served, and the ratio between them is the bank reuse rate.

Pre-call context checks. Before a call, the provider layer computes the prompt's token count against the routed model's context window and rejects or reroutes rather than discovering the overflow as a provider error. This is the LiteLLM pre-call check shape: `enable_pre_call_checks=True` filters deployments by context capacity against message length and by region, with `base_model` and `region_name` set (https://docs.litellm.ai/docs/routing [verified]). The direct cost saving is small; the real saving is not paying for a failed call and not stranding a student mid-grading.

One number that changes cost comparisons and is easy to miss: Claude 4.7 and later use a newer tokenizer producing roughly 30 percent more tokens for the same text, so per-MTok comparisons against 4.6 and earlier understate cost (https://platform.claude.com/docs/en/about-claude/pricing [verified]). Any budget forecast in this project that compares an Opus 5 price against a Sonnet 4.5 price without accounting for that is wrong by about a third on the input side.

Relevant list prices, all from the provider research and all [verified] at their cited URLs: claude-opus-5 at $5 in and $25 out per MTok with a 1M context and 128K max output; claude-sonnet-5 at $2 and $10, with the announced 1 September 2026 rise to $3 and $15 cancelled and $2 and $10 permanent; claude-haiku-4-5 at $1 and $5 with a 200K context (https://platform.claude.com/docs/en/about-claude/pricing). gemini-3.8-flash at $0.75 in and $3.75 out per 1M through 31 December 2026, then $1.50 and $7.50, with cache reads at $0.075 per 1M through the same date then $0.15 (https://ai.google.dev/gemini-api/docs/pricing). Those two lines are why the routing in D8 puts Anthropic first for anything where a wrong answer reaches a student and Gemini 3.8 Flash second for bulk grading of routine practice.

Tool overhead is a cost the system can avoid entirely. Tool definitions add tokens to every call: 286 tokens on Opus 5 for `tool_choice` auto or none and 406 for any or tool, 354 and 474 on Sonnet 5, 496 and 588 on Haiku 4.5 (https://platform.claude.com/docs/en/about-claude/pricing [verified]). The tutor has no tools, which is a safety decision in `09-security-and-privacy.md` and a small cost saving as a side effect.

## Scaling assumptions

Single user first. The numbers below are the load the system is designed for, and each one says whether it is measured, derived from a cited source, or inferred.

Requests per session. The Session assembly rule in `02-adaptive-engine.md` forecasts block 1 at most 5 items or 5 minutes, block 2 fringe learning to 25 minutes, block 3 interleaved mixed review at 10 to 15 minutes, and block 4 calibration prompts and one-line error notes, ending when all four blocks are empty rather than on a timer (R5). The forecast uses the per-archetype median attempt time, defaulting to 3 minutes per item until 5 attempts exist for that archetype [inferred], which puts a session at roughly 15 to 25 items [inferred; both the default and the per-item time are tunables]. Each item generates one `GET /sessions/{id}/next`, one `POST /attempts`, one confidence post and one feedback fetch, so roughly 60 to 100 REST requests per session, plus one long-lived SSE connection. Model calls are far fewer than requests because MCQ grading is deterministic and most items are served from the bank: the model calls in a typical learning session are the diagnostician on incorrect attempts and the tutor when invoked, so on the order of 5 to 20 model calls per session [inferred]. A session that carries per-point free-response grading is different, and per R10 that is only a unit check, a part drill, a mock or the six-week checkpoint: one transcription call per image, then per-point grading at 3 samples per judged point, so a 9 point FRQ with 5 judged points is 15 grading calls plus the transcription. A micro-session never incurs them, because its grading is deterministic.

Item bank size. The library has 541 active skills and 139 active archetypes in 77 families with 395 variants [verified, `data/`]. Skills per archetype are distributed 4 skills on 34 archetypes, 6 on 33, 5 on 31, 3 on 22, 2 on 15 and 1 on 4 [verified, `data/`], so archetypes are mostly multi-skill and the bank does not need 541 independent item families. D2's mastery declaration requires at least 3 credited unaided successes on at least 2 distinct archetypes across at least 3 calendar days for each skill, and D3's review mode then draws repeatedly on mastered skills as retrievability decays. A defensible working target is 30 to 60 verified items per archetype, giving roughly 4,200 to 8,300 items across 139 archetypes [inferred; derived from the mastery conditions and the desire not to repeat an item inside one FSRS interval, and listed as a tunable]. Only 31 skills are `independently_assessable` [verified, `data/`], which means most skills can only be observed through multi-skill items, which in turn means the bank has to cover skill combinations rather than skills, and the true required size may be larger. That is an open question, not a settled number.

Storage per month. Text rows are small. An attempt with its response, grading rows and diagnosis is on the order of a few kilobytes. At 20 items a day that is well under a megabyte a month of relational data [inferred]. The item bank at 8,000 items with stems, worked solutions and options is on the order of tens of megabytes [inferred]. FRQ images dominate: a photographed booklet page at a quality sufficient for transcription is plausibly 0.5 to 2 MB, and a full mock has 6 questions across multiple pages. At one mock every 4 to 6 weeks plus scattered FRQ practice, image storage is the only line that grows meaningfully, on the order of tens to low hundreds of megabytes a month [inferred; the per-image size is unmeasured]. Images are deletable per `09-security-and-privacy.md`, which is both a privacy control and the storage control.

Provider rate limits are not a constraint at this scale. Anthropic's Start tier gives 1,000 requests per minute, 2,000,000 input tokens per minute and 400,000 output tokens per minute for the Opus 5 and Sonnet 5 bucket, with a $500 monthly spend cap (https://platform.claude.com/docs/en/api/rate-limits [verified]). A single student generating 100 model calls a day is three orders of magnitude below the request limit. The binding constraint is the spend cap, not the rate limit, which is why the budget tables exist. OpenRouter's free-model limit of 20 requests per minute and 50 per day under $10 of lifetime purchase, rising to 1,000 per day at $10 or more (https://openrouter.ai/docs/api-reference/limits [verified]), would be binding, which is one more reason D8 keeps OpenRouter out of the hot path.

What changes later. Postgres replaces SQLite through the same SQLAlchemy models, with the migration triggered by concurrent writers rather than by data volume. Budgets become per user rather than global, which the `budgets` table already supports through its `user_id` column. The single worker becomes a pool, which the lease-based queue already supports, with Redis replacing the SQLite queue at the interface described above. Rate limits move from per IP and per session to per user.

What does not change. The content loader stays single-process and in-memory, because the graph is small and shared read-only; 541 skills and 1226 edges is not a distributed systems problem. The engine stays synchronous and deterministic given a state and a snapshot, which is what makes the offline simulation in `10-quality-and-evaluation.md` possible. The verifier stays in-process with SymPy. The per-point grading structure stays, because it is a correctness decision and not a performance one. And the claudebox adapter stays single-operator and is never part of any multi-user story, per D8 and `07-ai-provider-layer.md`.

## Observability

Structured logs. Every log line is JSON with a fixed set of fields: timestamp, level, request id, user id, session id when in a session, role when a model call is involved, provider and model, job id and type when in a worker, and an event name from a controlled vocabulary. No log line ever contains a provider key, a passphrase, a raw student response, or a raw provider response body. The prohibition on raw bodies is not only privacy; it is also the reason a log file can be shared when diagnosing a problem.

Request ids propagate. The id generated at the API boundary travels into the engine, into the provider layer as the adapter's correlation id, into the job payload when a job is enqueued, and into `audit_log`. A grading dispute can therefore be traced from the student's click back to the three samples that produced the split.

The audit log is not the application log. `audit_log` is a durable, queryable record of consequential actions: a key set or rotated, a budget changed, a snapshot reloaded, a skill state rewritten by a tombstone merge, an image deleted, an export produced, a purge run, a review queue item resolved. It is owned by `09-security-and-privacy.md` and it survives log rotation.

Metrics. The names live in `10-quality-and-evaluation.md` and this document only says where they come from. Engine metrics come from the state transitions the engine writes: mastery growth per study hour, retention at 7 and 30 days measured as first-attempt accuracy on due reviews, calibration as Brier score and as confidence minus accuracy, method-selection accuracy against execution accuracy, and error-type recurrence rate. Pipeline metrics come from `item_verifications` and `gradings`: verification pass rate per check type, key error rate on the hand-audited sample, grading split rate per BC-PT, dispute rate and dispute upheld rate. Operational metrics come from the provider layer and the job worker: tokens and dollars per role per day, cache hit rate as cached read tokens over total input tokens, fallback invocation count per role, job latency by type, job dead-letter count.

One deliberate absence: there is no third-party analytics. This is a D10 rule and it is also an architectural simplification, since the metrics above are all derivable from tables the system already keeps.

## Traceability

Which architecture element serves which mechanic in `01-learning-model.md` and which rule in `02-adaptive-engine.md`.

| Architecture element | Mechanic in 01 | Rule in 02 |
| --- | --- | --- |
| Immutable content snapshot with cycle refusal | All of them; nothing is servable without a valid graph | Prerequisite gating and the outer fringe, which is undefined on a cyclic graph |
| skills_state table with the full D2 state vector | Mastery gating; adaptive fading | Update rules, Decay, and the fading ladder counters `consecutive_successes` and `consecutive_failures` |
| pending_probes queue drained before scoring | Structured self-explanation on errors | Item selection algorithm, which drains the queue before its own scoring (R6) |
| judgments table | Metacognitive judgments of learning | Session assembly block 4, which collects them; no credit-assignment rule reads them |
| Engine selection with interleaving constraints enforced at queue build | Interleaving; spaced retrieval | Item selection algorithm: max 2 consecutive items on one primary skill; at least 4 skills per block of 10 spanning at least 2 units; at least 20 percent representation-translation variants |
| sessions.updates_mastery flag | Criterion-shaped rehearsal | Timed sessions update pacing metrics only, never mastery state |
| gradings as one row per BC-PT with three samples and an escalation path | Elaborated feedback withheld until submission | Credit assignment from a diagnosed mastery_state |
| Transcription confirm endpoint as a hard precondition on grading | Criterion-shaped rehearsal on the real artefact | Nothing; it protects the inputs every rule downstream depends on |
| diagnoses with probability-weighted misconceptions and a probe field | Structured self-explanation on errors; hypercorrection routing | Prerequisite gating and the outer fringe, which receives propagation from a diagnosed prerequisite_gap; the probe is written to `pending_probes` (R6) |
| Confidence field on attempts | Confidence ratings with hypercorrection routing | FSRS grade mapping, where mastered maps to Easy only if confidence was high and time was under the archetype median |
| SSE one-way transport, tutor without tools | No chat box beside an unsolved problem | Nothing; it enforces a 01 constraint at the transport layer |
| Verifier with SymPy, numeric probes and Monte Carlo | All practice mechanics, since a wrong key poisons every observation | Every credit assignment, which assumes the item's key is correct |
| Job worker with idempotent retry | Item availability, so the fringe is never empty for want of items | Fringe restriction, which fails closed if no verified item exists for a fringe archetype: the archetype is excluded from selection and written to `audit_log` as a coverage gap (R18) |
| Budgets per role with role-specific stop behaviour | Session continuity | Nothing directly; it bounds the cost of everything above |
| content_snapshots plus tombstone reconciliation | Long-horizon retention to May 2027, across library revisions | Mastery declaration conditions, recomputed after any merge |
| audit_log | None directly | Every state rewrite the engine did not initiate is recorded, so a state can be explained |
