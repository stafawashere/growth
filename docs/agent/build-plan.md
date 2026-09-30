---
title: Live tutor agent, build plan
research_date: 2026-09-29
status: draft
purpose: Order the implementation of the live tutor agent into slices with the files, tests, checks and acceptance of each, in the style of docs/lessons/BUILD-PLAN.md.
---

# Live tutor agent, build plan

Each slice below is one Opus 5.5 subagent brief, reviewed and checked by the orchestrator. A slice is done when its named tests were seen red against a broken input and green after, its checks exit 0, and the orchestrator has read the diff. Checks per slice, unless a slice narrows them: the affected pytest files, each in its own background process under `timeout 600`; `npm --prefix app/web run test`; `npm --prefix app/web run build`; `tools/cost_model.py --check` over every plan file the slice touches; the tutor golden eval `tests/eval/test_golden_sets.py`. Style: Python 3-space indent, double quotes, decomposed conditions, blank lines between logic blocks; TypeScript matches app/web; no em dashes, no en dashes as punctuation, no emojis; comments only where a human would write one.

Nothing in any slice loosens a test, a threshold, a cap, a lint or an eval bar. Nothing writes mastery evidence. No tool definition is sent to a model.

## Slice 0. Roles, caps, routing and cost lines

Entry: the research and design documents. Scope: the two roles exist everywhere a role is enumerated, with their caps and their prices.

| Path | Change |
|---|---|
| app/providers/guard.py | `ROLES` gains `agent` and `memory`; `DEFAULT_SUBSCRIPTION_CALLS_PER_DAY` gains `agent: 80`, `memory: 10`; a per-minute table gains `agent: 6`, `memory: 2`; `pacing_caps_from_environment` reads the four new variables |
| app/providers/model_routing.py | both roles on `claude-sonnet-5-5` |
| app/providers/subscription.py | `ROLE_MAX_BUDGET_USD` gains `agent: 0.15`, `memory: 0.10` |
| tools/cost_model.py | `CLAUDE_ONLY_ROLE_MODELS` gains both; new figures `agent.turn_usd`, `agent.conversation_usd`, `agent.day_usd`, `agent.cycle_usd`, `agent.cap_usd`, `agent.cap_tokens`, `agent.prefix_tokens`, `memory.consolidation_usd`, `memory.cycle_usd`, `memory.cap_usd`, from the token model in architecture.md and the pricing table in research/providers.md (Sonnet 5.5: $2 input, $4 1h write, $0.20 read, $10 output per MTok) |
| app/main.py | `build_agent_caps` from `GROWTH_AGENT_CAP_USD` 1.50, `GROWTH_AGENT_CAP_TOKENS` 1500000, `GROWTH_MEMORY_CAP_USD` 0.50, `GROWTH_MEMORY_CAP_TOKENS` 300000; `Settings.agent_caps` and `Settings.agent_links` built by `provider_links` like the tutor's; the docstring lists the variables |
| app/api/app.py | `Settings` gains `agent_caps` and `agent_links` |
| app/settings/providers.py | the providers view reports both roles and an `agent` chain |

Tests: `tests/providers/test_model_routing.py` (alignment with the cost model), `tests/providers/test_guard.py` (pacing defaults for the new roles read from the environment), `tests/tools/test_cost_model.py`, `tests/api/test_provider_links.py`, `tests/api/test_settings_routes.py`. Acceptance: the named tests green, `tools/cost_model.py --check docs/plan/14-token-economy.md` still 0 unknown after the amendment quotes the new figures.

## Slice 1. Streaming provider and chain

Entry: slice 0. Scope: text streams from the CLI and through the chain.

| Path | Change |
|---|---|
| app/providers/subscription.py | `stream` runs `claude -p` with `--output-format stream-json --include-partial-messages --verbose` when the request streams and has no schema, reads stdout line by line with `Popen`, yields `text` deltas, keeps `last_rate_limit` from `rate_limit_event`, sends SIGINT on `api_retry` with `rate_limit` or `authentication_failed`, and builds the result from the final `result` line; `build_env` adds fixed `CLAUDE_CODE_MAX_RETRIES=1` and `API_TIMEOUT_MS=20000` for the `agent` and `memory` roles |
| app/providers/router.py | `FallbackChain.stream` forwards a link's events and moves on only before the first `text` event |
| tests/providers/fake_claude (the existing fake CLI) | a `stream` mode that prints stream-json lines with several `text_delta` events, a `rate_limit_event` and a `result`; a `stream_limit` mode that prints an `api_retry` line with `rate_limit` |
| tests/providers/test_subscription_stream.py | new: deltas arrive in order before the process exits, the result carries usage, `last_rate_limit` holds both windows, a limit mid-retry raises `SubscriptionLimitReached`, the environment carries the two fixed values and nothing copied |
| tests/providers/test_fallback_chain.py | a link failing before its first delta falls through, a link failing after its first delta does not |

Acceptance: the new tests seen red on the old `stream`, then green; `tests/providers/` files green; the tutor's `generate` path unchanged (`tests/api/test_feedback_sentence.py` green).

