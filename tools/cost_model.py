"""The one place every cost figure in docs/plan/13-ai-engineering.md comes from.

Run it to print every figure the document quotes, one per line, as name = value.
Run it with --check <markdown file> to assert that every dollar amount printed in that file
is one of the figures below, so a figure cannot be patched by hand in one section while the
model that produced it moves in another. tests/tools/test_cost_model.py runs that check over
13 and over docs/operator/ai-operating-costs.md.

Every input is a named constant with its tag. Prices are [verified] against the provider
pricing pages read on 2026-09-20 and carry the URL in 13. Token counts are [measured] where 13
says so and [inferred] otherwise; the survival rates, the thinking counts and the call counts are
[inferred] and are the first-order drivers of the totals. Nothing here is fetched; a price change
is an edit to this file and a rerun, never an edit to the document.
"""
import argparse
import math
import re
import sys
from pathlib import Path

USD_PER_MTOK = 1e-6

# Prices, USD per million tokens, https://platform.claude.com/docs/en/about-claude/pricing and
# https://ai.google.dev/gemini-api/docs/pricing, both read 2026-09-20. [verified]
# The batch discount stacks with the cache multipliers, so a batch row halves every column.
#
# claude-opus-5-5 is the operator's Anthropic console announcement of 2026-09-23, not an
# independent reading of the pricing page, so it is [inferred] rather than [verified]: $4 input,
# $20 output and $0.20 cache reads as stated, with the writes derived from the standard 1.25x
# and 2x multipliers the other rows already carry.
PRICES = {
   "claude-opus-5": {"input": 5.00, "write_5m": 6.25, "write_1h": 10.00, "read": 0.50, "output": 25.00},
   "claude-opus-5-5": {"input": 4.00, "write_5m": 5.00, "write_1h": 8.00, "read": 0.20, "output": 20.00},
   "claude-sonnet-5": {"input": 2.00, "write_5m": 2.50, "write_1h": 4.00, "read": 0.20, "output": 10.00},
   "claude-haiku-4-5": {"input": 1.00, "write_5m": 1.25, "write_1h": 2.00, "read": 0.10, "output": 5.00},
   "gemini-3.8-flash": {"input": 0.75, "read": 0.075, "output": 3.75},
   "gemini-3.8-flash-2027": {"input": 1.50, "read": 0.15, "output": 7.50},
   "gemini-3.5-flash-lite": {"input": 0.30, "read": 0.03, "output": 2.50},
}

BATCH_DISCOUNT = 0.5
GEMINI_CACHE_STORAGE_PER_MTOK_HOUR = 0.50
GEMINI_CACHE_STORAGE_PER_MTOK_HOUR_2027 = 1.00
GEMINI_EMBEDDING_PER_MTOK = 0.20

# Traffic. [inferred] except the archetype count, which is measured over data/archetypes.json.
STUDY_DAYS = 230
SESSIONS = 230
ACTIVE_ARCHETYPES = 139
ITEMS_PER_SESSION_LOW = 15
ITEMS_PER_SESSION_HIGH = 25
TUTOR_CALLS_PER_SESSION = 12
TUTOR_CALLS_PER_SESSION_LOW = 5
TUTOR_CALLS_PER_SESSION_HIGH = 20
JUDGED_POINTS = 1200
GRADER_SAMPLES = 3
GRADING_OCCASIONS = 60
PHOTOGRAPHED_PAGES = 200
INCORRECT_ATTEMPT_SHARE = 0.35
ITEMS_PER_DAY_FOR_INCORRECT = 20
INCORRECT_ATTEMPTS = int(INCORRECT_ATTEMPT_SHARE * ITEMS_PER_DAY_FOR_INCORRECT * STUDY_DAYS)

# The bank. [inferred]
PUBLISHED_PER_ARCHETYPE = 40
FREE_CHECK_SURVIVAL = 0.80
VERIFICATION_SURVIVAL = 0.90
STAGE_1_TO_3_FAILURE = 0.20

# Characters per token: the 4-character rule of thumb raised by the 30 percent the pricing page
# attributes to the Claude 4.7 and later tokenizer. [verified for the 30 percent, inferred as a divisor]
CHARACTERS_PER_TOKEN = 3.1

# Thinking tokens per call at effort medium, [inferred] from the one live anchor in 13. Effort
# high is scaled from the generator's pair, 1,200 at medium against 2,500 at high, and that ratio
# is applied to every role because no per-role anchor exists.
GENERATOR_THINKING_MEDIUM = 1200
GENERATOR_THINKING_HIGH = 2500
HIGH_EFFORT_THINKING_RATIO = GENERATOR_THINKING_HIGH / GENERATOR_THINKING_MEDIUM

# Measured character counts that the token table is derived from. [measured]
METADATA_BLOCK_CHARS = 732
FULL_SCHEMA_RECORD_CHARS = 2286
WORKED_SOLUTION_CHARS = 594
TUTOR_PREFIX_CHARS_AS_BUILT = 1641
TUTOR_UNCACHED_INPUT_CHARS = 538

# Template architecture, docs/plan/14-token-economy.md. One authoring call per archetype replaces
# one generation call per item; the backend instantiates. Character counts are [measured] over
# tools/template_trial.py and the 26 artifacts under var/ on 2026-09-20.
TEMPLATE_INSTRUCTIONS_CHARS = 4420
TEMPLATE_USER_TURN_CHARS = 1582.3
TEMPLATE_SCHEMA_CHARS = 2280
TEMPLATE_BODY_CHARS = 2412.1
# [inferred] The 26 measured artifacts predate the representation, figure, parameter role and
# allowed-error-path fields the gate now requires, so the compliant body is larger than measured.
TEMPLATE_VISIBLE_TOKENS = 1100
# [inferred] Twice the per-item generator's thinking at the same effort, because a template has to
# hold over a parameter family rather than over one draw. No source prints a figure.
TEMPLATE_THINKING_TOKENS = 2400
# [inferred] MAX_GENERATION_ATTEMPTS is 3 in tools/template_trial.py and 0 of 26 templates pass the
# extended gate today, so an average archetype is authored more than once.
TEMPLATE_ATTEMPTS = 2.5

# Per-role token assumptions. prefix is cached above the breakpoint; writes is how many times the
# prefix is written over the cycle; uncached is input below the breakpoint per call.
ROLES = {
   "tutor": {"model": "claude-sonnet-5", "batch": False, "prefix": 1100, "writes": SESSIONS,
             "uncached": 174, "visible": 90, "thinking": 0},
   "grader": {"model": "claude-sonnet-5", "batch": False, "prefix": 1200, "writes": GRADING_OCCASIONS,
              "uncached": 1000, "visible": 300, "thinking": 700},
   "transcriber": {"model": "claude-sonnet-5", "batch": False, "prefix": 1100, "writes": GRADING_OCCASIONS,
                   "uncached": 4784, "visible": 600, "thinking": 0},
   "diagnostician": {"model": "claude-sonnet-5", "batch": False, "prefix": 1800, "writes": SESSIONS,
                     "uncached": 700, "visible": 400, "thinking": 600},
   "generator": {"model": "claude-opus-5", "batch": True, "prefix": 3900, "writes": ACTIVE_ARCHETYPES,
                 "uncached": 100, "visible": 501, "thinking": GENERATOR_THINKING_MEDIUM},
   "verifier": {"model": "gemini-3.8-flash", "batch": True, "prefix": 1100, "writes": 0,
                "uncached": 120, "visible": 258, "thinking": 1242},
   "screen": {"model": "claude-haiku-4-5", "batch": False, "prefix": 0, "writes": 0,
              "uncached": 700, "visible": 60, "thinking": 0},
   "template": {"model": "claude-opus-5", "batch": True,
                "prefix": round(TEMPLATE_INSTRUCTIONS_CHARS / CHARACTERS_PER_TOKEN),
                "writes": ACTIVE_ARCHETYPES,
                "uncached": round((TEMPLATE_USER_TURN_CHARS + TEMPLATE_SCHEMA_CHARS) / CHARACTERS_PER_TOKEN),
                "visible": TEMPLATE_VISIBLE_TOKENS, "thinking": TEMPLATE_THINKING_TOKENS},
}

