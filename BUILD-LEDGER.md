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

Session 2026-09-19 (second session), suite line at close: `72 passed in 14.23s`. Gate 31 `eval_simulation_mastery_growth` read `1 failed, 69 passed` at the first close, for the structural reason recorded under Decisions; after the gamma and condition 3 corrections it passes with pooled policy 88 mastered over 1457 items (0.0604) against control 92 over 1656 (0.0556), per trajectory printed by the eval. Style gate exit 0 on every touched file; `qa/12_report.py` exit 0; `data/` and `research/` untouched; `docs/plan/02`, `11` and `12` carry the two corrections below. Integrator-owned tests added: test_mastery_single_archetype_skill_needs_one_archetype, test_mastery_reachable_in_a_dozen_credited_successes (both quoted red before the engine edit).

- Agent A, simulation runner: `app/sim/runner.py`, `tests/eval/test_simulation.py`: test_simulation_reproducible_from_seed, test_simulation_prereq_gap_stalls_dependants (asserts on the served trace: no served item had an unmastered hard ancestor; shown red with gating bypassed, 165 blocked serves), test_simulation_records_both_predictions, eval_simulation_mastery_growth (gate 31).
- Agent B, snapshot persistence and reload reconciliation: `app/content/persist.py`, `app/content/reconcile.py`, `tests/content/test_persist.py`, `tests/content/test_reconcile.py`: test_snapshot_row_written_on_load, test_rejected_snapshot_row_records_reason, test_reload_with_unchanged_digest_reuses_active_row, test_reload_keeps_active_skill_and_sets_snapshot_id, test_reload_rewrites_superseded_skill, test_reload_merges_into_existing_successor_and_recomputes_mastered, test_reload_merge_union_failing_d2_clears_mastered, test_reload_merge_carries_difficulty_with_winning_stability, test_reload_merge_carries_difficulty_from_old_row_when_it_wins, test_reload_merge_preserves_flags_and_resets_consecutive_counters, test_reload_orphans_tombstone_without_successor, test_reload_refuses_inactive_successor, test_reload_writes_audit_entry.
- Agent C, session service and attempts writer (no HTTP layer): `app/session/repository.py`, `app/session/service.py`, `tests/session/test_service.py`: test_open_session_persists_four_blocks, test_attempt_row_logs_split_and_compensatory, test_attempt_updates_skills_state, test_confidence_before_feedback_sets_hypercorrection, test_error_note_stored_on_attempt, test_close_session_writes_ended_at, test_state_round_trip, test_rehearsal_session_writes_no_mastery, test_record_attempt_refuses_duplicate, test_ungraded_answer_skips_the_update, test_timestamps_are_timezone_aware_utc. Confidence design: `apply_observation` already sets `hypercorrection_due` from the rating, so `record_attempt` applies the observation immediately only at stage example (no rating, convention 3) and defers it at completion and unsupported until `record_confidence` supplies the rating, which runs the single update.

