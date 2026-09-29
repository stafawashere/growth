---
title: Providers for the live tutor agent
research_date: 2026-09-29
status: draft
purpose: Establish which model backends can serve a live, streaming, memory-carrying tutor agent in Growth, how each streams and caches, what each costs and retains, and how the agent degrades when a backend is gone.
---

# Providers for the live tutor agent

This file covers two strands. Part 1 is the Claude subscription backend that Growth already runs through the Claude Code CLI. Part 2 is every other provider plan 07 lists. The recommendations at the end are ranked and each names the alternative it rejects.

Constraints that hold regardless of what follows, restated so no recommendation below reads as arguing against them. The tutor role is never routed to claudebox, and the single-user rule of the subscription backend holds. No student-written text reaches a system prompt. Untrusted fields are JSON-encoded into the user message, below the prompt-variables marker of `app/providers/base.py` `render_template`. No tool definitions are sent to a model by default. Every agent call goes through `app/providers/guard.py` with a role and caps of its own. Consolidation and self-tuning run off the interactive path.

## What Growth already has [verified]

Read from the worktree on 2026-09-29.

`app/providers/subscription.py` `SubscriptionProvider` starts one `claude -p` process per call from an argument list, never a shell. The argv carries `--model`, `--system-prompt=<rendered prefix>`, `--output-format json`, `--max-budget-usd` (0.10 for the tutor, 0.25 otherwise), `--no-session-persistence`, `--setting-sources ""`, `--strict-mcp-config` with an empty MCP config, `--disable-slash-commands`, `--permission-prompts none`, `--tools ""` and a named `--disallowedTools` list, plus `--effort` and `--json-schema` when the request asks. The working directory is an empty temporary directory. The environment is built from `PATH`, `HOME`, `USER`, `LANG`, `TMPDIR` and `CLAUDE_CODE_OAUTH_TOKEN` when set, so no `ANTHROPIC_*` variable crosses. A request whose options disable thinking gets `MAX_THINKING_TOKENS=0`.

Three facts in that file bear directly on a live agent.

1. `SubscriptionProvider.stream` is not incremental. It calls `generate`, waits for the process to exit, and yields the whole reply as one delta. Its docstring says the json output format has no incremental text.
2. `prompt_text` flattens a multi-message request into one user message of `role: content` lines. A conversation therefore reaches the CLI as a single growing user message.
3. Images already use `--input-format stream-json --output-format stream-json --verbose`, and the answer is read from the last `result` line (`result_event_of`). The stream-json path is exercised in production code, only not for text streaming.

`app/providers/router.py` `FallbackChain.stream` also buffers. Its docstring states the chain decides a link before any text is shown, so a stream is the chosen link's whole result as one delta. A usage limit cools the subscription link for `LIMIT_COOLDOWN` of 30 minutes, and three consecutive other failures cool it for 60 seconds.

`app/providers/guard.py` `SubscriptionPacingCaps` counts calls per role per day (tutor 60, grader 120, transcriber and diagnostician 30 each, any other role 20) and per minute (grader 12, any other role 4), in `var/subscription_pacing.json`, global to the process because the subscription is one login. `pacing_caps_from_environment` reads `GROWTH_SUBSCRIPTION_<ROLE>_CALLS_PER_DAY` for every name in `ROLES`, so a new `agent` role needs an entry in `ROLES` before its variable is read.

`app/providers/call_queue.py` `queue_call` stores a deferred call in the `jobs` table with the full `messages` content in the payload. `app/feedback/autodrain.py` retries queued tutor calls every 10 minutes, at most 5 per pass, and `app/feedback/drain.py` re-queues a still-limited job after `LIMIT_RETRY_AFTER` of 30 minutes.

`app/providers/anthropic.py` already streams Anthropic SSE into the normalised vocabulary of `docs/plan/06-architecture.md`, sends `cache_control` on the system block, and maps a disabled-thinking request on the `claude-sonnet-5-5` family to `{"type": "between_tools"}` (`_SONNET_5_5_THINKING_OFF`). `app/providers/model_routing.py` routes the tutor, grader, transcriber and diagnostician to `claude-sonnet-5-5`, the generator to `claude-opus-5-5` and the verifier to `claude-haiku-4-5`, and records the operator's instruction of 2026-09-23 that the AI engine uses Anthropic Claude models only.

`docs/plan/14-token-economy.md` measured 20 tutor calls through CLI 2.1.277 on 2026-09-23. Median wall clock was 3.03 s on `claude-haiku-4-5` and 3.72 s on `claude-sonnet-5` (p90 3.16 s and 4.32 s), about one second of each being process start and exit. Sonnet 5 calls read 1,500 tokens from the prompt cache after the first call. No call was measured on `claude-sonnet-5-5`, and no API latency was recorded. The BUILD-LEDGER Known defects of 2026-09-23 add that no live call has met a usage limit, that the limit wording the adapter matches is unverified, that the CLI adds about 380 input tokens a call on Haiku 4.5 for reasons not determined, and that whether `MAX_THINKING_TOKENS=0` or `--effort low` stopped the CLI's thinking was not isolated.

## Part 1. The CLI surface a live agent needs [verified]

