"""SubscriptionProvider runs a role on the operator's own Claude subscription through the
official Claude Code CLI, headless, so runtime calls are not billed to ANTHROPIC_API_KEY.

Each call is one throwaway `claude -p` process started from an argument list, never a shell. The
CLI gets the role's system prompt, the user prompt on stdin, and nothing else: no session
persistence, no user or project settings, no MCP server, no slash commands and no tool. Its working
directory is an empty temporary directory removed after the call, so no CLAUDE.md, hook or plugin
in this repository or above it is found.

The subprocess environment is built from ENV_ALLOWLIST and never copied from os.environ, so no
ANTHROPIC_* variable reaches the CLI and it cannot fall back to billing the paid key. The one
credential passed through is the operator's long-lived OAuth token, by name only: this module
checks that it is present and copies it, and never reads, logs or compares its value. Without it
the CLI uses its own logged-in keychain session, which is the same subscription. This is the only
file in app/ that names that variable, and it imports no HTTP client, so the token has no route to
the Messages API (tests/providers/test_subscription_compliance.py scans for both).

A subscription login is the operator's alone. The provider refuses to construct when the app
database holds more than one user account, and app/auth/service.py refuses a second registration
outright, so the login is never offered to another person.

total_cost_usd in the CLI's result is what the call would have cost on the API. It is recorded in
app/providers/guard.py's SubscriptionSpendLedger, a separate counter that never touches the $15
developer cap on the API key.

A usage-limit answer (5-hour or weekly) raises SubscriptionLimitReached. The caller degrades as
docs/plan/07-ai-provider-layer.md degrades a hard stop and queues the call; nothing here falls
through to the API.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile

from app.providers.base import Provider, ProviderResult, RefusedBeforeWire, Usage
from app.providers.guard import SubscriptionSpendLedger

OAUTH_TOKEN_ENV_VAR = "CLAUDE_CODE_OAUTH_TOKEN"
BINARY_ENV_VAR = "GROWTH_CLAUDE_BIN"
DEFAULT_BINARY = "claude"

ENV_ALLOWLIST = ("PATH", "HOME", "USER", "LANG", "TMPDIR")

# The CLI thinks by default. On 2026-09-23 a tutor call on claude-haiku-4-5 through the CLI spent
# 6,176 output tokens and 60 s on a 407-character answer, where the same template on the API with
# thinking disabled spent about 120. A request whose provider_options disable thinking, as the
# tutor's do, runs the CLI with this fixed value, never one copied from the host.
THINKING_ENV_VAR = "MAX_THINKING_TOKENS"
THINKING_DISABLED_VALUE = "0"

DISALLOWED_TOOLS = (
   "Agent",
   "Bash",
   "BashOutput",
   "Edit",
   "ExitPlanMode",
   "Glob",
   "Grep",
   "KillShell",
   "ListMcpResourcesTool",
   "MultiEdit",
   "NotebookEdit",
   "PowerShell",
   "Read",
   "ReadMcpResourceTool",
   "SlashCommand",
   "Skill",
   "Task",
   "TodoWrite",
   "WebFetch",
   "WebSearch",
   "Write",
)

EMPTY_MCP_CONFIG = json.dumps({"mcpServers": {}})

DEFAULT_MAX_BUDGET_USD = 0.25
ROLE_MAX_BUDGET_USD = {
   "tutor": 0.10,
}

TEMP_DIR_PREFIX = "growth-claude-"
DEFAULT_TIMEOUT_SECONDS = 120

_LIMIT_PATTERNS = tuple(
   re.compile(pattern, re.IGNORECASE)
   for pattern in (
      r"weekly limit",
      r"5[- ]hour limit",
      r"usage limit",
      r"rate limit",
   )
)


class SubscriptionTransportError(RuntimeError):
   """A CLI failure that is not a usage limit: a timeout, a non-zero exit, or output that is
   not the JSON result. The message names the role and the CLI's subtype, never its output."""