Session 2026-09-19 (third session), suite line at open `72 passed in 14.53s`, at close `93 passed, 1 warning in 15.74s` (the warning is starlette's own anyio alias deprecation). Style gate exit 0 on every touched file; `qa/12_report.py` exit 0; `data/`, `research/`, `docs/` and `qa/` untouched. Slice: HTTP layer and account lifecycle, 11 P1 scope items 13, 14 and 15.

- Agent A, HTTP and passkey auth: `app/api/{app,deps}.py`, `app/api/routes/{auth,me,sessions,purge,content,health}.py`, `app/auth/{webauthn,cookies,service}.py`, `passkey_credentials` and `auth_sessions` tables in `app/db/models.py`, `tests/api/`, `tests/auth/`: test_purge_requires_reauth (gate 24), test_register_refused_once_users_nonempty, test_login_finish_sets_httponly_lax_cookie, test_sign_count_regression_refused, test_session_routes_open_next_attempt_confidence_close, test_session_routes_require_the_cookie, test_healthz_localhost_only, test_reauth_token_single_use, test_content_snapshot_route_reports_the_active_row, test_me_reports_exam_and_purge_dates, test_library_verifier_names_the_missing_package. WebAuthn verification sits behind `PasskeyVerifier`; `LibraryVerifier` imports the `webauthn` package lazily and raises naming it when absent, and every test drives a `FakeVerifier`, because 06 names no WebAuthn library and this session's rule was to add none. Re-authentication is `POST /auth/reauth/begin` and `/finish`, an assertion ceremony 06's table lacks. The purge confirmation string is `PURGE_CONFIRMATION = "DELETE EVERYTHING"` in `app/api/routes/purge.py`. Session cookie `calcbc_session`, HttpOnly, SameSite=Lax, Secure off loopback only.
- Agent B, services: `app/session/seed.py` (618 rows, 77 BC-PRQ plus 6 external BC-SKL parents mastered, beta from `beta_for_skill` elsewhere), `app/session/purge.py` (audit entry first, every user table, audit_log last), `record_judgment` and the close-session sweep in `app/session/service.py`: test_seed_writes_618_rows_with_83_mastered, test_seed_beta_matches_prior, test_seed_refuses_second_run, test_close_session_applies_unrated_attempts_as_unsure, test_judgment_never_enters_credit, test_purge_empties_user_tables_and_writes_final_audit, test_purge_audit_entry_precedes_deletion.
- Integrator, after the fresh review: `POST /sessions/{id}/close` now passes the engine context so the sweep runs over HTTP (test_close_route_applies_unrated_attempts, red `ValueError: close_session needs archetypes, engine_graph and today`); the judgments route calls `service.record_judgment` and refuses an unknown scope_id or a retention outside 0 to 1 (test_judgment_route_validates_scope_id_and_retention, red `assert 400 == 200`); registration seeds from `settings.resolve_snapshot()` (test_register_finish_seeds_from_the_resolved_snapshot, red `AttributeError: 'World' object has no attribute 'settings'`); purge deletes `passkey_credentials` and `auth_sessions` through the models (test_purge_deletes_credentials_and_auth_sessions, green on write, red `1 failed` under a mutation that skipped the credential delete); one `random.Random(rng_seed)` per process on `Settings.rng` instead of a fresh one per `POST /sessions`; `tests/db/test_models.py` table set extended by the two new tables; `test_session_routes_open_next_attempt_confidence_close` corrected to send its archetype id under scope `archetype`, since it had been storing an archetype id under scope `skill`.

## In progress [inferred]

Nothing at the time of writing. The next session starts from Next candidates.

Session 2026-09-19 (fourth session), suite line at open `93 passed, 1 warning in 19.90s`, at close
`122 passed, 1 warning in 19.04s`. Style gate exit 0 on every touched file, checked by feeding the
hook its JSON payload on stdin and confirmed to bite with a positive control (`style_gate:
gatecheck.py: em dash present`, exit 2); an argv-only invocation reads no file and exits 0 on
anything, so it is not evidence. `qa/12_report.py` exit 0; `data/`, `research/`, `docs/` and `qa/`
untouched. Slice: the four P1 deliverables that need no hand-authored content, no design tokens and
no provider key, 11 P1 scope items 7, 10, 12 (composition root only), 14 and 15. None of the 31
gates is named by these modules; they unblock gates 17, 29 and 30, which stay blocked on the 130
items and the operator audit.

- Agent A, deterministic elaborated feedback selection (11 P1 scope 10 and 13, R35):
  `app/feedback/render.py`, `tests/feedback/test_render.py`:
  test_step_verification_at_example_and_completion,
  test_nothing_returned_before_submission_at_unsupported,
  test_elaborated_payload_names_violated_step_and_error_path,
  test_scoring_consequence_comes_from_the_error_record,
  test_self_explanation_only_on_examples_and_corrected_errors,
  test_tutor_receives_no_answer_before_submission. The payload the tutor template receives is
  exactly four fields: violated_step, observed_behavior, scoring_consequence, worked_solution.
- Agent B, composition root and live item bank: `app/runtime/{context,bank}.py`, `app/main.py`,
  `tests/runtime/test_context.py`: test_context_builds_from_the_live_registries,
  test_bank_publishes_only_verified_rows,
  test_bank_has_no_published_item_for_a_draft_only_archetype,
  test_main_builds_an_application_without_touching_the_network.
- Agent C, recovery code at registration (09 Recovery): `app/auth/recovery.py`,
  `tests/auth/test_recovery.py`, `recovery_code_hash` on `users`:
  test_recovery_code_is_shown_once_and_stored_hashed,
  test_recovery_code_authenticates_a_new_registration_once, test_consumed_code_is_refused,
  test_recovery_writes_an_audit_entry. PBKDF2-SHA256 at 200,000 iterations, salted, compared with
  hmac.compare_digest; plaintext is returned once and never persisted or logged. Audit action
  `passkey_recovery_used`.
- Agent D, item ingestion and the review-queue audit writer: `app/items/ingest.py`,
  `app/review/audit.py`, `tests/items/test_ingest.py`, `tests/review/test_audit.py`:
  test_ingest_publishes_an_item_whose_key_passes_every_check, test_ingest_refuses_a_seeded_bad_key,
  test_indeterminate_check_routes_to_review_queue, test_verification_rows_written_per_check,
  test_item_audit_verdict_recorded, test_key_error_rate_published_over_the_recorded_verdicts.
- Integrator: the feedback route `GET /sessions/{id}/attempts/{aid}/feedback` from 06's API
  surface, wired to `app/feedback/render.py` (test_feedback_route_returns_the_elaborated_payload,
  test_feedback_route_refuses_an_unknown_attempt, red `KeyError: 'recovery_code'` and a 404 route
  miss before the wiring); registration now issues a recovery code and returns it once
  (test_register_finish_returns_a_recovery_code_once); recovery re-registration at
  `POST /auth/recovery/register/begin` and `/finish`
  (test_registration_with_a_valid_recovery_code_adds_a_credential). `SessionContext` gained an
  `errors` field so the feedback route can resolve a BC-ERR record from the chosen option.
- Integrator, after the fresh review: the served item is redacted (see Plan corrections), with
  test_bank_hides_the_answer_key_and_the_error_paths and
  test_next_item_never_carries_the_answer_key, the second shown red by re-adding `answer_key` to
  `_as_item_dict` (`1 failed`) and green after restoring; option classification now reads `is_key`
  (test_a_distractor_without_an_error_path_is_refused,
  test_the_key_is_read_from_is_key_not_from_a_null_error_path, both red first); a failed check now
  sets status `rejected` rather than `draft`; the ingestion-routed review row carries kind
  `item_verification_disagreement`
  (test_an_indeterminate_verification_row_stays_out_of_the_audit_sample); a duplicate `sole_user`
  the integrator had added was folded into `require_sole_user` over the existing one.
- Operator instruction, same session: the application is named Growth. `pyproject.toml` name
  `calc-bc-tutor` to `growth`, FastAPI title and the WebAuthn relying-party name to `Growth`, the
  session cookie `calcbc_session` to `growth_session`, the environment prefix `TUTOR_` to
  `GROWTH_` in `app/main.py`, the default database `var/tutor.db` to `var/growth.db`, and the
  tmp_path database name in nine test modules. The word tutor is kept where it names the provider
  role of 07 and the `prompts/tutor/` template path, because renaming those would contradict the
  plan. The third session's entry above still records the old cookie name, as history.

Session 2026-09-19 (fifth session), suite line at open `122 passed in 19.73s`, at close
`161 passed in 20.43s`. Style gate exit 0 on every changed file, fed the hook its JSON payload on
stdin and confirmed to bite with a positive control (`style_gate: gatecheck.py: em dash present`,
exit 2). `qa/12_report.py` exit 0; `data/`, `research/`, `docs/` and `qa/` untouched, which the
fresh reviewer checked independently. Slice: the deterministic grader of P1 scope 5 and R12, the
two operator review-queue rows of 06's API surface, and the one wired provider role of scope 12
with the two prompt templates of scope 13. No new gate name from 11 is claimed: gate 22 needs a
live key and gate 23 is blocked for the reasons under Known defects.

- Agent A, deterministic grader: `app/items/grade.py`, `tests/items/test_grade.py`:
  test_mcq_selection_compared_to_the_key, test_mcq_distractor_yields_its_error_path_skills,
  test_mcq_option_set_without_exactly_one_key_is_refused,
  test_mcq_unknown_option_id_is_refused_not_wrong, test_short_answer_equivalence_decides_correct,
  test_short_answer_unequal_blames_the_primary_skill_only,
  test_numeric_key_is_compared_to_three_decimal_places,
  test_units_declared_but_absent_is_notation_only,
  test_units_absent_from_the_key_never_reports_misnotation, test_unparseable_submission_is_ungraded,
  test_indeterminate_comparison_is_ungraded, test_served_format_decides_the_grading_path,
  test_submission_shape_that_contradicts_the_served_format_is_refused. The signature is
  `grade(item, submission, errors, served_format=None)` returning correct,
  equivalent_but_misnotated, error_path, error_path_skills and reason, the first, second and fourth
  of which are exactly the keys `rule_based_mastery_states` reads. The served format is passed
  explicitly because every published item carries options, so shape alone would grade every item as
  MCQ and the short answer path would be unreachable at the HTTP boundary.
- Agent B, operator review-queue API: `app/api/routes/review.py`, `tests/api/test_review_routes.py`:
  test_review_queue_lists_open_rows, test_review_queue_requires_the_cookie,
  test_resolve_records_the_operator_verdict, test_resolve_refuses_an_unknown_row,
  test_resolve_refuses_a_row_already_resolved. An `item_audit` row resolves through
  `record_item_audit_verdict` so gate 29's published key error rate keeps counting the same rows.
- Agent C, provider layer and prompt templates: `app/providers/{base,anthropic,replay}.py`,
  `prompts/tutor/guardrailed_practice_v1.md`, `prompts/feedback/elaborated_v1.md`,
  `tests/providers/`: test_call_maps_to_the_messages_wire_shape,
  test_usage_reports_all_four_token_fields, test_no_tool_definitions_are_ever_sent,
  test_adaptive_thinking_is_never_requested, test_replay_provider_makes_no_network_call,
  test_tutor_template_never_receives_the_answer_key,
  test_prompt_templates_are_versioned_and_golden. The transport is an injected callable and the
  only real one uses `urllib.request`, because 06 names no HTTP client dependency and the
  anthropic SDK is named nowhere in the plan. No test opens a socket and none needs a key.
- Integrator: `equivalence` lost its timeout guard off the main thread, which is where FastAPI runs
  a sync route (test_equivalence_runs_off_the_main_thread, red with
  `ValueError('signal only works in main thread of the main interpreter')`); `Usage` gained
  `reasoning_tokens`, the fifth field of 07's usage block that the builder's brief wrongly omitted
  (test_usage_carries_the_reasoning_token_field); `record_attempt` gained a `grader` callable whose
  verdict overrides anything the submission claims about itself, and
  `POST /sessions/{id}/attempts` always passes one built over the unredacted `items` row
  (test_attempt_is_graded_by_the_server_not_the_body, red `assert 200 == 409` and
  `assert 0 is False`; test_attempt_refuses_an_item_with_no_items_row); the attempts route now
  reports `correct` as a JSON boolean rather than the stored integer; `tests/api/conftest.py`
  publishes a real `items` row for every item the fixture bank serves, so every HTTP attempt test
  grades a real key, and the duplicate `publish_item` helper in `tests/api/test_routes.py` was
  deleted; the tutor role is wired into the feedback route per R35 through `app/feedback/tutor.py`
  (test_feedback_sentence_is_written_by_the_tutor,
  test_the_tutor_receives_only_the_four_selected_fields,
  test_feedback_without_a_tutor_still_returns_the_selected_payload,
  test_the_stored_attempt_is_untouched_by_the_tutor).
- Integrator, after the fresh review: an ungraded attempt no longer earns elaborated feedback and
  its worked solution, which was a live hole the reviewer reproduced, since a submission whose
  shape contradicts the served format was graded as nothing and fed back as everything
  (test_feedback_is_refused_on_an_ungraded_attempt, red on a 200 carrying `worked_solution`); the
  tutor request carries `CacheSettings(prefix_breakpoints=1, ttl="1h")` per scope 12
  (test_the_tutor_call_caches_its_static_prefix); a provider failure costs the sentence and not the
  deterministically selected payload (test_the_selected_payload_survives_a_provider_failure); an
  unknown review-queue verdict is a 400 rather than a `ValueError` out of the audit writer
  (test_resolve_refuses_an_unknown_verdict).

## Known defects [verified]

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
