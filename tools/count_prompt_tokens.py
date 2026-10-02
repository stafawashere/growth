"""Measure a prompt template's static prefix with Anthropic's free count_tokens endpoint.

Usage: python3 tools/count_prompt_tokens.py [--model MODEL] [--subscription] <template> [<template> ...]

The prefix is everything above the prompt-variables marker, exactly as app/providers/base.py
split_template returns it and as app/providers/anthropic.py sends it in the system block. Two
requests are counted per template: the prefix as the system block with a one-character user
message, and the same user message with no system block at all. The difference is the prefix's
own cost, which is the number the cache minimum is compared against.

Results are merged into tests/fixtures/prompt_token_counts.json, keyed first by the template's
path relative to the repository and then by the model the measurement was taken on, together
with the sha256 of the exact prefix bytes, so a prefix that changes after it was measured no
longer matches its entry and a second model measured against the same template does not
overwrite the first.

The key is read from ANTHROPIC_API_KEY in the repository's .env file and goes nowhere but the
x-api-key header of a request to api.anthropic.com. Only count_tokens is called, never messages.

--subscription measures on the operator's Claude subscription instead, through the claude CLI with
the argv and environment app/providers/subscription.py builds, at no API cost and with no key read.
The CLI has no count_tokens, so the prefix is read off the prompt cache: the template's tutor
request is sent twice with the prefix as its system prompt, and twice more with the prefix written
out two times, each pair with two different user messages so the second call of a pair reads only
the system block from the cache. The prefix count is the doubled pair's cache read minus the single
pair's, which cancels anything the CLI itself adds to the system block. A cache read above zero on
the single pair is also the direct evidence that the prefix clears the model's cache minimum. Four
subscription calls per template.
"""
import argparse
import dataclasses
import datetime
import hashlib
import json
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPOSITORY_ROOT))

from app.feedback import tutor
from app.feedback.tutor import TUTOR_MODEL
from app.providers.base import Message, split_template

ENV_PATH = REPOSITORY_ROOT / ".env"

COUNTS_PATH = REPOSITORY_ROOT / "tests" / "fixtures" / "prompt_token_counts.json"

COUNT_TOKENS_URL = "https://api.anthropic.com/v1/messages/count_tokens"

ANTHROPIC_VERSION = "2023-06-01"

MINIMAL_USER_MESSAGE = "x"

METHOD = (
   "POST /v1/messages/count_tokens twice: system set to the template's static prefix with a "
   "one-character user message, and the same user message with no system block; the prefix "
   "count is the first input_tokens minus the second"
)


def read_api_key():
   has_env_file = ENV_PATH.exists()

   if not has_env_file:
      raise SystemExit(f"{ENV_PATH} does not exist")

   for line in ENV_PATH.read_text().splitlines():
      is_key_line = line.startswith("ANTHROPIC_API_KEY=")

      if is_key_line:
         return line.split("=", 1)[1].strip().strip("\"").strip("'")

   raise SystemExit(f"ANTHROPIC_API_KEY is not set in {ENV_PATH}")


def prefix_of(template_path):
   prefix, _variable_section = split_template(template_path.read_text())

   return prefix


def prefix_digest(prefix):
   return hashlib.sha256(prefix.encode("utf-8")).hexdigest()


def count_input_tokens(api_key, model, system):
   body = {
      "model": model,
      "messages": [{"role": "user", "content": MINIMAL_USER_MESSAGE}],
   }
   has_system = system is not None

   if has_system:
      body["system"] = [{"type": "text", "text": system}]

   request = urllib.request.Request(
      COUNT_TOKENS_URL,
      data=json.dumps(body).encode("utf-8"),
      headers={
         "x-api-key": api_key,
         "anthropic-version": ANTHROPIC_VERSION,
         "content-type": "application/json",
      },
      method="POST",
   )

   try:
      with urllib.request.urlopen(request, timeout=30) as response:
         payload = json.loads(response.read())
   except urllib.error.HTTPError as failure:
      detail = json.loads(failure.read() or b"{}").get("error", {})
      raise SystemExit(f"count_tokens returned {failure.code}: {detail.get('type')} {detail.get('message')}")

   return payload["input_tokens"]