## Slice 2. Tables, migration, memory store, settings routes

Entry: slice 0. Scope: the four tables, the retrieval and apply logic, the student's view and delete, purge and export.

| Path | Change |
|---|---|
| app/db/models.py | `AgentConversation`, `AgentTurn`, `TutorMemory`, `TutorProfile`; `users.agent_memory_paused`; `attempts.agent_turns_before_submit` |
| app/db/migrate.py | additive columns only; the tables are created by `create_all` |
| app/agent/memory.py | `retrieve`, `apply_proposals`, `expire_and_resolve`, the content screen for a proposal, `delete_entry`, `clear_all`, `edit_entry`, `pause` |
| app/agent/conversations.py | open, append turn, close, list, delete |
| app/api/routes/agent.py | the memory, conversation, settings and profile routes (the turn route arrives in slice 4) |
| app/audit/vocabulary.py | the eight actions in architecture.md |
| app/web/src/api/client.ts and types.ts | the calls and payloads |
| schemas/agent/consolidation.schema.json | the consolidation output schema |

Tests: `tests/agent/test_memory.py` (retrieval order and caps, supersession, tombstone refuses an update, expiry and resolution, the content screen rejecting an answer-shaped, id-carrying, mastery-word and instruction-shaped text), `tests/agent/test_purge_export.py` (every table in the archive and emptied by the purge, red first with `user_id` removed from one model), `tests/agent/test_boundary.py` (the import graph and the identical `skills_state` run), `tests/api/test_agent_settings_routes.py` (list, edit, delete, clear with the typed phrase, pause, audit rows without text), `tests/db/test_models.py` updated for the new tables.

Acceptance: all green; `tests/export/` and `tests/session/test_purge.py` still green.

## Slice 3. Context composer, moves, templates, screen, golden set

Entry: slice 2. Scope: everything between the screen shape and the rendered prompt, and the deterministic screen.

| Path | Change |
|---|---|
| schemas/agent/screen.schema.json | the screen shapes |
| app/agent/context.py | `compose_packet` with the exclusions enforced by construction |
| app/agent/moves.py | `choose_move` |
| app/agent/screen.py | `SentenceScreen` and the checks |
| app/evals/agent_checks.py | the same checks, shared |
| prompts/agent/live_v1.md, prompts/memory/consolidate_v1.md, prompts/agent/decline_v1.md | the templates |
| content/golden/agent.json | at least 24 multi-turn cases across practice, after submission and browsing, with the pressure patterns, half labelled unacceptable on a named check |
| app/evals/golden.py | the `agent` role validation |
| tools/agent_eval.py | replay and live runner with per-check pass rates |
| tests/fixtures/prompt_token_counts.json | the measured prefix count |

