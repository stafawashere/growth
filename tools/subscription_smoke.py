"""Live smoke test of the subscription backend against the operator's real claude CLI.

Usage: python3 tools/subscription_smoke.py [--latency-calls N] [--pace-seconds S] [--skip-latency]

Never run from a test: it spends the operator's subscription (no API key is ever passed) and
reaches Anthropic through the CLI. tests/conftest.py fails any test that resolves this binary.

The provider is built the way the app builds it, app/main.py build_tutor with
GROWTH_AI_BACKEND=subscription, so the argv, the environment allowlist and the empty working
directory are the production ones. CLAUDE_CODE_OAUTH_TOKEN is taken from the environment, or
from the repository's .env when it is not set, and only ever handed to the CLI's environment;
this tool reports whether it was present, never its value. Without it the CLI uses its own
keychain login.

Phases, in order:
1. One tutor call on claude-haiku-4-5 and one on the model app/providers/model_routing.py gives
   the tutor, over a real item's fields. Each is checked for: a JSON result that parses, one turn
   and no permission denial (no tool ran), the reported input tokens against the API cassettes'
   input for the same template (a leaked CLAUDE.md or the CLI's default system prompt would add
   thousands of tokens), no text from the operator's CLAUDE.md in the reply, and usage and
   total_cost_usd present.
2. One structured-output call with --json-schema. The CLI answers a schema by having the model
   call its own internal StructuredOutput tool, which costs exactly one extra turn and is not one
   of the built-in tools --tools "" removes, so that call passes no_tool_ran at two turns only
   when structured_output came back.
3. Latency: --latency-calls tutor calls per model (default 10) over the fields of the eight
   recorded Haiku cassettes, at least --pace-seconds apart (default 5), recording wall-clock
   seconds and the CLI's duration_ms.

Writes every call to var/subscription_smoke.json and prints a summary. At most
2 + 1 + 2 * latency-calls live calls, 23 by default. --latency-only runs phase 3 alone.
"""
import argparse
import dataclasses
import json
import os
import statistics
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app.feedback import render, tutor
from app.main import build_tutor
from app.providers import subscription
from app.providers.model_routing import model_for

HAIKU = "claude-haiku-4-5"
CASSETTE_DIR = REPO_ROOT / "tests" / "fixtures" / "provider_cassettes"
ENV_FILE = REPO_ROOT / ".env"
OUTPUT_PATH = REPO_ROOT / "var" / "subscription_smoke.json"
LEAK_MARKERS = ("Mahfuj", "CLAUDE.md", "ADDRESS ME BY NAME", "laconic")
LEAK_INPUT_TOKEN_CEILING = 4000
STRUCTURED_SCHEMA = {
   "type": "object",
   "properties": {"sentence": {"type": "string"}},
   "required": ["sentence"],
   "additionalProperties": False,
}
MAX_LIVE_CALLS = 30


def token_from_env_file():
   has_env_file = ENV_FILE.is_file()

   if not has_env_file:
      return None

   prefix = f"{subscription.OAUTH_TOKEN_ENV_VAR}="

   for line in ENV_FILE.read_text().splitlines():
      names_the_token = line.startswith(prefix) and len(line) > len(prefix)

      if names_the_token:
         return line[len(prefix):].strip().strip('"')

   return None


def smoke_environment():
   env = dict(os.environ)
   env["GROWTH_AI_BACKEND"] = "subscription"
   env.pop("GROWTH_TUTOR_PROVIDER", None)
   has_token = subscription.OAUTH_TOKEN_ENV_VAR in env

   if not has_token:
      from_file = token_from_env_file()

      if from_file is not None:
         env[subscription.OAUTH_TOKEN_ENV_VAR] = from_file

   return env


class RecordingRun:
   """Wraps subprocess.run inside app/providers/subscription.py so the raw JSON the CLI printed
   can be inspected; the provider itself is untouched."""

   def __init__(self, real_run):
      self.real_run = real_run
      self.last_stdout = None
      self.last_stderr = None
      self.last_argv = None

   def forget(self):
      self.last_stdout = None
      self.last_stderr = None

   def __call__(self, argv, **kwargs):
      completed = self.real_run(argv, **kwargs)
      self.last_argv = list(argv)
      self.last_stdout = completed.stdout
      self.last_stderr = completed.stderr

      return completed


