"""The four rules that keep the subscription backend inside the operator's own Claude login.

(a) The OAuth token never reaches api.anthropic.com from this code: AnthropicProvider refuses an
sk-ant-oat key before the wire, only app/providers/subscription.py names the token variable, and
that module imports no HTTP client or socket.
(b) Single user: the backend refuses to start over a database with more than one account, and
registration refuses a second account while the backend is subscription.
(c) The CLI's environment carries no ANTHROPIC_* variable.
(d) No tool can run: the argv disables every tool.
"""
import ast
from datetime import datetime, timezone
from pathlib import Path

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.main import build_application
from app.providers.anthropic import AnthropicProvider, SubscriptionTokenRefused
from app.providers.base import RefusedBeforeWire
from app.providers.guard import SubscriptionSpendLedger
from app.providers.subscription import (
   SubscriptionProvider,
   SubscriptionSingleUserError,
)
from tests.api.conftest import FakeVerifier
from tests.providers.test_subscription import FakeCli, option_value, tutor_request

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = REPO_ROOT / "app"
SUBSCRIPTION_MODULE = APP_DIR / "providers" / "subscription.py"
TOKEN_VARIABLE = "CLAUDE_CODE_" + "OAUTH_TOKEN"
FORBIDDEN_IMPORT_ROOTS = {"urllib", "http", "requests", "httpx", "socket", "anthropic", "aiohttp", "urllib3"}
REQUIRED_DISALLOWED_TOOLS = {"Bash", "Edit", "Write", "Read", "WebFetch", "WebSearch", "Glob", "Grep", "NotebookEdit"}
CREATED_AT = datetime(2026, 9, 23, tzinfo=timezone.utc).isoformat()


class RecordingTransport:
   def __init__(self):
      self.calls = []

   def __call__(self, url, headers, body):
      self.calls.append(url)

      return {}


@pytest.fixture
def cli(tmp_path):
   home = tmp_path / "home"
   home.mkdir()
   fake = FakeCli(home)
   fake.mode("success")

   return fake


@pytest.fixture
def ledger(tmp_path):
   return SubscriptionSpendLedger(path=tmp_path / "subscription_ledger.json")


@pytest.mark.parametrize("key", ["sk-ant-oat01-not-a-real-token", " sk-ant-oat01-not-a-real-token"])
def test_the_api_adapter_refuses_an_oauth_token_before_the_wire(key):
   transport = RecordingTransport()
   provider = AnthropicProvider(transport=transport, environ={"ANTHROPIC_API_KEY": key})

   with pytest.raises(SubscriptionTokenRefused) as raised:
      provider.generate(tutor_request())

   assert isinstance(raised.value, RefusedBeforeWire)
   assert transport.calls == []
   assert "sk-ant-oat01" not in str(raised.value)


def test_the_api_adapter_refuses_an_oauth_token_on_the_stream_path_too():
   transport = RecordingTransport()
   provider = AnthropicProvider(
      stream_transport=transport, environ={"ANTHROPIC_API_KEY": "sk-ant-oat01-not-a-real-token"}
   )

   with pytest.raises(SubscriptionTokenRefused):
      list(provider.stream(tutor_request()))

   assert transport.calls == []


def test_only_the_subscription_module_names_the_oauth_token_variable():
   naming_files = sorted(
      path.relative_to(REPO_ROOT).as_posix()
      for path in APP_DIR.rglob("*")
      if path.is_file() and path.suffix in {".py", ".ts", ".tsx", ".js", ".json", ".md", ".toml"}
      and "node_modules" not in path.parts and TOKEN_VARIABLE in path.read_text(errors="ignore")
   )

   assert naming_files == ["app/providers/subscription.py"]


def imported_roots(source):
   roots = set()

   for node in ast.walk(ast.parse(source)):
      if isinstance(node, ast.Import):
         roots.update(alias.name.split(".")[0] for alias in node.names)

      is_absolute_from_import = isinstance(node, ast.ImportFrom) and node.level == 0

      if is_absolute_from_import:
         roots.add(node.module.split(".")[0])

   return roots


def test_the_subscription_module_imports_no_http_client_socket_or_sdk():
   source = SUBSCRIPTION_MODULE.read_text()
   roots = imported_roots(source)

   assert "subprocess" in roots
   assert roots & FORBIDDEN_IMPORT_ROOTS == set()
   assert "__import__" not in source
   assert "importlib" not in source
   assert "app.providers.anthropic" not in source


def test_the_backend_refuses_to_construct_over_more_than_one_account(ledger):
   SubscriptionProvider(user_count=1, subscription_ledger=ledger)

   with pytest.raises(SubscriptionSingleUserError):
      SubscriptionProvider(user_count=2, subscription_ledger=ledger)


