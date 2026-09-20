---
title: Build ledger
research_date: 2026-09-19
status: in_progress
purpose: Where the application build stands, session by session, so the next session can pick the next slice without rereading the plan.
---

# Build ledger

Application code lives at the repository root under `app/` and `tests/`, at the paths docs/plan names. The project CLAUDE.md still says "docs-only, no product"; that sentence is the operator's to amend and this ledger only records the conflict. Tooling: uv-managed Python 3.12.13 in `.venv/`, dependencies in `pyproject.toml`, tests via `.venv/bin/python -m pytest`. Every H2 below carries a tag because `qa/04_tags.py` scans root-level Markdown: [verified] means the test output or the registry was checked in the session named, [inferred] means a judgement.

## Done [verified]

Session 2026-09-20 (seventh), suite line at open `191 passed in 23.36s`, at close `230 passed in 46.12s`.
Style gate exit 0 on every touched file; `qa/12_report.py` exit 0; `data/`, `research/`, `schemas/`
and `cache/` untouched, confirmed by `git status --porcelain` over all four. The slice was the
provider seam of 07 plus gate 23, which were the last two pieces of P1 scope needing no key, no
screen and no hand-authored item. A fresh reviewer found ten defects over the first integration;
eight were fixed in session by two repair agents and the integrator, and the two that remain are
under Known defects.

- Agent A, the provider seam: `app/providers/guard.py`, `tests/providers/test_guard.py`.
  `GuardedProvider` estimates the worst case before the call, refuses on the dollar or token cap,
  reconciles against `raw_usage` after, keeps one `budgets` row per user per role per day, and
  writes `audit_log` only on the hard stop and the refusal, never per call. Tests:
  test_guard_estimates_the_worst_case_before_the_call,
  test_guard_refuses_when_the_estimate_crosses_the_dollar_cap,
  test_guard_refuses_when_the_estimate_crosses_the_token_cap,
  test_guard_reconciles_the_estimate_against_raw_usage,
  test_guard_keeps_one_budget_row_per_user_role_and_day,
  test_guard_writes_an_audit_entry_when_the_cap_stops_the_role,
  test_guard_writes_no_key_material_into_the_audit_detail,
  test_a_stopped_role_refuses_every_later_call_that_day,
  test_guard_prices_cached_reads_at_the_multiplier,
  test_an_abandoned_stream_releases_the_reservation,
  test_a_completed_stream_reconciles_against_raw_usage,
  test_a_stopped_role_records_the_refusal_once_and_still_refuses,
  test_a_lowered_cap_binds_on_the_existing_row,
  test_an_unpriced_result_model_is_charged_at_the_requested_model_price,
  test_a_result_without_usage_keeps_the_worst_case_reservation,
  test_a_role_with_no_configured_cap_is_refused.
- Agent B, the tutor sentence cache: `app/feedback/tutor.py`, `app/db/models.py` (one nullable
  `attempts.tutor_sentence` column), `tests/feedback/test_tutor_cache.py`. Tests:
  test_the_first_call_stores_the_sentence_on_the_attempt,
  test_a_cached_sentence_is_returned_without_a_second_provider_call,
  test_no_provider_stores_nothing_and_returns_no_sentence,
  test_a_provider_failure_stores_nothing_and_returns_no_sentence,
  test_an_empty_sentence_is_not_cached_and_is_composed_again,
  test_the_cached_sentence_is_read_back_through_a_fresh_session,
  test_without_a_session_and_attempt_the_function_behaves_as_before.
- Agent C, gate 23: `tests/e2e/`, `tests/fixtures/items_p1/` (36 synthetic records over
  BC-QA-01008, 02002, 02006, 02007, 02011 and 03008, all `no_calculator` and `BC-REP-01`, skills
  copied from `data/archetypes.json`), `tests/fixtures/provider_cassettes/`.
  test_session_login_to_feedback (gate 23) and test_the_socket_ban_itself_fails_a_network_call.
  The gate asserts every link 11 names: register with 618 seeded rows, logout, login, `/me`, a
  session drained and closed, a 409 on feedback before the confidence rating, the elaborated screen
  in both served formats, the named BC-ERR path, the tutor sentence through the cassette, the error
  note read back out of SQLite, a `skills_state` change read back out of SQLite, the socket ban
  firing on AF_INET, and membership of every served archetype in 11's 13.
- Integrator: the coverage-gap audit deduped per user per archetype
  (test_a_repeated_coverage_gap_writes_no_second_audit_entry, red `assert 3 == 1`;
  test_a_gap_recorded_for_another_user_still_writes_a_row); the guard and the cache wired into the
  feedback route behind `tutor_sentence_for`, with `tutor_unavailable` carrying 07's hard-stop line
  to the screen (tests/api/test_tutor_budget.py, four tests, red `KeyError: 'tutor_unavailable'`);
  `compose_sentence` re-raises `BudgetStopped` rather than swallowing it, because a cap is not a
  provider failure; `GROWTH_TUTOR_CAP_USD` and `GROWTH_TUTOR_CAP_TOKENS` on the composition root
  (test_main_gives_the_tutor_role_a_daily_cap, test_the_tutor_cap_is_read_from_the_environment);
  the controlled audit vocabulary at `app/audit/vocabulary.py`, enforced in all three writers, with
  a scanner test that walks `app/` and resolves module constants rather than checking one hand-
  copied list against another (tests/audit/test_vocabulary.py, six tests); the guard refuses a role
  with no configured cap (test_a_role_with_no_configured_cap_is_refused, red
  `Failed: DID NOT RAISE BudgetStopped`); the guard's price table pruned to claude-sonnet-5 alone,
  because the Opus 5 and Haiku 4.5 output prices the builder wrote appear in no plan document.

Session 2026-09-19, suite line at close: `42 passed in 12.58s`.

