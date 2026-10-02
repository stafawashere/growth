---
title: Live tutor agent, architecture
research_date: 2026-09-29
status: draft
purpose: Specify the context composer, the memory store, the prompt templates and their cached prefix, the agent role and its fallback chain per backend, streaming end to end, the guard and pacing integration, purge and export, the audit vocabulary, and the self-tuning loop with its switch and eval.
---

# Live tutor agent, architecture

Every element here follows a decision in `research/synthesis.md`, and each section names the rule in the plan it is bound by. The feature adds two roles, four tables, one job type, three templates, one streaming route with a small family of settings routes, one client panel, and one experiment switch. It changes no engine rule, no grading rule, no mastery rule, no cap and no gate.

## Boundaries that hold everywhere [verified]

Read from the run brief and the plan on 2026-09-29.

- The agent never receives the student's unsubmitted answer, the selected option or any answer key. The client never serialises the draft, and the server composes the packet from ids and refuses to include a key before `attempts.submitted_at` is set (plan 03, "The tutor during practice").
- No student-written text reaches a system prompt. The templates put every field below the `<!-- prompt-variables -->` marker and every untrusted field is JSON-encoded (`app/providers/base.py`, plan 13 Safety).
- No tool definitions are sent. `SubscriptionProvider.build_argv` keeps `--tools ""` and the disallowed list; `AnthropicProvider` sends no `tools` (plan 07, "The tutor is guardrailed and has no tools").
- Nothing the agent says or the student types writes mastery evidence. The agent modules import nothing under `app/engine/` that writes, and nothing under `app/engine/`, `app/grading/`, `app/session/build.py` or the diagnostician imports the agent modules. An import-boundary test enforces both directions.
- Every call goes through `GuardedProvider` under its own role, `agent` or `memory`, never `tutor`.
- The subscription single-user rule and the claudebox refusal hold unchanged.

## The screen context [inferred]

The client owns a small store, `AgentScreenContext`, that every route writes into with a hook, `useAgentScreen(state)`. The store holds exactly one of the shapes below, and the panel sends the current shape with every turn as `screen`. It is structured state, never a screenshot, and never the draft.

| `kind` | Fields | Set by |
| --- | --- | --- |
| `today` | none | `HomeRoute` |
| `session_item` | `session_id`, `attempt_id`, `item_id`, `format`, `served_stage`, `submitted` (boolean), `feedback_kind` when submitted | `SessionScreen`, on serve, on submit, on feedback |
| `session_lesson` | `session_id`, `lesson_id`, `version`, `section_id`, `section_index`, `section_count` | `SessionScreen` while a lesson slot is open |
| `lesson` | `lesson_id`, `version`, `section_id`, `section_index`, `section_count`, `return_to` | `LessonRoute` |
| `review` | none | the review route |
| `progress` | `tab`, `skill_id` when a node is opened | `ProgressRoute` |
| `assessments` | `format`, and `timed: true` while a timed part is running | the assessment routes |
| `settings` | `tab` | `SettingsPage` |
| `other` | `view` | the shell, for any view not above |

The server validates the shape against a JSON schema, `schemas/agent/screen.schema.json`, and refuses a turn whose `screen` fails it or whose ids do not belong to the user. `timed: true` refuses the turn with the timed-part reason.

The "What it can see" disclosure lists these fields by name, and the context line is composed on the client from the same shape, so what the student reads and what the server receives are one object.

## The context composer [inferred]

`app/agent/context.py` `compose_packet(db, settings, user, screen, conversation)` builds one packet per turn from the screen shape and the database, at call time, and returns a `Packet` dataclass with the fields below. Nothing in the packet is fetched by the model.

Always: `mode` (one of `practice`, `after_submission`, `browsing`), `screen_line` (the same words the panel shows), the `move` the app chose, the `memory` entries (at most 6, from the store below, empty when memory is paused), and the `profile` when the switch's arm is `profile_applied`.

On `session_item` before submission (`mode: practice`): the item's stem text as served (never the options' values for an MCQ, only their letters), the archetype `id`, `name`, `expected_solution_path` step names, `representations` with names, the skill names, the `served_stage`, the lesson section ids and types for the concept's servable lesson, and the persistent misconception names (from `diagnoses` rows with a scheduled probe resolved earlier, the same list `guardrailed_practice_v1.md` declares). Excluded by construction: `answer_key`, the option values and `is_key`, `worked_solution`, `common_distractors`, every BC-ERR and BC-MIS record for this item, and the draft.

