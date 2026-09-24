---
title: The provider key
research_date: 2026-09-23
status: in_progress
purpose: What gate 22 needs from an Anthropic key, and what already runs without one.
---

# The provider key

Gate 22 (`test_prompt_cache_prefix_length`) asserts that the tutor template's static prefix
exceeds the cacheable minimum on the routed model. That is the one thing in P1 a key is for.

## What already works without a key

The adapter (`app/providers/anthropic.py`), the two prompt templates
(`prompts/tutor/guardrailed_practice_v1.md`, `prompts/feedback/elaborated_v1.md`) and the replay
player (`app/providers/replay.py`) exist and are exercised with no key: `tests/providers/`
constructs and tests the adapter against recorded and hand-written responses, and
`tests/providers/test_prompts.py` golden-tests both templates by rendering them directly.

The cassettes under `tests/fixtures/provider_cassettes/` are hand-written, not recorded, until a
key exists. `tests/fixtures/provider_cassettes/README.md` says so directly, and marks its one
cassette `"synthetic": true` with placeholder token counts. That cassette is what gate 23
(`test_session_login_to_feedback`) runs against with no network call; it is explicitly not
evidence for gate 22, and its usage numbers must not be quoted as a token count.

## What the key is for

Gate 22 needs a real token count for the tutor template's static prefix, on the model P1 routes
it to, claude-sonnet-5. Measuring that count is the one thing in P1 that needs a key: nothing else
in P1 makes a live call. This document does not tell the operator to obtain a key by any
particular route, and it contains no key material.

## Environment variables

Read from `app/main.py` (the composition root's own docstring and `build_tutor`,
`build_tutor_caps`, `settings_from_environment`):

- `GROWTH_AI_BACKEND`: `subscription` (default), `api`, `replay` or `none`. `subscription` runs
  the official Claude Code CLI on the operator's own Claude subscription and serves one account
  only (docs/plan/07-ai-provider-layer.md, "The subscription backend"). `api` is the only value
  that uses the key. With `none`, `app/feedback/tutor.py` returns the deterministic payload and no
  sentence. A key sitting in the environment wires nothing on its own.
- `GROWTH_TUTOR_PROVIDER`: the older switch, `none` or `replay`, read only when
  `GROWTH_AI_BACKEND` is unset. Its old value `anthropic`, and `api`, now stop the app at startup unless
  `GROWTH_AI_BACKEND=api` is also set; remove it, or set `GROWTH_AI_BACKEND=api` if the paid key is
  what you meant.
- `GROWTH_SUBSCRIPTION_TUTOR_CALLS_PER_DAY` (default 60), `GROWTH_SUBSCRIPTION_<ROLE>_CALLS_PER_DAY`
  (default 20) and `GROWTH_SUBSCRIPTION_CALLS_PER_MINUTE` (default 4): the pacing guard on the
  `subscription` backend, which replaces the dollar and token caps below for a role on the
  subscription (`docs/plan/14-token-economy.md`, "Subscription pacing").
- `ANTHROPIC_API_KEY`: read only on the `api` backend.
- `GROWTH_CLAUDE_BIN`: the claude CLI the `subscription` backend runs. Default the claude on PATH.
- `GROWTH_TUTOR_CASSETTE`: path to a cassette JSON file, read only on the `replay` backend.
- `GROWTH_TUTOR_CAP_USD`: the tutor role's daily dollar cap. Default `1.00`
  (`app/main.py`, `DEFAULT_TUTOR_CAP_USD`), enforced by `app/providers/guard.py` before every
  call. The default is inferred, not sourced from any plan document, and is recorded as a
  tunable for 12-open-questions.md.
- `GROWTH_TUTOR_CAP_TOKENS`: the tutor role's daily token cap. Unset by default; when set, it
  binds alongside the dollar cap, whichever crosses first.

## Switching backends

The default needs nothing set: `GROWTH_AI_BACKEND` unset means `subscription`, which runs the
`claude` CLI on your own Claude login. To run on the paid key instead, set
`GROWTH_AI_BACKEND=api` and `ANTHROPIC_API_KEY` in the environment the app starts in; unset
`GROWTH_AI_BACKEND` again (or set it to `subscription`) to go back. `replay` and `none` are for
tests and for turning the tutor off. The backend is read once at startup, so restart the app after
changing it; the startup log names the backend it chose.

## Where the subscription token goes

The subscription backend works with no token at all: the CLI then uses the login stored by
`claude` in the macOS keychain, the same one an interactive `claude` session uses. On a machine
without that login, run `claude setup-token` and put the long-lived token in the environment the
app starts in as `CLAUDE_CODE_OAUTH_TOKEN`, for example in the repository's `.env` (gitignored)
if you load it into the shell before starting the app. The app does not read `.env` itself;
`tools/subscription_smoke.py` does, for the token only. The token is passed only to the `claude`
subprocess, never logged or printed, and the API adapter refuses it if it ever reaches
`ANTHROPIC_API_KEY`. Never commit it.

## When the subscription says no

A 5-hour or weekly usage limit leaves the student with the static feedback and queues the tutor
call. Once the window has reset, run `python3 tools/drain_subscription_queue.py` (add `--dry-run`
to see how many are due first); it retries through the same backend and puts each sentence where
the student will see it on their next look. It never uses the paid key unless
`GROWTH_AI_BACKEND=api`.

Building the composition root, including constructing an `anthropic` provider, never dials out by
itself: `app/main.py`'s own docstring states building it makes no network call, since the tutor
provider is only constructed, never called, at build time.