- Integrator: `pyproject.toml`, `app/engine/{constants,state,strength,fsrs_constants,prior}.py`, `tools/build_p1_fixture.py`, `tests/fixtures/graph_p1.json` (54 skills, 101 edges, 25 seeded parents, 4 inert BC-TOP), `tests/fixtures/fsrs_rs_inference_v7_c137ee6.rs`, `tests/engine/test_cold_start.py`: eval_cold_start_pA_distribution passes and prints split p10/p50/p90 0.250/0.450/0.587, compensatory 0.328/0.465/0.587, reproducing the plan's recorded gate.
- Agent A, loader: `app/content/loader.py`, `app/content/snapshot.py`, `tests/content/test_loader.py`: test_graph_acyclic, test_loader_against_real_data, test_loader_refuses_on_injected_cycle, test_loader_refuses_on_injected_dangling_id, test_loader_refuses_on_wrong_type_reference, test_inert_top_ids_include_p1_subgraph. Final suite at close: 42 passed, 0 failed.
- Agent B, engine update rules: `app/engine/update.py`, `app/engine/fsrs.py` (FSRS-7 forms from fsrs-rs), `app/engine/retention.py` (integrator), `tests/engine/test_update.py`: test_credit_assignment_table, test_correct_never_lowers_m, test_partial_never_raises_m, test_retrievability_monotone, test_mastery_conditions, test_fading_ladder, test_propagation_weights, test_mcq_guess_discount, plus test_fsrs_forms_from_source, test_stability_bounded, test_hypercorrection_clears, test_hypercorrection_spans_loaded_skills.
- Agent C, gating, selection, session assembly: `app/engine/fringe.py`, `app/engine/select.py`, `app/session/build.py`, `tests/engine/test_selection.py`: test_fringe_membership, test_retrieval_entry, test_format_alternates, test_co_requisite_inert, test_pending_probes_drained, test_fail_closed_no_item, test_session_assembly_blocks, test_interleave_max_two, test_never_serve_unmastered_prereq, plus test_requeue_gap, test_due_reviews_from_decay, test_probe_queue_cap, test_probe_served_without_explicit_now.
- Agent D, verifier tools, models, fixtures: `app/items/{mathjson,verify}.py`, `app/db/models.py`, `tests/fixtures/answers_equiv/pairs.json`, `tests/fixtures/student_trajectories/` (6), `tests/items/test_verify.py`: test_sympy_equivalence, eval_sympy_settle_rate (40 of 40 equivalent pairs settled); `tests/db/test_models.py`: test_models_create_all.
- Plan corrections below applied to docs/plan by agent E.

Session 2026-09-19 (second session), suite line at close: `72 passed in 14.23s`. Gate 31 `eval_simulation_mastery_growth` read `1 failed, 69 passed` at the first close, for the structural reason recorded under Decisions; after the gamma and condition 3 corrections it passes with pooled policy 88 mastered over 1457 items (0.0604) against control 92 over 1656 (0.0556), per trajectory printed by the eval. Style gate exit 0 on every touched file; `qa/12_report.py` exit 0; `data/` and `research/` untouched; `docs/plan/02`, `11` and `12` carry the two corrections below. Integrator-owned tests added: test_mastery_single_archetype_skill_needs_one_archetype, test_mastery_reachable_in_a_dozen_credited_successes (both quoted red before the engine edit).

- Agent A, simulation runner: `app/sim/runner.py`, `tests/eval/test_simulation.py`: test_simulation_reproducible_from_seed, test_simulation_prereq_gap_stalls_dependants (asserts on the served trace: no served item had an unmastered hard ancestor; shown red with gating bypassed, 165 blocked serves), test_simulation_records_both_predictions, eval_simulation_mastery_growth (gate 31).
- Agent B, snapshot persistence and reload reconciliation: `app/content/persist.py`, `app/content/reconcile.py`, `tests/content/test_persist.py`, `tests/content/test_reconcile.py`: test_snapshot_row_written_on_load, test_rejected_snapshot_row_records_reason, test_reload_with_unchanged_digest_reuses_active_row, test_reload_keeps_active_skill_and_sets_snapshot_id, test_reload_rewrites_superseded_skill, test_reload_merges_into_existing_successor_and_recomputes_mastered, test_reload_merge_union_failing_d2_clears_mastered, test_reload_merge_carries_difficulty_with_winning_stability, test_reload_merge_carries_difficulty_from_old_row_when_it_wins, test_reload_merge_preserves_flags_and_resets_consecutive_counters, test_reload_orphans_tombstone_without_successor, test_reload_refuses_inactive_successor, test_reload_writes_audit_entry.
- Agent C, session service and attempts writer (no HTTP layer): `app/session/repository.py`, `app/session/service.py`, `tests/session/test_service.py`: test_open_session_persists_four_blocks, test_attempt_row_logs_split_and_compensatory, test_attempt_updates_skills_state, test_confidence_before_feedback_sets_hypercorrection, test_error_note_stored_on_attempt, test_close_session_writes_ended_at, test_state_round_trip, test_rehearsal_session_writes_no_mastery, test_record_attempt_refuses_duplicate, test_ungraded_answer_skips_the_update, test_timestamps_are_timezone_aware_utc. Confidence design: `apply_observation` already sets `hypercorrection_due` from the rating, so `record_attempt` applies the observation immediately only at stage example (no rating, convention 3) and defers it at completion and unsupported until `record_confidence` supplies the rating, which runs the single update.