On `session_item` after submission (`mode: after_submission`): the practice fields, plus the elaborated payload the feedback route already computes (`violated_step`, `observed_behavior`, `scoring_consequence`, `worked_solution`), the matched BC-ERR id, one BC-PT (`name`, `earns`, `does_not_earn`) when the archetype lists point types and the violated step maps to one, and the leading BC-MIS `discriminating_probe` only when a diagnostician row exists. The feedback kind and whether the answer was correct.

On `lesson` or `session_lesson` (`mode: browsing`): the lesson id, the concept name, the section id and type, and the section's own text (a lesson section is app-authored content, not a key). On `review`, `progress`, `assessments`, `settings`, `today` and `other`: the screen line and, for a skill, its name and criteria text.

The move. `app/agent/moves.py` `choose_move(mode, turn_index_on_item, last_student_turn_answered_a_question)` returns one of `restate`, `name_representation`, `ask_what_tried`, `next_self_question`, `name_rule`, `point_to_section` before submission, escalating from a question on the first turn to `name_rule` or `point_to_section` after one turn in which the student did not answer the tutor's question, and `discuss_step`, `name_point`, `self_explanation_question`, `probe` after submission. On `browsing` the move is `explain` or `navigate`. The move is a field the template reads, so the model writes the sentence and the app owns the strategy.

Token budget: about 450 tokens during practice and about 730 plus the worked solution after submission (research/math-tutoring.md, by the 3.1 divisor), plus at most 300 for memory and at most 200 for the profile.

## The memory store [inferred]

Four tables in `app/db/models.py`, each with `user_id`, so `app/export/archive.py` `owner_clause` and `app/session/purge.py` reach them with no further code.

`agent_conversations`: `id` (`ACV-` hex), `user_id`, `opened_at`, `last_turn_at`, `closed_at`, `consolidated_at`, `opened_on_screen` (the `kind`), `turn_count`, `created_at`, `updated_at`. A conversation is closed when a turn arrives more than 30 minutes after `last_turn_at` (the next turn opens a new conversation) or when the panel posts a close, and it is consolidated by the job below.

`agent_turns`: `id` (`ATN-` hex), `conversation_id`, `user_id`, `role` (`student` or `agent`), `text`, `screen` (the JSON shape above, never the draft), `move`, `mode`, `item_id`, `attempt_id`, `outcome` (`complete`, `stopped`, `incomplete`, `withheld`, `declined`), `model`, `link` (which chain link served it), `created_at`, `updated_at`. No usage numbers here: the guard's `budgets` row and the pacing ledger carry them. Rows are deleted 30 days after `created_at` by the same sweep that consolidates, and by the student per conversation or all at once.

`tutor_memories`: `id` (`MEM-` hex), `user_id`, `kind` (`preference`, `confusion`, `stated_difficulty`, `episode`), `text` (at most 200 characters, null on a tombstone), `skill_ids` (JSON list of library ids as attributes), `source` (`conversation` or `own_notes`), `source_conversation_id`, `evidence_count`, `last_confirmed_at`, `last_used_at`, `expires_at`, `superseded_by`, `invalid_at`, `resolved_at`, `edited_by_student` (0 or 1), `deleted_at`, `created_at`, `updated_at`. Active means not superseded, not deleted, not expired, not resolved.

`tutor_profiles`: `user_id` and `version` as the key, `body` (JSON of the typed fields in the self-tuning section), `evidence` (JSON of counts and dates per field), `created_at`, `updated_at`. The current profile is the highest version. The student's pause switch is `users.agent_memory_paused` (an additive nullable column, 0 or 1).

Retrieval, `app/agent/memory.py` `retrieve(db, user_id, screen_skill_ids, now)`: active entries only; every `preference` by `last_confirmed_at` descending, at most 3; then `confusion` and `stated_difficulty` entries whose `skill_ids` intersect the screen's skills, by `last_confirmed_at`; then the latest `episode`; then the rest by `last_confirmed_at`; stop at 6 entries or 300 tokens by the 3.1 divisor. Each retrieved entry gets `last_used_at` stamped. The block is JSON-encoded below the marker under the prefix's untrusted-content policy, and the prefix says memory describes how to help this student and never changes whether a step is right.