class SubscriptionBinaryMissing(SubscriptionTransportError, RefusedBeforeWire):
   """No process started, so nothing reached Anthropic and the guard may refund the call."""


class SubscriptionLimitReached(RuntimeError):
   pass


class SubscriptionSingleUserError(RuntimeError):
   pass


def max_budget_for(role):
   return ROLE_MAX_BUDGET_USD.get(role, DEFAULT_MAX_BUDGET_USD)


def is_limit_message(text):
   is_text = isinstance(text, str) and text != ""

   if not is_text:
      return False

   return any(pattern.search(text) for pattern in _LIMIT_PATTERNS)


def thinking_disabled(provider_options):
   thinking = (provider_options or {}).get("thinking") or {}

   return thinking.get("type") == "disabled"


def effort_of(provider_options):
   output_config = (provider_options or {}).get("output_config") or {}

   return output_config.get("effort")


def build_env(host_environ, disable_thinking=False):
   env = {}

   for name in ENV_ALLOWLIST:
      value = host_environ.get(name)

      if value is not None:
         env[name] = value

   has_oauth_token = OAUTH_TOKEN_ENV_VAR in host_environ

   if has_oauth_token:
      env[OAUTH_TOKEN_ENV_VAR] = host_environ[OAUTH_TOKEN_ENV_VAR]

   if disable_thinking:
      env[THINKING_ENV_VAR] = THINKING_DISABLED_VALUE

   return env


def build_argv(binary, model, system_prompt, output_schema=None, max_budget_usd=DEFAULT_MAX_BUDGET_USD, effort=None):
   """The system prompt rides in the --system-prompt=value form because the tutor template opens
   with front matter, and a bare value starting with --- could be read as an option."""
   argv = [
      binary,
      "-p",
      "--model", model,
      f"--system-prompt={system_prompt}",
      "--output-format", "json",
      "--max-budget-usd", f"{max_budget_usd:.2f}",
      "--no-session-persistence",
      "--setting-sources", "",
      "--strict-mcp-config",
      "--mcp-config", EMPTY_MCP_CONFIG,
      "--disable-slash-commands",
      "--permission-prompts", "none",
      "--tools", "",
      "--disallowedTools", ",".join(DISALLOWED_TOOLS),
   ]

   has_effort = effort is not None and effort != ""

   if has_effort:
      argv.extend(["--effort", effort])

   has_schema = output_schema is not None

   if has_schema:
      argv.append(f"--json-schema={json.dumps(output_schema)}")

   return argv


def prompt_text(messages):
   if not messages:
      return ""

   is_single_message = len(messages) == 1

   if is_single_message:
      return messages[0].content

   return "\n\n".join(f"{message.role}: {message.content}" for message in messages)


def resolve_binary(binary, search_path):
   resolved = shutil.which(binary, path=search_path)

   if resolved is None:
      raise SubscriptionBinaryMissing(f"the claude CLI {binary!r} was not found")

   return os.path.realpath(resolved)


def usage_from(payload):
   usage_block = payload.get("usage") or {}

   return Usage(
      input_tokens=usage_block.get("input_tokens"),
      output_tokens=usage_block.get("output_tokens"),
      cached_read_tokens=usage_block.get("cache_read_input_tokens"),
      cached_write_tokens=usage_block.get("cache_creation_input_tokens"),
   )