# The Claude-only per-role model choice, docs/plan/14-token-economy.md "Per role model choice",
# operator's instruction of 2026-09-23 that the AI engine use Anthropic Claude models only.
# app/providers/model_routing.py ROLE_MODELS is the same table restated for the application, and
# tests/providers/test_model_routing.py asserts the two agree role by role, so a change here that
# is not carried into the app fails a test rather than drifting silently. tutor, grader,
# transcriber and diagnostician read their model from ROLES above, which already holds them on
# Claude; generator and verifier are named explicitly, because ROLES["template"] and
# ROLES["verifier"] stay on their 2026-09-20 pricing (Opus 5 and Gemini) so the figures
# 13-ai-engineering.md and docs/operator/ai-operating-costs.md already quote keep printing, and
# the Claude-only tier prices generator on claude-opus-5-5 and verifier on claude-haiku-4-5
# instead (see tier.hundred_claude_only below).
CLAUDE_ONLY_ROLE_MODELS = {
   "tutor": ROLES["tutor"]["model"],
   "grader": ROLES["grader"]["model"],
   "transcriber": ROLES["transcriber"]["model"],
   "diagnostician": ROLES["diagnostician"]["model"],
   "generator": "claude-opus-5-5",
   "verifier": "claude-haiku-4-5",
}

TUTOR_AS_BUILT_INPUT = 703
TUTOR_AS_BUILT_MAX_OUTPUT = 400
TUTOR_MAX_OUTPUT = 600
TUTOR_WORST_CASE_PROMPT = 1274
TUTOR_CAP_USD = 1.00
TUTOR_CAP_TOKENS = 250000

STANDARD_TIER_VISUAL_TOKENS_3840 = 1560
HIGH_RES_TIER_VISUAL_TOKENS = 4784

GOLDEN_SET_1_ITEMS = ACTIVE_ARCHETYPES
GOLDEN_SET_1_RUNS = 4
GOLDEN_SET_2_POINT_TYPES = 30
GOLDEN_SET_2_RESPONSES = 5
GOLDEN_SET_2_RESPONSES_GROWN = 11
GOLDEN_SET_2_INPUT = 2200
GOLDEN_SET_3_IMAGES = 35
MONTHLY_RUNS = 9

CREDIT_ON_HAND = 20.00
START_TIER_MONTHLY_SPEND_LIMIT = 500.00
# The operator's ceiling to exam day, instruction of 2026-09-20.
BUDGET_CEILING = 100.00

# The grader's deterministic partition, docs/plan/03-diagnosis-and-feedback.md. A point whose
# BC-PT record answers no to justification_required, interpretation_required and
# hypotheses_required, and whose earns text one of the four checks expresses, never reaches a
# model. [measured 2026-09-20: python3 over data/scoring_points.json, 76 active records, 59 answer
# no to all three.] The second condition is a per-record judgement and is not measured, so 17 of 76
# is a lower bound on the model share and 76 of 76 is the upper bound the recommended tier uses.
SCORING_POINT_RECORDS = 76
MODEL_JUDGED_POINT_RECORDS = 17
# The operator's labelling pass, docs/plan/14-token-economy.md open question 2, closed
# 2026-09-23: every active BC-PT record read against its own earns text and 03's four checks,
# in data/bc_pt_determinism_labels.json. [inferred: each per-record label is a judgement, tagged
# in that file; the count over the 76 labels is measured.] 48 of 76 are deterministic and 28 of 76
# are model_required, so this is the true model share the field-based 17 was always a lower bound
# on. It replaces the worst case in the Claude-only tier below.
MEASURED_MODEL_JUDGED_POINT_RECORDS = 28
# [inferred] The share of judged points on which two grader samples disagree and a third is drawn.
GRADER_DISAGREEMENT_SHARE = 0.25
# [inferred] The share of incorrect attempts on which the same BC-ERR path has already been seen,
# which is where a misconception hypothesis has something to rank.
DIAGNOSTICIAN_RECURRENCE_SHARE = 0.35
# The monthly canary measures exact match against fixed operator labels, which one sample settles;
# the escalation rate that needs three is measured free on real gradings.
GOLDEN_SET_2_CANARY_SAMPLES = 1
GOLDEN_SET_2_FULL_RUNS = 2
# Ruled 2026-09-23: the Claude-only $100 tier's own canary cadence, additive next to MONTHLY_RUNS
# above (see tier.hundred_claude_only below). tier.hundred's own canary line still reads
# MONTHLY_RUNS unchanged, because 13-ai-engineering.md and docs/operator/ai-operating-costs.md
# quote its $95.03 total and this file never patches a figure a document has already quoted; this
# cadence cut applies to the Claude-only tier alone.
CLAUDE_ONLY_GOLDEN_SET_2_CANARY_CADENCE = 2

# Uncapped tier settings.
UNCAPPED_PUBLISHED_PER_ARCHETYPE = 60
UNCAPPED_GRADER_SAMPLES = 5
UNCAPPED_PHOTOGRAPHED_PAGES = 400

# Kappa interval inputs, Cohen's large-sample form as published by NCSS.
KAPPA_PO = 0.78
KAPPA_PE = 0.50
KAPPA_GAP = 0.09
KAPPA_Z = 1.96
KAPPA_LITERATURE_LOW = 0.47
KAPPA_LITERATURE_HIGH = 0.56

# Bank draw arithmetic.
UNIFORM_SERVES_PER_ARCHETYPE = 33
TOP_DECILE_SERVES = 164
NO_REPEAT_CONFIDENCE = 0.95


def price(model, batch):
   table = dict(PRICES[model])

   if batch:
      table = {name: rate * BATCH_DISCOUNT for name, rate in table.items()}

   return table


def role_cost(role, calls, thinking=None, visible=None, writes=None, model=None, batch=None,
              cached=True):
   """cost = writes x prefix x write_rate + (calls - writes) x prefix x read_rate
           + calls x uncached x input_rate + calls x (visible + thinking) x output_rate

   A role whose prefix is below its model's cache minimum is priced with cached=False, which
   charges the prefix at the input rate on every call.
   """
   spec = ROLES[role]
   model = spec["model"] if model is None else model
   batch = spec["batch"] if batch is None else batch
   rates = price(model, batch)
   thinking = spec["thinking"] if thinking is None else thinking
   visible = spec["visible"] if visible is None else visible
   writes = spec["writes"] if writes is None else writes
   prefix = spec["prefix"]
   caches = cached and prefix > 0 and "write_1h" in rates

   if caches:
      writes = min(writes, calls)
      prefix_cost = writes * prefix * rates["write_1h"] + (calls - writes) * prefix * rates["read"]
   else:
      prefix_cost = calls * prefix * rates["input"]

   input_cost = calls * spec["uncached"] * rates["input"]
   output_cost = calls * (visible + thinking) * rates["output"]

   return (prefix_cost + input_cost + output_cost) * USD_PER_MTOK


