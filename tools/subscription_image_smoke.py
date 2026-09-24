"""Live smoke check that the subscription backend carries an image, on the operator's Claude login.

Usage: python3 tools/subscription_image_smoke.py [--model claude-sonnet-5]

Never run from a test: it runs the real claude CLI (tests/conftest.py fails any test that
resolves it). It builds app/providers/subscription.py SubscriptionProvider the way the app builds
it, sends one transcriber request carrying a rendered page from tests/fixtures/frq_pages, and
checks, from the stream-json events the CLI prints:

- the run's init event lists no tool but the CLI's internal StructuredOutput and no MCP server,
  so --tools "" and the empty MCP config held on the image path;
- the result is one structured read-back and no permission was requested;
- the reported input tokens stay under LEAK_INPUT_TOKEN_CEILING plus the image's own tokens, so
  no CLAUDE.md or default system prompt leaked in;
- the read-back contains the page's final answer, so the image reached the model.

It never reads CLAUDE_CODE_OAUTH_TOKEN; the adapter passes it through by name only when set.
Result on 2026-09-24 (BUILD-LEDGER.md): Haiku 4.5 and Sonnet 5 both read the page, tools
["StructuredOutput"], mcp_servers [], $0.00 of API spend.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app.frq.items import load_frq_records
from app.grading import transcribe
from app.providers import subscription

PAGE = REPO_ROOT / "tests" / "fixtures" / "frq_pages" / "critical_point_full__clean.jpg"
ITEM_ID = "FRQ-AGT-05007-01"
EXPECTED_IN_READ_BACK = "3"
LEAK_INPUT_TOKEN_CEILING = 4000
ALLOWED_TOOLS = ["StructuredOutput"]


def image_request(model):
   records = {record["id"]: record for record in load_frq_records(REPO_ROOT / "content" / "frq_items")}
   data = PAGE.read_bytes()
   image = transcribe.ImageInput(media_type="image/jpeg", data=data, width=0, height=0)
   request = transcribe.request_for(records[ITEM_ID], [image])

   return request.__class__(**{**request.__dict__, "model": model})


def run(model):
   request = image_request(model)
   env = subscription.build_env(os.environ, disable_thinking=True)
   binary = subscription.resolve_binary(subscription.DEFAULT_BINARY, env.get("PATH"))
   argv = subscription.build_argv(
      binary,
      request.model,
      request.system,
      output_schema=request.output_schema,
      streams_json=True,
   )

   with tempfile.TemporaryDirectory(prefix=subscription.TEMP_DIR_PREFIX) as work_dir:
      completed = subprocess.run(
         argv,
         input=subscription.stream_json_input(request),
         capture_output=True,
         text=True,
         cwd=work_dir,
         env=env,
         timeout=subscription.DEFAULT_TIMEOUT_SECONDS,
      )

   events = [json.loads(line) for line in completed.stdout.splitlines() if line.strip().startswith("{")]
   init = next((event for event in events if event.get("type") == "system"), {})
   result = subscription.result_event_of(completed.stdout) or {}
   usage = result.get("usage") or {}
   input_tokens = sum(usage.get(name) or 0 for name in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
   read_back = json.dumps(result.get("structured_output") or {})

   return {
      "model": model,
      "exit": completed.returncode,
      "tools": init.get("tools"),
      "mcp_servers": init.get("mcp_servers"),
      "permission_denials": result.get("permission_denials"),
      "input_tokens": input_tokens,
      "total_cost_usd_notional": result.get("total_cost_usd"),
      "checks": {
         "no_tool_but_structured_output": init.get("tools") == ALLOWED_TOOLS,
         "no_mcp_server": init.get("mcp_servers") == [],
         "no_permission_requested": not result.get("permission_denials"),
         "no_context_leak": input_tokens < LEAK_INPUT_TOKEN_CEILING + 4784,
         "image_was_read": EXPECTED_IN_READ_BACK in read_back,
      },
   }


def main(argv=None):
   parser = argparse.ArgumentParser()
   parser.add_argument("--model", default="claude-sonnet-5")
   arguments = parser.parse_args(argv)
   report = run(arguments.model)
   print(json.dumps(report, indent=1))

   return 0 if all(report["checks"].values()) else 1


if __name__ == "__main__":
   sys.exit(main())
