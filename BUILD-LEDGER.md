---
title: Build ledger
research_date: 2026-09-19
status: in_progress
purpose: Where the application build stands, session by session, so the next session can pick the next slice without rereading the plan.
---

# Build ledger

Application code lives at the repository root under `app/` and `tests/`, at the paths docs/plan names. The project CLAUDE.md still says "docs-only, no product"; that sentence is the operator's to amend and this ledger only records the conflict. Tooling: uv-managed Python 3.12.13 in `.venv/`, dependencies in `pyproject.toml`, tests via `.venv/bin/python -m pytest`. Every H2 below carries a tag because `qa/04_tags.py` scans root-level Markdown: [verified] means the test output or the registry was checked in the session named, [inferred] means a judgement.

## Done [verified]

Session 2026-09-19, suite line at close: `42 passed in 12.58s`.

- Integrator: `pyproject.toml`, `app/engine/{constants,state,strength,fsrs_constants,prior}.py`, `tools/build_p1_fixture.py`, `tests/fixtures/graph_p1.json` (54 skills, 101 edges, 25 seeded parents, 4 inert BC-TOP), `tests/fixtures/fsrs_rs_inference_v7_c137ee6.rs`, `tests/engine/test_cold_start.py`: eval_cold_start_pA_distribution passes and prints split p10/p50/p90 0.250/0.450/0.587, compensatory 0.328/0.465/0.587, reproducing the plan's recorded gate.
- Agent A, loader: `app/content/loader.py`, `app/content/snapshot.py`, `tests/content/test_loader.py`: test_graph_acyclic, test_loader_against_real_data, test_loader_refuses_on_injected_cycle, test_loader_refuses_on_injected_dangling_id, test_loader_refuses_on_wrong_type_reference, test_inert_top_ids_include_p1_subgraph. Final suite at close: 42 passed, 0 failed.
- Agent B, engine update rules: `app/engine/update.py`, `app/engine/fsrs.py` (FSRS-7 forms from fsrs-rs), `app/engine/retention.py` (integrator), `tests/engine/test_update.py`: test_credit_assignment_table, test_correct_never_lowers_m, test_partial_never_raises_m, test_retrievability_monotone, test_mastery_conditions, test_fading_ladder, test_propagation_weights, test_mcq_guess_discount, plus test_fsrs_forms_from_source, test_stability_bounded, test_hypercorrection_clears, test_hypercorrection_spans_loaded_skills.
- Agent C, gating, selection, session assembly: `app/engine/fringe.py`, `app/engine/select.py`, `app/session/build.py`, `tests/engine/test_selection.py`: test_fringe_membership, test_retrieval_entry, test_format_alternates, test_co_requisite_inert, test_pending_probes_drained, test_fail_closed_no_item, test_session_assembly_blocks, test_interleave_max_two, test_never_serve_unmastered_prereq, plus test_requeue_gap, test_due_reviews_from_decay, test_probe_queue_cap, test_probe_served_without_explicit_now.
- Agent D, verifier tools, models, fixtures: `app/items/{mathjson,verify}.py`, `app/db/models.py`, `tests/fixtures/answers_equiv/pairs.json`, `tests/fixtures/student_trajectories/` (6), `tests/items/test_verify.py`: test_sympy_equivalence, eval_sympy_settle_rate (40 of 40 equivalent pairs settled); `tests/db/test_models.py`: test_models_create_all.
- Plan corrections below applied to docs/plan by agent E.

## In progress [inferred]

Nothing at the time of writing. The next session starts from Next candidates.

## Known defects [verified]

