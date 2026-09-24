---
title: AI provider layer
research_date: 2026-09-19
status: draft
purpose: Specify the provider abstraction, the role routing and fallback policy, the per-provider adapters, the budget and prompt-template controls, and the single-operator restriction on the claudebox adapter.
---

# AI provider layer

This document specifies the component labelled "Provider layer" in `06-architecture.md`. Everything that calls a model goes through it. No caller constructs a provider request directly, because the budget guard, the usage accounting and the audit trail all live at this seam and a bypass would defeat all three.

Every number carries the URL it was read from and an evidence tag. Numbers that follow from a decision rather than a source are tagged `[inferred]` and listed in `12-open-questions.md`. Unknown means unknown; nothing here is recalled from memory.

The routing is D8 and is not reopened. What this document adds is the interface shape, the per-adapter trap list, the fallback policy, the budget behaviour and the guard on claudebox.

## Provider abstraction

The interface is shaped like the Vercel AI SDK's language model specification, which abstracts provider differences behind one API across 23 official providers and 35 or more community ones, with any OpenAI-spec endpoint reachable through an OpenAI Compatible provider (https://ai-sdk.dev/docs/foundations/providers-and-models [verified]). The specification is the right shape for three reasons, in the project's priority order.

Learning impact first. The roles that matter most for correctness are the verifier and the grader, and both need provider-specific features that a lowest-common-denominator interface would flatten away: Anthropic's structured outputs through `output_config.format`, Gemini's `responseSchema` with recursive `$ref`, Ollama's `format` accepting a full JSON schema. Flattening those into a single "json mode" boolean would mean the grader's per-point schema stops being enforced by the provider and starts being enforced by hope. The AI SDK's answer is one call signature with provider-specific settings passed through rather than flattened, which is exactly what is needed.