def add_user(db, user_id):
   db.add(models.User(id=user_id, display_name=None, created_at=CREATED_AT, updated_at=CREATED_AT))


def test_the_app_refuses_to_start_on_the_subscription_backend_with_two_accounts(tmp_path):
   db_path = tmp_path / "growth.db"
   engine = models.make_engine(db_path)

   with OrmSession(engine) as db:
      add_user(db, "USR-1")
      add_user(db, "USR-2")
      db.commit()

   engine.dispose()

   with pytest.raises(SubscriptionSingleUserError):
      build_application({"GROWTH_DB_PATH": str(db_path), "GROWTH_AI_BACKEND": "subscription"})

   api_backed = build_application(
      {"GROWTH_DB_PATH": str(db_path), "GROWTH_AI_BACKEND": "api", "ANTHROPIC_API_KEY": "test-key-not-real"}
   )

   assert isinstance(api_backed.state.settings.tutor, AnthropicProvider)


def test_registration_refuses_a_second_account_on_the_subscription_backend(tmp_path):
   from starlette.testclient import TestClient

   application = build_application(
      {"GROWTH_DB_PATH": str(tmp_path / "growth.db"), "GROWTH_AI_BACKEND": "subscription", "GROWTH_ITEMS_DIR": "none"}
   )
   application.state.settings.verifier = FakeVerifier()
   client = TestClient(application, client=("127.0.0.1", 40000), base_url="http://127.0.0.1")

   assert isinstance(application.state.settings.tutor, SubscriptionProvider)

   first_begin = client.post("/auth/passkey/register/begin", json={"display_name": "Operator"})
   first = client.post(
      "/auth/passkey/register/finish",
      json={"challenge_id": first_begin.json()["challenge_id"], "credential": {"sign_count": 1}},
   )

   assert first.status_code == 200

   second_client = TestClient(application, client=("127.0.0.1", 40001), base_url="http://127.0.0.1")
   second_begin = second_client.post("/auth/passkey/register/begin", json={"display_name": "Someone else"})

   assert second_begin.status_code == 403

   with OrmSession(application.state.engine) as db:
      assert db.query(models.User).count() == 1


def test_the_cli_environment_carries_no_anthropic_variable(cli, ledger):
   environ = cli.environ(
      ANTHROPIC_API_KEY="test-key-not-real",
      ANTHROPIC_AUTH_TOKEN="test-auth-not-real",
      ANTHROPIC_BASE_URL="http://127.0.0.1:9",
      ANTHROPIC_MODEL="claude-sonnet-5",
      UNRELATED_SECRET="not-for-the-cli",
      LANG="en_US.UTF-8",
      **{TOKEN_VARIABLE: "test-oauth-placeholder"},
   )
   SubscriptionProvider(environ=environ, subscription_ledger=ledger).generate(tutor_request())
   passed = cli.record()["env"]
   anthropic_names = [name for name in passed if name.startswith("ANTHROPIC")]

   assert anthropic_names == []
   assert "UNRELATED_SECRET" not in passed
   assert passed[TOKEN_VARIABLE] == "test-oauth-placeholder"
   assert passed["HOME"] == str(cli.home)
   assert passed["LANG"] == "en_US.UTF-8"
   assert "GROWTH_CLAUDE_BIN" not in passed


def test_without_the_token_the_cli_runs_on_its_own_keychain_login(cli, ledger):
   environ = cli.environ(ANTHROPIC_API_KEY="test-key-not-real")
   result = SubscriptionProvider(environ=environ, subscription_ledger=ledger).generate(tutor_request())
   passed = cli.record()["env"]
   interpreter_added = {"__CF_USER_TEXT_ENCODING", "LC_CTYPE", "PWD", "SHLVL", "_"}

   assert result.text is not None
   assert TOKEN_VARIABLE not in passed
   assert set(passed) - interpreter_added <= {"PATH", "HOME", "USER", "LANG", "TMPDIR"}


def test_the_argv_disables_every_tool(cli, ledger):
   SubscriptionProvider(environ=cli.environ(), subscription_ledger=ledger).generate(tutor_request())
   argv = cli.record()["argv"]
   disallowed = set(option_value(argv, "--disallowedTools").split(","))

   assert option_value(argv, "--tools") == ""
   assert REQUIRED_DISALLOWED_TOOLS <= disallowed
   assert option_value(argv, "--permission-prompts") == "none"
   assert "--dangerously-skip-permissions" not in argv
   assert "--allowedTools" not in argv