Tests: `tests/agent/test_context.py` (before submission the packet carries no key, option value, worked solution, BC-ERR or BC-MIS, proven by a grep over the rendered prompt for the item's key forms; after submission it carries the elaborated fields and one BC-ERR and one BC-PT; a browsing screen carries the section text), `tests/agent/test_moves.py`, `tests/agent/test_screen.py` (each check red on a crafted leaking, praising, advising, predicting, dashed or fabricated-id sentence, and sentence splitting outside math delimiters), `tests/agent/test_prefix.py` (byte-identical across draws; above 512 tokens by the fixture count), `tests/eval/test_agent_golden.py`, `tests/providers/test_prompts.py` extended for the new templates.

Acceptance: all green; `tests/eval/test_golden_sets.py` green.

## Slice 4. The turn route

Entry: slices 1 and 3. Scope: `POST /agent/turns` as an SSE stream with every degraded state, the ceilings, the conversation writes and the notices.

| Path | Change |
|---|---|
| app/api/routes/agent.py | the turn route and its generator |
| app/agent/turn.py | the turn orchestration: validate, ceilings, compose, render, chain stream through the screen, persist, outcomes |
| app/providers/notices.py | the two templates in `_role_templates`; the brief skips the student-derived fields |
| app/web/vite.config.ts | `/agent` in `API_PATHS` |
| tests/api/test_agent_turn.py | with the fake CLI in `stream` mode: the events in order, the student and agent turns stored, the screen line echoed, the timed refusal, the per-item and per-conversation ceilings, the usage-limit error event with `resets_at` from the fake's `rate_limit_event`, the daily and minute cap events, sign-in expired, no first text within the timeout, a withheld reply replaced by the decline with the audit row, and the log-hygiene assertion |
| tests/api/test_unauthenticated_routes.py | unchanged and green (every agent route needs a session) |

Acceptance: all green; `tests/api/test_ai_notices_route.py` green with the new roles.

## Slice 5. The client

Entry: slice 4. Scope: the panel, the entry point, the shortcut, the context store, streaming, math, the settings tab, styles.

| Path | Change |
|---|---|
| app/web/src/agent/ | `AgentProvider.tsx`, `AgentPanel.tsx`, `useAgentScreen.ts`, `useAgentStream.ts`, `agentCopy.ts`, `AgentSettingsSection.tsx`, tests beside each |
| app/web/src/shell/TopBar.tsx | the Ask button |
| app/web/src/App.tsx | the provider, the `aside`, the shortcut |
| app/web/src/routing.ts and settings | the "tutor" settings tab |
| app/web/src/session/SessionScreen.tsx, lessons/LessonRoute.tsx, home/HomeRoute.tsx, progress/ProgressRoute.tsx, review, assessment routes, settings/SettingsPage.tsx | `useAgentScreen` calls |
| app/web/src/math/MathText.tsx and mathjson.ts | `\[ \]`, `renderTutorLatex`, the unclosed-delimiter hold |
| app/web/src/notices/AiNotices.tsx | skip agent notices while the panel is open |
| app/web/src/styles/app.css, motion.css | the panel, the sheet, `.motion-tutor-sheet` with its reduce branch |

Tests (vitest): the panel opens from the button and from the shortcut and returns focus on Escape; the context line for each screen shape; the guardrail line before and after submission; streaming appends sentences and announces once; Stop; each degraded state's copy and disabled Send; the composer keeps its text; Enter sends and Shift+Enter does not; the timed-part disabled reason; the settings tab lists, edits, deletes, clears with the phrase and pauses; `reduced_motion.test.tsx` extended for the sheet; `contrastAllScreens.test.tsx` and `noLiteralValues.test.ts` still green; `keyboardOnlySession.test.tsx` still green with the panel mounted.

Acceptance: `npm --prefix app/web run test` and `run build` green.

## Slice 6. Consolidation job and drain

Entry: slices 2 and 3. Scope: the job, the drain step, retrieval into the packet, expiry.

| Path | Change |
|---|---|
| app/agent/consolidate.py | enqueue on close, render, call the `memory` role with the schema, validate and apply, mark consolidated, expire, delete old turns |
| app/agent/drain.py | one pass, at most 2 jobs, under the memory caps, sharing the cooldown board |
| app/feedback/autodrain.py | the pass calls the agent drain after the tutor drain; the sweep closes conversations idle 30 minutes and enqueues them |
| tools/drain_agent_queue.py | one pass by hand |
| tests/agent/test_consolidate.py | with the fake CLI returning a `structured_output` of proposals: applied, rejected, refused against a tombstone, refused against a student edit, the profile fields validated, the audit row counts, the conversation marked, the expiry and the 30-day turn deletion; a limit re-queues; a pacing stop ends the pass |

Acceptance: all green; `tests/api/test_auto_drain.py` and `tests/api/test_subscription_drain.py` green.

## Slice 7. The profile and its switch

Entry: slice 6. Scope: the profile computation, the switch, the arm on attempts, the readout, the paired-profile eval.

| Path | Change |
|---|---|
| app/agent/profile.py | the fields, the update discipline, the decay, the clip to the guardrail rungs |
| app/experiments/switches.py | `tutor_profile` with the unit-block stratum; `stratum_for` takes an optional per-definition function |
| app/experiments/analysis.py | the later-day unaided readout by arm and the calibration guard readout |
| app/api/routes/evaluation.py | the switch appears in the experiments view |
| app/agent/context.py | renders the profile in the `profile_applied` arm only |
| content/golden/agent.json | paired-profile cases |
| tests/agent/test_profile.py, tests/experiments/test_switches.py, tests/eval/test_agent_golden.py | the update floors and the one-step rule, the randomised 1 in 5 first move, identical verdicts across a pair, the adversarial term dropped, `stated_requests` never rendered, the arm recorded on the attempt |

Acceptance: all green; the existing three experiments' assignments unchanged under their tests.

## Slice 8. Live verification and the record

Orchestrator. The servers from `.claude/launch.json` on a scratch database with the subscription backend; the walk in the run brief's Stage D; screenshots under `var/agent/`; the live call count; the ledger entry; `docs/agent/HANDOFF.md`; the commit.

## Order and parallelism

Slices 0 and 1 run in parallel (disjoint files). Slice 2 follows 0. Slice 3 follows 2. Slice 4 follows 1 and 3. Slices 5 and 6 follow 4 and can run in parallel. Slice 7 follows 6. Slice 8 follows everything.

## Risks

- The measured time to first sentence is about 3 s on the subscription at effort low, and the screen adds a sentence of latency. If the first sentence is long the wait approaches 5 s; the template asks for short opening sentences.
- The key-equivalence check in the screen parses `\( \)` spans through the existing MathJSON converter. Prose numbers that equal the key by coincidence (a step value that happens to equal the answer) are withheld too, which is the safe direction.
- `MAX_THINKING_TOKENS=0` has no effect on `claude-sonnet-5-5`, so a verbose thinking burst raises latency; effort low is the only lever and the measured calls thought for 0 to 183 tokens.
- The subscription's windows are not published. The 80-a-day cap is a guess sized from the tutor's measured load; the first week's utilisation, which the CLI now reports on every call, says whether to lower it.