Cost second. Usage accounting including cached tokens has to be part of the return value, not an afterthought, because the entire cost-control story in `06-architecture.md` depends on knowing the cached read fraction per role. The AI SDK exposes `usage` with `inputTokens`, `outputTokens` and `totalTokens` plus throughput and time-to-first-token metrics; whether `cachedInputTokens` and `reasoningTokens` are exposed was not visible on the loaded page and is unknown (https://ai-sdk.dev/docs/ai-sdk-core/generating-text [verified]). Since it is unknown in the reference implementation, this project's interface states those fields explicitly rather than assuming them, and each adapter is responsible for populating them from the provider's own usage block.

Convenience third. The registry pattern, `createProviderRegistry` with IDs in `providerId:modelId` form and a configurable separator (https://ai-sdk.dev/docs/reference/ai-sdk-core/provider-registry [verified]), gives a clean way to name a deployment in configuration.

The call signature, as a shape rather than as code:

```
call(
  role,                # tutor | generator | verifier | grader | diagnostician | transcriber
  messages,            # normalised message list; system content separated
  system,              # the cache-prefix-stable system block for this role
  output_schema,       # JSON schema or null
  temperature,
  max_output_tokens,
  images,              # list of {bytes, media_type} or null
  stream,              # bool
  cache,               # {prefix_breakpoints: n, ttl: "5m" | "1h"}
  provider_options,    # opaque, passed through to the adapter untouched
  idempotency_key,
  correlation_id
) -> {
  text | structured,
  stream_events,       # the normalised event vocabulary from 06-architecture.md
  usage: {
    input_tokens, output_tokens,
    cached_read_tokens, cached_write_tokens,
    reasoning_tokens        # null where the provider does not report it
  },
  provider, model, request_id,
  finish_reason,
  raw_usage            # the provider's own usage block, retained for reconciliation
}
```

Three properties of that shape are load bearing.

`provider_options` is opaque. The router never inspects it and the adapter passes it through. This is what lets the generator set Anthropic's `thinking: {type: "adaptive"}` with `output_config: {effort: ...}` without the interface learning what adaptive thinking is.

`usage` always has all four token fields, with null meaning the provider did not report rather than zero. The distinction matters because a zero cached read is a cache miss to investigate and a null is a provider that does not tell you. Conflating them would make the cache hit rate metric in `10-quality-and-evaluation.md` silently wrong.

`raw_usage` is retained so the `budgets` table can be reconciled against a provider invoice later. Token accounting computed by the client is an estimate; the provider's own block is the record.

Middleware is the extension point, following the AI SDK's `wrapLanguageModel({model, middleware})` with hooks `transformParams`, `wrapGenerate` and `wrapStream` (https://ai-sdk.dev/docs/ai-sdk-core/middleware [verified]). This project's middleware stack, outermost to innermost, is: audit and correlation, budget guard, pre-call context check, fallback chain, prompt cache annotation, then the adapter. The fallback ladder has to be written as middleware because the AI SDK documents no built-in fallback primitive and a named fallback middleware is unknown on the loaded page (same URL [verified as absent]).

## Roles and routing

Six roles, and only six: tutor, generator, verifier, grader, diagnostician, transcriber. There is no classifier role and no other role may be added without a decision recorded here (R17). The separation is not organisational tidiness; each boundary exists because crossing it would damage something.

| Role | What it does | Streams | Tools | Structured output | Temperature |
| --- | --- | --- | --- | --- | --- |
| tutor | Guardrailed support during practice; never gives the final answer | Yes | None, ever | No | 0.3 [inferred] |
| generator | Parameter substitution into an archetype item model | No | None | Required: the item schema | 0.7 [inferred] |
| verifier | Independent re-solve of a generated item, having never seen the key | No | None | Required: answer plus solution path | 0.0 |
| grader | One call per scoring point (BC-PT), invoked only inside a unit check, a part drill, a mock or the six-week checkpoint (R10) | Progress only | None | Required: earned, rationale, rule cited | 0.0 for the two agreement samples; the strictness-varied sample also 0.0 with a different prompt |
| diagnostician | Errors and probability-weighted misconceptions from a graded point vector | No | None | Required: BC-ERR list, BC-MIS with probabilities, mastery_state per skill | 0.2 [inferred] |
| transcriber | Vision read-back of a photographed FRQ page | No | None | Required: structured transcription for rendering | 0.0 |

Withdrawn 2026-09-20: none of the six temperatures in that column can be sent. "On Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, and Claude Sonnet 5, non-default `temperature`, `top_p`, or `top_k` values return a 400 error on every request, regardless of whether thinking is used" (https://platform.claude.com/docs/en/build-with-claude/thinking [verified]). Zero is a non-default value, so the three zeros 400 exactly as the three non-zeros do. The column is retained above only to record what was withdrawn.

That removes an argument this document made rather than merely a parameter. The three zeros were justified here as not tunable, because "a grader, a verifier and a transcriber that vary run to run make the agreement check meaningless, because the disagreement it detects would be sampling noise rather than genuine uncertainty". There is now no parameter that pins them, and nothing in the provider documentation offers a substitute. The grader's three-sample protocol therefore measures disagreement directly rather than measuring it against a pinned baseline, and the escalation rate is read as what it is rather than as evidence about a baseline that no longer exists. `app/providers/anthropic.py:79` sends `"temperature": request.temperature` unconditionally with a default of 0.0 at `app/providers/base.py:41`, so the first real call on any role would 400 until that line goes. Track 3 is explicit that majority voting should be treated as a disagreement detector rather than an accuracy booster (https://arxiv.org/pdf/2203.11171 for the underlying self-consistency result [verified]; the reframing is [inferred] in track 3), and a disagreement detector only works when the samples were supposed to agree.

Two roles are cadence-bound rather than always-on. The grader is never invoked by a micro-session, whose MCQ and MathLive answers are graded deterministically and whose one-sentence justification prompts go to the tutor role as feedback only, carrying no credit (R10). The generator and the verifier are first invoked in P4: P1's items are authored by hand, so P1's only live provider role is the tutor on claude-sonnet-5 (R9).

Routing, exactly D8:

| Role | Primary | Secondary | Offline fallback |
| --- | --- | --- | --- |
| tutor | Anthropic claude-sonnet-5 | Gemini 3.8 Flash | none; the session continues without the tutor |
| generator | Anthropic claude-opus-5 | Anthropic claude-sonnet-5 (batch) | none; the bank is pre-generated |
| verifier | Gemini 3.5 Flash-Lite (batch, paid tier) | Gemini 3.8 Flash (batch, paid tier), then Anthropic claude-sonnet-5 (batch) | none; verification waits |
| grader | Anthropic claude-sonnet-5 | Gemini 3.8 Flash | none; grading is queued |
| diagnostician | Anthropic claude-sonnet-5 | Gemini 3.8 Flash | Ollama DeepSeek-R1-Distill-Qwen-14B, feedback marked provisional |
| transcriber | Anthropic claude-sonnet-5 | Gemini 3.8 Flash | none; the student types the answer instead |

The generator's secondary moved off Gemini 3.8 Flash on 2026-09-20 for one reason: the verifier's primary is now Gemini 3.8 Flash, and leaving both roles able to reach one model meant a single generator fallback put the generator and its own verifier on the identical model, which is exactly the correlated failure the independent re-solve exists to catch. The router additionally refuses any chain that would place the generator and the verifier on the same model for one item, whatever the deployments say.

The verifier's primary moved one Gemini tier down later the same day, to Gemini 3.5 Flash-Lite, and the reason is in `14-token-economy.md`. The pricing page prints Flash-Lite at $0.30 in and $2.50 out per MTok with no promotional end date beside those figures, against 3.8 Flash's $0.75 and $3.75 through 31 December 2026 and $1.50 and $7.50 after, and Flash-Lite's model page prints structured outputs, thinking, caching and the Batch API as supported (https://ai.google.dev/gemini-api/docs/pricing and https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite [verified, fetched 2026-09-20]). 3.8 Flash becomes the second deployment and claude-sonnet-5 on batch the third, so the chain still never reaches the generator's own model. The role is safe on a weaker model for a structural reason rather than a hopeful one: its answer is never trusted, it is compared under SymPy against a key three deterministic checks already agree on, and a disagreement routes to review rather than to publication.

Four rows moved on 2026-09-20 and the reasons are in `13-ai-engineering.md`, which quotes the sentence each one contradicts. The verifier left claude-opus-5 because routing it to the generator's own model maximises the correlated failure that `04-item-generation.md` and `10-quality-and-evaluation.md` both name as the worst case, and because Gemini's paid-tier data policy has now been read. The diagnostician left claude-opus-5 because this document's own justification for Anthropic-first names the grader, the verifier and the transcriber as the roles whose errors reach a student directly, and the diagnostician is not among them while being the highest-volume non-tutor role. The transcriber left claude-haiku-4-5 because Haiku 4.5 sits in the standard vision tier at a 1568 px long edge and 1568 visual tokens against the high-resolution tier's 2576 px and 4784 on Claude 4.7 and later (https://platform.claude.com/docs/en/build-with-claude/vision [verified]), and halving the resolution of a handwritten page on the one role whose dominant failure mode is misreading saves under a cent a page. The other three rows are kept.

OpenAI is supported but off by default. OpenRouter is supported but not in the hot path. claudebox is disabled by default and is not routable for the tutor role at all; the whole of its section below is the reason.

Why Anthropic first, by learning impact then cost. The roles whose errors reach a student directly are the grader, the verifier and the transcriber, and the project's stated position is that the bank's key error rate and the grader's agreement rate are the two numbers that decide whether the product is trustworthy. One of those three moved off Anthropic on 2026-09-20 and the reason is worth stating here rather than only under the table, because otherwise this paragraph reads as an argument the routing ignores. The verifier's errors do reach a student, which is exactly why it is the one role where independence from the generator outranks provider preference: a verifier on the generator's own model is not a second opinion. The premise stands and the verifier is the exception it creates. Anthropic is the default because the structured-output surface is documented and enforced (`output_config.format` with `strict: true` on tools, supported on Opus 5, Sonnet 5, Haiku 4.5 and the 4.x line: https://platform.claude.com/docs/en/build-with-claude/structured-outputs [verified]), the prompt cache minimum of 512 tokens on Opus 5 is the lowest of the three major providers (https://platform.claude.com/docs/en/build-with-claude/prompt-caching [verified]), and the batch discount of 50 percent applies to both input and output (https://platform.claude.com/docs/en/build-with-claude/batch-processing [verified]).

Why Gemini 3.8 Flash second for five roles and first for the verifier. For the five it is cost. At $0.75 in and $3.75 out per 1M through 31 December 2026, then $1.50 and $7.50 (https://ai.google.dev/gemini-api/docs/pricing [verified]), it is materially cheaper than claude-sonnet-5 at $2 and $10 (https://platform.claude.com/docs/en/about-claude/pricing [verified]) for bulk grading of routine practice where the decision surface is small and a deterministic pre-check has already settled the mechanical points. It also has the structured-output capability Anthropic lacks, namely recursive `$ref`, plus `minimum` and `maximum` (https://ai.google.dev/gemini-api/docs/structured-output [verified]), which Anthropic's structured outputs do not support (https://platform.claude.com/docs/en/build-with-claude/structured-outputs [verified]).

Why Ollama only as an offline fallback and never as a grading peer. DeepSeek-R1-Distill-Qwen-14B reports MATH-500 pass@1 of 93.9 and AIME 2024 pass@1 of 69.7 on the official model card (https://huggingface.co/deepseek-ai/DeepSeek-R1 [verified]), which makes it the smallest officially documented model above 93 on MATH-500 alongside the 32B at 94.3. That is a defensible local choice. It is not a grading peer, for a reason stated plainly in track 4: MATH-500 and AIME are not AP Calculus BC, AIME in particular over-indexes on competition cleverness, and BC free response rewards correct notation, justification and units, so benchmark rank is a weak proxy for grading a student's related-rates justification [inferred]. The offline fallback's job is to keep a session alive with pre-generated items and provisional feedback, not to decide a point.

Why OpenRouter is not in the hot path. Its value is breadth of model access, which is not a problem a single-student app has, and its free-model rate limit of 20 requests per minute and 50 per day under $10 of lifetime purchase would be the binding constraint anyway (https://openrouter.ai/docs/api-reference/limits [verified]). It stays supported because it is the cheapest way to evaluate an unfamiliar model once, not because it belongs in a session.

Two hard rules that the router enforces rather than trusting callers to observe.

The verifier must never see the generator's key. This is enforced structurally: the verifier's message construction takes the item stem and the archetype's `expected_solution_path` and cannot reach `items.answer_key`, because the verification job passes a projection of the item that omits it. Track 3's recommended sequence is generate with an intended answer, then independently re-solve with a second model that has not seen the first answer, then check symbolically, then check numerically, publishing only on unanimous agreement and routing disagreement to a review queue rather than to an average. A verifier that has seen the key is not an independent check; it is a confirmation, and it would make the unanimity gate report a pass rate that means nothing.

The tutor is guardrailed and has no tools. No tool definitions are ever sent on a tutor call. The learning reason is D1: plain chat beside an unsolved problem cost 17 percent on the unassisted exam in Bastani et al while a guardrailed tutor was at parity, so the tutor's whole value depends on what it refuses to do. The security reason is in `09-security-and-privacy.md`: a model with no tools cannot be induced by injected text to take an action. There is also a small cost effect, since tool definitions add 286 tokens on Opus 5 for `tool_choice` auto or none and 406 for any or tool, 354 and 474 on Sonnet 5, and 496 and 588 on Haiku 4.5 (https://platform.claude.com/docs/en/about-claude/pricing [verified]). The cost saving is not the reason; it is a side effect of the right decision.

## Provider adapters

Each adapter maps the normalised call to one provider's wire format, maps the provider's stream to the normalised event vocabulary in `06-architecture.md`, and populates `usage` including the cached token fields.

### Anthropic

| Capability | Supported | Key numbers | Source |
| --- | --- | --- | --- |
| Models and pricing | Yes | claude-opus-5 1M context, 128K max output, $5 in / $25 out per MTok. claude-sonnet-5 1M / 128K, $2 / $10. claude-haiku-4-5 200K / 64K, $1 / $5. claude-fable-5-1 1M / 128K, $10 / $50, listed for completeness and routed to by no role (N10) | https://platform.claude.com/docs/en/about-claude/models/overview and https://platform.claude.com/docs/en/about-claude/pricing [verified] |
| Sonnet 5 price | $2 / $10 permanent; the announced 1 September 2026 rise to $3 / $15 was cancelled | same pricing page [verified] |
| Tokenizer | Claude 4.7 and later use a newer tokenizer producing roughly 30 percent more tokens for the same text | same [verified] |
| Long context surcharge | None on 4.6 and later | same [verified] |
| Data residency | `inference_geo: "us"` applies a 1.1x multiplier on every token category on 4.6 and later; earlier models return 400 | same [verified] |
| Streaming | SSE. Events `message_start`, `message_delta`, `message_stop`, `content_block_start`, `content_block_delta`, `content_block_stop`, `ping`, `error`. Delta types `text_delta`, `input_json_delta`, `thinking_delta`, `signature_delta`. Whether `citations_delta` is still emitted is unknown | https://platform.claude.com/docs/en/build-with-claude/streaming [verified] |
| Prompt caching minimum | 512 tokens on Opus 5 and the Fable/Mythos 5 lines; 1,024 on Sonnet 5, Opus 4.8, Sonnet 4.6 and 4.5; 2,048 on Opus 4.7; 4,096 on Opus 4.6, Opus 4.5 and Haiku 4.5. Below the minimum the prompt is silently processed uncached with no error | https://platform.claude.com/docs/en/build-with-claude/prompt-caching [verified] |
| Prompt caching TTL | 5 minutes by default, refreshed on each read; 1 hour via `cache_control: {type: "ephemeral", ttl: "1h"}` | same [verified] |
| Cache multipliers | 5m write 1.25x base input, 1h write 2x, read 0.1x (0.025x on Fable 5.1 and Mythos 5.1). On Opus 5: $6.25/MTok 5m write, $10/MTok 1h write, $0.50/MTok read. Up to 4 explicit breakpoints; automatic caching consumes one slot | same [verified] |
| Cache reads vs rate limit | Cache reads do not count toward ITPM on current models; only Haiku 3.5 counts them | same [verified] |
| Batch | 50 percent off input and output. 100,000 requests or 256 MB per batch. Most finish under 1 hour, all expire at 24 hours. Results retained 29 days. Oversized returns 413 `request_too_large`. `max_tokens: 0` rejected inside a batch | https://platform.claude.com/docs/en/build-with-claude/batch-processing [verified] |
| Rate limits | Start tier 1,000 RPM / 2,000,000 ITPM / 400,000 OTPM for the Opus 5, Sonnet 5, 4.x and Haiku 4.5 bucket. Build 5,000 / 5,000,000 / 1,000,000. Scale 10,000 / 10,000,000 / 2,000,000. Monthly spend caps $500 Start, $1,000 Build, $200,000 Scale | https://platform.claude.com/docs/en/api/rate-limits [verified] |
| Extended thinking | `budget_tokens` minimum 1,024 and must be below `max_tokens`. Manual `thinking.type: "enabled"` is deprecated on Opus 4.6 and Sonnet 4.6 and returns 400 on Claude 4.7 and later, which includes Opus 5 and Sonnet 5; on those use `thinking: {type: "adaptive"}` with `output_config: {effort: ...}`, default high. Above a 32k budget the docs advise batch. Changing `budget_tokens` invalidates cache breakpoints | https://platform.claude.com/docs/en/build-with-claude/extended-thinking [verified] |
| Structured outputs | `output_config.format` with `{"type": "json_schema", "schema": {...}}`, plus `strict: true` on tool definitions. Supported: objects, arrays, enums, anyOf, allOf, string formats, `minItems` restricted to 0 or 1. Not supported: recursive schemas, minimum/maximum, minLength/maxLength, external `$ref`. First use pays a grammar-compilation latency, cached 24 hours; changing the format invalidates the prompt cache | https://platform.claude.com/docs/en/build-with-claude/structured-outputs [verified] |
| Vision | JPEG, PNG, GIF, WebP; animation unsupported, first frame only. Base64, URL or Files API. Max 10 MB per image on the Claude API. Max 600 images per request, 100 for 200K-context models. Max dimensions 8000x8000. Request cap 32 MB. Tokens = ceil(width/28) x ceil(height/28). Claude 4.7+ resize to 2576 px long edge, 4,784 visual tokens max; earlier 1568 px and 1,568 tokens | https://platform.claude.com/docs/en/build-with-claude/vision [verified] |
| PDF | 32 MB max request, 600 pages, 100 when the context window is under 1M. No passwords. Roughly 1,500 to 3,000 tokens per page at standard rates with no surcharge | https://platform.claude.com/docs/en/build-with-claude/pdf-support [verified] |

What the adapter maps: `system` to the top-level system block carrying the `cache_control` breakpoint; `output_schema` to `output_config.format`; `images` to base64 content blocks; the stream events per the mapping in `06-architecture.md`; `usage` from `input_tokens`, `output_tokens`, `cache_read_input_tokens` and `cache_creation_input_tokens`.

Stream error retryability, ruled 2026-09-23. The normalised `error` event's `retryable` flag reads
the Anthropic error `type` string against the table below, sourced from the claude-api skill's
own HTTP error code reference (`shared/error-codes.md`, "Error Code Summary"), which is the
Retryable column of Anthropic's own error taxonomy:

| Error type | HTTP code | Retryable |
| --- | --- | --- |
| `overloaded_error` | 529 | Yes |
| `api_error` | 500 | Yes |
| `rate_limit_error` | 429 | Yes |
| `invalid_request_error` | 400 | No |
| `authentication_error` | 401 | No |
| `billing_error` | 402 | No |
| `permission_error` | 403 | No |
| `not_found_error` | 404 | No |
| `request_too_large` | 413 | No |

That reference names no timeout error type at all, so a stream error whose type is not in the
nine rows above (a timeout included) stays `retryable: False` rather than being guessed at; the
skill is the only source consulted, per the operator's ruling, and it does not document one.
`app/providers/anthropic.py` `_RETRYABLE_STREAM_ERROR_TYPES` holds the three Yes rows.

Known traps. Adaptive thinking on 4.7 and later is the sharpest one: sending `thinking: {type: "enabled"}` to Opus 5 or Sonnet 5 returns 400, so an adapter written against the older shape fails on exactly the models this project routes to first. The adapter selects the thinking form by model family and a golden test asserts the selection. Corrected 2026-09-20: not sending a thinking parameter does not turn thinking off. On Opus 5 and Sonnet 5 "thinking is already on and needs no configuration", its tokens are billed as output and count toward `max_tokens`, and turning it off takes an explicit `thinking: {"type": "disabled"}`, which Sonnet 5 accepts and Opus 5 accepts at effort `high` or below (https://platform.claude.com/docs/en/build-with-claude/thinking [verified]). There is also an `output_config.effort` parameter with levels low, medium, high, xhigh and max, defaulting to `high`, which is not supported on Haiku 4.5, and changing its resolved value invalidates the prompt cache (https://platform.claude.com/docs/en/build-with-claude/effort [verified]). Both are pinned per role in `13-ai-engineering.md`; leaving either at its default is the single largest avoidable cost in the tutor role. Second, the silent cache miss: a prefix under the model's minimum is processed uncached with no error, so the only way to detect it is to watch `cache_read_input_tokens` stay at zero, which is why the cache hit rate is a named metric. Third, changing the structured-output format or the thinking budget invalidates the cache, so both are pinned per role and versioned with the prompt template rather than tuned per call. Fourth, the 4.7 tokenizer change of roughly 30 percent more tokens for the same text means any cost comparison against a 4.6-or-earlier baseline understates the newer model by about a third on input.

### OpenAI

| Capability | Supported | Key numbers | Source |
| --- | --- | --- | --- |
| Responses vs Chat Completions | Both | Responses takes `input` and returns typed output Items reachable as `response.output_text`. System guidance moves to a top-level `instructions` field. No `n` parameter, so one generation per call. Built-in tools available that Chat Completions lacks. State via `previous_response_id`. Structured outputs move from `response_format` to `text.format`. Streaming becomes typed semantic SSE. Stored by default | https://developers.openai.com/api/docs/guides/migrate-to-responses [verified]; a claimed 3 percent SWE-bench improvement for reasoning models is [single-source] |
| Structured outputs | Yes | `response_format: {type: "json_schema", ...}` from the gpt-4o-mini, gpt-4o-mini-2024-07-18 and gpt-4o-2024-08-06 snapshots onward. Refusals arrive in a separate `refusal` field rather than as schema-conforming output. Nesting depth, property counts and unsupported keywords were not enumerated on the loaded page and are unknown | https://developers.openai.com/api/docs/guides/structured-outputs [verified] |
| Streaming | Yes | `stream: true`. Named events on the loaded page: `response.created`, `response.output_text.delta`, `response.completed`, `error`. The full catalogue lives in the API reference, which was not loaded, so it is unknown. The docs caution that streaming complicates moderation because scores arrive only after a full generation | https://developers.openai.com/api/docs/guides/streaming-responses [verified] |
| Batch | Yes | 50 percent off. 24h is the only completion window. Input file cap 200 MB. 50,000 requests per batch. Up to 2,000 batches created per hour | https://developers.openai.com/api/docs/guides/batch [verified] |
| Prompt caching | Automatic | Minimum cacheable prefix 1,024 tokens on GPT-5.6 and later; earlier models vary with tools, images and reasoning effort. Reads 0.1x the uncached input rate on GPT-5.6 and later. A cached prefix stays reusable for 30 minutes after last use on GPT-5.6 and later; earlier models hold 5 to 10 minutes of inactivity up to an hour, with a 24h option. No write premium | https://developers.openai.com/api/docs/guides/prompt-caching [verified] |
| Models and pricing | Partial | gpt-6-astra 1.05M context, $10 / $50 per 1M. gpt-5.6-sol 1.05M, $4 / $20 promotional through 21 November 2026. gpt-5.6-terra and gpt-5.6-luna both 1.05M, pricing unknown from the loaded section. gpt-4o $2.50 / $10.00, gpt-4o-mini $0.15 / $0.60, context windows unknown. Batch about 50 percent off, flex matching batch rates on eligible models, fast mode about 2x standard | https://developers.openai.com/api/docs/models and https://developers.openai.com/api/docs/pricing [verified] |
| Vision | Yes | PNG, JPEG/JPG, WEBP, non-animated GIF. Up to 512 MB total per request and up to 1,500 images. Detail levels low, high, original, auto. Token cost patch-based or tile-based by model with 1.2x to 2.46x multipliers | https://developers.openai.com/api/docs/guides/images-vision [verified] |

What the adapter maps: `system` to `instructions`; `output_schema` to `text.format` on Responses; images to input image parts; the typed semantic events to the normalised vocabulary, treating an unrecognised event as ignorable rather than fatal, since the full catalogue is unknown.

Known traps. Responses stores by default, which is a data-policy decision and not merely a convenience; it is why OpenAI is off by default in this project and why enabling it surfaces the storage statement in the settings screen. The `refusal` field is a separate channel, so an adapter that only parses the schema path sees an empty structured result on a refusal and reports a schema failure instead of a refusal. The absence of `n` on Responses means the grader's three samples are three calls, not one call with three completions, which changes the cost arithmetic for the agreement check. The documented moderation caveat on streaming is noted but does not bind here, since the tutor's guardrail is a prompt-level and architectural control rather than a moderation-score gate.

### Gemini

| Capability | Supported | Key numbers | Source |
| --- | --- | --- | --- |
| Model IDs | Yes | Current generation is 3.x: gemini-3.8-flash, 3.7-flash, 3.6-flash, 3.5-flash, 3.5-flash-lite, 3.1-flash-lite, 3.1-pro-preview, 3.8-live, 3.1-flash-image, 3-pro-image, embedding-2. The 2.5 family is previous generation | https://ai.google.dev/gemini-api/docs/models [verified] |
| Pricing | Yes | gemini-3.8-flash $0.75 in / $3.75 out per 1M through 31 December 2026, then $1.50 / $7.50. gemini-3.1-pro-preview $2.00 / $12.00 at or below 200k and $4.00 / $18.00 above, no free tier. gemini-3.5-flash-lite $0.30 / $2.50. gemini-3.1-flash-lite $0.25 in for text, image and video, $0.50 for audio, $1.50 out. Batch 50 percent off. Priority inference about 1.8x standard | https://ai.google.dev/gemini-api/docs/pricing [verified] |
| Structured output | Yes | Types string, number, integer, boolean, object, array, null. Supports description, title, enum, format (date-time, date, time), minimum, maximum, items, prefixItems, minItems, maxItems, additionalProperties and recursive `$ref`. Pydantic and Zod supported. Partial JSON can be streamed | https://ai.google.dev/gemini-api/docs/structured-output [verified] |
| Streaming | Yes | Chunked streaming is documented. `interactions.create()` with `previous_interaction_id` exists alongside `generateContent`. The streaming method name on the Interactions path was not on the loaded page and is unknown | https://ai.google.dev/gemini-api/docs/text-generation [verified] |
| Implicit caching | On by default | Minimum 4,096 tokens on 3.8, 3.7, 3.6 and 3.5 Flash and on 3.1 Pro Preview. Minimum 2,048 on 2.5 Flash and 2.5 Pro. Telemetry via `usage.total_cached_tokens`. The Interactions API supports implicit caching only | https://ai.google.dev/gemini-api/docs/caching [verified] |
| Explicit caching | generateContent only | Explicit caches are not available on the Interactions path | same [verified] |
| Cache pricing | Yes | gemini-3.8-flash cache read $0.075 per 1M through 31 December 2026 then $0.15, storage $0.50 per 1M tokens per hour then $1.00. gemini-3.1-pro cache $0.20 per 1M at or below 200k and $0.40 above | pricing page [verified] |
| Vision | Yes | Up to 3,600 image files per request. Inline base64 bounded by a 20 MB total request size; use the File API above that. 258 tokens when both dimensions are 384 px or less, otherwise 258 tokens per 768x768 tile. MIME types png, jpeg, webp, heic, heif | https://ai.google.dev/gemini-api/docs/image-understanding [verified] |
| Rate limits | Documented, numbers partial | Expressed as RPM, TPM and RPD per project; the page defers free-tier numbers to AI Studio, so they are unknown. Tier 1 needs billing, Tier 2 needs $100 or more of spend and 3 days, Tier 3 needs $1,000 or more and 30 days. Rolling 10-minute spend caps of $10, $50 and $200 by tier | https://ai.google.dev/gemini-api/docs/rate-limits [verified] |
| Max context | unknown from the loaded pages | | |
| Data policy | Read 2026-09-20 | Paid tier: "Google doesn't use your prompts (including associated system instructions, cached content, and files such as images, videos, or documents) or responses to improve our products." Unpaid tier: the content is used to provide, improve and develop Google products and machine learning technologies, and human reviewers may read, annotate and process the input and output. Default log retention 55 days, configurable to 7, 14, 28 or 55 | https://ai.google.dev/gemini-api/terms and https://ai.google.dev/gemini-api/docs/logs-policy [verified] |

What the adapter maps: `output_schema` to `responseSchema`, which is the one place this project can use a recursive schema if a future diagnosis structure needs one; images to inline base64 under the 20 MB request bound, switching to the File API above it; `usage.total_cached_tokens` to `cached_read_tokens`.

Known traps. The implicit caching minimum of 4,096 tokens on the 3.x Flash line is four times Anthropic's Sonnet 5 minimum and eight times the Opus 5 minimum, so a prefix sized for Anthropic will not cache on Gemini. Since Gemini is the secondary for five roles and the primary for the verifier, a fallback silently loses the cache discount unless the prefix clears 4,096 tokens, and the verifier's own prefix of about 1,100 tokens does not clear it, so the verifier is priced uncached, and the adapter records that as a distinct condition rather than as an ordinary cache miss. Explicit caches are unavailable on the Interactions path, so if this project ever adopts Interactions for server-side state it loses explicit cache control; the adapter therefore uses `generateContent`. Gemini's data policy was read on 2026-09-20 and is no longer an open question: the paid tier does not use prompts or responses to improve Google products and the unpaid tier does, with human reviewers able to read the content. That makes the tier, not the provider, the thing the router has to check, and an unpaid Gemini deployment is refused for the tutor, the grader, the diagnostician and the transcriber, which are the four roles that carry student text. The verifier carries only a stem, which is generated material rather than student material, which is one reason it is the role this project routes to Gemini first.

### OpenRouter

| Capability | Supported | Key numbers | Source |
| --- | --- | --- | --- |
| Model ID format | Yes | `vendor/model`, with `:free`, `:nitro` (throughput first) and `:floor` (cheapest) suffixes | https://openrouter.ai/docs/features/model-routing [verified] |
| Auto Router | Yes | Classifies prompts into roughly 30 task types and ranks models by 7-day aggregate spend share. Cost tiers low, medium, high, xhigh, max. `session_id` gives stickiness. No extra fee | same [verified] |
| Provider preferences | Yes | `order`, `allow_fallbacks` (default true), `require_parameters`, `data_collection` ("allow" or "deny"), `zdr`, `only`, `ignore`, `quantizations`, `sort`, `max_price`, `preferred_min_throughput`, `preferred_max_latency` | https://openrouter.ai/docs/features/provider-routing [verified] |
| Default routing | Yes | Load balances by price with uptime weighting; providers without recent outages are weighted by the inverse square of cost | same [verified] |
| Thresholds | Yes | p50, p75, p90, p99 percentile preferences deprioritise rather than filter. `max_price` is a hard filter | same [verified] |
| Fees | Yes | No markup on inference. Credit purchase costs 5.5 percent with a $0.80 minimum via Stripe, 5 percent for crypto. BYOK free up to $25,000 per month of list-price inference on pay-as-you-go, or $200,000 per month on enterprise, then 5 percent deducted from credits | https://openrouter.ai/docs/faq [verified] |
| Data policy | Opt-in logging | Prompts and completions are not logged by default. Opting in gives a 1 percent discount. Providers that log, or that lack a confirmed privacy policy, are not routed to unless the training toggle is on | same [verified] |
| Rate limits | Yes | Free models: under $10 lifetime purchased gives 20 requests per minute and 50 per day; $10 or more gives 20 per minute and 1,000 per day. Credit exhaustion returns 402; rate limiting returns 429 with `X-RateLimit-*` headers and `Retry-After`. `GET /api/v1/key` returns `limit_remaining` | https://openrouter.ai/docs/api-reference/limits [verified] |
| Streaming | Yes | SSE. Keepalive comment lines reading `: OPENROUTER PROCESSING` must be skipped before JSON parsing. A usage chunk arrives before `[DONE]`. Mid-stream errors arrive as an SSE event with `finish_reason: "error"` under a 200 OK | https://openrouter.ai/docs/api-reference/streaming [verified] |
| Cancellation | Partial | `AbortController` stops billing only on supported providers (OpenAI, Anthropic and Fireworks are named); others keep generating and billing | same [verified] |
| Tool calling | Presumed OpenAI-shaped | The tool-calling doc page returned 404. The model-routing page states the Auto Router works with streaming and tool calling, which implies an OpenAI-shaped tools surface, but `tool_choice` semantics and parallel-call behaviour are unknown | [inferred] |

What the adapter maps: the OpenAI-compatible request shape; `provider_options` to the provider-preferences block, with `data_collection: "deny"` set by default because this project's default posture is no logging; the SSE stream with the keepalive filter.

Known traps, both of which are why this adapter is written defensively even though it is not in the hot path. First, the keepalive comment lines: a client that feeds every SSE data line to a JSON parser crashes on `: OPENROUTER PROCESSING`. The adapter skips comment lines before parsing, and a unit test feeds a recorded stream containing them. Second, and worse, mid-stream errors under a 200 OK: the HTTP status says success and the failure arrives as an event with `finish_reason: "error"`. Any code that treats a 2xx as a successful generation records a truncated answer as a complete one. For a verifier or a grader that is a silent correctness failure, which is the class of bug this project cannot tolerate, so the adapter treats `finish_reason: "error"` as a thrown error and the normalised `error` event is allowed to arrive after `start`. Third, cancellation does not always stop billing, so an aborted call must still be recorded against the budget unless the underlying provider is one of the named three.

### Ollama

| Capability | Supported | Key numbers | Source |
| --- | --- | --- | --- |
| /api/generate | Yes | Fields: model (required), prompt, stream, format, images (base64), options, keep_alive (default 5m), system, raw, seed | https://github.com/ollama/ollama/blob/main/docs/api.md [verified] |
| /api/chat | Yes | Fields: model, messages, stream, tools, format, images, options, keep_alive | same [verified] |
| Structured outputs | Yes | `format` accepts "json" or a full JSON schema object. The guidance is to define the schema with Pydantic `model_json_schema()` or Zod, instruct the model to return JSON in the prompt, and set temperature 0 | https://ollama.com/blog/structured-outputs [verified] |
| Tool calling | Yes | `tools` is an array of function objects with name, description and JSON Schema parameters; the model replies with `tool_calls` and results return as messages with role tool. The model list in that post predates Qwen3 and is not a current roster | https://ollama.com/blog/tool-support [single-source] |
| OpenAI-compatible endpoint | Yes | Local base `http://localhost:11434/v1/`, cloud `https://ollama.com/v1`. Endpoints `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/responses`, `/v1/models`. Supports vision, tools, reasoning control, streaming and JSON mode | https://docs.ollama.com/api/openai-compatibility [verified] |
| OpenAI-compat gaps | Documented | `tool_choice`, `logprobs`, stateful responses, image URLs (base64 only) and array-of-tokens input are not supported | same [verified] |
| Auth | Local ignores the key | Cloud requires `OLLAMA_API_KEY`; local accepts any value | same [verified] |
| GPU support | Yes | NVIDIA compute capability 5.0 or higher with driver 550 or later (570 or later for CC 5.0 to 6.2). AMD requires ROCm v7. Apple Metal, plus Vulkan on Windows and Linux. Device selection via `CUDA_VISIBLE_DEVICES`, `ROCR_VISIBLE_DEVICES`, `GGML_VK_VISIBLE_DEVICES` | https://docs.ollama.com/gpu [verified] |
| Per-quantisation VRAM | Not published | The GPU page gives no per-model-size VRAM table, so those figures are unknown from official docs and must be measured | same |

Note that `https://github.com/ollama/ollama/blob/main/docs/openai.md` now 404s; the live page is `docs.ollama.com/api/openai-compatibility`.

What the adapter maps: `output_schema` to `format` as a full JSON schema; images to base64 in the `images` array; temperature through `options`; `keep_alive` raised above the 5 minute default so the model stays resident across a session's gaps.

Known traps. Images are base64 only, with no URL support on the OpenAI-compatible path, which means the transcriber path cannot pass a stored image by reference and must inline it; combined with the unknown VRAM requirements, a vision fallback on Ollama is not assumed to work and is not part of the D8 routing table for the transcriber. `tool_choice` is unsupported, which is irrelevant here because no role uses tools. The VRAM figures being unpublished is the reason the offline fallback is a measured configuration rather than a documented one, and it is listed in `12-open-questions.md`.

### claudebox

Covered in full in its own section below, because the interesting content is a restriction rather than a capability. The capability facts are these.

| Item | Finding | Source |
| --- | --- | --- |
| What it is | A Docker wrapper putting an HTTP server in front of the Claude Code CLI. Two modes: CLI (`claudebox prompt "text"`, with `--json`) and service (`claudebox server`, optionally `--openai`). Container egress is restricted by iptables to an allowlist | https://raw.githubusercontent.com/ArmanJR/claudebox/main/README.md [verified] |
| API surface | `GET /health` returning status and active request count. `POST /prompt` with `{"prompt": "...", "options": {...}}` where options carry model, maxTurns, maxBudgetUsd, systemPrompt, allowedTools, cwd. `POST /v1/chat/completions` and `GET /v1/models`, OpenAI-compatible, gated behind `OPENAI_COMPAT=1` | server.js and README [verified] |
| Streaming | Not supported. The server buffers child process output and replies only after the process exits. There is no SSE path | server.js [verified] |
| Inbound auth | Static bearer token compared against `CLAUDEBOX_API_KEY` on the `/v1/*` routes. When `CLAUDEBOX_API_KEY` is unset, authentication is bypassed entirely | server.js [verified] |
| Env vars | `CLAUDEBOX_PORT` (3000), `CLAUDEBOX_IMAGE` (ghcr.io/armanjr/claudebox:latest), `CLAUDEBOX_API_KEY`; server-side `PORT` (3000), `MAX_CONCURRENT` (4), `OPENAI_COMPAT`, `CLAUDEBOX_TMP_DIR` (/workspace/.tmp) | README and server.js [verified] |
| Stated limitation | The iptables domain allowlist resolves IPs at container startup, so a CDN rotating IPs mid-run requires a container restart. Custom allowlists mount at /etc/allowed-domains.txt | README [single-source] |
| Repo stats | 63 stars, 10 forks, primary language Shell, default branch main, last push 2026-08-23, metadata updated 2026-09-17 | https://api.github.com/repos/ArmanJR/claudebox [verified] |
| Licence | Contested. The GitHub API returns no license object and no LICENSE file is present at the repo root, while the README text says MIT | same [verified] |

## Fallback chains

The policy shape is LiteLLM's router: explicit ordered deployments with cooldowns and a pre-call context check, rather than a try-catch chain. The parameters available there are `num_retries`, `allowed_fails` (default 3), `cooldown_time` (default 5s), `retry_after`, `order` (lower is higher priority), `weight` and `max_parallel_requests` (https://docs.litellm.ai/docs/routing [verified]). Context-window handling is through `enable_pre_call_checks=True`, which filters deployments by context capacity against message length and by region, with `base_model` and `region_name` set; the literal parameter name `context_window_fallbacks` was not on the loaded page and is unknown (same URL [verified]). Routing strategies available are simple-shuffle (default, weighted by rpm and tpm), latency-based, usage-based-v2, least-busy and cost-based (same URL [verified]).

This project uses ordered deployments rather than any of the load-balancing strategies, because with one student there is no load to balance and the ordering is a quality judgement rather than a throughput one.

The chain configuration, as a shape:

```json
{
  "grader": {
    "deployments": [
      {"order": 1, "provider": "anthropic", "model": "claude-sonnet-5", "allowed_fails": 2, "cooldown_s": 60},
      {"order": 2, "provider": "gemini",    "model": "gemini-3.8-flash", "allowed_fails": 2, "cooldown_s": 60}
    ],
    "pre_call_checks": {"context": true, "budget": true},
    "on_exhausted": "queue"
  },
  "tutor": {
    "deployments": [
      {"order": 1, "provider": "anthropic", "model": "claude-sonnet-5", "allowed_fails": 2, "cooldown_s": 60},
      {"order": 2, "provider": "gemini",    "model": "gemini-3.8-flash", "allowed_fails": 2, "cooldown_s": 60}
    ],
    "pre_call_checks": {"context": true, "budget": true},
    "on_exhausted": "disable_tutor_for_session"
  },
  "diagnostician": {
    "deployments": [
      {"order": 1, "provider": "anthropic", "model": "claude-sonnet-5", "allowed_fails": 2, "cooldown_s": 60},
      {"order": 2, "provider": "gemini",    "model": "gemini-3.8-flash", "allowed_fails": 2, "cooldown_s": 60},
      {"order": 3, "provider": "ollama",    "model": "deepseek-r1-distill-qwen-14b", "allowed_fails": 1, "cooldown_s": 300,
       "marks_output": "provisional"}
    ],
    "pre_call_checks": {"context": true, "budget": true},
    "on_exhausted": "verification_feedback_only"
  },
  "generator": { "deployments": [...], "on_exhausted": "queue" },
  "verifier":  { "deployments": [...], "on_exhausted": "queue" },
  "transcriber": { "deployments": [...], "on_exhausted": "typed_input_fallback" }
}
```

`allowed_fails` of 2 with a 60 second cooldown is `[inferred]` and is a tunable; LiteLLM's defaults are 3 and 5 seconds, and a 5 second cooldown is too short for a rate-limit response that carries a `Retry-After` measured in tens of seconds. When a provider returns `Retry-After`, that value overrides the configured cooldown.

The pre-call context check matters more here than in a general router, because two of this project's payloads are large in a way that is easy to underestimate. A full FRQ grading payload carries the transcription, the worked solution, the scoring point definitions and possibly the image. An Anthropic image costs `ceil(width/28) x ceil(height/28)` tokens, capped at 4,784 visual tokens on Claude 4.7 and later after resizing to a 2576 px long edge (https://platform.claude.com/docs/en/build-with-claude/vision [verified]). Discovering an overflow as a provider error mid-grading strands a student, so the check happens before the call and an overflow reroutes to a larger-context deployment or splits the payload by question, which track 3 recommends anyway: batch by question, persist partial results, and never depend on one run covering a whole exam.

What happens when every deployment in a chain fails. This is where the design earns its keep, because the answer is different per role and every answer keeps the student learning.

Tutor exhausted: the tutor is disabled for the session and the session screen says so in one line. The student keeps practising. This is acceptable precisely because D1 already holds that the tutor is not the mechanism; mastery-gated practice, interleaving and spaced retrieval are, and none of them need a model.

Generator and verifier exhausted: the jobs queue and retry with backoff. The student never notices, because the session draws from the pre-generated verified bank. This is the single most important consequence of building a bank rather than generating on demand: provider availability stops being on the critical path of a session.

Grader exhausted: the grading is queued and the attempt shows as awaiting grading. The student continues with the rest of the queue and the feedback arrives when the chain recovers. The alternative, grading with a degraded model, is rejected, because a wrong point decision is worse than a late one and the offline model is explicitly not a grading peer.

Diagnostician exhausted after the Ollama fallback: the feedback degrades from elaborated to verification feedback, meaning the student is told which points were earned and which rule each unearned point required, from the BC-PT record, without a misconception hypothesis. That is a real loss, since Shute 2008 supports elaborated feedback over verification feedback, but it is a graceful one and it is honest about what it does not know.

Transcriber exhausted: the student is offered typed entry through MathLive instead, which is the secondary capture mode anyway per D6.

## Budget caps

Each role has a daily cap in tokens and in dollars, stored in `budgets` with one row per user per role per day. Both units are kept because tokens are what the provider meters and dollars are what the operator cares about, and the conversion changes when a price changes or when a fallback moves a call to a different provider.

The guard runs before the call, inside the provider layer, as middleware outside the fallback chain so that a fallback cannot spend past a cap. It estimates the call's cost from the prompt token count and the configured `max_output_tokens`, using the worst case rather than the expected case, and refuses if the estimate would cross the cap. After the call it reconciles the estimate against `raw_usage`.

Hard stop behaviour per role, which is deliberately not uniform:

| Role | At the cap | What the student sees |
| --- | --- | --- |
| tutor | Stop. No further tutor calls today | A line on the session screen: the tutor is unavailable for the rest of today, with the practice queue unaffected |
| grader | Stop interactive grading; continue queueing for the batch endpoint tomorrow | The attempt shows as awaiting grading with the expected time |
| diagnostician | Stop. Fall through to verification feedback | Feedback names the rule and the scoring consequence without a misconception hypothesis |
| transcriber | Stop. Offer typed entry | The capture screen offers MathLive instead of the camera |
| generator | Stop. The bank is not topped up today | Nothing, unless the bank is short for a fringe archetype, in which case selection avoids it |
| verifier | Stop. Unverified items stay unpublished | Nothing; an unverified item is never served |

The ordering principle behind that table is that the caps degrade support before they degrade correctness, and they never degrade correctness silently. A verifier at its cap means fewer new items, never an unverified item served.

What the student sees, in general. The budget is visible in settings as today's usage against the cap per role, and a role that has stopped says so where it stopped rather than only in settings. Nothing about the budget is hidden, and nothing about it is presented as the student's fault. This is a design decision owned jointly with `08-design-brief.md`: a student who does not understand why the tutor went quiet will assume the product is broken.

Batch queue for non-interactive work. Generation, verification and deferred grading go to batch endpoints at 50 percent off on Anthropic (https://platform.claude.com/docs/en/build-with-claude/batch-processing [verified]), 50 percent on OpenAI (https://developers.openai.com/api/docs/guides/batch [verified]) and 50 percent on Gemini (https://ai.google.dev/gemini-api/docs/pricing [verified]). Against the daily cap, batch work is charged at the discounted rate, so the same dollar cap buys twice the batch work it buys of interactive work. The binding constraint is the 24 hour expiry on all three, so nothing whose result a session needs is ever submitted to a batch endpoint.

One Anthropic batch detail the job builder must respect: `max_tokens: 0` is rejected inside a batch, and an oversized batch returns 413 `request_too_large` against a limit of 100,000 requests or 256 MB (same URL [verified]). The generator's batches are chunked below both bounds. Two further batch details were read on 2026-09-20 and both change how a batch is built. "Batch results can be returned in any order", so results are matched by `custom_id` and never by position; a job builder that assumes input order writes one item's key onto another, which is a silent key error. And prompt caching inside a batch is best effort, with reported hit rates of 30 to 98 percent, because batch requests process concurrently; the documented mitigations are identical `cache_control` blocks across the batch, a steady request stream and the 1-hour TTL (same URL [verified]). `13-ai-engineering.md` turns those into one batch per archetype, warmed by an ordinary call before submission because `max_tokens: 0` pre-warming is rejected inside a batch.

## Prompt template management

Templates live in the repository as versioned files, one directory per role, with the version in the filename or in front matter. A template is never constructed by string concatenation at call time; it is rendered from named parameters, and the parameter list is part of the template's contract.

Parameters, per role. The tutor takes the student's persistent misconception list, the current item's skills and the guardrail level. The generator takes the archetype's `invariant_structure`, `safe_variables`, `difficulty_variables`, the chosen difficulty setting per BC-DF, `calculator_status`, the target BC-REP representation and the `expected_solution_path`. The verifier takes the stem and nothing that reveals the key. The grader takes one BC-PT record with its earns, does not earn, eligibility after error and notation requirements, plus the student's confirmed transcription. The diagnostician takes the graded point vector, the observed work, the archetype and its skills, and the BC-ERR and BC-MIS candidates reachable from those skills. The transcriber takes the image and the notation conventions.

Golden tests per template. Each template has a fixture set of inputs with expected structural properties of the output, and a change to a template must pass them before release. The properties asserted are structural rather than textual, because asserting exact model output would be a test of the model rather than of the template. Examples: the generator's output validates against the item schema and contains no string from the official corpus text cache above the 25-word anchor limit; the verifier's output contains an answer and a solution path and no reference to a key it was not given; the grader's output names a rule and a scoring consequence for every unearned point; the diagnostician's output contains at least two misconception hypotheses with probabilities summing to at most 1.0 and never a single cause at 1.0; the transcriber's output renders without error through KaTeX.

The templates are also where the leniency dial lives, and it is a dial with measured effect. Track 3 reports a study that ran a strict baseline policy prompt against a liberal policy added after the baseline "sometimes applied harsh point deductions", and liberal prompting improved mean absolute error for every model tested (https://arxiv.org/html/2607.01247 [single-source]). Strictness is therefore a template parameter with a measurable effect rather than a model property, and it must be calibrated against real data before release rather than chosen by taste. The grader's third sample is deliberately the strictness-varied one, so a point whose decision flips under a strictness change is detected as a split and escalated rather than recorded as a score.

How a template change is released. A change bumps the template version. The version is recorded in `items.provenance` for generated items and in `gradings.samples` for grading decisions, so a later question about why an item or a grade looks the way it does resolves to a specific template. Golden tests run on the change. If the change touches the system-prompt prefix, it also runs the cache-prefix stability check below. A template change never retroactively alters an existing grade; a re-grade is a new grading row with the new version recorded.

Cache-prefix stability. The cached prefix is the part of the system block above the first `cache_control` breakpoint, and its stability is the whole economics of the caching story. Two rules follow. First, nothing that varies per call may appear in the prefix, which means the student's misconception list, being slow-moving, sits in the prefix while the current item does not. Second, a template change that alters the prefix invalidates the cache for every subsequent call, so prefix-touching changes are released at a session boundary rather than mid-session where possible. A test asserts that each role's rendered prefix is byte-identical across a set of representative parameter draws, and a second test asserts that the prefix exceeds the routed model's cache minimum (512 tokens on Opus 5, 1,024 on Sonnet 5 and 4,096 on Haiku 4.5, per https://platform.claude.com/docs/en/build-with-claude/prompt-caching [verified], 4,096 implicit on the Gemini 3.x Flash line per https://ai.google.dev/gemini-api/docs/caching [verified]). The second test is what catches the silent uncached processing that Anthropic performs with no error below the minimum.

## Encrypted key storage

Provider keys are encrypted at rest with libsodium secretbox under a key derived from an operator passphrase, per D8 and D10. The ciphertext and nonce live in `provider_configs`; the passphrase is never stored.

The derivation uses a memory-hard KDF with a per-installation salt stored alongside the ciphertext. The derived key exists in process memory only while the application is unlocked, and unlocking is an explicit action at startup or at first key use rather than something that happens implicitly.

Rules that hold without exception. Keys never appear in a log line, an error message, a stack trace, a URL, a query string or an `audit_log` detail field. The `audit_log` records that a key was set, rotated or used, never any part of its value. `GET /settings/providers` returns configuration without key material and never returns a masked prefix either, because a masked prefix is still a disclosure. A key is passed to an adapter as a request-scoped value and is not retained on the adapter object between calls.

Rotation. `PUT /settings/providers/{provider}` with a new key requires passphrase re-entry, writes a new ciphertext and nonce, records the rotation in `audit_log` with a timestamp and no key material, and invalidates any cached client object holding the old key. There is no key history, because retaining a superseded key is a liability with no benefit.

OS keychain option for desktop. Where the application runs as a desktop app on a machine with a platform credential store, the derived key may be held by the OS keychain instead of being re-derived from a passphrase at each start. This is a convenience trade and it is stated as one: it removes a passphrase prompt and it moves the trust boundary to the operating system account. It is offered, not defaulted, and the settings screen states what it changes.

What is stored for claudebox. Not an Anthropic API key, because claudebox does not use one. What is stored is the base URL, which must be a localhost address, and the `CLAUDEBOX_API_KEY` bearer token that the claudebox server compares on its `/v1/*` routes. That bearer token is stored with the same secretbox encryption as any other secret. The operator's Claude subscription OAuth token is never read, written, copied or transported by this application; it lives where claudebox's own `setup-auth.sh` puts it and this application does not touch it. That separation is deliberate and it is the minimum this application can do while still supporting the adapter at all.

## The claudebox adapter

claudebox is a Docker wrapper that puts an HTTP server in front of the Claude Code CLI, so that a Claude Code agent becomes a network service (https://raw.githubusercontent.com/ArmanJR/claudebox/main/README.md [verified]). Its stated selling point is running on an existing Claude subscription rather than metered API billing.

How it authenticates. `setup-auth.sh` reads the macOS Keychain entry "Claude Code-credentials" via `security find-generic-password` and invokes `claude setup-token`; on Linux it reads `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/.credentials.json` and invokes `claude login`. It extracts `claudeAiOauth.accessToken` and `claudeAiOauth.expiresAt`, writes `CLAUDE_CODE_OAUTH_TOKEN` into `.env.claude` at chmod 600, and compares `expiresAt` against `Date.now()` to report remaining hours (https://raw.githubusercontent.com/ArmanJR/claudebox/main/setup-auth.sh [verified]). The field name `claudeAiOauth` is the tell: this is the consumer Claude.ai subscription credential, not an `ANTHROPIC_API_KEY`.

How it reaches Anthropic. `server.js` never speaks HTTP to Anthropic and never handles the token directly; it spawns the local `claude` binary via Node `child_process.spawn()` and collects stdout, so the endpoint contacted is whatever Claude Code normally contacts. The egress allowlist contains exactly four domains: anthropic.com, claude.ai, api.anthropic.com, console.anthropic.com. No wire-level capture was taken, so the exact endpoint path is unknown (server.js and allowed-domains.txt [verified]).

The API surface is `GET /health` returning status and active request count, `POST /prompt` with `{"prompt": "...", "options": {...}}` where options carry model, maxTurns, maxBudgetUsd, systemPrompt, allowedTools and cwd, plus `POST /v1/chat/completions` and `GET /v1/models` gated behind `OPENAI_COMPAT=1` (server.js and README [verified]). Inbound authentication is a static bearer token compared against `CLAUDEBOX_API_KEY` on the `/v1/*` routes, and when `CLAUDEBOX_API_KEY` is unset authentication is bypassed entirely (server.js [verified]).

There is no streaming. The server buffers child process output and replies only after the process exits; there is no SSE path (server.js [verified]).

### The single-operator restriction

The adapter exists at all only as a convenience for one developer pointing their own tools at their own subscription on their own machine. It is never a multi-user feature, it is never a way to serve a student, and nothing in this plan treats it as one.

The restriction, exactly as D8 states it, with each clause's reason:

1. **Disabled by default.** `provider_configs.enabled` is 0 for claudebox and the settings screen shows it collapsed under an advanced section. Reason: a feature that carries a terms-of-service exposure must be an explicit act, not an available checkbox.

2. **`CLAUDEBOX_SINGLE_OPERATOR=1` in the environment plus a typed acknowledgement in the interface.** Both are required; either alone is insufficient. Reason: the environment variable makes it a deployment decision by whoever runs the process, and the typed acknowledgement makes it a knowing decision by whoever reads the warning. Neither substitutes for the other.

3. **Localhost-only binding.** The configured `base_url` must resolve to a loopback address, and the adapter refuses any other host at configuration time and again at call time. Reason: the claudebox server bypasses inbound authentication entirely when `CLAUDEBOX_API_KEY` is unset, so a non-loopback binding is an open proxy spending the operator's subscription, with no rate limiting of its own beyond `MAX_CONCURRENT=4`.

4. **Refuses to start with more than one user record.** The adapter queries `users` at initialisation and refuses if the count exceeds 1. Reason: the consumer terms bar making the account available to anyone else, and a second user record is the operational definition of a second person.

5. **The tutor role is not routable to it.** Not a preference, a refusal: a routing table entry mapping tutor to claudebox fails validation at startup. Reason: there is no streaming, so every tutor response would arrive as one buffered block after the whole generation, which for a tutoring interface means the student watches a spinner for the full duration. That is a product failure independent of any policy question.

6. **Never a grading or verification peer in a chain with another Anthropic deployment.** Reason: claudebox reaches the same underlying models, so an agreement check between claudebox and an Anthropic API deployment is not an independent check.

The acknowledgement string is exactly `ENABLE CLAUDEBOX SINGLE OPERATOR`, and this document owns it along with the warning copy below; `08-design-brief.md` and `11-phased-delivery.md` reference this section rather than restating either (R19).

The warning copy, displayed in full above the typed acknowledgement:

```
Enabling claudebox routes this application's model calls through a local
HTTP server that spawns the Claude Code CLI, which authenticates with the
operator's personal Claude.ai subscription OAuth token rather than with an
Anthropic API key.

Anthropic's consumer terms state that you may not share your account login
information, API key or account credentials with anyone else, and may not
make your account available to anyone else. They also prohibit accessing the
Services through automated or non-human means, whether by bot, script or
otherwise, except when accessing via an Anthropic API key or where otherwise
explicitly permitted. They further bar reselling the Services and using them
to develop competing products or services, and state that the Commercial
Terms govern any Anthropic API key, the Console, and other offerings that
reference them.
https://www.anthropic.com/legal/consumer-terms

claudebox's stated advantage is that it avoids the API key so that traffic
bills against the subscription instead. The API key is the carve-out those
terms name. The feature and the exposure are the same design decision.

Therefore:
  - Enable this only for yourself, on your own machine, against your own
    subscription, with no other person's traffic reaching this application.
  - This application will refuse to use claudebox if more than one user
    record exists, if the configured address is not loopback, or if the
    tutor role is routed to it.
  - There is no streaming. Responses arrive as one block after the whole
    generation completes.
  - The subscription OAuth token carries an expiry, so a long-running
    server will stop working at an unpredictable time.
  - Usage counts against the operator's five-hour session limits and, on
    Max plans, weekly limits.
    https://support.claude.com/en/articles/9797557-usage-limit-best-practices
  - The operator alone bears the risk of this configuration.

The recommended configuration is an ANTHROPIC_API_KEY against
api.anthropic.com. That is the path the consumer terms explicitly carve out
and the path the published rate limit tiers are designed for.
https://platform.claude.com/docs/en/api/rate-limits

I understand. Type ENABLE CLAUDEBOX SINGLE OPERATOR to continue.
```

### Why an API key is the recommendation

Four reasons, each of which holds on its own.

The credential. claudebox harvests the operator's consumer subscription OAuth token and writes it to a file a long-running HTTP server consumes. Anthropic's consumer terms say you may not share account login information or credentials with anyone else and may not make your account available to anyone else (https://www.anthropic.com/legal/consumer-terms [verified]). The moment a second person's traffic reaches that port, the account is being made available to someone else, whether that person is a paying user, a friend, or a student.

The automation carve-out runs the wrong way. The consumer terms permit automated access when accessing via an Anthropic API key and prohibit it otherwise (same URL [verified]). claudebox's advantage is precisely that it avoids the API key.

The default deployment is unauthenticated. `server.js` bypasses inbound authentication entirely when `CLAUDEBOX_API_KEY` is unset [verified], and the operator absorbs the five-hour session limits and, on Max, the weekly limits (https://support.claude.com/en/articles/9797557-usage-limit-best-practices and https://support.claude.com/en/articles/11049741-what-is-the-max-plan [verified]; exact numeric weekly hour ranges per tier are unknown, since the support pages fetched publish no concrete figures and Anthropic direct users to Settings then Usage).

The operational profile is unsuitable regardless of policy. No streaming, so every response is one buffered block. The OAuth token carries an `expiresAt` and the project's own script exists to refresh it manually, so a long-lived server stops working at an unpredictable time. The repository is 63 stars, last pushed August 2026, with a README claiming MIT and no LICENSE file present [verified].

If cost is the motivation, the honest levers are the ones this document already specifies: prompt caching at 0.1x reads, the 50 percent batch discount for everything off the interactive path, and a bank of reusable verified items that turns generation cost into a one-time expense per item rather than a per-session one. Those three together move the cost curve further than credential reuse would, and none of them puts the operator's account at risk.

One note on Claude Code and subscriptions generally, because it is easy to get backwards: Claude Code is included with Pro and Max, authenticated with Claude credentials, and activity in both tools counts against the same usage limits; that page's warning runs the other way, namely that if `ANTHROPIC_API_KEY` is set, Claude Code authenticates with the API key instead of the subscription and produces API charges. The page does not state that subscription credentials may be used to power a third-party service (https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan [verified]).

## The subscription backend

Ruled 2026-09-23 on the operator's instruction, and distinct from claudebox above: the application's AI roles run by default on the operator's own Claude subscription through the official Claude Code CLI, so runtime API spend goes to about $0 and `ANTHROPIC_API_KEY` becomes a fallback [inferred]. The adapter is `app/providers/subscription.py` `SubscriptionProvider`, selected by `GROWTH_AI_BACKEND` in `app/main.py`: `subscription` is the default, `api` is the only value that wires `AnthropicProvider` and the paid key, and `replay` and `none` are unchanged. The older `GROWTH_TUTOR_PROVIDER` is read only when `GROWTH_AI_BACKEND` is unset, and only its `none` and `replay` values work: its old `anthropic` value, and `api`, stop the process at startup unless `GROWTH_AI_BACKEND=api` is set beside it, because the paid API is used only when `GROWTH_AI_BACKEND` says so.

What it runs. One `claude -p` process per call, started from an argument list and never a shell, with the role's model, the rendered static prefix as `--system-prompt`, `--output-format json`, `--json-schema` when the role asks for structured output, a per-role `--max-budget-usd`, `--no-session-persistence`, `--setting-sources ""`, `--strict-mcp-config` with an empty MCP config, `--disable-slash-commands`, `--tools ""` and a named `--disallowedTools` list. The user prompt goes on stdin. The working directory is an empty temporary directory, so no CLAUDE.md, hook, plugin or MCP server reaches the call. `--bare` is not used because it skips the OAuth and keychain login, and `--max-turns` does not exist in CLI 2.1.277 (`claude -p --help` [verified]).

The environment allowlist. The subprocess environment is built from `PATH`, `HOME`, `USER`, `LANG` and `TMPDIR`, plus the operator's long-lived OAuth token when it is set, passed through by name and never read or logged. No `ANTHROPIC_*` variable crosses, so the CLI cannot fall back to billing the paid key. Without the token the CLI uses its own keychain login, which is the same subscription. Separately, `AnthropicProvider` refuses any key starting `sk-ant-oat` before the wire, so the subscription token has no route to the Messages API from this code.

The single-user rule. The Agent SDK quickstart does not allow offering claude.ai login or its rate limits to other users (see 14, "Offline work on the operator's Claude Code subscription"). The backend therefore serves one account only: it refuses to start when the database holds more than one user, and registration refuses a second account. A multi-user installation must use `GROWTH_AI_BACKEND=api`.

Limits and failures. A 5-hour or weekly usage-limit answer raises `SubscriptionLimitReached`, and the tutor degrades as the hard-stop table above says: static feedback, the tutor marked unavailable, and the call queued as a `provider_call_queued` row in the `jobs` table. `tools/drain_subscription_queue.py` (`app/feedback/drain.py`) retries queued calls through the configured backend once the window resets and stores each sentence on its attempt. It never falls through to the API. A role on the subscription is capped by call counts per day and per minute (`app/providers/guard.py` `SubscriptionPacingCaps`, sized in `14-token-economy.md`, "Subscription pacing") instead of the per-role dollar and token caps, and a request that disables thinking runs the CLI with `MAX_THINKING_TOKENS=0` and its effort as `--effort`. A missing binary, a timeout, a non-zero exit or output that is not the JSON result is an ordinary provider failure, and a missing binary counts as refused before the wire. The CLI's `total_cost_usd` is recorded in a subscription ledger of its own and never counts against the $15.00 developer cap on the API key.

## Traceability

| Provider layer element | Mechanic in `01-learning-model.md` | Rule in `02-adaptive-engine.md` | Other |
| --- | --- | --- | --- |
| Six-role separation | Guardrailed tutoring; elaborated feedback | Credit assignment, which requires a mastery_state per skill from the diagnostician | `03-diagnosis-and-feedback.md` |
| Tutor with no tools, guardrailed, no final answer | No chat box beside an unsolved problem (Bastani et al: plain chat minus 17 percent, guardrailed at parity) | none | `09-security-and-privacy.md` |
| Verifier structurally blind to the key | All practice, since a wrong key corrupts every observation | Every credit assignment assumes a correct key | `04-item-generation.md` |
| Grader at temperature 0 with three samples and escalation | Elaborated feedback withheld until submission | Mastery_state to credit mapping | `03-diagnosis-and-feedback.md` |
| Strictness-varied third sample | none | none | `10-quality-and-evaluation.md` calibration |
| Diagnostician structured output with BC-ERR, BC-MIS and probabilities | Structured self-explanation on errors; hypercorrection routing | Prerequisite propagation on a diagnosed gap; scheduling the discriminating probe | `03-diagnosis-and-feedback.md` |
| Transcriber with a confirmed read-back before grading | Criterion-shaped rehearsal on the real artefact | none | `05-assessment-modes.md` |
| Ordered fallback chains with per-role exhaustion behaviour | Session continuity; practice does not depend on provider availability | Fringe-restricted selection continues from the pre-generated bank | `06-architecture.md` |
| Ollama offline fallback, never a grading peer | Session continuity offline | none | `12-open-questions.md` for the unmeasured VRAM requirement |
| Per-role budget caps degrading support before correctness | Mastery gating survives a budget stop | An unverified item is never served, at any budget | `06-architecture.md` |
| Batch endpoints for generation, verification and deferred grading | none directly | none | `06-architecture.md` cost controls |
| Versioned templates with golden tests and a stable cache prefix | Consistent feedback quality across sessions | Consistent item difficulty priors, since the generator's prompt is part of the item's provenance | `10-quality-and-evaluation.md` |
| Encrypted key storage with no key in any log or URL | none | none | `09-security-and-privacy.md` |
| claudebox single-operator guard | none; the tutor is not routable to it | none | `09-security-and-privacy.md` threat model, operator actor |