def measure(api_key, model, template_path):
   prefix = prefix_of(template_path)
   with_prefix = count_input_tokens(api_key, model, prefix)
   without_prefix = count_input_tokens(api_key, model, None)

   return {
      "sha256": prefix_digest(prefix),
      "model": model,
      "prefix_tokens": with_prefix - without_prefix,
      "input_tokens_with_prefix": with_prefix,
      "input_tokens_without_prefix": without_prefix,
      "measured_on": datetime.date.today().isoformat(),
      "method": METHOD,
   }


SUBSCRIPTION_METHOD = (
   "prompt cache reads through the claude CLI on the operator's subscription, with the production "
   "argv of app/providers/subscription.py: the tutor request with the static prefix as its system "
   "prompt, sent twice with two different user messages, and the same with the prefix written out "
   "twice; the prefix count is the second doubled call's cache_read_input_tokens minus the second "
   "single call's, so a constant the CLI adds cancels and the two-character separator between the "
   "copies is counted with the prefix"
)
PREFIX_SEPARATOR = "\n\n"
FIRST_MESSAGE = "Which step does this feedback refer to?"
SECOND_MESSAGE = "Say the rule in one sentence."


def subscription_call(provider, request, system, message):
   result = provider.generate(dataclasses.replace(request, system=system, messages=[Message(role="user", content=message)]))

   return {
      "cache_read_input_tokens": result.usage.cached_read_tokens,
      "cache_creation_input_tokens": result.usage.cached_write_tokens,
      "input_tokens": result.usage.input_tokens,
      "output_tokens": result.usage.output_tokens,
      "model": result.model,
   }


def measure_on_subscription(provider, model, template_path, measured_by):
   prefix = prefix_of(template_path)
   request = dataclasses.replace(tutor.request_from_messages([Message(role="user", content=FIRST_MESSAGE)]), model=model)
   doubled = prefix + PREFIX_SEPARATOR + prefix
   calls = {}

   for label, system in (("single", prefix), ("doubled", doubled)):
      calls[label] = [
         subscription_call(provider, request, system, FIRST_MESSAGE),
         subscription_call(provider, request, system, SECOND_MESSAGE),
      ]

   single_read = calls["single"][1]["cache_read_input_tokens"] or 0
   doubled_read = calls["doubled"][1]["cache_read_input_tokens"] or 0

   return {
      "sha256": prefix_digest(prefix),
      "model": model,
      "prefix_tokens": doubled_read - single_read,
      "single_prefix_cache_read": single_read,
      "doubled_prefix_cache_read": doubled_read,
      "calls": calls,
      "backend": "subscription",
      "measured_by": measured_by,
      "measured_on": datetime.date.today().isoformat(),
      "method": SUBSCRIPTION_METHOD,
   }


def load_counts():
   has_counts = COUNTS_PATH.exists()

   if not has_counts:
      return {}

   return json.loads(COUNTS_PATH.read_text())


def main():
   parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   parser.add_argument("templates", nargs="+", type=Path)
   parser.add_argument("--model", default=TUTOR_MODEL)
   parser.add_argument("--subscription", action="store_true", help="measure through the claude CLI, no key")
   parser.add_argument("--measured-by", default="", help="who ran the measurement, recorded with it")
   arguments = parser.parse_args()
   counts = load_counts()

   if arguments.subscription:
      from app.providers.guard import SubscriptionSpendLedger
      from app.providers.subscription import SubscriptionProvider

      ledger_path = Path(tempfile.mkdtemp(prefix="count-prompt-tokens-")) / "subscription_spend.json"
      provider = SubscriptionProvider(subscription_ledger=SubscriptionSpendLedger(path=ledger_path))
   else:
      api_key = read_api_key()

   for template in arguments.templates:
      template_path = template.resolve()
      relative_name = str(template_path.relative_to(REPOSITORY_ROOT))

      if arguments.subscription:
         entry = measure_on_subscription(provider, arguments.model, template_path, arguments.measured_by)
      else:
         entry = measure(api_key, arguments.model, template_path)

      by_model = counts.setdefault(relative_name, {})
      by_model[arguments.model] = entry
      print(f"{relative_name}: {entry['prefix_tokens']} prefix tokens on {entry['model']}")

   COUNTS_PATH.write_text(json.dumps(counts, indent=3, sort_keys=True) + "\n")


if __name__ == "__main__":
   main()