- Resolved 2026-09-19: `data/prereq_edges.csv` carried a cycle over the full typed edge set (BC-SKL-05020 to BC-SKL-05021 hard_prerequisite, BC-SKL-05021 to BC-SKL-06023 supporting, BC-SKL-06023 to BC-SKL-05020 supporting) because one supporting row was stored in the reverse direction. The row was flipped (see Decisions); `tools/graph_check.py` reports 0 cycles, test_graph_acyclic and test_loader_against_real_data pass, and the helper test that removed the cycle from a temporary copy was deleted as obsolete. A full `tools/merge_staging.py` replay after the flip regressed unrelated evidence links in archetypes, scoring_points and skills, so those three registries and `data/staging/sync-dependents.json` were restored to HEAD; the replay order in that tool lets older staging files overwrite later link-evidence merges, which the library owner should look at before the next merge.
- FSRS-7 forms: docs/plan/02 transcribes stability and difficulty updates with parameter indices that do not match the shipped model (the plan's w7 as an exponent on S made stability explode by about 500x per review; its difficulty step had the sign inverted). Per R28 the forms are copied from the reference implementation instead, fsrs-rs at commit c137ee6e096f9217632397a8fb2bdb6f6e1b92ae, `src/model_v7.rs` and `src/inference_v7.rs`, cross-checked against srs-benchmark `models/fsrs_v7.py`; the source is recorded in `app/engine/fsrs.py` and the vector's source file is committed as `tests/fixtures/fsrs_rs_inference_v7_c137ee6.rs` with its sha256 in `app/engine/fsrs_constants.py`. The awesome-fsrs wiki page R28 names documents only v0 to v6.
- FSRS-7 carries a second, fast stability per card that the P1 schema does not store; `app/engine/fsrs.py` reconstructs it as 0.8 times the long stability, which is the source's own SM-2 bridge. A `fast_stability` column is a P2 schema decision.
- The mastery corroboration test `test_stability_bounded` shows stability saturating at the source's 36500-day clamp after about 12 successive Good reviews at elapsed = S; retrievability still decays below 0.90 at large elapsed times. Whether that clamp is acceptable for an exam horizon of months is unexamined.
- `drain_probe_queue` in `app/engine/fringe.py` still takes `now` as a required positional; every public entry point supplies it through `session_now`, so only a direct call without it raises. `session_now` accepts a datetime `today`, but the rest of the selection path compares dates, so pass a date.
- `qa/last_report.json` is regenerated whenever `qa/12_report.py` runs and is restored with `git checkout -- qa/last_report.json` at session close, so the library's committed report does not drift because of build sessions.

## Plan corrections applied [verified]

- 02 and 11: the vector's source is `src/inference_v7.rs` in fsrs-rs, 34 entries, not the srs-benchmark README, whose "Default Parameters" block at commit bd9110f791e5b37282c55a9aa8db35f68f0c4aa2 prints 35 values from a superseded March 2026 draft (the README's own results table and `models/fsrs_v7.py` say 34). The plan's count of 34 was right and its named source was wrong. An earlier edit in this session that changed 34 to 35 was reverted.
- 02 Item selection pseudocode: `K_hard` no longer includes the primary skill itself. The plan's own recorded pre-computation (p10 0.250, p50 0.456, p90 0.587) reproduces only when the primary skill sits in the compensatory mean; with the primary in the product the 90th percentile is 0.344. Recomputed 2026-09-19 with `app/engine/prior.py`.
- 02 and 06: "The current library has 0 cycles over 1226 edges" is true of the hard_prerequisite subgraph only; see Known defects.
- 02 FSRS section: the stability, difficulty and D0 forms and their parameter indices are superseded by the reference implementation, per R28's own instruction to copy from source.
- 02 next_item_review pseudocode omits the fringe gating filter that invariant 3 requires in every non-diagnostic mode; the implementation applies it and test_never_serve_unmastered_prereq drives review mode and session assembly too.
- 02 R6 ("every selection function drains the probe queue") and 11 test 15 ("block 2 serves the probe first") conflict when block 1 runs before block 2; session assembly hands the queue to block 2 only, and standalone review mode still drains it.
- 01, 02, 11, 12: the lambda ablation is arm 6 in 10-quality-and-evaluation.md, not arm 5.
- 01 and 03: active misconception counts are 213 with a probe and 210 with rivals, per 11 P3; the 236 and 233 figures counted retired records.
- 06 attempts table: added `error_note`, `self_explanation` and `snapshot_id`, which 03, 09 and 11 already require. 06 skills_state: added `unaided_success_count`, because mastery condition 2 (3 credited unaided successes) and condition 4 (3 distinct days) are otherwise one predicate.
- 06 versus 11 convention 1 on skills_state column names: the models follow 06 (`credited_successes`, `credited_failures`, `stability`, `difficulty`); convention 1's `c`, `f`, `S`, `D` names are not used. The dataclass in `app/engine/state.py` uses the short names; the mapping is one to one.
- 02 next_item_review: the ties list is rebuilt only over candidates that passed the p_A_knowledge >= 0.5 filter, and the hypercorrection pool is served before that filter.
- 11 fixture (d): `answers_equiv/` carries 40 equivalent and 13 non-equivalent pairs; three near-miss pairs were added after the numeric tolerance was found to accept them, the last pinning the relative tolerance to within an order of magnitude of 1e-6. Applied to 11.
- 12: removed "6-hour sleep threshold", which names no parameter in 01; co_requisite inertness is invariant 21, not 20.
- 11 P6: removed "and cheap classification" from the Haiku routing line, per R17.
- `tools/style_gate.py` (pre-existing uncommitted edit from the planning session): the gate now also covers `/docs/` paths, and the two dash literals are written as escapes so the file passes its own check. Both edits strengthen or preserve the gate. The wider scope is pending operator confirmation and is listed as an out-of-scope change.
- 02 block 1 ("5 items or 5 minutes of forecast, whichever comes first") with the 3-minute default forecast admits exactly one item until an archetype has 5 timed attempts, so the 5-item cap is unreachable early on. Implemented as written; the exit-criterion-5 walkthrough must not be read as evidence the item cap works.
- 02 invariant 23 (both the split and the compensatory prediction logged on every observation): `attempts` carries `p_split` and `p_compensatory` columns from this session, schema only; the writer arrives with the session loop in the slice that builds `POST /sessions/{id}/attempts`.

## Decisions taken on the operator's instruction, 2026-09-19 [inferred]

- The prerequisite-graph cycle was closed by flipping the reversed row: `BC-SKL-06023,BC-SKL-05020,supporting` became `BC-SKL-05020,BC-SKL-06023,supporting`, because the row's own note stated that the Unit 6 skill depends on the Unit 5 one, which is the opposite of the direction it was stored in. Applied directly to `data/prereq_edges.csv`, then `tools/sync_dependents.py`, `tools/merge_staging.py`, the post-change tool chain and `qa/12_report.py`.
- The FSRS-7 forms stay as copied from fsrs-rs; 02's transcribed block stays marked superseded.
- The application lives in this repository; the local CLAUDE.md was amended to say so. The style gate keeps its wider `/docs/` scope.
- The build is committed on the branch `build/p1-backend-core`; main is untouched.

## Next candidates [inferred]

- Human-only, blocks P1 exit: 130 hand-authored items (10 per P1 archetype) with MathJSON keys and per-option BC-ERR paths; the 100-item key audit; design tokens with a named contrast checker.
- Needs a screen: `app/web/` session, home and settings screens; tests 23, 25, 26.
- Needs a provider key: Anthropic tutor role, prompt templates, cassettes, test 22.
- Needs items: test 17 (item verification over each archetype), eval 29, eval 30, eval 31 (six synthetic trajectories exist as fixtures; a minimal simulation runner is needed).
- Passkeys and purge re-authentication, test 24. FastAPI routes from 06 API surface. Content snapshot persistence and the tombstone reconciliation on reload.