def cassette_fields():
   archetypes = {record["id"]: record for record in json.loads((REPO_ROOT / "data" / "archetypes.json").read_text())["archetypes"]}
   errors = {record["id"]: record for record in json.loads((REPO_ROOT / "data" / "errors.json").read_text())["errors"]}
   inputs = []

   for cassette_path in sorted(CASSETTE_DIR.glob("tutor_haiku_live_*.json")):
      cassette = json.loads(cassette_path.read_text())
      item = json.loads((REPO_ROOT / "content" / "items_p1_agent" / cassette["source_item"]).read_text())
      error_record = errors[cassette["source_error"]]
      chosen = next(option for option in item["options"] if option.get("error_path") == cassette["source_error"])
      payload = render.elaborated_payload(archetypes[cassette["source_archetype"]], item, chosen, error_record)
      api_input = cassette["usage"]["input_tokens"]
      inputs.append((cassette_path.name, payload.as_prompt_fields(), api_input))

   return inputs


def reported_input_tokens(raw_usage):
   parts = (
      raw_usage.get("input_tokens"),
      raw_usage.get("cache_read_input_tokens"),
      raw_usage.get("cache_creation_input_tokens"),
   )

   return sum(part for part in parts if isinstance(part, int))


def one_call(provider, recorder, request, label):
   recorder.forget()
   started = time.monotonic()
   error = None
   result = None

   try:
      result = provider.generate(request)
   except Exception as raised:
      error = f"{type(raised).__name__}: {raised}"

   wall_seconds = time.monotonic() - started
   payload = {}

   try:
      payload = json.loads(recorder.last_stdout or "")
   except ValueError:
      payload = {}

   text = result.text if result is not None else payload.get("result")
   raw_usage = dict(payload.get("usage") or {})
   leaked_markers = [marker for marker in LEAK_MARKERS if text and marker.lower() in text.lower()]
   input_tokens = reported_input_tokens(raw_usage)

   return {
      "label": label,
      "model": request.model,
      "error": error,
      "wall_seconds": round(wall_seconds, 3),
      "duration_ms": payload.get("duration_ms"),
      "duration_api_ms": payload.get("duration_api_ms"),
      "num_turns": payload.get("num_turns"),
      "subtype": payload.get("subtype"),
      "is_error": payload.get("is_error"),
      "permission_denials": payload.get("permission_denials"),
      "total_cost_usd": payload.get("total_cost_usd"),
      "usage": {key: raw_usage.get(key) for key in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")},
      "reported_input_tokens": input_tokens,
      "model_usage_keys": sorted((payload.get("modelUsage") or {}).keys()),
      "structured_output": payload.get("structured_output"),
      "text_characters": len(text or ""),
      "leaked_markers": leaked_markers,
      "payload_keys": sorted(payload.keys()),
      "stderr_head": (recorder.last_stderr or "")[:400] if error else "",
      "result_head": (payload.get("result") or "")[:300] if error else "",
   }


def checks_for(call, api_input_tokens=None, asked_for_structured_output=False):
   returned_structured_output = call["structured_output"] is not None
   took_the_structured_output_turn = asked_for_structured_output and returned_structured_output
   expected_turns = 2 if took_the_structured_output_turn else 1
   took_only_the_expected_turns = call["num_turns"] == expected_turns
   had_no_permission_denial = not call["permission_denials"]
   no_tool_ran = took_only_the_expected_turns and had_no_permission_denial
   cost_parsed = isinstance(call["total_cost_usd"], (int, float))
   usage_parsed = isinstance(call["usage"]["input_tokens"], int) and isinstance(call["usage"]["output_tokens"], int)
   under_leak_ceiling = 0 < call["reported_input_tokens"] < LEAK_INPUT_TOKEN_CEILING
   no_marker = call["leaked_markers"] == []

   return {
      "succeeded": call["error"] is None,
      "no_tool_ran": no_tool_ran,
      "usage_parsed": usage_parsed,
      "cost_parsed": cost_parsed,
      "input_under_leak_ceiling": under_leak_ceiling,
      "no_claude_md_marker": no_marker,
      "api_input_tokens_same_template": api_input_tokens,
   }


def percentile(values, fraction):
   ordered = sorted(values)
   rank = max(0, min(len(ordered) - 1, int(round(fraction * (len(ordered) - 1)))))

   return ordered[rank]


def summarise(calls):
   by_model = {}

   for call in calls:
      succeeded = call["error"] is None

      if succeeded:
         by_model.setdefault(call["model"], []).append(call)

   summary = {}

   for model, model_calls in by_model.items():
      walls = [call["wall_seconds"] for call in model_calls]
      durations = [call["duration_ms"] / 1000 for call in model_calls if isinstance(call["duration_ms"], int)]
      summary[model] = {
         "n": len(model_calls),
         "wall_median_s": round(statistics.median(walls), 2),
         "wall_p90_s": round(percentile(walls, 0.9), 2),
         "duration_ms_median_s": round(statistics.median(durations), 2) if durations else None,
         "duration_ms_p90_s": round(percentile(durations, 0.9), 2) if durations else None,
         "notional_cost_usd": round(sum(call["total_cost_usd"] or 0 for call in model_calls), 6),
      }

   return summary


def parse_arguments(argv):
   parser = argparse.ArgumentParser(description="Live smoke test of the subscription backend.")
   parser.add_argument("--latency-calls", type=int, default=10)
   parser.add_argument("--pace-seconds", type=float, default=5.0)
   parser.add_argument("--skip-latency", action="store_true")
   parser.add_argument("--latency-only", action="store_true", help="skip phases 1 and 2")

   return parser.parse_args(argv)


def main(argv=None):
   arguments = parse_arguments(argv)
   check_calls = 0 if arguments.latency_only else 3
   planned_calls = check_calls + (0 if arguments.skip_latency else 2 * arguments.latency_calls)

   if planned_calls > MAX_LIVE_CALLS:
      print(f"{planned_calls} live calls planned, more than the {MAX_LIVE_CALLS} this slice allows", file=sys.stderr)

      return 2

   env = smoke_environment()
   token_present = subscription.OAUTH_TOKEN_ENV_VAR in env
   provider = build_tutor(env)
   recorder = RecordingRun(subscription.subprocess.run)
   subscription.subprocess.run = recorder
   tutor_model = model_for("tutor")
   inputs = cassette_fields()
   report = {
      "cli_binary": subscription.resolve_binary(subscription.DEFAULT_BINARY, env.get("PATH")),
      "oauth_token_present": token_present,
      "provider": type(provider).__name__,
      "template_prefix_tokens": json.loads((REPO_ROOT / "tests" / "fixtures" / "prompt_token_counts.json").read_text())["prompts/feedback/elaborated_v2.md"],
      "argv_flags": None,
      "phase_1": [],
      "phase_2": None,
      "latency": [],
   }
   last_call_at = [0.0]

   def paced_call(request, label):
      wait = arguments.pace_seconds - (time.monotonic() - last_call_at[0])

      if wait > 0:
         time.sleep(wait)

      call = one_call(provider, recorder, request, label)
      last_call_at[0] = time.monotonic()
      print(f"{label} {call['model']} wall={call['wall_seconds']}s duration_ms={call['duration_ms']} "
            f"cost={call['total_cost_usd']} error={call['error']}", flush=True)

      return call

   if not arguments.latency_only:
      stopped = run_checks(report, inputs, tutor_model, recorder, paced_call)

      if stopped:
         write_report(report)

         return 1

   if not arguments.skip_latency:
      for model in (HAIKU, tutor_model):
         for index in range(arguments.latency_calls):
            name, fields, api_input = inputs[index % len(inputs)]
            request = dataclasses.replace(tutor.request_for(fields), model=model)
            call = paced_call(request, f"latency:{name}")
            call["checks"] = checks_for(call, api_input)
            report["latency"].append(call)

   report["latency_summary"] = summarise(report["latency"])
   write_report(report)

   print(json.dumps({"latency_summary": report["latency_summary"], "live_calls": report["live_calls"],
                     "notional_cost_usd_total": report["notional_cost_usd_total"],
                     "oauth_token_present": token_present}, indent=3))

   return 0


def run_checks(report, inputs, tutor_model, recorder, paced_call):
   """Phases 1 and 2. Returns True when a phase 1 call failed, so no latency call is spent on an
   argv the CLI refuses."""
   first_name, first_fields, first_api_input = inputs[0]
   base_request = tutor.request_for(first_fields)

   for model in (HAIKU, tutor_model):
      request = dataclasses.replace(base_request, model=model)
      call = paced_call(request, f"phase1:{first_name}")
      call["checks"] = checks_for(call, first_api_input)
      report["phase_1"].append(call)

   report["argv_flags"] = [
      "--system-prompt=<template prefix>" if part.startswith("--system-prompt=") else part
      for part in recorder.last_argv[1:]
   ]
   phase_one_failed = any(call["error"] is not None for call in report["phase_1"])

   if phase_one_failed:
      return True

   structured_request = dataclasses.replace(base_request, model=HAIKU, output_schema=STRUCTURED_SCHEMA)
   structured = paced_call(structured_request, "phase2:structured")
   structured["checks"] = checks_for(structured, first_api_input, asked_for_structured_output=True)
   structured_output = structured["structured_output"] or {}
   structured["checks"]["structured_output_has_sentence"] = isinstance(structured_output.get("sentence"), str)
   report["phase_2"] = structured

   return False


def write_report(report):
   phase_two = [report["phase_2"]] if report["phase_2"] else []
   every_call = report["phase_1"] + phase_two + report["latency"]
   report["live_calls"] = len(every_call)
   report["notional_cost_usd_total"] = round(sum(call["total_cost_usd"] or 0 for call in every_call), 6)
   OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
   OUTPUT_PATH.write_text(json.dumps(report, indent=3, sort_keys=True))


if __name__ == "__main__":
   sys.exit(main())