def high_thinking(role):
   return round(ROLES[role]["thinking"] * HIGH_EFFORT_THINKING_RATIO)


def generator_pass(generated_per_archetype, thinking, metadata_tokens=0):
   calls = ACTIVE_ARCHETYPES * generated_per_archetype
   visible = ROLES["generator"]["visible"] + metadata_tokens

   return calls, role_cost("generator", calls, thinking=thinking, visible=visible)


def kappa_interval(po, pe, n, z):
   sd = math.sqrt(po * (1 - po) / (1 - pe) ** 2)
   se = sd / math.sqrt(n)
   kappa = (po - pe) / (1 - pe)

   return sd, se, kappa - z * se, kappa + z * se


def bank_for_no_repeat(serves, confidence):
   """Smallest uniform-random bank whose chance of zero repeats over the serves is at least
   the confidence, by the exact birthday product."""
   bank = serves

   while True:
      probability = 1.0

      for index in range(serves):
         probability *= 1 - index / bank

      if probability >= confidence:
         return bank

      bank = int(bank * 1.05) + 1


def expected_repeat_share_random(serves, bank):
   distinct = bank * (1 - (1 - 1 / bank) ** serves)

   return (serves - distinct) / serves


def repeat_share_least_recently_served(serves, bank):
   return max(serves - bank, 0) / serves