class SubscriptionProvider(Provider):
   name = "subscription"

   def __init__(
      self,
      binary=None,
      environ=None,
      user_count=None,
      timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
      subscription_ledger=None,
   ):
      is_multi_user = user_count is not None and user_count > 1

      if is_multi_user:
         raise SubscriptionSingleUserError(
            f"GROWTH_AI_BACKEND=subscription runs on the operator's own Claude login and serves "
            f"one account only, but the database holds {user_count} user accounts. Use "
            f"GROWTH_AI_BACKEND=api or replay for a multi-user installation."
         )

      self._environ = environ if environ is not None else os.environ
      configured_binary = self._environ.get(BINARY_ENV_VAR)
      has_configured_binary = configured_binary is not None and configured_binary != ""
      self._binary = binary or (configured_binary if has_configured_binary else DEFAULT_BINARY)
      self._timeout_seconds = timeout_seconds
      self._ledger = subscription_ledger if subscription_ledger is not None else SubscriptionSpendLedger()

   def generate(self, request):
      env = build_env(self._environ, disable_thinking=thinking_disabled(request.provider_options))
      binary_path = resolve_binary(self._binary, env.get("PATH"))
      argv = build_argv(
         binary_path,
         request.model,
         request.system,
         output_schema=request.output_schema,
         max_budget_usd=max_budget_for(request.role),
         effort=effort_of(request.provider_options),
      )
      work_dir = tempfile.mkdtemp(prefix=TEMP_DIR_PREFIX)
      failure = None

      try:
         completed = subprocess.run(
            argv,
            input=prompt_text(request.messages),
            capture_output=True,
            text=True,
            cwd=work_dir,
            env=env,
            timeout=self._timeout_seconds,
         )
      except subprocess.TimeoutExpired:
         failure = SubscriptionTransportError(f"the claude CLI timed out on role {request.role}")
      except OSError as raised:
         failure = SubscriptionBinaryMissing(f"the claude CLI could not start: {type(raised).__name__}")
      finally:
         shutil.rmtree(work_dir, ignore_errors=True)

      if failure is not None:
         raise failure

      return self._to_result(request, completed)

   def stream(self, request):
      """The json output format has no incremental text, so the whole result is one delta."""
      result = self.generate(request)

      if result.text:
         yield {"type": "text", "delta": result.text}

      return result

   def _to_result(self, request, completed):
      payload = self._payload_of(completed.stdout)
      exit_failed = completed.returncode != 0
      has_payload = payload is not None

      if has_payload:
         self._record_cost(payload)

      reported_error = has_payload and bool(payload.get("is_error"))
      failed = exit_failed or reported_error

      if failed:
         self._raise_for_failure(request, completed, payload)

      if not has_payload:
         raise SubscriptionTransportError(f"the claude CLI returned no JSON result on role {request.role}")

      return self._result_from_payload(request, payload)

   def _payload_of(self, stdout):
      try:
         payload = json.loads(stdout or "")
      except ValueError:
         return None

      is_object = isinstance(payload, dict)

      return payload if is_object else None

   def _record_cost(self, payload):
      total_cost_usd = payload.get("total_cost_usd")
      is_number = isinstance(total_cost_usd, (int, float)) and not isinstance(total_cost_usd, bool)

      if is_number:
         self._ledger.add(float(total_cost_usd))

   def _raise_for_failure(self, request, completed, payload):
      payload = payload or {}
      subtype = payload.get("subtype")
      candidate_texts = (payload.get("result"), subtype, completed.stderr, completed.stdout)
      hit_a_limit = any(is_limit_message(text) for text in candidate_texts)

      if hit_a_limit:
         raise SubscriptionLimitReached(f"the Claude subscription usage limit stopped role {request.role}")

      raise SubscriptionTransportError(
         f"the claude CLI failed on role {request.role}: exit {completed.returncode}, subtype {subtype}"
      )

   def _result_from_payload(self, request, payload):
      structured_output = payload.get("structured_output")
      has_structured_output = structured_output is not None
      text = json.dumps(structured_output) if has_structured_output else payload.get("result")

      raw_usage = dict(payload.get("usage") or {})
      raw_usage["total_cost_usd"] = payload.get("total_cost_usd")
      raw_usage["duration_ms"] = payload.get("duration_ms")

      return ProviderResult(
         text=text,
         finish_reason=payload.get("subtype"),
         usage=usage_from(payload),
         provider=self.name,
         model=request.model,
         request_id=payload.get("session_id"),
         raw_usage=raw_usage,
      )