Installed version is 2.1.284 (`claude --version`, run 2026-09-29). Each flag below appears both in `claude -p --help` on this machine and in the CLI reference (https://code.claude.com/docs/en/cli-reference, accessed 2026-09-29), which makes two agreeing sources.

| Need | Flag or variable | What the sources say |
| --- | --- | --- |
| Token streaming | `--output-format stream-json --verbose --include-partial-messages` | Partial chunks are emitted only with `--print` and `stream-json`. The headless page filters them with `select(.type == "stream_event" and .event.delta.type? == "text_delta")` |
| Multi-turn input in one process | `--input-format stream-json` | Help text calls it "realtime streaming input". Only works with `--print` |
| Structured output | `--json-schema <schema>` | Validated JSON lands in the result's `structured_output` field. An invalid schema exits with an error from 2.1.205 on |
| System prompt | `--system-prompt`, `--system-prompt-file`, `--append-system-prompt` | The first two replace the default prompt and are mutually exclusive. Append flags add to the default |
| Cache split inside a custom system prompt | a line holding only `__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__` | Splits the prompt into two blocks, each with its own breakpoint. Requires 2.1.275 or later |
| Session state | `--resume`, `--continue`, `--session-id`, `--fork-session`, `--no-session-persistence` | Without persistence a session "cannot be resumed" |
| Spend ceiling | `--max-budget-usd` | Print mode only. Totals restored by `--resume` do not count |
| Effort | `--effort <level>`, one of low, medium, high, xhigh, max | Levels depend on the model |
| Turn limit | `--max-turns` | In the reference, absent from local `--help`. The reference says `--help` does not list every flag |
| Model fallback | `--fallback-model` | Retries on overload or unavailability, not on a usage limit |

The stream itself. With partial messages on, the CLI emits `stream_event` lines whose `event` field is a raw Messages API event, in the order `message_start`, `content_block_start`, `content_block_delta` (text in `delta.text` when `delta.type` is `text_delta`), `content_block_stop`, `message_delta`, `message_stop`, and the last line is a `result` message with the final text, cost and session id (https://code.claude.com/docs/en/headless and https://code.claude.com/docs/en/agent-sdk/streaming-output, both accessed 2026-09-29). The first line is normally `system/init`. A retryable API failure produces a `system/api_retry` line carrying `attempt`, `max_retries`, `retry_delay_ms`, `error_status` and an `error` category drawn from a list that includes `rate_limit`, `overloaded`, `authentication_failed` and `billing_error` (headless page, same date). The TypeScript reference prints the same category list as `SDKAssistantMessageError`, where `rate_limit` means the API returned a 429 against the quota (https://code.claude.com/docs/en/agent-sdk/typescript, accessed 2026-09-29).

Structured output does not stream as prose. With partial messages enabled, the schema-bound JSON arrives as unvalidated `input_json_delta` chunks of an internal tool call, and only the validated object reaches the final result (streaming-output page, accessed 2026-09-29). The BUILD-LEDGER image smoke of 2026-09-24 saw the CLI load its internal StructuredOutput tool, which agrees. A live turn that must stream readable text therefore cannot also use `--json-schema`.

Retries can stall a live turn. `CLAUDE_CODE_MAX_RETRIES` defaults to 10 and `API_TIMEOUT_MS` to 600,000 ms (https://code.claude.com/docs/en/env-vars, accessed 2026-09-29), and the TypeScript reference gives the worst case as roughly `API_TIMEOUT_MS x (CLAUDE_CODE_MAX_RETRIES + 1)` plus backoff. `build_env` passes neither variable today, so the CLI defaults apply and only the app's own 120 s `DEFAULT_TIMEOUT_SECONDS` bounds a call.

Session transcripts. Without `--no-session-persistence` the CLI writes transcripts under `~/.claude/projects/<encoded-cwd>/*.jsonl` (https://code.claude.com/docs/en/agent-sdk/sessions, accessed 2026-09-29). `--resume` needs that file, so resume-based multi-turn and the privacy rule of plan 09 pull in opposite directions. One process per conversation fed through `--input-format stream-json` holds the conversation in memory and needs no file. The sessions page lists "Multi-turn chat in one process" as the case for `ClaudeSDKClient`, which is the Python SDK's client over that input mode. That the raw CLI with `--no-session-persistence` keeps context across stream-json user messages is my reading of those two pages together and has not been run [inferred].

## Part 1. Thinking and effort through the CLI [verified]

Two sources agree that thinking cannot be turned off on `claude-sonnet-5-5` through the CLI. The model configuration page says the session toggle, `alwaysThinkingEnabled` and `MAX_THINKING_TOKENS=0` "have no effect" on Opus 5.5, Sonnet 5.5 or the Fable models (https://code.claude.com/docs/en/model-config, accessed 2026-09-29). The environment variable page says neither `CLAUDE_CODE_DISABLE_THINKING` nor `MAX_THINKING_TOKENS=0` turns thinking off on those models (https://code.claude.com/docs/en/env-vars, accessed 2026-09-29). The API's `between_tools` setting, which is how `app/providers/anthropic.py` turns up-front thinking off on Sonnet 5.5, has no documented CLI equivalent. On the subscription path the only latency lever for Sonnet 5.5 is `--effort`.

Default effort differs by surface. The API effort page says `high` is the default on Sonnet 5.5 (https://platform.claude.com/docs/en/build-with-claude/effort, accessed 2026-09-29). The Claude Code model configuration page says Opus 5.5 and Sonnet 5.5 default to `medium` in Claude Code (same model-config URL). Growth should always send `--effort` explicitly so the two surfaces cannot drift.

The 2026-09-23 latency table was taken on `claude-sonnet-5` and `claude-haiku-4-5`, where `MAX_THINKING_TOKENS=0` does act. It says nothing about `claude-sonnet-5-5`, the model `model_routing.py` now assigns the tutor. The Sonnet 5.5 subscription latency is unknown until measured.

## Part 1. Prompt caching through the CLI [verified]

What the CLI caches on its own. Claude Code orders each request as system prompt, then project context, then conversation, and caching matches the longest identical prefix (https://code.claude.com/docs/en/prompt-caching, accessed 2026-09-29). On a Claude subscription within plan usage, the main conversation, which includes `-p` runs, gets a one-hour TTL, and once usage credits are being drawn it drops to five minutes (same page). `CLAUDE_CODE_PROMPT_CACHE_TTL` set to `5m` or `1h` overrides that from 2.1.242 (same page and env-vars page, same date). Two sources for the minimum: the prompt caching page lists 512 tokens for `claude-sonnet-5-5` and `claude-opus-5-5`, 1,024 for `claude-sonnet-5` and `claude-opus-5`, and 4,096 for `claude-haiku-4-5` (https://platform.claude.com/docs/en/build-with-claude/prompt-caching, accessed 2026-09-29), and the Claude Code page says the subscription cache lives in Anthropic's infrastructure accessed through the Claude API, so the same minimums apply. Plan 14's 1,500 cached tokens on Sonnet 5 is consistent with a static system prompt above 1,024 tokens being cached without being asked.

What that means for a conversation on the current per-call path. Because `prompt_text` joins every message into one user message, the previous turn's cache entry ends mid-block in the next request. Cache writes happen only at breakpoints and lookups compare block boundaries (prompt caching page, same date), so on that path only the system prompt can hit [inferred]. Placing the student memory above `__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__` would cache it, but memory is derived from student text and the ground rules keep it out of any system prompt. Two layouts survive the rule. One keeps the static system prompt cached and re-sends memory uncached each turn. The other runs one long-lived process per conversation, so the CLI appends each turn to its own history and the whole growing prefix, memory included, stays cached.

Size of what is lost on the first layout. A memory block of about 2,000 tokens resent uncached is 2,000 x $2 / MTok = $0.004 a turn at the `claude-sonnet-5-5` API rate (https://platform.claude.com/docs/en/about-claude/pricing, accessed 2026-09-29). On the subscription it is usage, not money, and how the subscription weights cached against uncached tokens is not published. The usage-limit article says only that project content is cached and "counts less against your limits when reused" (https://support.claude.com/en/articles/9797557-usage-limit-best-practices, accessed 2026-09-29).

## Part 1. Terms for a single-user self-hosted installation [verified]

Two sources state the restriction the subscription backend already honours. The Agent SDK quickstart says Anthropic does not allow third-party developers "to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK" (https://code.claude.com/docs/en/agent-sdk/quickstart, accessed 2026-09-29). The Claude Code legal page says Anthropic does not permit developers "to route requests through Free, Pro, or Max plan credentials on behalf of their users" and adds that advertised Pro and Max limits "assume ordinary, individual usage of Claude Code and the Agent SDK" (https://code.claude.com/docs/en/legal-and-compliance, accessed 2026-09-29).

The consumer terms say you may not share account credentials "with anyone else" and "may not make your Account available to anyone else", and bar automated or non-human access except via an Anthropic API key or where otherwise explicitly permitted (https://www.anthropic.com/legal/consumer-terms, accessed 2026-09-29, effective 8 October 2025). The same terms require users to be at least 18 or the local age of consent, whichever is higher.

What is permitted, as far as the fetched pages go. The legal page allows an end user to sign in to the unmodified Claude Code binary with their own subscription. Headless `claude -p` runs on the operator's own login, on the operator's own machine, serving the operator's own single account, is the narrow reading plan 07 and plan 14 rely on. No page fetched states in so many words that powering a self-hosted application for its owner is permitted, and none states that it is barred.

What remains open [uncertain]. Growth's learner is a minor (plan 09). If the learner is not the adult who holds the subscription, a live agent that the learner converses with sends that learner's turns through the operator's consumer account. Whether that is "making the account available to anyone else" is not settled by any page fetched. This is the operator's decision, and the agent design below does not change the answer, only the volume.

Consumer data handling applies on this path. For Free, Pro and Max, deleted data leaves back-end storage within 30 days, and if the account holder allows use for model improvement, data "may" be kept de-identified for up to 5 years, and this covers coding sessions (https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data, accessed 2026-09-29). Flagged content is kept up to 2 years. Growth cannot read or set the operator's model-improvement toggle.

## Part 1. What a usage limit looks like [single-source]

The five-hour session limit and the weekly limit are shown as progress bars under Settings then Usage, and the article names the factors that count (message length, attachments, conversation length, tool use, model, effort) without publishing a count (https://support.claude.com/en/articles/9797557-usage-limit-best-practices, accessed 2026-09-29). The Pro and Max support page says Claude and Claude Code share one set of limits, lists the options at a limit (upgrade, usage credits, switch to the Console, or wait for the reset), and publishes no count either (https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan, accessed 2026-09-29). Both come from one publisher, so the absence of a published count is tagged single-source.

What the application can know in a live turn. From the documented stream it can see a `system/api_retry` line whose `error` is `rate_limit`, an assistant message whose error category is `rate_limit`, and a final `result` with `is_error` and a text line. The adapter's `_LIMIT_PATTERNS` were read out of the 2.1.277 binary on 2026-09-24 and no real limit answer has been observed. Whether the CLI reports when the window resets, as a timestamp or as text, is unknown. A fetch summary of the TypeScript reference described a `rate_limit_event` with a reset time, but a verbatim re-read found no such text on the page, so it is not relied on here [uncertain].

## Part 2. The Anthropic API key path [verified]

Model ids as the models overview prints them (https://platform.claude.com/docs/en/about-claude/models/overview, accessed 2026-09-29).

| Model | API id | Alias | Comparative latency | Thinking | Default effort | Context and max output | Retirement not sooner than |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Fable 5.1 | `claude-fable-5-1` | `claude-fable-5-1` | Slower | Adaptive, always on | high | 1M, 128K | 1 September 2027 |
| Claude Opus 5.5 | `claude-opus-5-5` | `claude-opus-5-5` | Moderate | Adaptive, always on | medium | 1M, 128K | 22 September 2027 |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | `claude-sonnet-5-5` | Fast | Adaptive | high | 1M, 128K | 28 September 2027 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | `claude-haiku-4-5` | Fastest | Extended | not supported | 200K, 64K | 15 October 2026 |

Legacy but available: `claude-opus-5` and `claude-sonnet-5`, among others (same page). Haiku 4.5's retirement floor is 16 days after this file's date, which matters for any chain that leans on it.

Thinking per model, from the per-model table of https://platform.claude.com/docs/en/build-with-claude/thinking (accessed 2026-09-29), agreeing with the effort page for the Sonnet 5.5 and Opus 5.5 rows.

| Model | `adaptive` | `between_tools` | `disabled` |
| --- | --- | --- | --- |
| `claude-opus-5-5` | accepted | 400 | 400 at every effort |
| `claude-sonnet-5-5` | accepted | up-front thinking off at effort high or below, 400 at xhigh or max | 400 |
| `claude-opus-5` | accepted | 400 | thinking off at effort high or below |
| `claude-sonnet-5` | accepted | 400 | thinking off |
| `claude-haiku-4-5` | 400 | 400 | thinking off (also the default) |

The effort parameter is `output_config.effort`, levels `low`, `medium`, `high`, `xhigh`, `max`, unsupported on Haiku 4.5. Sonnet 5.5's levels are recalibrated against Sonnet 5, and the effort page advises starting chat and other latency-sensitive work at `medium` or `low`. On Sonnet 5.5 with `between_tools`, a per-message effort change returns 400, so the agent should hold one effort level for a conversation. A non-default `temperature`, `top_p` or `top_k` is a 400 on every current Opus and Sonnet model (thinking page). No docs page fetched prints a streaming latency figure. The overview's latency column is relative only.

Prices per million tokens (https://platform.claude.com/docs/en/about-claude/pricing, accessed 2026-09-29).

| Model | Input | 5m cache write | 1h cache write | Cache read | Output | Batch in / out |
| --- | --- | --- | --- | --- | --- | --- |
| `claude-opus-5-5` | $4 | $5 | $8 | $0.20 (0.05x) | $20 | $2 / $10 |
| `claude-sonnet-5-5` | $2 | $2.50 | $4 | $0.20 | $10 | $1 / $5 |
| `claude-haiku-4-5` | $1 | $1.25 | $2 | $0.10 | $5 | $0.50 / $2.50 |
| `claude-sonnet-5` | $2 | $2.50 | $4 | $0.20 | $10 | $1 / $5 |

The models overview agrees on base prices and on Opus 5.5's 5 percent cache read. `inference_geo: "us"` multiplies every category by 1.1. `app/providers/guard.py` prices every cache read at `CACHE_READ_MULTIPLIER = 0.1`, which overstates an Opus 5.5 read by a factor of two. No agent recommendation below uses Opus 5.5, so this is recorded and not acted on here.

Streaming. `"stream": true` returns SSE with `message_start`, content blocks of `content_block_start`, `content_block_delta` and `content_block_stop`, then `message_delta` and `message_stop`, with `ping` events anywhere and an `error` event such as `overloaded_error` possible mid-stream (https://platform.claude.com/docs/en/build-with-claude/streaming, accessed 2026-09-29, and the headless page's description of the same events, same date). Usage in `message_delta` is cumulative. For recovery on Claude 4.6 and later the page advises capturing the partial text and asking the model to continue in a new user message.

Structured output. `output_config.format` with `{"type": "json_schema", "schema": ...}` on `claude-opus-5-5`, `claude-sonnet-5-5` and `claude-haiku-4-5`. Recursive schemas, numeric bounds and string length bounds are unsupported. A new schema pays a grammar compilation delay, cached 24 hours from last use, and changing the format invalidates the prompt cache (https://platform.claude.com/docs/en/build-with-claude/structured-outputs, accessed 2026-09-29).

Caching rules the prefix layout depends on (prompt caching page, same date). Up to 4 breakpoints. Automatic caching is one top-level `cache_control` that moves the breakpoint to the last cacheable block. A breakpoint looks back at most 20 blocks. Longer TTLs must come before shorter ones. The hierarchy is tools, then system, then messages, and a change at one level invalidates it and everything after. Cache hits need 100 percent identical segments. Caches are isolated per workspace. Cache reads do not count toward ITPM on current models, which the rate limits page confirms (https://platform.claude.com/docs/en/api/rate-limits, accessed 2026-09-29).

Rate limits and spend caps (rate limits page, same date). Start tier gives `claude-sonnet-5-5`, `claude-opus-5-5` and `claude-haiku-4-5` each 1,000 RPM, 2,000,000 ITPM and 400,000 OTPM, with a $500 monthly spend cap. A spend cap answers HTTP 429 `rate_limit_error` with `error_code` `enforced_spend_limit_reached` and no `retry-after`, so a retry loop cannot tell it from a rate limit unless it reads that code. A self-set spend limit answers HTTP 400 `invalid_request_error`. None of these limits bind one student.

Retention. The platform page says conversation content "is not retained by default" apart from the Covered Models (the Fable and Mythos lines), which require 30 days, and that retained data is never used for training without permission. ZDR is per organization through sales, and both prompt caching and structured outputs are ZDR-eligible (https://platform.claude.com/docs/en/manage-claude/api-and-data-retention, accessed 2026-09-29). The commercial privacy article says inputs and outputs are deleted within 30 days (https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data, accessed 2026-09-29). The two disagree on the default, so the retention row should state the longer figure, 30 days. Flagged content can be kept up to 2 years on either. Anthropic's guidelines for organizations serving minors apply to API products minors interact with and require disclosure that the user is talking to an AI, plus age checks, moderation and monitoring (https://support.claude.com/en/articles/9307344-responsible-use-of-anthropic-s-models-guidelines-for-organizations-serving-minors, accessed 2026-09-29).

## Part 2. OpenAI [verified]

Current recommended models (https://developers.openai.com/api/docs/models, accessed 2026-09-29) and standard prices per million tokens (https://developers.openai.com/api/docs/pricing, accessed 2026-09-29).

| Model id | Position on the models page | Input | Cached input | Output |
| --- | --- | --- | --- | --- |
| `gpt-6-astra` | most capable | $10.00 | $1.00 | $50.00 |
| `gpt-6.1-sol` | balances performance and price | $2.00 | $0.10 | $10.00 |
| `gpt-6-luna` | most efficient | $0.10 | $0.01 | $0.50 |
| `gpt-5.6-sol` | earlier mid model, promotional through at least 21 November 2026 | $4.00 | $0.40 | $20.00 |

Streaming is `stream: true` on the Responses API with typed SSE events including `response.created`, `response.output_text.delta`, `response.completed` and `error` (https://developers.openai.com/api/docs/guides/streaming-responses, accessed 2026-09-29, matching plan 07's reading of 2026-09-20). Structured output is `text.format` with `type: "json_schema"` and `strict: true`, and a refusal arrives in a separate `refusal` field (https://developers.openai.com/api/docs/guides/structured-outputs, accessed 2026-09-29). Prompt caching is automatic, the minimum is 1,024 visible input tokens on GPT-5.6 and later, reads are 0.1x (0.05x on GPT-6.1 Sol), and a prefix stays reusable 30 minutes after its last use (https://developers.openai.com/api/docs/guides/prompt-caching, accessed 2026-09-29).

Retention. Abuse monitoring logs are kept up to 30 days, API data is not used for training unless the customer opts in, and Responses `store` defaults to true, keeping response data at least 30 days (https://developers.openai.com/api/docs/guides/your-data, accessed 2026-09-29). ZDR needs prior approval. OpenAI's under-18 guidance requires age-appropriate filtering, disclosure, monitoring and age verification, and ZDR before processing personal data of children under 13 (https://developers.openai.com/api/docs/guides/safety-checks/under-18-api-guidance, accessed 2026-09-29).

Role for a live agent. Technically capable of streaming a tutor. Excluded by the operator's Claude-only instruction recorded in `app/providers/model_routing.py`, and on its own terms it would need `store: false` on every call.

## Part 2. Gemini [verified]

Paid-tier prices per million tokens (https://ai.google.dev/gemini-api/docs/pricing, accessed 2026-09-29).

| Model id | Input | Output | Cache read | Cache storage per hour |
| --- | --- | --- | --- | --- |
| `gemini-3.8-flash` | $0.75, $1.50 after 31 December 2026 | $3.75, then $7.50 | $0.075, then $0.15 | $0.50, then $1.00 |
| `gemini-3.5-flash-lite` | $0.30 | $2.50 | $0.03 | $1.00 |
| `gemini-3.1-flash-lite` | $0.25 text | $1.50 | $0.025 | $1.00 |
| `gemini-3.1-pro-preview` | $2.00 up to 200k | $12.00 | $0.20 | $4.50 |

Streaming uses `?alt=sse` on REST or `stream=True` in the SDK, system text goes in `system_instruction`, and thinking is steered by `thinking_level` (https://ai.google.dev/gemini-api/docs/text-generation, accessed 2026-09-29). Structured output streams as valid partial JSON chunks (https://ai.google.dev/gemini-api/docs/structured-output, accessed 2026-09-29). Implicit caching is on by default with a 4,096-token minimum on the 3.5 to 3.8 Flash models and 2,048 on 2.5, and savings pass on automatically (https://ai.google.dev/gemini-api/docs/caching, accessed 2026-09-29). A prompt shaped for Sonnet 5.5's 512-token minimum will not cache on Gemini Flash.

Data use. Paid services do not use prompts or responses to improve Google products. Unpaid services do, and human reviewers may read the content (https://ai.google.dev/gemini-api/terms, accessed 2026-09-29, matching plan 07's reading of 2026-09-20).

Role for a live agent. None. The same terms, under "Age Requirements", say the Services may not be used in an application "directed towards or is likely to be accessed by individuals under the age of 18" (https://ai.google.dev/gemini-api/terms, accessed 2026-09-29, read twice verbatim). Growth is built for a minor learner. This also bears on plan 07's fallback JSON, which lists `gemini-3.8-flash` second in the tutor chain, and it is a finding for a plan amendment rather than something this file settles. The Claude-only instruction excludes Gemini anyway.

## Part 2. OpenRouter [verified]

Streaming is SSE with `stream: true`. Keepalive comment lines `: OPENROUTER PROCESSING` must be skipped before JSON parsing, a mid-stream error arrives under HTTP 200 with `finish_reason: "error"`, and cancelling stops billing only on providers that support it, OpenAI and Anthropic among them (https://openrouter.ai/docs/api-reference/streaming, accessed 2026-09-29, matching plan 07). Caching passes `cache_control` through to Anthropic models, reads are 0.1x for Anthropic, sticky routing keeps a provider for 10 minutes of inactivity, and usage shows in `prompt_tokens_details.cached_tokens` (https://openrouter.ai/docs/features/prompt-caching, accessed 2026-09-29). Provider preferences include `data_collection` set to `"deny"` to use only providers that do not store user data, `zdr: true` for ZDR endpoints only, `allow_fallbacks`, `order`, `sort` and `preferred_max_latency` (https://openrouter.ai/docs/features/provider-routing, accessed 2026-09-29). OpenRouter does not store prompts or responses unless the account opts in, but does store request metadata (https://openrouter.ai/docs/guides/privacy/data-collection, accessed 2026-09-29). Paid models have no platform request cap, and credit exhaustion returns 402 (https://openrouter.ai/docs/api-reference/limits, accessed 2026-09-29).

Role for a live agent. None that the direct Anthropic key does not already cover. Routed to Anthropic it reaches the same models behind an extra hop, and its own terms on minors were not found on the pages fetched [uncertain].

## Part 2. Ollama, the offline floor [single-source]

Local base `http://localhost:11434/v1/`, key ignored, with `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/responses` (stateless, v0.13.3 and later) and `/v1/models`. Streaming, JSON mode, vision and reasoning control work, and `tool_choice`, logprobs and image URLs do not (https://docs.ollama.com/api/openai-compatibility, accessed 2026-09-29, agreeing with plan 07). Streaming is on by default on the REST API and chunks carry `message.content` and, on thinking models, `message.thinking` (https://docs.ollama.com/capabilities/streaming, accessed 2026-09-29). Thinking is set with `think` as true, false or a level (https://docs.ollama.com/capabilities/thinking, accessed 2026-09-29). Structured output is `format` with a JSON schema natively or `response_format` on the compatible path, local only, with the advice to set temperature 0 and repeat the schema in the prompt (https://docs.ollama.com/capabilities/structured-outputs, accessed 2026-09-29). No provider retention applies because nothing leaves the machine.

Small models whose library pages claim maths strength. Each claim is the model publisher's, not a measurement.

| Tag | Download size | Context | Library page claim |
| --- | --- | --- | --- |
| `phi4-mini-reasoning:3.8b` | 3.2 GB | 128K | designed for multi-step, logic-intensive mathematical problem solving under compute limits (https://ollama.com/library/phi4-mini-reasoning, accessed 2026-09-29) |
| `qwen3:8b` | 5.2 GB | 40K | reasoning above QwQ and Qwen2.5 on mathematics (https://ollama.com/library/qwen3, accessed 2026-09-29) |
| `qwen3:14b` | 9.3 GB | 40K | same family claim |
| `deepseek-r1:8b` | 5.2 GB | 128K | strong on mathematics, programming and logic (https://ollama.com/library/deepseek-r1, accessed 2026-09-29) |
| `deepseek-r1:14b` | 9.0 GB | 128K | same family claim |

VRAM and tokens per second on the operator's machine are not published and must be measured. None of these has been checked against AP Calculus BC items in this repository.

## Part 2. claudebox [verified]

Restated only to close the list. claudebox buffers the child process output and has no SSE path (plan 07, "The claudebox adapter"), and the tutor role is never routed to it. An agent role that talks to a student falls under the same refusal.

## Measured on 2026-09-29 by the orchestrator [verified]

Four live calls through the installed CLI (2.1.284) on the operator's subscription, made by the orchestrator after this file was drafted, settle four of the unknowns above. Each ran `claude -p --output-format stream-json --include-partial-messages --verbose --no-session-persistence` with the lockdown flags `build_argv` applies, `--model claude-sonnet-5-5 --effort low`, `MAX_THINKING_TOKENS=0`, and on calls 2 to 4 `CLAUDE_CODE_MAX_RETRIES=1` and `API_TIMEOUT_MS=20000`, from an empty temporary directory. Call 1 used a two-sentence system prompt. Calls 2 to 4 used the static prefix of `prompts/tutor/guardrailed_practice_v1.md` grown with a filler block to about 2,380 tokens, one process per call, with a different student message each time. The tag is [verified] because the numbers were read off the CLI's own `result` and `rate_limit_event` lines and the script is recorded in the run's ledger entry.

| Call | Time to first `text_delta` | Wall | `cache_read_input_tokens` | `cache_creation_input_tokens` | Output tokens | Thinking tokens | `total_cost_usd` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | not timed | 1.7 s (`duration_ms`) | 0 | 0 | 60 | 0 | 0.00157 |
| 2 | 3.34 s | 5.09 s | 0 | 2,380 | 230 | 148 | 0.01182 |
| 3 | 2.82 s | 4.60 s | 1,906 | 454 | 86 | 0 | 0.00306 |
| 4 | 3.21 s | 5.18 s | 1,906 | 474 | 307 | 183 | 0.00535 |

What this settles.

1. The CLI streams partial text through `stream_event` lines whose `event.delta.type` is `text_delta`, in the order the headless page describes, and the final `result` line carries usage and cost. Time to first visible text on `claude-sonnet-5-5` at effort low is about 3 s and a short reply completes in about 5 s, of which about 1 s is process start and exit.
2. One process per turn hits the prompt cache on the system prompt. Calls 3 and 4 read 1,906 cached tokens written by call 2, so a static system prefix above the 512-token minimum is cached across separate `claude -p` processes without a long-lived process. What is not cached is the user message, which is where memory, screen context and the conversation history go on the per-turn path.
3. `MAX_THINKING_TOKENS=0` does not switch thinking off on `claude-sonnet-5-5`: calls 2 and 4 spent 148 and 183 thinking tokens at effort low, which agrees with the model configuration page. Effort low keeps the thinking short, and it is the only lever on this model through the CLI.
4. The CLI emits a `rate_limit_event` line on every call. Its `rate_limit_info` carried `status: allowed`, `rateLimitType: five_hour`, `resetsAt` as a Unix timestamp, `overageStatus: rejected`, and `unifiedWindows` with `five_hour` and `seven_day` entries each holding `utilization` (0.18 and 0.29 on these calls) and `resetsAt`. So the application can read the utilisation of both windows and the reset time of each on every call, before any limit is met, and can show a reset time when a limit stops the agent. What a limit answer itself looks like is still unobserved.

The three replies each declined to say whether the draft was right and asked which part was the outside and which the inside function, so the current template's guardrail held on the model the tutor is routed to.

## What this means for Growth [inferred]

Ranked. Each item names the alternative rejected.

1. Stream the agent on the subscription through one long-lived CLI process per conversation. Start `claude -p --input-format stream-json --output-format stream-json --verbose --include-partial-messages --no-session-persistence --model claude-sonnet-5-5 --effort low`, with the same setting, MCP, slash-command and tool lockdown `build_argv` already applies. Send each student turn as one stream-json user message, and forward each `stream_event` whose delta is `text_delta` to the client. Close the process after 10 idle minutes or at the conversation cap. Rejected: the current per-call `SubscriptionProvider.stream`, which shows nothing until the process exits, pays about one second of start-up per turn, and caches only the system prompt because `prompt_text` flattens history. Also rejected: the Python Agent SDK, which would add a dependency that bundles its own CLI binary where the installed CLI already speaks the same protocol. The multi-turn behaviour of this mode without persistence is not yet run, so the first slice measures it before building on it.

2. Keep the live turn plain text and move structure off the path. The conversational reply streams as prose with no `--json-schema` and no `output_config.format`. Memory updates, self-tuning signals and any classification of the turn run afterwards as a job in the `jobs` table through the drain, with their own schema. Rejected: one structured call that returns both the reply and the memory patch, because structured output reaches the client only after validation and would remove streaming. It would also put a changing schema on the conversation's cache key.

3. Map both transports onto the one SSE route plan 06 already names, `GET /sessions/{id}/stream`, with the normalised `start`, `text`, `usage`, `end` and `error` events. The CLI `stream_event` carries the same Messages API events as API SSE, so one mapper serves both once the `stream_event` wrapper is removed. Change `FallbackChain.stream` so a link may be abandoned only before its first `text` event. After the first delta, a failure ends the turn with the partial text marked incomplete and no fallback, because splicing a second model's words onto the first misrepresents one answer as another. Rejected: the current chain, which chooses a link by waiting for its whole result.

4. Fallback chain for the agent role, per backend.

   | `GROWTH_AI_BACKEND` | Order | Condition to move on |
   | --- | --- | --- |
   | `subscription` | subscription `claude-sonnet-5-5`, effort low, then unavailable state | limit, pacing stop, auth failure, missing CLI, or no first text within 15 s |
   | `api` | subscription as above, then API `claude-sonnet-5-5` with `thinking: {"type": "between_tools"}` and effort low, then unavailable state | same, plus API budget stop or 429 or 529 before the first delta |
   | either, with a local model configured | the chain above, then Ollama `qwen3:8b` or `phi4-mini-reasoning:3.8b`, labelled offline | every hosted link refused |

   Rejected for the live agent: `claude-opus-5-5` (thinking cannot be turned off, moderate latency, $4 and $20 per MTok), `claude-haiku-4-5` as a standing link (retirement floor 15 October 2026, and a 4,096-token caching minimum a short prefix will not meet), Gemini (its terms bar applications likely to be used by under-18s), OpenAI and OpenRouter (the operator's Claude-only instruction, and on OpenAI `store` defaults to true), claudebox (no streaming, and never for this role). The Ollama floor is restricted to explaining a submitted item from its stored worked solution and to navigation help. It is never used for hints on an unsubmitted item, because no local model here has been checked on BC mathematics and a confident wrong hint is worse than none.

5. Bound every live turn in time. Add `CLAUDE_CODE_MAX_RETRIES=1` and an `API_TIMEOUT_MS` of 20,000 to the agent's subprocess environment, fixed values never copied from the host, in the way `THINKING_DISABLED_VALUE` is handled. On any `system/api_retry` whose `error` is `rate_limit` or `authentication_failed`, send SIGINT and degrade at once. SIGINT, not SIGTERM, because the headless page says SIGTERM leaves the turn unfinished with no result. Rejected: the CLI defaults, under which a student could wait through ten retries against a closed window.

6. Prefix layout.

   On the API, in order: no tools. System block holding the static agent policy, the untrusted-content policy and the AP Calculus BC conventions, with `cache_control` at `ttl: "1h"`. The first user message holding the memory as JSON, with a second `1h` breakpoint. Then the conversation turns carrying only what the student typed and what the agent said, never earlier screen snapshots. A third breakpoint, `5m`, on the last assistant message. Then the new user message, which carries the current screen context as JSON and stays uncached, because next turn's history keeps only the student's words and a cache write of this block would never be read. That uses three of four breakpoints, puts 1h entries before 5m as the rules require, and keeps the system prompt above Sonnet 5.5's 512-token minimum.

   On the subscription, the system prompt is the same static block. Memory goes in the conversation's first user message and each turn's screen context in that turn's message. The long-lived process keeps its own history, so the prefix grows by appending and the CLI's one-hour main-conversation TTL covers it. Screen context stays in that history, so it must stay small, a few hundred tokens of structured state. Rejected: memory above `__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__`, which would cache but would put student-derived text in a system prompt.

7. Degraded states.

   | Trigger | What the app knows | What the student sees | Queue |
   | --- | --- | --- | --- |
   | Subscription usage limit | limit text or a `rate_limit` category, reset time unknown | one line saying the tutor is unavailable until the Claude usage window resets, and that practice continues | No |
   | Agent pacing cap, day or minute | which cap bound | unavailable for today, or asked to wait a moment | No |
   | Sign-in expired | `authentication_failed` | unavailable, and the operator settings screen says to sign in again | No |
   | CLI missing or no first text in 15 s | refused before the wire, or timeout | unavailable for now, and the typed message kept in the box | No |
   | API budget or spend-cap stop | the guard's cap, or `enforced_spend_limit_reached` | unavailable for today | No |
   | Every hosted link down, local model configured | chain exhausted | the offline model with its restricted scope, labelled as offline | No |

   Rejected: queueing a conversational turn through `queue_call`. A reply delivered 30 minutes later is not a reply, and the queue payload stores the full `messages` content, which for an agent is the student's own text in the `jobs` table. The student's unsent draft stays on the client until the student sends or clears it.

8. Caps for a new `agent` role. It needs its own entry in `ROLES`, its own `GROWTH_SUBSCRIPTION_AGENT_CALLS_PER_DAY` and per-minute rate, and its own dollar and token row, never the tutor's.

   Subscription. 20 turns a conversation, matching `TUTOR_CALLS_PER_SESSION`, and 4 conversations a day, gives 80 calls a day. 6 a minute, above the default of 4, because a short reply such as "yes" can follow an answer within ten seconds. Load estimate: a 5,000-token prefix (system about 2,500, memory about 2,000, screen about 500) and 450 tokens added per turn give a 20-turn conversation 20 x 5,000 + 450 x (0 + 1 + ... + 19) = 185,500 input tokens, or about 9,300 a turn and about 740,000 a day at 80 turns, most of it cache reads. Output at about 400 tokens a turn is about 32,000 a day. The tutor's measured day in plan 14 is about 150,000 tokens, so this role is roughly five times the tutor's load against windows whose size is not published. The first week should be read against Settings then Usage and the cap lowered if the weekly bar climbs faster than the operator's own work allows.

   API, at `claude-sonnet-5-5` prices. The same 20-turn conversation costs 185,500 x $0.20 / MTok = $0.0371 in cache reads, 9,000 x $2.50 / MTok = $0.0225 in 5-minute writes, 5,000 x $4 / MTok = $0.0200 for the 1-hour prefix write, and 8,000 x $10 / MTok = $0.0800 in output, $0.1596 in all, about $0.008 a turn and about $0.64 a day at 80 turns. Cap at $1.50 and 1,500,000 tokens a day, about 2.3 times the expected spend, with `max_output_tokens` of 800 a turn. The guard's worst-case pre-check for one turn is 15,000 uncached input tokens at $2 / MTok plus 800 output at $10 / MTok, $0.038, well inside the cap. Used every day to an early-May exam, about 216 days, the expected rate is about $138, above the operator's $100.00 ceiling, and the persistent $15.00 developer cap would cover about 1,875 turns, about 23 full days. The API stays a fallback for this role for that reason as well as for the terms.

9. Privacy rows before any code. The agent's transcript, memory and screen snapshots each need a plan 09 retention row, purge, export, and a student view and delete. `--no-session-persistence` stays mandatory on the agent's process so no transcript lands under `~/.claude/projects/`. The raw stream lines are parsed in memory and never logged. The operator should be told plainly that on the subscription path the student's words travel under the operator's consumer terms, and that the model-improvement setting in the operator's Claude account decides whether they may be kept up to 5 years. Growth cannot check that toggle.

10. Measure before tuning. Run the smoke tool's pattern against `claude-sonnet-5-5` for time to first text delta and total time at `--effort low` and `medium`, on the per-call path and on the long-lived path, 10 calls each. Confirm that stream-json input keeps context across turns with persistence off. Capture one real usage-limit answer in stream-json, including whether it names a reset time. Until then every latency figure in this file for Sonnet 5.5 is unknown.

## Claims I could not source [uncertain]

- Numeric sizes of the five-hour and weekly subscription windows. No page fetched publishes them.
- How subscription usage weights cached against uncached tokens through the CLI.
- The shape of a usage-limit answer in stream-json. The `rate_limit_event` line and its reset time were observed on allowed calls (see the measured section), but no limit answer has been observed.
- Whether a long-lived `--input-format stream-json` process with `--no-session-persistence` keeps multi-turn context. Inferred from the sessions and headless pages, not run, and not needed once the per-turn path was measured to cache the system prefix.
- Any streaming latency figure from the documentation. The docs give relative latency only; the measured section gives the only numbers.
- Whether a minor who is not the subscription holder conversing through the operator's login is "making the account available to anyone else".
- OpenRouter's own terms on applications used by minors.
- VRAM and speed of the Ollama models on the operator's machine, and their accuracy on BC items.
- Which of the two Anthropic commercial retention statements (not retained by default, or deleted within 30 days) governs a Growth API call.

## Sources [verified]

- https://code.claude.com/docs/en/cli-reference, accessed 2026-09-29
- https://code.claude.com/docs/en/headless, accessed 2026-09-29
- https://code.claude.com/docs/en/agent-sdk/streaming-output, accessed 2026-09-29
- https://code.claude.com/docs/en/agent-sdk/quickstart, accessed 2026-09-29
- https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts, accessed 2026-09-29
- https://code.claude.com/docs/en/agent-sdk/sessions, accessed 2026-09-29
- https://code.claude.com/docs/en/agent-sdk/typescript, accessed 2026-09-29
- https://code.claude.com/docs/en/prompt-caching, accessed 2026-09-29
- https://code.claude.com/docs/en/env-vars, accessed 2026-09-29
- https://code.claude.com/docs/en/model-config, accessed 2026-09-29
- https://code.claude.com/docs/en/legal-and-compliance, accessed 2026-09-29
- https://code.claude.com/docs/en/authentication, accessed 2026-09-29
- `claude -p --help` and `claude --version` (2.1.284), run locally 2026-09-29
- https://www.anthropic.com/legal/consumer-terms, accessed 2026-09-29
- https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan, accessed 2026-09-29
- https://support.claude.com/en/articles/9797557-usage-limit-best-practices, accessed 2026-09-29
- https://support.claude.com/en/articles/9307344-responsible-use-of-anthropic-s-models-guidelines-for-organizations-serving-minors, accessed 2026-09-29
- https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data, accessed 2026-09-29
- https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data, accessed 2026-09-29
- https://platform.claude.com/docs/en/about-claude/models/overview, accessed 2026-09-29
- https://platform.claude.com/docs/en/about-claude/pricing, accessed 2026-09-29
- https://platform.claude.com/docs/en/build-with-claude/thinking, accessed 2026-09-29
- https://platform.claude.com/docs/en/build-with-claude/effort, accessed 2026-09-29
- https://platform.claude.com/docs/en/build-with-claude/streaming, accessed 2026-09-29
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs, accessed 2026-09-29
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching, accessed 2026-09-29
- https://platform.claude.com/docs/en/api/rate-limits, accessed 2026-09-29
- https://platform.claude.com/docs/en/manage-claude/api-and-data-retention, accessed 2026-09-29
- https://developers.openai.com/api/docs/models, accessed 2026-09-29
- https://developers.openai.com/api/docs/pricing, accessed 2026-09-29
- https://developers.openai.com/api/docs/guides/streaming-responses, accessed 2026-09-29
- https://developers.openai.com/api/docs/guides/structured-outputs, accessed 2026-09-29
- https://developers.openai.com/api/docs/guides/prompt-caching, accessed 2026-09-29
- https://developers.openai.com/api/docs/guides/your-data, accessed 2026-09-29
- https://developers.openai.com/api/docs/guides/safety-checks/under-18-api-guidance, accessed 2026-09-29
- https://ai.google.dev/gemini-api/docs/pricing, accessed 2026-09-29
- https://ai.google.dev/gemini-api/docs/caching, accessed 2026-09-29
- https://ai.google.dev/gemini-api/docs/text-generation, accessed 2026-09-29
- https://ai.google.dev/gemini-api/docs/structured-output, accessed 2026-09-29
- https://ai.google.dev/gemini-api/terms, accessed 2026-09-29
- https://openrouter.ai/docs/api-reference/streaming, accessed 2026-09-29
- https://openrouter.ai/docs/features/prompt-caching, accessed 2026-09-29
- https://openrouter.ai/docs/features/provider-routing, accessed 2026-09-29
- https://openrouter.ai/docs/guides/privacy/data-collection, accessed 2026-09-29
- https://openrouter.ai/docs/api-reference/limits, accessed 2026-09-29
- https://docs.ollama.com/api/openai-compatibility, accessed 2026-09-29
- https://docs.ollama.com/capabilities/streaming, accessed 2026-09-29
- https://docs.ollama.com/capabilities/thinking, accessed 2026-09-29
- https://docs.ollama.com/capabilities/structured-outputs, accessed 2026-09-29
- https://ollama.com/library/qwen3, accessed 2026-09-29
- https://ollama.com/library/phi4-mini-reasoning, accessed 2026-09-29
- https://ollama.com/library/deepseek-r1, accessed 2026-09-29
- Repository files read 2026-09-29: `app/providers/subscription.py`, `app/providers/guard.py`, `app/providers/router.py`, `app/providers/call_queue.py`, `app/providers/anthropic.py`, `app/providers/model_routing.py`, `app/feedback/drain.py`, `app/feedback/autodrain.py`, `app/feedback/tutor.py`, `docs/plan/06-architecture.md`, `docs/plan/07-ai-provider-layer.md`, `docs/plan/14-token-economy.md`, `BUILD-LEDGER.md`