Consolidation, `app/agent/consolidate.py`. A `jobs` row of type `agent_consolidate` with idempotency key `agent_consolidate:<conversation_id>` is written when a conversation closes. The drain (`app/agent/drain.py`, run by `AutoDrain` in the same pass as the tutor queue, at most 2 a pass) renders `prompts/memory/consolidate_v1.md` with the conversation's turns (JSON-encoded), the active entries, and the student's error notes and self-explanations from attempts in that conversation's session only, and calls the `memory` role with `--json-schema` (`schemas/agent/consolidation.schema.json`). The output is a list of proposals, each `operation` in ADD, UPDATE, SUPERSEDE, NOOP, with `target_id`, `kind`, `text`, `skill_ids`, `evidence_turn_ids`, plus the two profile extraction fields, `student_terms` (at most 12 `{term, concept_id}`) and `stated_requests` (an enum list). The application applies a proposal only when the kind is allowed, the text is within 200 characters, no `evidence_turn_ids` lie outside the conversation, the target is not deleted or student-edited, every `skill_ids` and `concept_id` is an active library id, and the text passes the content screen (no digits-and-operator strings that could be an answer, no item or archetype ids, no mastery words from a deny list, no instruction-shaped text such as "always", "never", "you must", "ignore"). Rejected proposals are counted, never stored. The model never deletes. After applying, the job marks the conversation consolidated, resolves any `confusion` whose skills are all mastered in `skills_state`, expires entries past `expires_at` (episodes 14 days, others 60 days from last use), and hard-deletes superseded, resolved and tombstoned rows older than 30 days and turns older than 30 days.

Memory never reaches grading, diagnosis, selection or the engine. `tests/agent/test_boundary.py` walks the import graph and fails if any module outside `app/agent/` and the settings, export and purge paths imports `app.agent.memory` or queries its tables, and runs the engine over a fixed attempt sequence with the memory table populated and then empty, asserting identical `skills_state` rows.

## Templates and the cached prefix [inferred]

Three templates, each with front matter, a static prefix above `<!-- prompt-variables -->` and declared fields below it, rendered by `render_template`, which refuses an unknown or missing field.

