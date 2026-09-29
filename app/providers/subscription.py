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

A request that carries images (the transcriber's photographed page) cannot ride on stdin as plain
text, so it runs with --input-format stream-json and --output-format stream-json: stdin holds one
user message whose content is the base64 image blocks followed by the prompt text, and the answer
is the final "result" event, which has the same fields as the json format's single object. The
flags that switch every tool, setting source and MCP server off are the same on both paths. A live
run on 2026-09-24 (tools/subscription_image_smoke.py, BUILD-LEDGER.md) confirmed the CLI then
loads only its internal StructuredOutput tool and reads the image.

A request with stream set and no schema (the live agent's turn) runs with --output-format
stream-json --include-partial-messages --verbose and is read line by line as the CLI writes it, so
text reaches the student about 3 s into a 5 s reply rather than at exit (docs/agent/architecture.md,
Streaming end to end; docs/agent/research/providers.md, Measured on 2026-09-29).

A usage-limit answer (5-hour or weekly) raises SubscriptionLimitReached. The caller degrades as
docs/plan/07-ai-provider-layer.md degrades a hard stop and queues the call; nothing here falls
through to the API.
"""
import base64
import json
import logging
import os
import re
import shutil
import signal
import subprocess
import tempfile
import threading

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

# The live agent and its memory job must fail in seconds when a usage window is closed, not after
# the CLI's default ten retries (docs/agent/research/providers.md, What this means for Growth, item
# 5). Fixed values, never copied from the host, in the way THINKING_DISABLED_VALUE is.
BOUNDED_RETRY_ROLES = ("agent", "memory")
MAX_RETRIES_ENV_VAR = "CLAUDE_CODE_MAX_RETRIES"
BOUNDED_MAX_RETRIES_VALUE = "1"
API_TIMEOUT_ENV_VAR = "API_TIMEOUT_MS"
BOUNDED_API_TIMEOUT_VALUE = "20000"

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
   "agent": 0.15,
   "memory": 0.10,
}

TEMP_DIR_PREFIX = "growth-claude-"
DEFAULT_TIMEOUT_SECONDS = 120
INTERRUPT_WAIT_SECONDS = 5

# No live call has met a usage limit yet, so the wording comes from the CLI itself: claude 2.1.277
# composes its limit line as "You've hit your <limit>" and keeps a list of the prefixes it treats as
# a limit, both read out of the installed binary on 2026-09-24 (BUILD-LEDGER.md, stage 7). The first
# four patterns are the ones in use before that reading and stay.
_LIMIT_PATTERNS = tuple(
   re.compile(pattern, re.IGNORECASE)
   for pattern in (
      r"weekly limit",
      r"5[- ]hour limit",
      r"usage limit",
      r"rate limit",
      r"you've hit your",
      r"you've reached your",
      r"you're out of (extra )?usage",
      r"out of usage credits",
      r"org is out of usage",
      r"seat type doesn't include (extra )?usage",
      r"usage allocation has been disabled",
      r"usage limit is set to \$0",
      r"requires usage credits",
   )
)

_AUTH_PATTERNS = tuple(
   re.compile(pattern, re.IGNORECASE)
   for pattern in (
      r"authentication_failed",
      r"failed to authenticate",
      r"invalid api key",
      r"oauth session expired",
   )
)

logger = logging.getLogger(__name__)
_sign_in_warning = {"logged": False}


class SubscriptionTransportError(RuntimeError):
   """A CLI failure that is not a usage limit: a timeout, a non-zero exit, or output that is
   not the JSON result. The message names the role and the CLI's subtype, never its output."""


class SubscriptionAuthFailed(SubscriptionTransportError):
   """The CLI's login expired or was rejected, so no call can succeed until someone signs in again."""


class SubscriptionBinaryMissing(SubscriptionTransportError, RefusedBeforeWire):
   """No process started, so nothing reached Anthropic and the guard may refund the call."""


class SubscriptionLimitReached(RuntimeError):
   pass


class SubscriptionSingleUserError(RuntimeError):
   pass


RETRY_FAILURES = {
   "rate_limit": SubscriptionLimitReached,
   "authentication_failed": SubscriptionAuthFailed,
}


def max_budget_for(role):
   return ROLE_MAX_BUDGET_USD.get(role, DEFAULT_MAX_BUDGET_USD)


def is_auth_message(text):
   is_text = isinstance(text, str) and text != ""

   if not is_text:
      return False

   return any(pattern.search(text) for pattern in _AUTH_PATTERNS)


def warn_sign_in_failed_once():
   if _sign_in_warning["logged"]:
      return

   _sign_in_warning["logged"] = True
   logger.warning("The claude CLI sign-in expired or was rejected. Log in again with the claude CLI.")


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


def build_env(host_environ, disable_thinking=False, bounded_retries=False):
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

   if bounded_retries:
      env[MAX_RETRIES_ENV_VAR] = BOUNDED_MAX_RETRIES_VALUE
      env[API_TIMEOUT_ENV_VAR] = BOUNDED_API_TIMEOUT_VALUE

   return env


def env_for(host_environ, request):
   return build_env(
      host_environ,
      disable_thinking=thinking_disabled(request.provider_options),
      bounded_retries=request.role in BOUNDED_RETRY_ROLES,
   )


def build_argv(
   binary,
   model,
   system_prompt,
   output_schema=None,
   max_budget_usd=DEFAULT_MAX_BUDGET_USD,
   effort=None,
   streams_json=False,
   streams_partial=False,
):
   """The system prompt rides in the --system-prompt=value form because the tutor template opens
   with front matter, and a bare value starting with --- could be read as an option.

   streams_json is the image path: stream-json on both sides, which the CLI accepts only with
   --verbose. streams_partial is the incremental text path: stream-json output with the partial
   message events, which also needs --verbose. The two combine."""
   outputs_stream_json = streams_json or streams_partial
   output_format = "stream-json" if outputs_stream_json else "json"
   argv = [
      binary,
      "-p",
      "--model", model,
      f"--system-prompt={system_prompt}",
      "--output-format", output_format,
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

   if streams_json:
      argv.extend(["--input-format", "stream-json"])

   if streams_partial:
      argv.append("--include-partial-messages")

   if outputs_stream_json:
      argv.append("--verbose")

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


def image_block(image):
   return {
      "type": "image",
      "source": {
         "type": "base64",
         "media_type": image.media_type,
         "data": base64.b64encode(image.data).decode("ascii"),
      },
   }


def stream_json_input(request):
   """One user message: every image block first, then the prompt text."""
   content = [image_block(image) for image in request.images]
   content.append({"type": "text", "text": prompt_text(request.messages)})
   message = {"type": "user", "message": {"role": "user", "content": content}}

   return json.dumps(message) + "\n"


def stream_line_event(line):
   """One stdout line as a JSON object, or None for anything else."""
   try:
      event = json.loads(line)
   except ValueError:
      return None

   is_object = isinstance(event, dict)

   return event if is_object else None


def text_delta_of(event):
   inner = event.get("event")
   delta = inner.get("delta") if isinstance(inner, dict) else None
   is_text_delta = isinstance(delta, dict) and delta.get("type") == "text_delta"

   if not is_text_delta:
      return None

   text = delta.get("text")
   is_text = isinstance(text, str) and text != ""

   return text if is_text else None


def retry_failure_of(event):
   """The exception class an api_retry line calls for, or None when the retry may run."""
   is_retry = event.get("type") == "system" and event.get("subtype") == "api_retry"

   if not is_retry:
      return None

   return RETRY_FAILURES.get(event.get("error"))


def result_event_of(stdout):
   """The last stream-json line whose type is result, or None."""
   found = None

   for line in (stdout or "").splitlines():
      try:
         event = json.loads(line)
      except ValueError:
         continue

      is_result = isinstance(event, dict) and event.get("type") == "result"

      if is_result:
         found = event

   return found


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


def send_stdin(process, stdin_text):
   """A CLI that exits before reading its input closes the pipe; its exit status says why."""
   try:
      process.stdin.write(stdin_text)
      process.stdin.close()
   except (BrokenPipeError, OSError):
      pass


def kill_on_timeout(process, timed_out):
   timed_out.set()
   process.kill()


def interrupt(process):
   """SIGINT, then a kill if the CLI has not exited within INTERRUPT_WAIT_SECONDS."""
   is_running = process.poll() is None

   if not is_running:
      return

   process.send_signal(signal.SIGINT)

   try:
      process.wait(timeout=INTERRUPT_WAIT_SECONDS)
   except subprocess.TimeoutExpired:
      process.kill()
      process.wait()


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
      self.last_rate_limit = None

   def generate(self, request):
      env = env_for(self._environ, request)
      binary_path = resolve_binary(self._binary, env.get("PATH"))
      carries_images = len(request.images) > 0
      argv = build_argv(
         binary_path,
         request.model,
         request.system,
         output_schema=request.output_schema,
         max_budget_usd=max_budget_for(request.role),
         effort=effort_of(request.provider_options),
         streams_json=carries_images,
      )
      stdin_text = stream_json_input(request) if carries_images else prompt_text(request.messages)
      work_dir = tempfile.mkdtemp(prefix=TEMP_DIR_PREFIX)
      failure = None

      try:
         completed = subprocess.run(
            argv,
            input=stdin_text,
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

      return self._to_result(request, completed, streamed=carries_images)

   def stream(self, request):
      """A request that streams without a schema is read incrementally. Any other request keeps
      the json output format, which has no incremental text, so its whole result is one delta."""
      streams_incrementally = request.stream and request.output_schema is None

      if streams_incrementally:
         result = yield from self._stream_partial(request)

         return result

      result = self.generate(request)

      if result.text:
         yield {"type": "text", "delta": result.text}

      return result

   def _stream_partial(self, request):
      """One `claude -p` process per turn, started with Popen and read line by line. A process per
      turn, not one held for the conversation, because on 2026-09-29 separate processes read the
      system prompt from the prompt cache and the multi-turn behaviour of a long-lived process
      without session persistence has not been run.

      A text_delta stream_event is yielded as it arrives. A rate_limit_event's rate_limit_info is
      kept on last_rate_limit. An api_retry line for a closed usage window or a rejected sign-in
      ends the process with SIGINT, not SIGTERM, because the headless docs say SIGTERM leaves the
      turn with no result, and raises at once rather than waiting through the retry. The last
      result line becomes the ProviderResult, which is this generator's return value. No line is
      logged."""
      env = env_for(self._environ, request)
      binary_path = resolve_binary(self._binary, env.get("PATH"))
      carries_images = len(request.images) > 0
      argv = build_argv(
         binary_path,
         request.model,
         request.system,
         max_budget_usd=max_budget_for(request.role),
         effort=effort_of(request.provider_options),
         streams_json=carries_images,
         streams_partial=True,
      )
      stdin_text = stream_json_input(request) if carries_images else prompt_text(request.messages)
      work_dir = tempfile.mkdtemp(prefix=TEMP_DIR_PREFIX)
      stderr_file = None
      process = None
      watchdog = None
      timed_out = threading.Event()

      try:
         stderr_file = tempfile.TemporaryFile(mode="w+")

         try:
            process = subprocess.Popen(
               argv,
               stdin=subprocess.PIPE,
               stdout=subprocess.PIPE,
               stderr=stderr_file,
               text=True,
               cwd=work_dir,
               env=env,
            )
         except OSError as raised:
            raise SubscriptionBinaryMissing(f"the claude CLI could not start: {type(raised).__name__}") from None

         watchdog = threading.Timer(self._timeout_seconds, kill_on_timeout, args=(process, timed_out))
         watchdog.daemon = True
         watchdog.start()
         send_stdin(process, stdin_text)
         payload = None
         stdout_lines = []

         for line in iter(process.stdout.readline, ""):
            stdout_lines.append(line)
            event = stream_line_event(line)

            if event is None:
               continue

            event_type = event.get("type")
            retry_failure = retry_failure_of(event)

            if event_type == "stream_event":
               delta = text_delta_of(event)

               if delta is not None:
                  yield {"type": "text", "delta": delta}
            elif event_type == "rate_limit_event":
               self._keep_rate_limit(event)
            elif retry_failure is not None:
               interrupt(process)
               raise self._retry_failure(request, retry_failure)
            elif event_type == "result":
               payload = event

         process.wait()

         if timed_out.is_set():
            raise SubscriptionTransportError(f"the claude CLI timed out on role {request.role}")

         stderr_file.seek(0)
         completed = subprocess.CompletedProcess(argv, process.returncode, "".join(stdout_lines), stderr_file.read())

         return self._settle_payload(request, completed, payload)
      finally:
         if watchdog is not None:
            watchdog.cancel()

         if process is not None:
            interrupt(process)
            process.stdout.close()

         if stderr_file is not None:
            stderr_file.close()

         shutil.rmtree(work_dir, ignore_errors=True)

   def _keep_rate_limit(self, event):
      info = event.get("rate_limit_info")
      is_object = isinstance(info, dict)

      if is_object:
         self.last_rate_limit = info

   def _retry_failure(self, request, failure_class):
      is_auth = failure_class is SubscriptionAuthFailed

      if is_auth:
         warn_sign_in_failed_once()

         return SubscriptionAuthFailed(f"the Claude sign-in expired or was rejected on role {request.role}")

      return SubscriptionLimitReached(f"the Claude subscription usage limit stopped role {request.role}")

   def _to_result(self, request, completed, streamed=False):
      payload = result_event_of(completed.stdout) if streamed else self._payload_of(completed.stdout)

      return self._settle_payload(request, completed, payload)

   def _settle_payload(self, request, completed, payload):
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

      auth_texts = (payload.get("error"),) + candidate_texts
      sign_in_failed = any(is_auth_message(text) for text in auth_texts)

      if sign_in_failed:
         warn_sign_in_failed_once()
         raise SubscriptionAuthFailed(f"the Claude sign-in expired or was rejected on role {request.role}")

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