def figures():
   out = {}

   def add(name, value):
      out[name] = value

   for model, table in PRICES.items():
      for column, rate in table.items():
         add(f"price.{model}.{column}", rate)

   for model in ("claude-opus-5", "claude-sonnet-5"):
      for column, rate in price(model, True).items():
         add(f"price.{model}.batch.{column}", rate)

   for model in ("gemini-3.8-flash", "gemini-3.5-flash-lite"):
      for column, rate in price(model, True).items():
         add(f"price.{model}.batch.{column}", rate)

   add("price.gemini.cache_storage_per_mtok_hour", GEMINI_CACHE_STORAGE_PER_MTOK_HOUR)
   add("price.gemini.cache_storage_per_mtok_hour_2027", GEMINI_CACHE_STORAGE_PER_MTOK_HOUR_2027)
   add("price.gemini.embedding_per_mtok", GEMINI_EMBEDDING_PER_MTOK)
   add("credit.on_hand", CREDIT_ON_HAND)
   add("credit.start_tier_monthly_spend_limit", START_TIER_MONTHLY_SPEND_LIMIT)

   add("tokens.metadata_block", METADATA_BLOCK_CHARS / CHARACTERS_PER_TOKEN)
   add("tokens.tutor_prefix_as_built", TUTOR_PREFIX_CHARS_AS_BUILT / CHARACTERS_PER_TOKEN)
   add("tokens.tutor_uncached_input", TUTOR_UNCACHED_INPUT_CHARS / CHARACTERS_PER_TOKEN)

   for role, spec in ROLES.items():
      add(f"tokens.{role}.thinking_medium", spec["thinking"])
      add(f"tokens.{role}.thinking_high", high_thinking(role))
      add(f"tokens.{role}.output_medium", spec["visible"] + spec["thinking"])

   metadata_tokens = round(METADATA_BLOCK_CHARS / CHARACTERS_PER_TOKEN)
   generator_output = ROLES["generator"]["visible"] + ROLES["generator"]["thinking"]
   add("tokens.generator.output_high", ROLES["generator"]["visible"] + GENERATOR_THINKING_HIGH)
   add("share.generator_thinking_of_output", ROLES["generator"]["thinking"] / generator_output)
   add("share.metadata_of_output", metadata_tokens / (generator_output + metadata_tokens))
   add("share.metadata_of_record_chars", METADATA_BLOCK_CHARS / FULL_SCHEMA_RECORD_CHARS)
   add("share.worked_solution_of_record_chars", WORKED_SOLUTION_CHARS / FULL_SCHEMA_RECORD_CHARS)

   # Tutor.
   tutor_calls = TUTOR_CALLS_PER_SESSION * SESSIONS
   sonnet = price("claude-sonnet-5", False)
   tutor_prefix = ROLES["tutor"]["prefix"]
   add("tutor.calls", tutor_calls)
   add("tutor.session.write", tutor_prefix * sonnet["write_1h"] * USD_PER_MTOK)
   add("tutor.session.reads", (TUTOR_CALLS_PER_SESSION - 1) * tutor_prefix * sonnet["read"] * USD_PER_MTOK)
   add("tutor.session.uncached_input", TUTOR_CALLS_PER_SESSION * ROLES["tutor"]["uncached"] * sonnet["input"] * USD_PER_MTOK)
   add("tutor.session.output", TUTOR_CALLS_PER_SESSION * ROLES["tutor"]["visible"] * sonnet["output"] * USD_PER_MTOK)
   add("tutor.session.total", role_cost("tutor", TUTOR_CALLS_PER_SESSION, writes=1))
   add("tutor.cycle", role_cost("tutor", tutor_calls))
   add("tutor.cycle_at_5_calls", role_cost("tutor", TUTOR_CALLS_PER_SESSION_LOW * SESSIONS))
   add("tutor.cycle_at_20_calls", role_cost("tutor", TUTOR_CALLS_PER_SESSION_HIGH * SESSIONS))
   as_built_call = (TUTOR_AS_BUILT_INPUT * sonnet["input"] + TUTOR_AS_BUILT_MAX_OUTPUT * sonnet["output"]) * USD_PER_MTOK
   thinking_off_uncached_call = (TUTOR_AS_BUILT_INPUT * sonnet["input"] + ROLES["tutor"]["visible"] * sonnet["output"]) * USD_PER_MTOK
   add("tutor.as_built.call", as_built_call)
   add("tutor.as_built.cycle", as_built_call * tutor_calls)
   add("tutor.thinking_off_uncached.cycle", thinking_off_uncached_call * tutor_calls)
   add("tutor.gap.total", as_built_call * tutor_calls - out["tutor.cycle"])
   add("tutor.gap.thinking", as_built_call * tutor_calls - thinking_off_uncached_call * tutor_calls)
   add("tutor.gap.caching", thinking_off_uncached_call * tutor_calls - out["tutor.cycle"])
   uncached_5 = thinking_off_uncached_call * TUTOR_CALLS_PER_SESSION_LOW * SESSIONS
   add("tutor.uncached_at_5_calls", uncached_5)
   add("tutor.uncached_at_6_calls", thinking_off_uncached_call * 6 * SESSIONS)
   add("tutor.cached_at_6_calls", role_cost("tutor", 6 * SESSIONS))
   worst_case_call = (TUTOR_WORST_CASE_PROMPT * sonnet["input"] + TUTOR_MAX_OUTPUT * sonnet["output"]) * USD_PER_MTOK
   add("tutor.worst_case_reserve.usd", worst_case_call)
   add("tutor.calls_until_usd_cap", math.floor(TUTOR_CAP_USD / worst_case_call))
   add("tutor.calls_until_token_cap", math.floor(TUTOR_CAP_TOKENS / (TUTOR_WORST_CASE_PROMPT + TUTOR_MAX_OUTPUT)))
   add("tutor.cap_multiple_of_traffic", out["tutor.calls_until_usd_cap"] / TUTOR_CALLS_PER_SESSION_HIGH)
   add("tutor.uncapped_cycle", role_cost("tutor", TUTOR_CALLS_PER_SESSION_HIGH * SESSIONS, visible=TUTOR_AS_BUILT_MAX_OUTPUT))

   # Cache floor, in multiples of the base input rate on the prefix.
   read_multiplier = sonnet["read"] / sonnet["input"]
   write_multiplier = sonnet["write_1h"] / sonnet["input"]
   add("cache.three_calls_cached_multiple", write_multiplier + 2 * read_multiplier)
   add("cache.three_calls_uncached_multiple", 3.0)
   add("cache.two_calls_cached_multiple", write_multiplier + read_multiplier)
   add("cache.two_calls_uncached_multiple", 2.0)

   # Grader, transcriber, diagnostician, screen.
   grader_calls = JUDGED_POINTS * GRADER_SAMPLES
   add("grader.calls", grader_calls)
   add("grader.cycle", role_cost("grader", grader_calls))
   add("grader.uncapped_calls", JUDGED_POINTS * UNCAPPED_GRADER_SAMPLES)
   add("grader.uncapped_cycle", role_cost("grader", JUDGED_POINTS * UNCAPPED_GRADER_SAMPLES, thinking=high_thinking("grader")))
   add("grader.five_samples_cycle", role_cost("grader", JUDGED_POINTS * UNCAPPED_GRADER_SAMPLES))
   add("transcriber.calls", PHOTOGRAPHED_PAGES)
   add("transcriber.cycle", role_cost("transcriber", PHOTOGRAPHED_PAGES))
   add("transcriber.uncapped_cycle", role_cost("transcriber", UNCAPPED_PHOTOGRAPHED_PAGES))
   haiku = price("claude-haiku-4-5", False)
   add("transcriber.page_on_haiku_standard_tier", STANDARD_TIER_VISUAL_TOKENS_3840 * haiku["input"] * USD_PER_MTOK)
   add("transcriber.page_on_sonnet_high_res_tier", HIGH_RES_TIER_VISUAL_TOKENS * sonnet["input"] * USD_PER_MTOK)
   add("transcriber.page_difference", out["transcriber.page_on_sonnet_high_res_tier"] - out["transcriber.page_on_haiku_standard_tier"])
   add("diagnostician.calls", INCORRECT_ATTEMPTS)
   add("diagnostician.cycle", role_cost("diagnostician", INCORRECT_ATTEMPTS))
   add("diagnostician.uncapped_cycle", role_cost("diagnostician", INCORRECT_ATTEMPTS, model="claude-opus-5", thinking=high_thinking("diagnostician")))
   add("diagnostician.on_opus_cycle", role_cost("diagnostician", INCORRECT_ATTEMPTS, model="claude-opus-5"))
   add("screen.calls", PHOTOGRAPHED_PAGES)
   add("screen.page", role_cost("screen", 1, cached=False))
   add("screen.cycle", role_cost("screen", PHOTOGRAPHED_PAGES, cached=False))

   # Generator.
   combined_survival = FREE_CHECK_SURVIVAL * VERIFICATION_SURVIVAL
   generated_exact = PUBLISHED_PER_ARCHETYPE / combined_survival
   generated = math.ceil(generated_exact)
   add("bank.combined_survival", combined_survival)
   add("bank.generated_per_archetype_exact", generated_exact)
   add("bank.generated_per_archetype", generated)
   add("bank.published_items", ACTIVE_ARCHETYPES * PUBLISHED_PER_ARCHETYPE)
   calls, recommended = generator_pass(generated, GENERATOR_THINKING_MEDIUM)
   add("generator.calls", calls)
   opus_batch = price("claude-opus-5", True)
   generator_prefix = ROLES["generator"]["prefix"]
   add("generator.prefix_writes", ACTIVE_ARCHETYPES * generator_prefix * opus_batch["write_1h"] * USD_PER_MTOK)
   add("generator.prefix_reads", (calls - ACTIVE_ARCHETYPES) * generator_prefix * opus_batch["read"] * USD_PER_MTOK)
   add("generator.uncached_input", calls * ROLES["generator"]["uncached"] * opus_batch["input"] * USD_PER_MTOK)
   add("generator.output", calls * generator_output * opus_batch["output"] * USD_PER_MTOK)
   add("generator.cycle", recommended)
   add("generator.per_item", recommended / calls)
   _calls, high_out = generator_pass(generated, GENERATOR_THINKING_HIGH)
   _calls, medium_in = generator_pass(generated, GENERATOR_THINKING_MEDIUM, metadata_tokens)
   _calls, high_in = generator_pass(generated, GENERATOR_THINKING_HIGH, metadata_tokens)
   add("generator.effort_high_metadata_out", high_out)
   add("generator.effort_medium_metadata_in", medium_in)
   add("generator.effort_high_metadata_in", high_in)
   add("generator.lever.effort", high_out - recommended)
   add("generator.lever.metadata", medium_in - recommended)
   add("generator.lever.both", high_in - recommended)
   add("generator.lever.ratio", (high_out - recommended) / (medium_in - recommended))
   sonnet_calls, on_sonnet = generator_pass(generated, GENERATOR_THINKING_MEDIUM)
   on_sonnet = role_cost("generator", sonnet_calls, model="claude-sonnet-5")
   add("generator.on_sonnet_batch_cycle", on_sonnet)
   add("generator.on_sonnet_saving", recommended - on_sonnet)
   wave = generated // 2
   wave_calls, wave_cost = generator_pass(wave, GENERATOR_THINKING_MEDIUM)
   add("generator.wave_generated_per_archetype", wave)
   add("generator.wave_cycle", wave_cost)
   add("generator.two_waves_cycle", 2 * wave_cost)
   add("generator.staging_premium", 2 * wave_cost - recommended)
   uncapped_generated = math.ceil(UNCAPPED_PUBLISHED_PER_ARCHETYPE / combined_survival)
   uncapped_calls, uncapped_generator = generator_pass(uncapped_generated, GENERATOR_THINKING_HIGH, metadata_tokens)
   add("generator.uncapped_generated_per_archetype", uncapped_generated)
   add("generator.uncapped_calls", uncapped_calls)
   add("generator.uncapped_cycle", uncapped_generator)
   add("generator.uncapped_extra_items", uncapped_calls - calls)

   # Verifier.
   verifier_calls = round(calls * FREE_CHECK_SURVIVAL)
   gemini_batch = price("gemini-3.8-flash", True)
   verifier_input = ROLES["verifier"]["prefix"] + ROLES["verifier"]["uncached"]
   verifier_output = ROLES["verifier"]["visible"] + ROLES["verifier"]["thinking"]
   add("verifier.calls", verifier_calls)
   add("verifier.call.input", verifier_input * gemini_batch["input"] * USD_PER_MTOK)
   add("verifier.call.output", verifier_output * gemini_batch["output"] * USD_PER_MTOK)
   add("verifier.call", role_cost("verifier", 1, cached=False))
   add("verifier.cycle", role_cost("verifier", verifier_calls, cached=False))
   uncapped_verifier_calls = round(uncapped_calls * FREE_CHECK_SURVIVAL)
   add("verifier.uncapped_calls", uncapped_verifier_calls)
   add("verifier.uncapped_cycle", role_cost("verifier", uncapped_verifier_calls, model="claude-opus-5",
                                            batch=True, writes=ACTIVE_ARCHETYPES,
                                            thinking=high_thinking("verifier")))
   add("verifier.on_opus_batch_cycle", role_cost("verifier", uncapped_verifier_calls, model="claude-opus-5",
                                                 batch=True, writes=ACTIVE_ARCHETYPES))

   # Spend avoided by cheapest-first ordering.
   add("pipeline.avoided_by_stages_1_to_3", STAGE_1_TO_3_FAILURE * calls * out["verifier.call"])
   doomed_archetype = generated * (out["generator.per_item"] + out["verifier.call"])
   add("pipeline.doomed_archetype", doomed_archetype)
   add("pipeline.ten_doomed_archetypes", 10 * doomed_archetype)
   add("pipeline.avoided_low_share", out["pipeline.avoided_by_stages_1_to_3"] / recommended)
   add("pipeline.avoided_high", out["pipeline.avoided_by_stages_1_to_3"] + 10 * doomed_archetype)
   add("pipeline.avoided_high_share", out["pipeline.avoided_high"] / recommended)

   # Evals.
   add("evals.golden_set_1.run", GOLDEN_SET_1_ITEMS * out["generator.per_item"])
   add("evals.golden_set_1.cycle", GOLDEN_SET_1_RUNS * out["evals.golden_set_1.run"])
   grader_output = ROLES["grader"]["visible"] + ROLES["grader"]["thinking"]
   golden_2_call = (GOLDEN_SET_2_INPUT * sonnet["input"] + grader_output * sonnet["output"]) * USD_PER_MTOK
   golden_2_calls = GOLDEN_SET_2_POINT_TYPES * GOLDEN_SET_2_RESPONSES * GRADER_SAMPLES
   add("evals.golden_set_2.call.input", GOLDEN_SET_2_INPUT * sonnet["input"] * USD_PER_MTOK)
   add("evals.golden_set_2.call.output", grader_output * sonnet["output"] * USD_PER_MTOK)
   add("evals.golden_set_2.call", golden_2_call)
   add("evals.golden_set_2.calls", golden_2_calls)
   add("evals.golden_set_2.run", golden_2_calls * golden_2_call)
   add("evals.golden_set_2.cycle", MONTHLY_RUNS * golden_2_calls * golden_2_call)
   grown_calls = GOLDEN_SET_2_POINT_TYPES * GOLDEN_SET_2_RESPONSES_GROWN * GRADER_SAMPLES
   add("evals.golden_set_2.grown_calls", grown_calls)
   add("evals.golden_set_2.grown_run", grown_calls * golden_2_call)
   add("evals.golden_set_2.grown_premium", (grown_calls - golden_2_calls) * golden_2_call)
   transcriber_input = ROLES["transcriber"]["prefix"] + ROLES["transcriber"]["uncached"]
   golden_3_image = (transcriber_input * sonnet["input"] + ROLES["transcriber"]["visible"] * sonnet["output"]) * USD_PER_MTOK
   add("evals.golden_set_3.image.input", transcriber_input * sonnet["input"] * USD_PER_MTOK)
   add("evals.golden_set_3.image.output", ROLES["transcriber"]["visible"] * sonnet["output"] * USD_PER_MTOK)
   add("evals.golden_set_3.image", golden_3_image)
   add("evals.golden_set_3.run", GOLDEN_SET_3_IMAGES * golden_3_image)
   add("evals.golden_set_3.cycle", MONTHLY_RUNS * GOLDEN_SET_3_IMAGES * golden_3_image)
   full_sweep = out["evals.golden_set_1.run"] + out["evals.golden_set_2.run"] + out["evals.golden_set_3.run"]
   add("evals.full_sweep.run", full_sweep)
   add("evals.full_sweep.cycle", MONTHLY_RUNS * full_sweep)
   add("evals.cycle", out["evals.golden_set_1.cycle"] + out["evals.golden_set_2.cycle"] + out["evals.golden_set_3.cycle"])
   add("evals.calls", GOLDEN_SET_1_RUNS * GOLDEN_SET_1_ITEMS + MONTHLY_RUNS * golden_2_calls + MONTHLY_RUNS * GOLDEN_SET_3_IMAGES)

   # Tiers.
   anthropic = (out["tutor.cycle"] + out["grader.cycle"] + out["transcriber.cycle"] + out["diagnostician.cycle"]
                + out["generator.cycle"] + out["screen.cycle"] + out["evals.cycle"])
   google = out["verifier.cycle"]
   add("tier.minimum.cycle", out["tutor.cycle"])
   add("tier.recommended.anthropic", anthropic)
   add("tier.recommended.google", google)
   add("tier.recommended.cycle", anthropic + google)
   add("tier.recommended.beyond_credit", anthropic + google - CREDIT_ON_HAND)
   uncapped = (out["tutor.uncapped_cycle"] + out["grader.uncapped_cycle"] + out["transcriber.uncapped_cycle"]
               + out["diagnostician.uncapped_cycle"] + out["generator.uncapped_cycle"]
               + out["verifier.uncapped_cycle"] + out["screen.cycle"] + out["evals.full_sweep.cycle"])
   add("tier.uncapped.cycle", uncapped)
   add("tier.uncapped.premium", uncapped - (anthropic + google))
   add("tier.uncapped.thinking_ratio_share", (out["grader.uncapped_cycle"] - out["grader.five_samples_cycle"])
       + (out["diagnostician.uncapped_cycle"] - out["diagnostician.on_opus_cycle"])
       + (out["verifier.uncapped_cycle"] - out["verifier.on_opus_batch_cycle"]))
   add("credit.minimum_multiple", CREDIT_ON_HAND / out["tutor.cycle"])
   add("credit.spare_after_minimum", CREDIT_ON_HAND - out["tutor.cycle"])
   generated_items = math.floor(CREDIT_ON_HAND / out["generator.per_item"])
   add("credit.generated_items", generated_items)
   add("credit.published_items", math.floor(generated_items * combined_survival))
   add("credit.published_per_archetype", generated_items * combined_survival / ACTIVE_ARCHETYPES)

   # Batch queue.
   add("batch.generation_requests", calls)
   add("batch.verification_requests", verifier_calls)

   # Directions costed in docs/plan/14-token-economy.md.
   add("budget.ceiling", BUDGET_CEILING)
   add("tutor.saving_at_12_against_20", out["tutor.cycle_at_20_calls"] - out["tutor.cycle"])
   add("tier.recommended.other_roles", out["tutor.cycle"] + out["transcriber.cycle"]
       + out["diagnostician.cycle"] + out["verifier.cycle"] + out["screen.cycle"])

   template_calls = math.ceil(ACTIVE_ARCHETYPES * TEMPLATE_ATTEMPTS)
   template_cycle = role_cost("template", template_calls)
   add("template.measured_body_tokens", TEMPLATE_BODY_CHARS / CHARACTERS_PER_TOKEN)
   add("template.calls", template_calls)
   add("template.call", role_cost("template", 1, writes=1))
   add("template.cycle", template_cycle)
   add("template.saving_against_per_item", recommended - template_cycle)
   add("template.share_of_per_item_pass", template_cycle / recommended)
   credit_template_calls = math.floor(CREDIT_ON_HAND / out["template.call"])
   add("credit.template_calls", credit_template_calls)
   add("credit.archetypes_templated", credit_template_calls / TEMPLATE_ATTEMPTS)
   add("credit.spare_after_template_pass", CREDIT_ON_HAND - template_cycle)

   published = ACTIVE_ARCHETYPES * PUBLISHED_PER_ARCHETYPE
   published_verifier_calls = math.ceil(published / VERIFICATION_SURVIVAL)
   add("verifier.published_calls", published_verifier_calls)
   add("verifier.on_published_cycle", role_cost("verifier", published_verifier_calls, cached=False))
   add("verifier.on_published_cycle_2027",
       role_cost("verifier", published_verifier_calls, model="gemini-3.8-flash-2027", cached=False))
   lite_cycle = role_cost("verifier", published_verifier_calls, model="gemini-3.5-flash-lite",
                          cached=False)
   add("verifier.call_on_flash_lite", role_cost("verifier", 1, model="gemini-3.5-flash-lite",
                                                cached=False))
   add("verifier.on_flash_lite_cycle", lite_cycle)
   add("verifier.flash_lite_saving", out["verifier.on_published_cycle"] - lite_cycle)
   add("verifier.flash_lite_saving_2027", out["verifier.on_published_cycle_2027"] - lite_cycle)

   model_share = MODEL_JUDGED_POINT_RECORDS / SCORING_POINT_RECORDS
   model_points = round(JUDGED_POINTS * model_share)
   add("grader.model_share_of_point_types", model_share)
   add("grader.model_judged_points", model_points)
   add("grader.model_share_calls", model_points * GRADER_SAMPLES)
   add("grader.model_share_cycle", role_cost("grader", model_points * GRADER_SAMPLES))
   add("grader.model_share_saving", out["grader.cycle"] - out["grader.model_share_cycle"])
   add("grader.thinking_off_cycle", role_cost("grader", grader_calls, thinking=0))
   add("grader.thinking_off_saving", out["grader.cycle"] - out["grader.thinking_off_cycle"])
   conditional_calls = round(JUDGED_POINTS * (2 + GRADER_DISAGREEMENT_SHARE))
   add("grader.conditional_third_calls", conditional_calls)
   add("grader.conditional_third_cycle", role_cost("grader", conditional_calls))
   add("grader.conditional_third_saving", out["grader.cycle"] - out["grader.conditional_third_cycle"])
   add("grader.thinking_off_conditional_third_cycle",
       role_cost("grader", conditional_calls, thinking=0))

   recurrence_calls = round(INCORRECT_ATTEMPTS * DIAGNOSTICIAN_RECURRENCE_SHARE)
   add("diagnostician.recurrence_calls", recurrence_calls)
   add("diagnostician.on_recurrence_cycle", role_cost("diagnostician", recurrence_calls))
   add("diagnostician.recurrence_saving", out["diagnostician.cycle"] - out["diagnostician.on_recurrence_cycle"])

   canary_calls = GOLDEN_SET_2_POINT_TYPES * GOLDEN_SET_2_RESPONSES * GOLDEN_SET_2_CANARY_SAMPLES
   add("evals.golden_set_2.canary_calls", canary_calls)
   add("evals.golden_set_2.canary_run", canary_calls * golden_2_call)
   canary_cycle = MONTHLY_RUNS * canary_calls * golden_2_call
   full_cycle = GOLDEN_SET_2_FULL_RUNS * golden_2_calls * golden_2_call
   add("evals.golden_set_2.canary_cycle", canary_cycle)
   add("evals.golden_set_2.full_runs_cycle", full_cycle)
   add("evals.golden_set_2.mixed_cycle", canary_cycle + full_cycle)
   add("evals.golden_set_2.mixed_saving", out["evals.golden_set_2.cycle"] - canary_cycle - full_cycle)
   add("evals.golden_set_1.template_run", ACTIVE_ARCHETYPES * out["template.call"])
   add("evals.golden_set_1.on_the_template_gate", 0.0)
   add("evals.golden_set_1.template_gate_saving", out["evals.golden_set_1.cycle"])
   add("evals.hundred_calls", MONTHLY_RUNS * canary_calls + GOLDEN_SET_2_FULL_RUNS * golden_2_calls
       + MONTHLY_RUNS * GOLDEN_SET_3_IMAGES)

   # The tier that fits the operator's ceiling. Every line is one of the directions above.
   hundred_evals = canary_cycle + full_cycle + out["evals.golden_set_3.cycle"]
   hundred = (out["tutor.cycle"] + out["grader.model_share_cycle"] + out["transcriber.cycle"]
              + out["diagnostician.on_recurrence_cycle"] + template_cycle + lite_cycle
              + out["screen.cycle"] + hundred_evals)
   add("tier.hundred.evals", hundred_evals)
   add("tier.hundred.anthropic", hundred - lite_cycle)
   add("tier.hundred.google", lite_cycle)
   add("tier.hundred.cycle", hundred)
   add("tier.hundred.headroom", BUDGET_CEILING - hundred)
   add("tier.hundred.saving_against_recommended", out["tier.recommended.cycle"] - hundred)
   worst = (out["tutor.cycle"] + out["grader.cycle"] + out["transcriber.cycle"]
            + out["diagnostician.on_recurrence_cycle"] + template_cycle + lite_cycle
            + out["screen.cycle"] + hundred_evals)
   add("tier.hundred.grader_worst_case", worst)
   add("tier.hundred.grader_worst_case_overrun", worst - BUDGET_CEILING)
   rescued = worst - out["grader.cycle"] + out["grader.thinking_off_conditional_third_cycle"]
   add("tier.hundred.grader_worst_case_rescued", rescued)
   add("tier.hundred.grader_worst_case_rescued_headroom", BUDGET_CEILING - rescued)
   add("tier.hundred.beyond_credit", hundred - CREDIT_ON_HAND)

   # The Claude-only $100 tier, docs/plan/14-token-economy.md "The $100 tier", operator's
   # instruction of 2026-09-23: no non-Anthropic model anywhere in the tier. Additive next to
   # tier.hundred above, which stays exactly as printed because 13-ai-engineering.md and
   # docs/operator/ai-operating-costs.md quote its figures and this file never patches a figure a
   # document has already quoted; it retires a configuration by pricing the new one beside it.
   #
   # The verifier moves to claude-haiku-4-5 on the Batch API. Its prefix is 1,100 tokens, below
   # Haiku 4.5's 4,096 token cache minimum for the same reason the tutor's prefix cannot cache on
   # Haiku 4.5 (see "Per role model choice" above), so it prices uncached like the Gemini row it
   # replaces. The template author moves to claude-opus-5-5, cheaper than claude-opus-5 at every
   # rate and already in PRICES. The grader line prices at the operator's labelling pass,
   # MEASURED_MODEL_JUDGED_POINT_RECORDS, 28 of 76 active BC-PT records model_required, rather
   # than at the worst case every one of the 1,200 judged points reaching the model; 17 of 76 was
   # always a lower bound and the labelling pass is the measurement that replaces it. Direction 7
   # still applies underneath it, 2 samples with a third drawn only on disagreement, thinking left
   # on. Golden set 1 stays free on the template gate and golden set 2 stays the
   # canary-plus-full-run mix, both already the shape hundred_evals prices above.
   claude_only_generator_model = CLAUDE_ONLY_ROLE_MODELS["generator"]
   claude_only_verifier_model = CLAUDE_ONLY_ROLE_MODELS["verifier"]
   claude_only_template_cycle = role_cost("template", template_calls, model=claude_only_generator_model)
   add("template.cycle_on_opus_5_5", claude_only_template_cycle)
   add("template.saving_on_opus_5_5", template_cycle - claude_only_template_cycle)
   add("template.call_on_opus_5_5", role_cost("template", 1, writes=1, model=claude_only_generator_model))
   claude_only_verifier_cycle = role_cost("verifier", published_verifier_calls, model=claude_only_verifier_model,
                                          batch=True, cached=False)
   add("verifier.on_haiku_batch_cycle", claude_only_verifier_cycle)
   add("verifier.call_on_haiku_batch", role_cost("verifier", 1, model=claude_only_verifier_model, batch=True,
                                                 cached=False))

   # The labelling pass closes open question 2: the grader line below reads the measured share
   # rather than the worst case every one of the 1,200 points reaching the model. Direction 7,
   # 2 samples with a third drawn on disagreement, still applies underneath it.
   measured_model_share = MEASURED_MODEL_JUDGED_POINT_RECORDS / SCORING_POINT_RECORDS
   measured_model_points = round(JUDGED_POINTS * measured_model_share)
   measured_grader_calls = round(measured_model_points * (2 + GRADER_DISAGREEMENT_SHARE))
   claude_only_grader_cycle = role_cost("grader", measured_grader_calls)
   add("grader.measured_model_share_of_point_types", measured_model_share)
   add("grader.measured_model_judged_points", measured_model_points)
   add("grader.measured_model_share_calls", measured_grader_calls)
   add("grader.measured_model_share_cycle", claude_only_grader_cycle)
   add("grader.worst_case_conditional_third_cycle", out["grader.conditional_third_cycle"])
   add("grader.measured_saving_against_worst_case",
       out["grader.conditional_third_cycle"] - claude_only_grader_cycle)

   # Ruled 2026-09-23: golden set 3 stays at MONTHLY_RUNS (9, "golden set 3 monthly" in 14's own
   # table) because it is the cheaper of the two levers and MONTHLY_RUNS canary_cycle above already
   # cannot fit the ceiling even with golden set 3 cut to zero, so keeping one line monthly and
   # cutting the other is the only shape that leaves a monthly regression signal anywhere; the
   # canary is the line that moves. This is a plan ruling, not a loosened gate: the operator's own
   # $100 hard ceiling forces a cadence choice 13's kappa analysis and 10's "monthly canary" wording
   # did not anticipate, so the cadence is set here rather than assumed.
   claude_only_canary_cycle = (
      CLAUDE_ONLY_GOLDEN_SET_2_CANARY_CADENCE * canary_calls * golden_2_call
   )
   claude_only_evals = claude_only_canary_cycle + full_cycle + out["evals.golden_set_3.cycle"]
   add("evals.golden_set_2.claude_only_canary_cycle", claude_only_canary_cycle)
   add("tier.hundred_claude_only.evals_canary_cadence", CLAUDE_ONLY_GOLDEN_SET_2_CANARY_CADENCE)
   add("tier.hundred_claude_only.evals_golden_set_3_cadence", MONTHLY_RUNS)

   # History, quoted above: the tier's total before the 2026-09-23 cadence ruling, at the labelling
   # pass's measured grader share but the canary still at MONTHLY_RUNS. Kept as its own figure so
   # the history this document quotes stays a real emitted number rather than dead prose the
   # checker cannot verify.
   add("tier.hundred_claude_only.pre_cadence_ruling_evals_line", hundred_evals)

   claude_only_hundred = (out["tutor.cycle"] + claude_only_grader_cycle + out["transcriber.cycle"]
                          + out["diagnostician.on_recurrence_cycle"] + claude_only_template_cycle
                          + claude_only_verifier_cycle + out["screen.cycle"] + claude_only_evals)
   add("tier.hundred_claude_only.tutor_line", out["tutor.cycle"])
   add("tier.hundred_claude_only.grader_line", claude_only_grader_cycle)
   add("tier.hundred_claude_only.transcriber_line", out["transcriber.cycle"])
   add("tier.hundred_claude_only.diagnostician_line", out["diagnostician.on_recurrence_cycle"])
   add("tier.hundred_claude_only.template_line", claude_only_template_cycle)
   add("tier.hundred_claude_only.verifier_line", claude_only_verifier_cycle)
   add("tier.hundred_claude_only.screen_line", out["screen.cycle"])
   add("tier.hundred_claude_only.evals_line", claude_only_evals)
   add("tier.hundred_claude_only.cycle", claude_only_hundred)
   add("tier.hundred_claude_only.headroom", BUDGET_CEILING - claude_only_hundred)
   add("tier.hundred_claude_only.overrun", claude_only_hundred - BUDGET_CEILING)

   # History, quoted in 14: the tier's total and overrun before the 2026-09-23 cadence ruling
   # closed it, at the labelling pass's measured grader share but the canary still at
   # MONTHLY_RUNS. Emitted so the history this document quotes stays a checkable figure.
   pre_cadence_ruling_hundred = (out["tutor.cycle"] + claude_only_grader_cycle + out["transcriber.cycle"]
                                 + out["diagnostician.on_recurrence_cycle"] + claude_only_template_cycle
                                 + claude_only_verifier_cycle + out["screen.cycle"] + hundred_evals)
   add("tier.hundred_claude_only.pre_cadence_ruling_cycle", pre_cadence_ruling_hundred)
   add("tier.hundred_claude_only.pre_cadence_ruling_overrun", pre_cadence_ruling_hundred - BUDGET_CEILING)
   add("tier.hundred_claude_only.saving_against_recommended", out["tier.recommended.cycle"] - claude_only_hundred)
   add("tier.hundred_claude_only.grader_premium_over_split_guess",
       claude_only_grader_cycle - out["grader.model_share_cycle"])
   add("tier.hundred_claude_only.verifier_premium_over_gemini", claude_only_verifier_cycle - lite_cycle)

   # The figures 14 quotes as history, from before the labelling pass closed open question 2 on
   # 2026-09-23: the grader priced at the full worst case, every one of the 1,200 judged points.
   add("grader.worst_case_premium_over_split_guess",
       out["grader.conditional_third_cycle"] - out["grader.model_share_cycle"])
   worst_case_hundred = (out["tutor.cycle"] + out["grader.conditional_third_cycle"]
                         + out["transcriber.cycle"] + out["diagnostician.on_recurrence_cycle"]
                         + claude_only_template_cycle + claude_only_verifier_cycle
                         + out["screen.cycle"] + claude_only_evals)
   add("tier.hundred_claude_only.worst_case_cycle", worst_case_hundred)
   add("tier.hundred_claude_only.worst_case_overrun", worst_case_hundred - BUDGET_CEILING)

   # History, quoted in 14: the worst-case figure from before the 2026-09-23 cadence ruling, at
   # the pre-labelling grader worst case and the canary still at MONTHLY_RUNS.
   pre_cadence_ruling_worst_case = (out["tutor.cycle"] + out["grader.conditional_third_cycle"]
                                    + out["transcriber.cycle"] + out["diagnostician.on_recurrence_cycle"]
                                    + claude_only_template_cycle + claude_only_verifier_cycle
                                    + out["screen.cycle"] + hundred_evals)
   add("tier.hundred_claude_only.pre_cadence_ruling_worst_case_cycle", pre_cadence_ruling_worst_case)
   add("tier.hundred_claude_only.pre_cadence_ruling_worst_case_overrun",
       pre_cadence_ruling_worst_case - BUDGET_CEILING)

   # Offline split, docs/plan/14-token-economy.md "Offline work on the operator's Claude Code
   # subscription", operator's instruction of 2026-09-23: use the operator's Claude Code
   # subscription to cut AI cost wherever the terms allow. Template authoring and verifier
   # blind re-solves are development work that produces content committed to the repository,
   # the same shape as the 130 items in content/items_p1_agent/ authored on 2026-09-23 at $0 API
   # spend, so both lines move off the API key and onto Claude Code sessions. Every other role
   # in the tier serves a live student or grades a live attempt and stays on the API key, per the
   # Agent SDK quickstart's own instruction against routing product runtime traffic through a
   # claude.ai login or rate limit
   # (https://code.claude.com/docs/en/agent-sdk/quickstart.md [verified]).
   #
   # Evals do not split. Golden set 1 already costs $0.00, moved onto the deterministic template
   # gate in "The $100 tier, line by line" above, so there is nothing left on it to move. Golden
   # set 2 measures the grader and golden set 3 measures the transcriber, both the production
   # prompt run on its production model against fixed operator labels; a Claude Code agent is a
   # different harness, a different system prompt and a different tool surface, so running either
   # set there would not measure what ships to a student. Both stay on the API key in full.
   claude_only_offline_cycle = claude_only_template_cycle + claude_only_verifier_cycle
   claude_only_api_cycle = claude_only_hundred - claude_only_offline_cycle
   add("tier.hundred_claude_only.offline_template_line", claude_only_template_cycle)
   add("tier.hundred_claude_only.offline_verifier_line", claude_only_verifier_cycle)
   add("tier.hundred_claude_only.offline_cycle", claude_only_offline_cycle)
   add("tier.hundred_claude_only.api_cycle", claude_only_api_cycle)
   add("tier.hundred_claude_only.api_headroom", BUDGET_CEILING - claude_only_api_cycle)
   add("tier.hundred_claude_only.offline_share", claude_only_offline_cycle / claude_only_hundred)
   add("evals.claude_only.api_share", claude_only_evals)
   add("evals.claude_only.offline_share", 0.0)

   # Kappa.
   n_aggregate = GOLDEN_SET_2_POINT_TYPES * GOLDEN_SET_2_RESPONSES
   sd, se, low, high = kappa_interval(KAPPA_PO, KAPPA_PE, n_aggregate, KAPPA_Z)
   add("kappa.sd", sd)
   add("kappa.se_at_150", se)
   add("kappa.interval_low", low)
   add("kappa.interval_high", high)
   add("kappa.interval_width", high - low)
   add("kappa.gap_in_se", KAPPA_GAP / se)
   n_needed = (KAPPA_Z * sd / KAPPA_GAP) ** 2
   add("kappa.n_to_exclude_exact", n_needed)
   add("kappa.n_to_exclude", math.ceil(n_needed))
   add("kappa.responses_per_point_type", math.ceil(n_needed / GOLDEN_SET_2_POINT_TYPES))
   add("kappa.point_types_at_5", math.ceil(n_needed / GOLDEN_SET_2_RESPONSES))
   add("kappa.n_per_arm_two_kappas", math.ceil(2 * n_needed))
   sd_check, _se, _low, _high = kappa_interval(0.80, 0.50, 1, KAPPA_Z)
   add("kappa.validation.sd", sd_check)
   add("kappa.validation.n_for_width_0_1", (KAPPA_Z * sd_check / 0.05) ** 2)

   # Bank draw.
   serves_low = ITEMS_PER_SESSION_LOW * SESSIONS
   serves_high = ITEMS_PER_SESSION_HIGH * SESSIONS
   add("draw.serves_low", serves_low)
   add("draw.serves_high", serves_high)
   add("draw.serves_mid", (serves_low + serves_high) / 2)
   add("draw.per_archetype_low", serves_low / ACTIVE_ARCHETYPES)
   add("draw.per_archetype_high", serves_high / ACTIVE_ARCHETYPES)
   add("draw.per_archetype_mid", (serves_low + serves_high) / 2 / ACTIVE_ARCHETYPES)
   top = math.ceil(ACTIVE_ARCHETYPES / 10)
   add("draw.top_decile_archetypes", top)
   add("draw.top_decile_serves_each", (serves_low + serves_high) / 2 / 2 / top)
   add("draw.rest_serves_each", (serves_low + serves_high) / 2 / 2 / (ACTIVE_ARCHETYPES - top))
   add("draw.bank_for_no_repeat_at_33", bank_for_no_repeat(UNIFORM_SERVES_PER_ARCHETYPE, NO_REPEAT_CONFIDENCE))
   add("draw.bank_for_no_repeat_at_164", bank_for_no_repeat(TOP_DECILE_SERVES, NO_REPEAT_CONFIDENCE))

   for bank in (30, 40, 60):
      add(f"draw.repeat_share_random_bank_{bank}_at_33", expected_repeat_share_random(UNIFORM_SERVES_PER_ARCHETYPE, bank))
      add(f"draw.repeat_share_lrs_bank_{bank}_at_33", repeat_share_least_recently_served(UNIFORM_SERVES_PER_ARCHETYPE, bank))
      add(f"draw.repeat_share_lrs_bank_{bank}_at_164", repeat_share_least_recently_served(TOP_DECILE_SERVES, bank))

   return out


