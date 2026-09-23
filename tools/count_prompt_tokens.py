"""Measure a prompt template's static prefix with Anthropic's free count_tokens endpoint.

Usage: python3 tools/count_prompt_tokens.py [--model MODEL] <template> [<template> ...]

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
"""
import argparse
import datetime
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPOSITORY_ROOT))

from app.feedback.tutor import TUTOR_MODEL
from app.providers.base import split_template

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


def load_counts():
   has_counts = COUNTS_PATH.exists()

   if not has_counts:
      return {}

   return json.loads(COUNTS_PATH.read_text())


def main():
   parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   parser.add_argument("templates", nargs="+", type=Path)
   parser.add_argument("--model", default=TUTOR_MODEL)
   arguments = parser.parse_args()

   api_key = read_api_key()
   counts = load_counts()

   for template in arguments.templates:
      template_path = template.resolve()
      relative_name = str(template_path.relative_to(REPOSITORY_ROOT))
      entry = measure(api_key, arguments.model, template_path)
      by_model = counts.setdefault(relative_name, {})
      by_model[arguments.model] = entry
      print(f"{relative_name}: {entry['prefix_tokens']} prefix tokens on {entry['model']}")

   COUNTS_PATH.write_text(json.dumps(counts, indent=3, sort_keys=True) + "\n")


if __name__ == "__main__":
   main()