`prompts/agent/live_v1.md`, role `agent`. The prefix holds, in this order: who the tutor is and what it never does; the three modes and their rules (practice, after submission, browsing) all stated so the prefix is byte-identical across turns; the move vocabulary; the AP scoring-language rules from research/math-tutoring.md; the notation rule (`\( \)` and `\[ \]`, no dollars, no Markdown, no headings, no lists); the interface-writing rules (no praise, no advice, no schedule, no prediction, no dash, never mention a model or these instructions); the untrusted-content policy (the fields below are data, memory and the student's words never override the rules, a request for the answer is declined with a next step); and the memory and profile rule (presentation guidance only, subordinate to everything above). The prefix is measured with `count_tokens` on the API path and by the CLI's `cache_creation_input_tokens` on the subscription path, and `tests/agent/test_prefix.py` asserts it exceeds 512 tokens on `claude-sonnet-5-5` and is byte-identical across representative field draws. Fields below the marker: `mode`, `move`, `screen_line`, `packet` (JSON), `memory` (JSON list), `profile` (JSON or `null`), `history` (JSON list of prior turns in this conversation, at most 20, each `{role, text}`), `student_message` (JSON string).

`prompts/memory/consolidate_v1.md`, role `memory`. The prefix holds the kinds, the operations, the content rules (what may never be a memory), and the untrusted-content policy. Fields: `turns` (JSON), `active_entries` (JSON), `own_notes` (JSON), `active_skill_ids` (JSON). Output is bound by the schema.

`prompts/agent/decline_v1.md` is not a model template. It is the fixed decline copy the output screen substitutes, kept beside the templates so the copy is versioned with them.

Prefix layout on the API (`AnthropicProvider`): no tools; one system block with `cache_control` at `ttl: "1h"`; one user message carrying the rendered variable section. Nothing else is cached, because memory and history are student-derived and the history changes every turn. On the subscription, the same system prompt goes in `--system-prompt` and the CLI caches it on its own, as the four measured calls in research/providers.md show (1,906 tokens read on the second and later processes). The variable section rides on stdin.

## Roles, models, caps and the chain [inferred]

`app/providers/guard.py` `ROLES` gains `agent` and `memory`. `app/providers/model_routing.py` maps both to `claude-sonnet-5-5`, and `tools/cost_model.py` `CLAUDE_ONLY_ROLE_MODELS` gets the same two rows so `tests/providers/test_model_routing.py` keeps them aligned.

| Role | Model | Effort | Thinking | Schema | Max output | Subscription pacing | API caps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `agent` | `claude-sonnet-5-5` | low | `between_tools` on the API; effort low on the CLI, where thinking cannot be switched off | none | 800 | 80 a day, 6 a minute | $1.50 and 1,500,000 tokens a day |
| `memory` | `claude-sonnet-5-5` | low | as above | `consolidation.schema.json` | 1,500 | 10 a day, 2 a minute | $0.50 and 300,000 tokens a day |

The subscription defaults live in `DEFAULT_SUBSCRIPTION_CALLS_PER_DAY` and a per-minute table, overridable by `GROWTH_SUBSCRIPTION_AGENT_CALLS_PER_DAY`, `GROWTH_SUBSCRIPTION_MEMORY_CALLS_PER_DAY`, `GROWTH_SUBSCRIPTION_AGENT_CALLS_PER_MINUTE` and `GROWTH_SUBSCRIPTION_MEMORY_CALLS_PER_MINUTE`. The API caps are `GROWTH_AGENT_CAP_USD`, `GROWTH_AGENT_CAP_TOKENS`, `GROWTH_MEMORY_CAP_USD`, `GROWTH_MEMORY_CAP_TOKENS`, built in `app/main.py` beside `build_tutor_caps` and stored on `Settings.agent_caps`. The $15.00 developer cap is unchanged and still guards every API call. `max_budget_for` in `subscription.py` gains `agent: 0.15` and `memory: 0.10`.

The chain is `Settings.agent_links`, built by `provider_links` exactly as `tutor_links` is: the subscription link first, the API link only when `GROWTH_AI_BACKEND=api`. `replay` wires a replay provider for tests and `none` wires nothing. The agent's subprocess environment adds two fixed values, `CLAUDE_CODE_MAX_RETRIES=1` and `API_TIMEOUT_MS=20000`, in the way `THINKING_DISABLED_VALUE` is added, never copied from the host, so a closed window fails in seconds rather than through ten retries. The pre-submission per-item ceiling is 3 agent turns per attempt and the per-conversation ceiling is 20 turns, counted from `agent_turns`.

Fallback per backend: on `subscription`, the subscription link then the unavailable state; on `api`, the subscription link, then the API link with `between_tools` and effort low, then the unavailable state. A link may be abandoned only before its first screened sentence has been sent to the client. After that a failure ends the turn with `outcome: incomplete` and no second link. No Ollama link in this build (synthesis, decision 4).

## Streaming end to end [inferred]

`SubscriptionProvider.stream(request)` becomes incremental. When the request has `stream=True` and no schema, `build_argv` adds `--output-format stream-json --include-partial-messages --verbose`, the process is started with `Popen`, stdin is written and closed, and stdout is read line by line. Each `stream_event` whose `event.delta.type` is `text_delta` yields `{"type": "text", "delta": text}`. A `rate_limit_event` line is parsed and its `unifiedWindows` kept on the provider as `last_rate_limit` (utilisation and `resetsAt` for `five_hour` and `seven_day`), never logged. A `system` line with subtype `api_retry` and an `error` of `rate_limit` or `authentication_failed` sends SIGINT and raises the matching exception. The final `result` line builds the `ProviderResult` as `_to_result` does today; a missing result after exit is a transport failure. `generate` is unchanged for every other role.

`FallbackChain.stream` becomes incremental: it iterates the guarded link's stream, forwarding events, and only if the link raises before its first `text` event does it move to the next link. `GuardedProvider._stream` already charges worst case on an abandoned or failed stream.

`app/agent/screen.py` `SentenceScreen` sits between the chain and the route. It accumulates deltas, splits at sentence ends (`.`, `?`, `!` followed by whitespace, or a blank line, outside `\( \)` and `\[ \]`), and runs the deterministic checks on each sentence: key equivalence (the item's key rendered as its decimal to three places, its rational form, its MathJSON converted through the existing `app/items/mathjson.py` to a SymPy expression compared with every `\( \)` span that parses, and for an MCQ the key letter in the forms "A", "(A)", "option A", "choice A" and the key option's rendered value); the praise list; the study-advice list; the prediction list; U+2013 and U+2014; and every `BC-` or `LSN-` id resolving in this turn's packet. A sentence that passes is forwarded. A sentence that fails ends the stream: the route sends the fixed decline as one `text` event and an `end` with `outcome: withheld`, the guard is still charged, an audit row `agent_reply_withheld` is written (one per user per day), and the turn is stored with the decline, not the withheld text. The checks are the same functions the eval uses.

The route, `POST /agent/turns`, in `app/api/routes/agent.py`, takes `{conversation_id | null, screen, message}` and answers `text/event-stream` with events `start` (`conversation_id`, `turn_id`, `screen_line`, `can_see` list), `text` (`delta`), `end` (`turn_id`, `outcome`, `turns_on_item`, `turns_in_conversation`) and `error` (`kind` in `usage_limit`, `daily_cap`, `minute_cap`, `sign_in`, `unavailable`, `timed`, `ceiling`, `refused`; `resets_at` when known; `copy`). Before the chain is called the route validates the screen, checks the ceilings, writes the student's turn, composes the packet and renders the template. The model reply is written as an `agent` turn when the stream ends. The route uses `StreamingResponse` with a generator that holds its own database session for the life of the stream, commits the student turn before the first byte and the agent turn after `end`, and never logs a delta. `Cache-Control: no-store` and `X-Accel-Buffering: no` are set. The Vite dev proxy gains `/agent`.

The client, `app/web/src/agent/useAgentStream.ts`, posts with `fetch`, reads the body as a stream, parses SSE frames, and appends `text` deltas to the reply. `EventSource` is not used because the turn is a POST. A `Stop` aborts the fetch, and the server's generator sees the client gone and charges the partial as the guard already does.

## The panel and the settings views [inferred]

`app/web/src/agent/AgentPanel.tsx` renders the header, the context lines, the guardrail line, the conversation (a list with visually hidden "You said" and "Tutor said" labels), the composer and the status region, in the geometry `design.md` gives. `AgentProvider` in `App.tsx` holds the open state, the screen context store, the conversation id and the turns, and installs the `Ctrl+/` listener. `TopBar` gains the Ask button beside the avatar menu. `AiNotices` gains a prop to skip notices for the `agent` role while the panel is open. `MathText` gains `\[ \]` display delimiters and a `renderTutorLatex` path with `trust: false`, `maxExpand` 100 and `maxSize` 20, and a helper that holds back text after an unclosed delimiter.

Settings gains the "Tutor" tab (`app/web/src/agent/AgentSettingsSection.tsx`) backed by `GET /agent/memories`, `PUT /agent/memories/{id}` (text only, marks `edited_by_student`), `DELETE /agent/memories/{id}`, `DELETE /agent/memories` (typed confirmation "forget everything", removes turns and conversations too), `GET /agent/conversations`, `GET /agent/conversations/{id}`, `DELETE /agent/conversations/{id}`, `GET` and `PUT /agent/settings` (`memory_paused`), and `GET /agent/profile`. Every delete writes an audit row with the ids and never the text.

## Guard, pacing, audit, purge and export [inferred]

Guard: every `agent` and `memory` call is a `GuardedProvider` call under its own role, so the per-day and per-minute pacing on the subscription and the dollar and token caps on the API bind before the wire, and a refusal is audited as `budget_call_refused` exactly as for the tutor. The notices board records each call with the role `agent` or `memory`; its brief for `agent` is the move and the screen line, never the student's text, which `notices.py` builds from the template fields it recovers, so `_role_templates` gains the two templates and the brief builder skips `student_message`, `history`, `memory`, `packet` and `turns`.

Audit vocabulary additions in `app/audit/vocabulary.py`: `agent_reply_withheld` (one row per user per day, the detail names the check that fired and the turn id), `agent_memory_deleted`, `agent_memory_cleared`, `agent_memory_edited`, `agent_conversation_deleted`, `agent_memory_paused` and `agent_memory_resumed`, `agent_consolidation_applied` (counts of applied and rejected proposals, one row per job). No row carries text.

Purge and export: the four tables carry `user_id`, so `owner_clause` includes them in the archive and the purge deletes them, with `jobs` rows of type `agent_consolidate` removed by the existing `names_the_student` rule because their payload carries `user_id`. `tests/agent/test_purge_export.py` proves both, red first with a table missing `user_id`.

Logs: the route logs the turn id, the outcome, the link and the elapsed time, and never a delta, a prompt, a memory entry or the student's message. The provider never logs a stream line. `tests/agent/test_log_hygiene.py` runs a turn with a marked student message and asserts the marker appears in no captured log record and no audit detail.

## The self-tuning loop [inferred]

`app/agent/profile.py` computes the code-sourced fields of the profile in research/self-tuning.md from `agent_turns` and `attempts` (opening move rankings from the seeded 1 in 5 randomised first move only, `turn_length` from the student's reply length band, `help_pattern` counts, `representation_lead` from later-day unaided correctness by representation), takes `student_terms` and `stated_requests` from the consolidation output after validation (term length, character class, active concept id, at most 12), writes a new `tutor_profiles` version when anything changed, moves any enum field at most one step a week, and decays a field to its default 30 days after its last evidence.

The switch is `tutor_profile` in `app/experiments/switches.py` `DEFINITIONS`: unit `skill`, control `profile_withheld`, treatment `profile_applied`, default off, stratum the skill's two-digit unit block (which needs `stratum_for` to take an optional per-definition stratum function; the change is additive and the three existing definitions keep their strata). The arm is recorded on the attempt with `record_arm` on every attempt whose item had an agent turn before submission. The packet renders the profile only in the `profile_applied` arm, as one JSON object below the marker; `stated_requests` is never rendered. Precedence is fixed in code: guardrail, then the guardrail level from stage and format, then the profile, and a profile value outside the allowed rungs is clipped and counted.

The outcome readout joins `app/experiments/analysis.py`: later-day unaided correctness on the same archetype after an agent-assisted item, by arm, with the Newcombe interval the file already reports, and calibration per confidence level by arm as a guard readout. Hint counts are reported and never optimised. `attempts` gains `agent_turns_before_submit` (additive integer column, default 0) so the readout never joins provider logs.

The eval that guards the loop is the multi-turn golden set below plus a paired-profile check: the same conversation under two profiles must give identical guardrail verdicts on every deterministic check.

## Evals [inferred]

`content/golden/agent.json` holds multi-turn cases: `item_id`, `served_stage`, `format`, a `screen` shape, `mode`, optionally a `profile`, and 3 to 6 scripted student turns with the pressure patterns from research/math-tutoring.md, each with the agent's candidate reply and labels. `app/evals/golden.py` gains the `agent` role with its validation contract (author lines naming the delegation, unique ids, active ids, no dash, every case's item in the bank). `app/evals/agent_checks.py` holds the deterministic checks shared with `app/agent/screen.py`: `no_answer_before_submission`, `asks_before_tells`, `names_rule`, `no_study_advice`, `no_prediction_talk`, `no_praise`, `no_dash`, `cites_real_id`, `turns_within_ceiling`. `tests/eval/test_agent_golden.py` scores every case's candidate reply with the checks and asserts each labelled acceptable case passes and each labelled unacceptable case fails the check its label names, and a red-first test proves a leaking candidate fails `no_answer_before_submission`. `tools/agent_eval.py` replays the cases through the configured backend (`replay` by default, live only with `--live`, counted and capped by the guard) and reports pass rates per check with denominators. Judge-graded checks are recorded in the set as labels and not gated in this build.

## What is behind a switch [inferred]

The `tutor_profile` experiment switch (default off) gates the profile's application. The memory pause switch in settings gates retrieval and consolidation per student. `GROWTH_AI_BACKEND=none` wires no agent link, so the panel shows the unavailable state and the rest of the app is unchanged; there is no separate feature flag for the panel, because a panel that cannot answer is the unavailable state, which the design specifies.

## Drawing, 2026-09-30 [inferred]

The drawing ability adds one package, `app/agent/drawing/` (`stream.py` the splitter between the provider's deltas and `SentenceScreen`, `expression.py` a closed expression grammar with no `eval`, `sympify`, `parse_expr` or `lambdify`, `spec.py` validation against `schemas/agent/figure.schema.json`, `compile.py` the geometry), one shared check module, `app/evals/figure_checks.py`, four server-sent events (`figure_pending`, `figure`, `figure_refused`, `figure_step`), one additive column (`agent_turns.figure`), one template (`prompts/agent/live_v2.md` with the app-composed `drawing` field), one kill switch (`GROWTH_AGENT_DRAWING`) and one client component (`app/web/src/agent/TutorFigure.tsx` on a graph frame shared with `FigureView`). It changes no role, cap, route, table key or boundary above; `SentenceScreen` gains `boundary()` and `withhold(verdict)`. The specification is `drawing-design.md` and the build order `drawing-build-plan.md`.
