---
title: The provider key
research_date: 2026-09-20
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

- `GROWTH_TUTOR_PROVIDER`: `none` (default), `replay`, or `anthropic`. With no tutor provider,
  `app/feedback/tutor.py` returns the deterministic payload and no sentence. A key sitting in the
  environment wires nothing on its own; this variable has to be set to `anthropic` as well.
- `ANTHROPIC_API_KEY`: read only when `GROWTH_TUTOR_PROVIDER=anthropic`.
- `GROWTH_TUTOR_CASSETTE`: path to a cassette JSON file, read only when
  `GROWTH_TUTOR_PROVIDER=replay`.
- `GROWTH_TUTOR_CAP_USD`: the tutor role's daily dollar cap. Default `1.00`
  (`app/main.py`, `DEFAULT_TUTOR_CAP_USD`), enforced by `app/providers/guard.py` before every
  call. The default is inferred, not sourced from any plan document, and is recorded as a
  tunable for 12-open-questions.md.
- `GROWTH_TUTOR_CAP_TOKENS`: the tutor role's daily token cap. Unset by default; when set, it
  binds alongside the dollar cap, whichever crosses first.

Building the composition root, including constructing an `anthropic` provider, never dials out by
itself: `app/main.py`'s own docstring states building it makes no network call, since the tutor
provider is only constructed, never called, at build time.