def render(value):
   if isinstance(value, int):
      return f"{value:,}"

   magnitude = abs(value)

   if magnitude >= 1:
      return f"{value:,.2f}"

   if magnitude >= 0.01:
      return f"{value:.4f}"

   return f"{value:.6f}"


def spellings(value):
   """Every way a document may print this value: the currency rendering, the integer, and the
   rounded forms the prose uses for sub-cent amounts."""
   forms = set()

   if isinstance(value, int):
      forms.add(f"{value:,}")
      forms.add(f"{value:,.2f}")

      return forms

   forms.add(f"{value:,.2f}")
   forms.add(f"{round(value):,}")
   rounded_up = math.ceil(value)
   forms.add(f"{rounded_up:,}")

   for places in (3, 4, 5, 6):
      forms.add(f"{value:.{places}f}")

   return forms


DOLLAR = re.compile(r"\$([0-9][0-9,]*(?:\.[0-9]+)?)")


def check(path, values):
   """Every dollar figure in the file must be a spelling of some figure this model emits."""
   known = set()

   for value in values.values():
      known |= spellings(value)

   text = Path(path).read_text()
   unknown = []

   for line_number, line in enumerate(text.splitlines(), start=1):
      for match in DOLLAR.finditer(line):
         printed = match.group(1)

         if printed not in known:
            unknown.append((line_number, printed))

   return unknown


def main(argv=None):
   parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   parser.add_argument("--check", nargs="*", default=None,
                       help="markdown files whose dollar figures must all be emitted here")
   args = parser.parse_args(argv)
   values = figures()

   if args.check is None:
      for name, value in values.items():
         print(f"{name} = {render(value)}")

      return 0

   failed = False

   for path in args.check:
      unknown = check(path, values)

      for line_number, printed in unknown:
         print(f"{path}:{line_number}: ${printed} is not a figure in tools/cost_model.py")
         failed = True

      print(f"{path}: {len(unknown)} unknown dollar figures")

   return 1 if failed else 0


if __name__ == "__main__":
   sys.exit(main())