Session 2026-09-19 (third session), suite line at open `72 passed in 14.53s`, at close `93 passed, 1 warning in 15.74s` (the warning is starlette's own anyio alias deprecation). Style gate exit 0 on every touched file; `qa/12_report.py` exit 0; `data/`, `research/`, `docs/` and `qa/` untouched. Slice: HTTP layer and account lifecycle, 11 P1 scope items 13, 14 and 15.

- Agent A, HTTP and passkey auth: `app/api/{app,deps}.py`, `app/api/routes/{auth,me,sessions,purge,content,health}.py`, `app/auth/{webauthn,cookies,service}.py`, `passkey_credentials` and `auth_sessions` tables in `app/db/models.py`, `tests/api/`, `tests/auth/`: test_purge_requires_reauth (gate 24), test_register_refused_once_users_nonempty, test_login_finish_sets_httponly_lax_cookie, test_sign_count_regression_refused, test_session_routes_open_next_attempt_confidence_close, test_session_routes_require_the_cookie, test_healthz_localhost_only, test_reauth_token_single_use, test_content_snapshot_route_reports_the_active_row, test_me_reports_exam_and_purge_dates, test_library_verifier_names_the_missing_package. WebAuthn verification sits behind `PasskeyVerifier`; `LibraryVerifier` imports the `webauthn` package lazily and raises naming it when absent, and every test drives a `FakeVerifier`, because 06 names no WebAuthn library and this session's rule was to add none. Re-authentication is `POST /auth/reauth/begin` and `/finish`, an assertion ceremony 06's table lacks. The purge confirmation string is `PURGE_CONFIRMATION = "DELETE EVERYTHING"` in `app/api/routes/purge.py`. Session cookie `calcbc_session`, HttpOnly, SameSite=Lax, Secure off loopback only.
- Agent B, services: `app/session/seed.py` (618 rows, 77 BC-PRQ plus 6 external BC-SKL parents mastered, beta from `beta_for_skill` elsewhere), `app/session/purge.py` (audit entry first, every user table, audit_log last), `record_judgment` and the close-session sweep in `app/session/service.py`: test_seed_writes_618_rows_with_83_mastered, test_seed_beta_matches_prior, test_seed_refuses_second_run, test_close_session_applies_unrated_attempts_as_unsure, test_judgment_never_enters_credit, test_purge_empties_user_tables_and_writes_final_audit, test_purge_audit_entry_precedes_deletion.
- Integrator, after the fresh review: `POST /sessions/{id}/close` now passes the engine context so the sweep runs over HTTP (test_close_route_applies_unrated_attempts, red `ValueError: close_session needs archetypes, engine_graph and today`); the judgments route calls `service.record_judgment` and refuses an unknown scope_id or a retention outside 0 to 1 (test_judgment_route_validates_scope_id_and_retention, red `assert 400 == 200`); registration seeds from `settings.resolve_snapshot()` (test_register_finish_seeds_from_the_resolved_snapshot, red `AttributeError: 'World' object has no attribute 'settings'`); purge deletes `passkey_credentials` and `auth_sessions` through the models (test_purge_deletes_credentials_and_auth_sessions, green on write, red `1 failed` under a mutation that skipped the credential delete); one `random.Random(rng_seed)` per process on `Settings.rng` instead of a fresh one per `POST /sessions`; `tests/db/test_models.py` table set extended by the two new tables; `test_session_routes_open_next_attempt_confidence_close` corrected to send its archetype id under scope `archetype`, since it had been storing an archetype id under scope `skill`.

Session 2026-09-20 (sixth session), suite line at open `161 passed in 19.56s`, at close
`191 passed in 23.40s`, both taken with `--ignore-glob="* 2.py"`. Style gate exit 0 on all 15
changed files, fed the hook its JSON payload on stdin and confirmed to bite with a positive control
(`style_gate: gatecheck.py: em dash present`, exit 2). `qa/12_report.py` exit 0; `data/`,
`research/`, `docs/` and `qa/` untouched, checked with `git status --porcelain` on those four
paths. Slice: everything the fifth session named as blocking gate 23 that needs no hand-authored
item, no design token and no provider key. Gate 23 is not claimed and no new gate name from 11 is
claimed.

- Agent A, serve-time format resolution (R16, R29, gate 12): `app/session/service.py`,
  `tests/session/test_serve_format.py`: test_first_unsupported_serve_is_short_answer,
  test_second_unsupported_serve_on_the_same_archetype_is_mcq,
  test_example_and_completion_slots_are_always_short_answer,
  test_serving_twice_without_submitting_returns_the_same_format,
  test_the_served_format_is_persisted_on_the_queue_slot. `resolve_served_format` re-reads R29
  against the attempts as they stand and writes the answer back onto the queue slot; the stage
  stays frozen at assembly.
- Agent B, elaborated feedback without a BC-ERR record (03 Content, R12 rule 3):
  `app/feedback/render.py`, `tests/feedback/test_render.py`:
  test_wrong_short_answer_without_an_error_record_still_elaborates,
  test_absent_error_fields_are_empty_and_never_invented,
  test_the_violated_step_falls_back_to_the_last_path_step,
  test_the_tutor_payload_is_still_exactly_the_four_fields,
  test_no_scoring_consequence_when_the_archetype_supplies_none. Of the 13 P1 archetypes 8 carry
  `point_types: []` and 5 carry BC-PT id lists; no archetype record carries `does_not_earn` text.
- Agent C, the error-note route (06's API surface has no row): `app/api/routes/sessions.py`,
  `tests/api/test_error_note.py`: test_error_note_route_stores_the_note_on_the_attempt,
  test_error_note_route_requires_the_cookie, test_error_note_route_refuses_an_unknown_attempt,
  test_error_note_route_refuses_an_empty_note.
- Agent D, wiring and audit gaps: `app/main.py`, `app/api/routes/auth.py`, `app/session/build.py`,
  `tests/api/test_wiring.py`, `tests/session/test_coverage_audit.py`:
  test_main_wires_a_tutor_when_a_key_is_configured,
  test_main_builds_without_a_tutor_when_no_key_is_configured,
  test_main_respects_an_explicit_none_provider_even_with_a_key,
  test_building_the_application_opens_no_socket, test_reauth_finish_writes_an_audit_entry,
  test_a_fail_closed_coverage_gap_writes_an_audit_entry,
  test_the_audit_entry_names_the_skill_and_the_reason. Audit actions `reauth_established` and
  `coverage_gap_fail_closed`.
- Integrator: `open_session` passes `db` and `user_id` into `assemble_session`, so the coverage-gap
  audit fires on the production path and not only in a direct call
  (test_open_session_writes_the_coverage_gap_audit_entry, red `assert 0 >= 1`); the wrong short
  answer reaches elaborated feedback over HTTP
  (test_a_wrong_short_answer_gets_elaborated_feedback, test_the_absent_error_fields_are_empty_over_http,
  both shown red by a positive control that restored the old refusal inside `elaborated_payload`,
  `KeyError: 'elaborated'`, then restored).
- Integrator, after the fresh review, which found two blocking defects and reproduced both:
  `record_attempt` now resolves the format on the write path too, because gate 12 states the
  property over `attempts.format` and a client that never calls `GET /next` recorded the
  assembly-frozen format, which would have granted full credit on an attempt R29 says was MCQ
  (test_an_attempt_that_skipped_the_serve_still_records_the_resolved_format, red
  `At index 1 diff: 'short_answer' != 'mcq'`); `tests/api/test_routes.serve_as_mcq` no longer
  writes `mcq` onto the queue row, which the write-path resolution now overwrites, and instead
  consumes a real prior stage-unsupported attempt so the MCQ case is earned through R29 (seven
  HTTP tests went red on the old helper and pass on the new one); the tutor is opt-in through
  `GROWTH_TUTOR_PROVIDER`, default none, because 07 puts the budget guard, the usage accounting
  and the audit trail at the provider seam and P1 has built none of the three, so a key sitting in
  the environment no longer wires a billed role (test_a_stray_key_alone_wires_no_tutor); the
  coverage-gap audit row is stamped by `write_audit` with the wall clock rather than with the
  engine's session clock, which is local midnight of `today` and wrote `2026-03-01T05:00:00+00:00`
  for a row written in September (test_the_audit_entry_is_stamped_with_the_real_moment); the gap
  guard now checks `user_id` as well as `db`, since `audit_log.actor` is NOT NULL; the error-note
  route refuses a note on an attempt that was not corrected, per 02's block 4
  (test_error_note_route_refuses_a_correct_attempt, red `200 != 409`), and the test that stored a
  note on a correct attempt was rewritten to submit a wrong answer; a distractor whose
  `error_path` does not resolve in the snapshot is refused again rather than composing an empty
  payload, which restores the negative case the agent's deletion had dropped
  (test_a_distractor_whose_error_path_does_not_resolve_is_refused, red `DID NOT RAISE ValueError`).

## In progress [inferred]

Session 2026-09-20 (eighth). Suite line at open `230 passed in 34.85s`. Phase stays P1: 11's P2
entry criterion is "P1 merged with all gates green" and P1 has five gates open, so P2 may not
start. The five open P1 gates are 17, 22, 25, 26, 29 and 30, and every one of them is human-only
at its core. What this session builds is the whole of Buildable now plus the operator unblock kit
for the human-only list, so that each remaining gate is one operator artefact away from green.

Declared interfaces, written before any module starts, so wave 2 builds against these rather than
against wave 1's code.

- `app/design/contrast.py`: `relative_luminance(hex_color) -> float` and
  `contrast_ratio(hex_a, hex_b) -> float`, taking `#rgb` or `#rrggbb`, case insensitive, raising
  `ValueError` on anything else.
- `app/db/migrate.py`: `missing_columns(engine) -> dict` mapping table name to a tuple of column
  names declared on `Base.metadata` and absent from the live database; `apply_additive_migrations
  (engine) -> tuple` returning the `table.column` strings added; `SchemaDriftError(RuntimeError)`
  raised when the drift is not additive or the missing column is NOT NULL with no server default.
- `app/audit/vocabulary.py`: one new action `provider_result_unreadable`.
- `app/items/distractor_paths.py`: `error_ids_for_skills(snapshot, skill_ids) -> frozenset` and
  `distractor_path_violations(record, error_ids) -> list` of human-readable violation strings,
  empty when gate 30's property holds of the record.
- `app/review/verdicts.py`: `verdict_violations(record) -> list` and
  `audit_completeness(records, sample_ids) -> dict` carrying the audited count, the missing ids and
  the published key error rate.
- `app/design/tokens.py`: `TYPE_TOKENS` and `COLOUR_TOKENS` scanned from 08's own tables and role
  list, `load_tokens(path) -> dict`, `token_violations(tokens) -> list`.

Wave 1, seven modules, disjoint files and disjoint test names.

- M1, integrator: `tools/gate_status.py`, `tests/tools/test_gate_status.py`. Reads the gate list
  out of `docs/plan/11-phased-delivery.md` for every phase, greps `tests/` for each gate's test
  name and prints phase, gate number, test name, present or missing.
- M2: `app/db/migrate.py`, `tests/db/test_migrate.py`. Closes the `attempts.tutor_sentence` defect.
- M3: `app/providers/guard.py`, `app/audit/vocabulary.py`, `tests/providers/test_guard_settle.py`.
  Closes the silent `_settle` defect with an audit action, deduped per user per role per day.
- M4: `app/design/contrast.py`, `tests/design/test_contrast.py`. Gate 26's arithmetic.
- M5: `app/items/distractor_paths.py`, `tests/items/test_distractor_paths.py`. Gate 30's property
  as a checker the operator can run before an item is published.
- M6: `app/api/routes/sessions.py`, `tests/api/test_error_note.py`. One note per corrected item,
  per 03's "the student writes one line", closing the silent-overwrite defect.
- M7: `app/review/verdicts.py`, `tests/review/test_verdicts.py`. Gate 29's completeness and rate.

Wave 2, the operator unblock kit.

- M8: `app/design/tokens.py`, `tools/check_tokens.py`, `tests/design/test_tokens.py`,
  `docs/operator/design-tokens.template.json`.
- M9: `tools/check_items.py`, `tools/check_audit_verdicts.py`, `tests/tools/test_operator_clis.py`.
- M10: `docs/operator/README.md`, `docs/operator/items.md`, `docs/operator/key-audit.md`,
  `docs/operator/design-tokens.md`, `docs/operator/provider-key.md`.
- Integrator: wires `apply_additive_migrations` into `app/main.py`, and strengthens gate 23's
  archetype assertion.

## Known defects [verified]

- From the seventh session's review, not fixed. `attempts.tutor_sentence` has no migration. The
  column reaches an existing `var/growth.db` only through `Base.metadata.create_all`, which does
  not alter a table that already exists, so a database created before this session will raise on
  the first feedback read. No migration tool is in `06-architecture.md` and adding one was out of
  the slice. Until then, an existing development database is deleted and re-created.
- From the seventh session's review, not fixed. `GuardedProvider._settle` swallows a pricing or
  usage failure with no audit row, so an unreadable provider result is visible only as a budget row
  left at the worst-case estimate. The audit vocabulary is closed and no action name covers it.
- From the seventh session's review, accepted rather than fixed. Gate 23's subset assertion checks
  membership in the 13, so a regression that serves only one of them still passes. Six of the 13
  are unreachable at cold start because each one's primary skill has a hard prerequisite that is an
  ordinary BC-SKL rather than one of the 25 seeded assumed-mastered parents, and BC-QA-01004's
  gating parent BC-SKL-01028 is one of BC-QA-01004's own skills, so it can never open. That last
  one looks like a library shape worth a question rather than a test defect.
- From the seventh session, a behaviour change to note. `compose_sentence` now returns `None` where
  it used to return `""` when a provider returns an empty string, on the uncached path as well.
  Nothing in the suite depended on the old reading and the route treats a missing sentence as the
  degradation case.

- From the sixth session's review, not fixed. The tutor is still called from the feedback route on
  every GET with no budget guard, no usage accounting and no `audit_log` write, which is the seam
  07 describes; the sixth session only made the role opt-in so an unconfigured deployment cannot
  spend. Until that seam exists, `GROWTH_TUTOR_PROVIDER=anthropic` is a deliberate operator choice
  to spend without a cap.
- `write_coverage_gap_audit` writes one row per gap per `open_session` with no dedupe, so a
  permanent coverage gap produces a row every session for the life of the deployment. 06 asks for
  the gap to be written to `audit_log`, not for a per-session heartbeat.
- The error note takes any length and a repeat POST silently overwrites the previous one, although
  02's block 4 says one note per corrected item. 06 sets no cap, so none was invented.
- `reauth_established` and `coverage_gap_fail_closed` are free strings at their call sites. 09 asks
  for an action drawn from a controlled vocabulary and nothing in the code enumerates one. The
  reauth entry carries `detail=None`, so it records that a re-tap happened but not what it gated.
- `scoring_consequence` is empty on every wrong short answer, so feedback carries two of 03's three
  required parts on that path. See Plan corrections for why the BC-PT branch was not implemented.

- From the fifth session's review, not fixed. Session assembly freezes `format` on every queue slot
  at assembly time, so the R16 alternation never happens inside one session: every item of a fresh
  session is served as short answer, and an MCQ case exists over HTTP only when a test rewrites the
  queue row. Because R12 rule 3 gives a wrong short answer no error path, and
  `elaborated_payload` refuses to compose without a BC-ERR record, elaborated feedback is
  unreachable through the natural P1 flow. These two together are what block gate 23
  `test_session_login_to_feedback`, along with two smaller gaps: no HTTP route writes the error
  note that gate 23 names, although `service.record_error_note` exists, and
  `tests/fixtures/provider_cassettes/` does not exist, so "no network calls outside the recorded
  cassettes" has no cassettes to replay. `app/main.py` also sets no `settings.tutor`, so the one
  wired role is wired only in tests.
- The static prefixes of both prompt templates are far short of the 1,024-token minimum that binds
  on claude-sonnet-5: `guardrailed_practice_v1.md` is 2,473 characters and `elaborated_v1.md` is
  1,641, which is roughly 620 and 410 tokens. Gate 22 would fail on length, not merely be
  unmeasurable, and the plan's own trap is that a short prefix is processed uncached with no error.
- `AnthropicProvider.stream` sets `"stream": true` and then parses the body as JSON, so the first
  real streaming call raises a decode error on the `text/event-stream` response. No test covers it
  because every test feeds a dict back. 07 gives no concrete SSE to normalised event mapping that
  could be validated without a key.
- `app/providers/anthropic.py` refuses `thinking` in `provider_options` outright, including the
  adaptive form 07 names as the correct one for Claude 4.7 and later, and drops `provider_options`
  rather than passing it through. Defensible for a tutor that needs none, a deviation for the P4
  generator. The result field is `stop_reason` where 07's shape names `finish_reason`.
- The tutor is called from the feedback route on every GET, so re-reading the screen re-spends and
  returns a different sentence, and the `usage` block is discarded, so nothing feeds a budgets row,
  the cache hit rate or `audit_log`. 07 puts the budget guard, the usage accounting and the audit
  trail at the provider seam.
- A BC-ERR record whose skills are all outside the archetype leaves `error_path_skills` empty, and
  `rule_based_mastery_states` then falls back to blaming the primary skill, which is R12 rule 3's
  behaviour for an answer with no error path. The fallback predates this session; the grader is
  what starts feeding it real error paths.
- `equivalence` now returns without a bound when it runs off the main thread, which is where a sync
  FastAPI route runs. The `signal` crash is fixed and the timeout is not replaced, so a
  pathological submission can pin a worker thread. The exposure is one authenticated user on their
  own installation.
- `record_attempt` persists the submitted body verbatim in `attempts.response`, so a claimed
  `"correct": true` is stored beside the server verdict that overrode it.
- `audit.write_resolution_audit_entry` hard-codes the `item_audit` kind, so resolving a row of any
  other kind is logged as an item audit. `resolve_item_audit` passes `row.ref_id` rather than the
  row, so `record_item_audit_verdict` re-looks-up the open row by item id and would resolve the
  wrong one if two were open for the same item.
- `_misnotated` treats any units mismatch as `notation_only` with correct true, which credits 0.25
  for an answer whose units are dimensionally wrong. 03's check 4 asks for units present and
  dimensionally correct; R12 rule 4 is loose enough to permit the reading.
- Three tests assert less than their names claim, and none of them is a gate from 11:
  `test_next_item_never_carries_the_answer_key` checks only that the literal string `answer_key` is
  absent and never checks `is_key` or `error_path`, which are what identify the key;
  `test_the_tutor_receives_only_the_four_selected_fields` proves no "only" and never inspects
  `request.system`; `test_prompt_templates_are_versioned_and_golden` holds no snapshot or digest,
  so any rewrite of either template passes it.
- The working tree carries 24 untracked files whose names end in `" 2.py"`, copies made by a file
  sync. pytest collects them and reports `200 passed` instead of `161 passed`, so every count in
  this ledger is taken with `--ignore-glob="* 2.py"`. They are the operator's to delete.


- From the fourth session's review, not fixed: `close_session` sweeps graded, unrated attempts and
  applies them with `Confidence.UNSURE`, which is an observation the student never rated entering
  `c_k`, `distinct_archetypes_succeeded` and `success_days`; it rests on the operator's second
  session instruction, not on a plan sentence, and `close_session` now raises `ValueError` (409)
  when no engine bundle is supplied, so a caller without one cannot close a session at all.
  `reauth_finish` writes no audit entry although 09 records "a session established from a new
  authenticator". `app/review/audit.py` divides the key error count by the verdicts recorded
  rather than by the sample size, which reads correctly only because `verdicts_complete` ships
  beside it. Coverage gaps from the fail-closed rule go into `sessions.queue` rather than
  `audit_log`, which 06's traceability row asks for; pre-existing, and live now that the real bank
  is wired. `app/items/verify.py` still splits options on a null `error_path`; only the ingestion
  path was corrected to read `is_key`.
- Recovery issues a replacement code after a successful recovery. 09 says a code is "generated once
  at registration", so this is a deviation; without it a recovered account has no recovery path
  left. The plaintext replacement is returned once in the finish response.
- `app/runtime/bank.py` decides what a served item may carry. Anything a later phase adds to the
  `items` row is withheld from the student by default and has to be added to `_as_item_dict`
  deliberately.

- From the third session's review, not fixed: registration issues no recovery code (09 Recovery requires one, hashed, shown once); purge leaves `review_queue`, `jobs`, `items`, `item_verifications` and `content_snapshots` untouched because they carry no `user_id`, and it empties `audit_log` globally, so the purge audit entry itself does not survive; no ASGI entrypoint builds `Settings`, resolves the snapshot and the `SessionContext` for a real run, so `create_app` is reachable only from tests; `LibraryVerifier`'s calls into the `webauthn` package have never executed; challenges live in a per-process `ChallengeStore` with a 300 second TTL; the Secure flag derives from `bind_host` rather than the request scheme; audit actions `session_established` and `session_closed` are not in 09's vocabulary; no per-IP rate limit, CSP or HSTS middleware.
- `test_purge_requires_reauth` drives a purge double, so no HTTP test runs the real `purge_user`; the real one is covered in `tests/session/test_purge.py` only.
- Gate 31 margin is thin: pooled 0.0604 against 0.0556 on the fixed per-trajectory seeds, and on ceiling and slipper the control arm scores higher per item than the policy. The pooled win comes from the policy serving fewer items on absent_30_days and floor (block 1 requeues), not from faster mastery. A different seed set could flip it. The eval asserts pooled only, as written.
- Dependants of BC-SKL-02025 do reach mastery in the prereq_gap trajectory as secondary loaded skills of archetypes whose primary is ungated (BC-SKL-02044, 02045 via BC-QA-02010; BC-SKL-03006 via BC-QA-03001). Invariant 3 gates on the primary skill only, so this is plan-conformant; `test_simulation_prereq_gap_stalls_dependants` asserts that no mastered dependant was credited by an archetype whose primary is itself a dependant. Whether secondary loading should be gated too is a 02 question.
- `test_simulation_prereq_gap_stalls_dependants` asserts gating on the served trace and is load-bearing; its second clause (dependants of BC-SKL-02025 unmastered) is vacuous until mastery is reachable.
- `app/sim/runner.py` reads `tests/fixtures/graph_p1.json` and `tests/fixtures/student_trajectories/` by path and synthesises 10 published items per archetype because `tests/fixtures/items_p1/` does not exist; when the 130 items land, the bank should be read from them.
- Session service: an attempt at stage completion or unsupported whose confidence rating never arrives is never applied, and nothing sweeps abandoned sessions. Stage example fabricates `Confidence.UNSURE` because `grade_for` requires a rating and convention 3 collects none there. `transcription_confirmed` is not enforced as a precondition on the update (P1 has no transcription). `constants.LAMBDA` is 0 in P1, so the retrievability passed into the logged predictions is inert until the lambda arm turns on. Nothing seeds the 618 `skills_state` rows at account creation; tests seed from the fixture.
- Reconciliation: consecutive counters are zeroed on merge, an inferred choice recorded in `ReloadReport.notes`; a `skills_state` row whose id is neither active nor in `ids.json` refuses the reload (folded into the pseudocode's final else). Orphaned rows are surfaced only through the report and `audit_log` (`skill_orphaned`); nothing in selection excludes them yet.
- Resolved 2026-09-19: `data/prereq_edges.csv` carried a cycle over the full typed edge set (BC-SKL-05020 to BC-SKL-05021 hard_prerequisite, BC-SKL-05021 to BC-SKL-06023 supporting, BC-SKL-06023 to BC-SKL-05020 supporting) because one supporting row was stored in the reverse direction. The row was flipped (see Decisions); `tools/graph_check.py` reports 0 cycles, test_graph_acyclic and test_loader_against_real_data pass, and the helper test that removed the cycle from a temporary copy was deleted as obsolete. A full `tools/merge_staging.py` replay after the flip regressed unrelated evidence links in archetypes, scoring_points and skills, so those three registries and `data/staging/sync-dependents.json` were restored to HEAD; the replay order in that tool lets older staging files overwrite later link-evidence merges, which the library owner should look at before the next merge.
- FSRS-7 forms: docs/plan/02 transcribes stability and difficulty updates with parameter indices that do not match the shipped model (the plan's w7 as an exponent on S made stability explode by about 500x per review; its difficulty step had the sign inverted). Per R28 the forms are copied from the reference implementation instead, fsrs-rs at commit c137ee6e096f9217632397a8fb2bdb6f6e1b92ae, `src/model_v7.rs` and `src/inference_v7.rs`, cross-checked against srs-benchmark `models/fsrs_v7.py`; the source is recorded in `app/engine/fsrs.py` and the vector's source file is committed as `tests/fixtures/fsrs_rs_inference_v7_c137ee6.rs` with its sha256 in `app/engine/fsrs_constants.py`. The awesome-fsrs wiki page R28 names documents only v0 to v6.
- FSRS-7 carries a second, fast stability per card that the P1 schema does not store; `app/engine/fsrs.py` reconstructs it as 0.8 times the long stability, which is the source's own SM-2 bridge. A `fast_stability` column is a P2 schema decision.
- The mastery corroboration test `test_stability_bounded` shows stability saturating at the source's 36500-day clamp after about 12 successive Good reviews at elapsed = S; retrievability still decays below 0.90 at large elapsed times. Whether that clamp is acceptable for an exam horizon of months is unexamined.
- `drain_probe_queue` in `app/engine/fringe.py` still takes `now` as a required positional; every public entry point supplies it through `session_now`, so only a direct call without it raises. `session_now` accepts a datetime `today`, but the rest of the selection path compares dates, so pass a date.
- `qa/last_report.json` is regenerated whenever `qa/12_report.py` runs and is restored with `git checkout -- qa/last_report.json` at session close, so the library's committed report does not drift because of build sessions.

## Plan corrections applied [verified]

Session 2026-09-20 (seventh).

- `docs/plan/06-architecture.md`, the `attempts` table: a `tutor_sentence` nullable column was
  added to the field list. The sentence is one-to-one with the attempt, dies with it under purge
  and carries the same retention as `error_note` and `self_explanation`, so a separate table would
  buy nothing and would need its own purge join. Without the column a re-read of the feedback
  screen spends a second tutor call against the daily cap 07 sets.
- `docs/plan/06-architecture.md`, the API surface row for
  `GET /sessions/{id}/attempts/{aid}/feedback`: the model role read `diagnostician`, which
  contradicts R35 and 11's P1 scope, where the tutor writes the P1 sentence and no diagnostician is
  wired until P3. It now reads tutor in P1, diagnostician from P3, and names the `tutor_unavailable`
  field the route returns when the cap has stopped the role.
- `docs/plan/09-security-and-privacy.md`, the Audit log Recorded sentence: extended with the role
  stopped by its budget cap, the call refused by it and the fringe archetype excluded for want of a
  published item, and with the statement that an ordinary provider call is not recorded because its
  accounting lives in `budgets`. The vocabulary is now enumerated in code at
  `app/audit/vocabulary.py` and a write outside it is refused, so the word controlled is true of the
  code and not only of the prose.
- `docs/plan/12-open-questions.md`, the tunables table: two rows added. The tutor daily cap at $1.00
  with the token cap unset, and the client token estimate divisor at 4 characters per token. 07 sets
  no number for either and the guard cannot run without both, so each is inferred here with what
  settles it. The divisor in particular is the unsafe direction: 07 records the Claude 4.7 tokenizer
  producing about 30 percent more tokens for the same text, so 4 likely under-estimates.


- 03 Content part 2 gives the scoring consequence as the BC-PT `does_not_earn` text when no error
  matched. `app/content/loader.py` does read `data/scoring_points.json` and the archetypes carry
  BC-PT ids, but that text answers which point the response failed to earn, and naming one of an
  archetype's several point types needs the per-point decision 03 puts behind mechanic 6, which P1
  has no component to make. The field stays empty rather than naming a guessed exam consequence.
- 06's API surface has no row for the error note although the `attempts` table carries the column.
  The build adds `POST /sessions/{id}/attempts/{aid}/error-note`, refused unless the attempt was
  corrected, per 02's Session assembly block 4.
- 09's audit vocabulary has no entry for re-authentication or for a fail-closed coverage gap. The
  build writes `reauth_established` and `coverage_gap_fail_closed`, which the operator should carry
  into 09's list or rename there.
- 11 gate 12 states the alternation over `attempts.format`, so R29 is resolved both when a slot is
  served and when the attempt is written. A format frozen at assembly was the only thing any test
  had ever checked, and the serve path alone left a client that skips `GET /next` recording the
  frozen value.
- 07 puts the budget guard, the usage accounting and the audit trail at the provider seam. P1 has
  none of the three, so the composition root wires the tutor only when `GROWTH_TUTOR_PROVIDER`
  names a provider; an `ANTHROPIC_API_KEY` alone wires nothing.

- 03's rule-based assignment names a mis-notated answer as one of P1's four answer shapes but gives
  no mechanical notation check. Check 4 of 03's deterministic pre-checks, units present, is the
  only one a P1 item record can carry, so it is the only one implemented, and an item whose key
  declares no units can never report `notation_only`.
- `grade` takes the served format explicitly, because 04's Output schema lets an item carry options
  and be served either way, and R16 and R29 put the MCQ and short answer alternation on the attempt
  history rather than on the item.


- 06 API surface has no row for the recovery ceremony, and 09's registration rule keeps
  `/auth/passkey/register/begin` closed once the installation has a user, so recovery runs at
  `POST /auth/recovery/register/begin` and `/finish`. The existing 403 gate on ordinary
  registration was not loosened.
- 06 calls `item_audit` the only `review_queue` kind P1 writes, while 04 and 06 both route an
  indeterminate symbolic check to `review_queue`, and 11 P1 scope 14 says `item_audit` holds the
  operator's hand-audit verdicts on published items. The routed row carries
  `item_verification_disagreement`, because `app/review/audit.py` computes gate 29's published key
  error rate over `item_audit` rows and an ingestion artefact must not move that number.
- 04's Output schema makes `is_key` required on every option, so the key is read from it. Reading
  the key as "the option whose `error_path` is null" made rejection rule 7 unreachable and could
  compare every distractor against another distractor when the mis-authored option came first.
- 06's `items.status` vocabulary is draft, verified, rejected, retired. A failed check now sets
  `rejected`, which 04 wants kept with its provenance; `draft` is reserved for an unsettled check.
- 11 P1 scope 10 and 13 (R35) say nothing reaches the student before submission, and the plan does
  not say which fields a served item carries. `app/runtime/bank.py` withholds `answer_key`,
  `worked_solution`, `provenance` and the per-option `error_path` and `is_key` fields, because a
  served item is copied into `sessions.queue` and returned by `GET /sessions/{id}/next` before
  anything is submitted, and a null `error_path` would have identified the key by inspection.
- The application is named Growth on the operator's instruction. No plan document names the
  product, so nothing in docs/plan changed.

- 06 API surface: re-authentication has no row; the build adds `POST /auth/reauth/begin` and `/finish` because 09 forces re-authentication for purge. 09 "typed confirmation": the string is fixed as `DELETE EVERYTHING`. 09 sign-count regression: refused when the offered counter is below the stored one, or equal while the stored one is non-zero. 06 `users.purge_after`: exam date plus 30 days, 2027-06-09 on the default. None of these edits docs/plan; the sentences are recorded here for the operator to carry into 06 and 09.
- `skills_state.snapshot_id` at seeding is the `content_snapshots` row id from `SessionContext.snapshot_id`, per the 06 correction above; `seed_skills_state` falls back to the digest only when no row id is supplied.
- 06 `skills_state.snapshot_id` holds the `content_snapshots.id` row id, not the digest; 06 never says which. `reconcile_skills_state` takes the row id explicitly.
- 06 reconciliation pseudocode is silent on `difficulty`, `fading_stage`, the consecutive counters, `hypercorrection_due`, `concept_opener_done` and `unaided_success_count`; the code carries difficulty with the winning stability, earliest stage, latest hypercorrection date, OR of the opener flag, summed unaided successes, zeroed counters.
- 02 invariant 23 does not say whether the two logged predictions use retrievability 1.0 or current retrievability; the service and the runner both use current retrievability, and `p_split` is `p_knowledge` without the MCQ guessing floor so the two columns share a scale.
- 10 "The world" says synthetic students range over the real 541-skill graph; gate 31 and the trajectory fixtures range over the 54-skill `graph_p1.json`, which is what the runner uses. Gate 31 does not say pooled or per trajectory; the eval asserts pooled and prints per trajectory. 10 arm 2 does not say whether the control is fringe-random for block 2 only or the whole session; the control pins retrievability to 1.0 for the whole session, which empties the due set and leaves the arms one term apart.
- 06 `sessions.queue` "interleaving constraints recorded as satisfied": P1 records one boolean `interleaving_satisfied` for the max-2 rule, the only one enforced.
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

## Decisions taken on the operator's instruction, 2026-09-20 [inferred]

Sixth session, on the instruction "answer all decisions for me". Every open question the ledger
held for the operator is answered here. None of these is implemented yet except the last; they are
the standing answers the next slice builds against.

- A wrong short answer does get elaborated feedback in P1, as built this session. R12 rule 3 gives
  it no error path, so it carries the violated step and the worked solution and leaves the two
  BC-ERR fields empty. Feedback that names the step beats no feedback at all on the whole short
  answer path, and 03's Content section already contemplates an archetype with no matched error.
- `tests/fixtures/items_p1/` may be filled with synthetic items for gate 23. Gate 23's property is
  the flow, login to feedback to a persisted `skills_state` change, not item quality, so a fixture
  item exercises it honestly. Gates 17, 29 and 30 are item-quality gates and still wait for the 130
  hand-authored items; no synthetic item may be counted toward them, and the fixture directory
  carries a README saying so.
- Cassettes under `tests/fixtures/provider_cassettes/` may be hand-written fixtures rather than
  recordings, until a key exists. A cassette is a fixture response for `ReplayProvider`, so writing
  one by hand proves the replay path and the no-network rule. Every hand-written cassette is marked
  synthetic in the file, and gate 22's token count still waits for a real key.
- Purge truncates the tables that carry no `user_id`: `review_queue`, `jobs`, `items` and
  `item_verifications`. The installation is single-user, so every row in them is that user's work.
  `content_snapshots` is kept, because it is derived from the read-only library and holds nothing
  the student wrote. The purge audit entry survives the purge instead of being deleted with the
  rest of `audit_log`.
- py_webauthn (`webauthn` on PyPI) is approved for `pyproject.toml` and is to be named in 06 when
  the dependency lands.
- The error note is capped at 500 characters and a second POST replaces the first. One note per
  corrected item is 02's rule; replacing a note is editing it, not adding a second one.
- `reauth_established` and `coverage_gap_fail_closed` join 09's audit vocabulary, and the code gets
  one module-level enumeration of action names so the vocabulary is controlled in fact and not only
  in the plan.
- The coverage-gap audit writes one row per user per archetype and skips a gap already recorded,
  rather than one row per session opened.
- The tutor stays opt-in through `GROWTH_TUTOR_PROVIDER` until 07's budget, usage and audit seam is
  built. That seam is the next slice.
- The 24 stray `* 2.py` files were deleted. Twenty-two were byte-identical to their counterparts,
  and `tests/api/conftest 2.py` and `tests/items/test_verify 2.py` were strictly older versions of
  files that still hold everything they held. The suite now reports `191 passed` without
  `--ignore-glob`.

## Decisions taken on the operator's instruction, 2026-09-19 [inferred]

Second session, on the instruction "decide anything that needs my input yourself":

- Gate 31: both structural causes were corrected in the engine and the plan rather than in the fixture, because the real library has the same shape (440 of 522 listed skills sit in exactly one active archetype, `data/archetypes.json`). `gamma` 0.4 to 1.0 and `rho` -0.2 to -0.5 in `app/engine/constants.py`, 02, 11 and 12; 1.0 is PFA's own unit weight on `phi(c)` and keeps the 2 to 1 asymmetry. Mastery condition 3 becomes min(2, archetypes listing the skill in the active snapshot) via `EngineGraph.archetype_counts` and `evaluate_mastery(state, today, archetypes_available)`; a graph without counts keeps the old unconditional 2.
- Three selection-test fixture rows lacked the `stage` key that every production attempts row carries (`repository.load_attempts_history`, the runner); the new gamma pushed cold-start `p_knowledge` above 0.9 and reached `format_for_attempt`, which reads it. The rows were completed, no assertion changed.
- `httpx2` as the test dependency for FastAPI's TestClient.
- WebAuthn: use py_webauthn (`webauthn` on PyPI) when the passkey slice is built; record it in 06 then.
- Attempts at stage completion or unsupported whose rating never arrives: `close_session` will apply them with rating unsure (no hypercorrection can fire from unsure), so no observation is lost; to be built with the routes slice.
- Seeding the 618 `skills_state` rows happens on passkey registration finish, the only account-creation path.

- The prerequisite-graph cycle was closed by flipping the reversed row: `BC-SKL-06023,BC-SKL-05020,supporting` became `BC-SKL-05020,BC-SKL-06023,supporting`, because the row's own note stated that the Unit 6 skill depends on the Unit 5 one, which is the opposite of the direction it was stored in. Applied directly to `data/prereq_edges.csv`, then `tools/sync_dependents.py`, `tools/merge_staging.py`, the post-change tool chain and `qa/12_report.py`.
- The FSRS-7 forms stay as copied from fsrs-rs; 02's transcribed block stays marked superseded.
- The application lives in this repository; the local CLAUDE.md was amended to say so. The style gate keeps its wider `/docs/` scope.
- The build is committed on the branch `build/p1-backend-core`; main is untouched.

## Next candidates [inferred]

Session 2026-09-20 (seventh) leaves P1 with no deliverable buildable without the operator. Every
remaining gate is one of the three human-only classes below.

- Human-only, blocks P1 exit, gates 17, 29 and 30: the 130 hand-authored items, 10 per P1
  archetype, in the record shape `app/items/ingest.py` reads. `tests/fixtures/items_p1/` now holds
  36 synthetic records in exactly that shape, which are a template for the authoring and are marked
  in their README as not countable toward any item-quality gate. Each needs `is_key` on every
  option, a BC-ERR `error_path` on every distractor resolving to an error the archetype's skills
  hold, and MathJSON on the last worked-solution step. Then the 100-item key audit, whose verdicts
  `app/review/audit.py` records and whose rate it publishes.
- Human-only, gates 25 and 26: the design tokens with a named contrast checker, and the screens.
  `app/web/` does not exist.
- Human-only, gate 22: a provider key. The token count of the tutor template's static prefix cannot
  be measured without one, and the recorded cassettes under `tests/fixtures/provider_cassettes/`
  are hand-written until then. `app/providers/anthropic.py`'s wire mapping has still never executed.
- Buildable, small, if a session wants P1 work before the items arrive: a migration path for
  `attempts.tutor_sentence`, and an audit action for a provider result the guard cannot read. Both
  are under Known defects.
- Buildable, the next real slice: P2's entry criteria in 11 decide whether the FSRS scheduling work
  can start while P1 waits on the operator. That is the first thing the next session should read.


- Most likely next slice without human input: the provider seam of 07, meaning the budget row, the
  usage accounting and the `audit_log` write on every provider call, plus caching the tutor
  sentence on the attempt so re-reading the feedback screen does not re-spend and does not return a
  different sentence. That is the last piece of P1 scope 12 that needs no key, and it is what makes
  `GROWTH_TUTOR_PROVIDER=anthropic` safe to turn on.
- Still open and not human-only: deduping the coverage-gap audit rows, a controlled vocabulary for
  audit actions, and the `audit_log` entry 09 asks for on ordinary registration.

- Human-only, blocks P1 exit: 130 hand-authored items (10 per P1 archetype) in the record shape
  `app/items/ingest.py` reads, each with `is_key` on every option, a BC-ERR `error_path` on every
  distractor and MathJSON on the last worked-solution step, which is the second statement of the
  key that the SymPy and numeric checks compare against; the 100-item key audit, whose verdicts
  `app/review/audit.py` records and whose rate it publishes; design tokens with a named contrast
  checker; confirmation that py_webauthn (`webauthn` on PyPI) may be added to `pyproject.toml` and
  named in 06; a decision on whether purge truncates the tables without `user_id`.
- Needs a screen: `app/web/` session, home and settings screens; tests 23, 25, 26.
- Needs a provider key: the recorded tutor cassettes under `tests/fixtures/provider_cassettes/`,
  the token count that gate 22 asserts, and the first real call through
  `app/providers/anthropic.py`, whose wire mapping has never executed. The adapter, the two
  templates and the replay player exist and are exercised without a key.
- Needs items: test 17, eval 29, eval 30; `app/sim/runner.py` should read `tests/fixtures/items_p1/`
  through `app/items/ingest.py` once it exists.
- Most likely next slice without human input: whatever unblocks gate 23. That means resolving the
  served format at serve time rather than freezing it at assembly, so the R16 alternation happens
  inside a session and an MCQ item is reachable; deciding what elaborated feedback says for a wrong
  short answer, which today has no BC-ERR record and so composes nothing; an HTTP route for the
  error note; and `settings.tutor` wired in `app/main.py`. Also still open from the fourth session:
  the `audit_log` write for the fail-closed coverage gap and `reauth_finish`'s missing audit entry.
- Two questions only the operator answers. Whether a wrong short answer at stage unsupported should
  get elaborated feedback at all in P1, given that R12 produces no error path for it and 03 builds
  the elaborated payload out of one. Whether the deliberately empty `tests/fixtures/items_p1/` may
  be filled with a handful of synthetic items for gate 23's sake, or whether gate 23 waits for the
  130 hand-authored ones.
