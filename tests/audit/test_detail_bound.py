"""docs/plan/13-ai-engineering.md item 9, "Where app/providers/guard.py is wrong" (about
line 365): write_audit has no mechanical bound on the detail field, and inspection of each
call site is exactly the control that stops holding at the next one. app/audit/detail.py's
bind_audit_detail is the mechanical bound; this file checks that it does what 13 asks and
that every AuditLog constructor site in app/ is wired to it, found by scanning rather than
by a hand-kept list of call sites.
"""
import ast
import json
import re
from pathlib import Path

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.audit import detail as detail_module
from app.audit.detail import bind_audit_detail
from app.auth.service import write_audit
from app.content import reconcile
from app.db import models
from app.session import purge

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = REPO_ROOT / "app"
PROVIDER_PLAN = REPO_ROOT / "docs" / "plan" / "07-ai-provider-layer.md"
SECURITY_PLAN = REPO_ROOT / "docs" / "plan" / "09-security-and-privacy.md"
ENV_VAR_NAME_PATTERN = re.compile(r"\b[A-Z][A-Z0-9_]*_API_KEY\b")

KEY_SHAPED_DETAILS = (
   {"ANTHROPIC_API_KEY": "sk-does-not-matter"},
   {"headers": {"x-api-key": "sk-does-not-matter"}},
   {"CLAUDEBOX_API_KEY": "token"},
   {"OLLAMA_API_KEY": "token"},
   {"provider": {"api_key": "token"}},
)

NOT_JSON_PLAIN_DETAILS = (
   {"tags": {1, 2, 3}},
   {"handler": lambda: None},
   {"raw": b"bytes"},
)


def test_a_plain_detail_passes_through_unchanged():
   detail = {"kind": "item_audit", "verdict": "clean", "count": 3, "ok": True, "note": None}

   assert bind_audit_detail(detail) == detail


@pytest.mark.parametrize("detail", KEY_SHAPED_DETAILS)
def test_a_key_shaped_field_is_refused(detail):
   with pytest.raises(ValueError) as excinfo:
      bind_audit_detail(detail)

   message = str(excinfo.value)

   assert "sk-does-not-matter" not in message
   assert "token" not in message


@pytest.mark.parametrize("detail", NOT_JSON_PLAIN_DETAILS)
def test_a_non_json_plain_value_is_refused(detail):
   with pytest.raises(ValueError):
      bind_audit_detail(detail)


def test_a_key_shaped_field_nested_in_a_list_is_refused():
   detail = {"providers": [{"kind": "anthropic"}, {"ANTHROPIC_API_KEY": "sk-nope"}]}

   with pytest.raises(ValueError) as excinfo:
      bind_audit_detail(detail)

   assert "sk-nope" not in str(excinfo.value)


def test_write_audit_refuses_a_key_shaped_detail(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      with pytest.raises(ValueError):
         write_audit(
            db,
            "USER-0001",
            "provider_key_set",
            "provider_configs:PRV-0001",
            {"ANTHROPIC_API_KEY": "sk-nope"},
         )


def test_write_audit_refuses_leave_nothing_staged(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      try:
         write_audit(
            db,
            "USER-0001",
            "provider_key_set",
            "provider_configs:PRV-0001",
            {"ANTHROPIC_API_KEY": "sk-nope"},
         )
      except ValueError:
         pass

      db.flush()

      assert db.query(models.AuditLog).count() == 0


def test_write_audit_still_records_a_plain_detail(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      row = write_audit(
         db,
         "USER-0001",
         "provider_key_set",
         "provider_configs:PRV-0001",
         {"provider": "anthropic"},
      )
      db.commit()

      stored = db.get(models.AuditLog, row.id)

      assert json.loads(stored.detail) == {"provider": "anthropic"}


SECRET_NAMED_FIELDS = (
   {"token": "opaque"},
   {"session_token": "opaque"},
   {"secret": "opaque"},
   {"key": "opaque"},
   {"provider_key": "opaque"},
   {"passphrase": "opaque"},
   {"bearer": "opaque"},
   {"claudeAiOauth": {"accessToken": "opaque"}},
)

FIELDS_THAT_ARE_NOT_SECRETS = (
   {"role": "tutor", "before": {"cap_usd": 1.0, "cap_tokens": None}, "after": {"cap_usd": 2.0, "cap_tokens": 5}},
   {"provider": "anthropic", "model": "claude-opus-5", "role": "tutor", "cap": "tokens"},
   {"old_id": "SKL-0101", "new_id": "SKL-0102"},
)


@pytest.mark.parametrize("detail", SECRET_NAMED_FIELDS)
def test_a_field_named_for_a_secret_is_refused(detail):
   with pytest.raises(ValueError) as excinfo:
      bind_audit_detail(detail)

   assert "opaque" not in str(excinfo.value)


@pytest.mark.parametrize("detail", FIELDS_THAT_ARE_NOT_SECRETS)
def test_the_fields_current_writers_use_still_pass(detail):
   assert bind_audit_detail(detail) == detail


def provider_key_env_var_names_in_code_and_plan():
   sources = [path.read_text() for path in sorted(APP_ROOT.rglob("*.py"))]
   sources.append(PROVIDER_PLAN.read_text())
   sources.append(SECURITY_PLAN.read_text())

   return {name for source in sources for name in ENV_VAR_NAME_PATTERN.findall(source)}


def test_every_provider_key_env_var_named_in_code_or_plan_is_watched():
   named = provider_key_env_var_names_in_code_and_plan()

   assert "ANTHROPIC_API_KEY" in named
   assert named <= set(detail_module.PROVIDER_KEY_ENV_VARS)


@pytest.mark.parametrize("env_var", ["ANTHROPIC_API_KEY", "CLAUDEBOX_API_KEY", "OLLAMA_API_KEY"])
def test_a_value_carrying_a_configured_provider_key_is_refused(monkeypatch, env_var):
   configured_key = "configured-provider-key-value-7d1f"
   monkeypatch.setenv(env_var, configured_key)
   detail = {"note": f"call failed with {configured_key} attached"}

   with pytest.raises(ValueError) as excinfo:
      bind_audit_detail(detail)

   assert configured_key not in str(excinfo.value)


def test_a_key_configured_after_import_still_binds(monkeypatch):
   monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
   late_key = "late-configured-key-9a2c"
   detail = {"items": ["fine", {"note": late_key}]}

   assert bind_audit_detail(detail) == detail

   monkeypatch.setenv("ANTHROPIC_API_KEY", late_key)

   with pytest.raises(ValueError):
      bind_audit_detail(detail)


def test_an_empty_env_var_does_not_refuse_every_string(monkeypatch):
   monkeypatch.setenv("ANTHROPIC_API_KEY", "")

   assert bind_audit_detail({"note": "plain"}) == {"note": "plain"}


def test_a_configured_key_inside_a_field_name_is_refused(monkeypatch):
   configured_key = "configured-provider-key-value-3e8b"
   monkeypatch.setenv("CLAUDEBOX_API_KEY", configured_key)

   with pytest.raises(ValueError) as excinfo:
      bind_audit_detail({f"note-{configured_key}": 1})

   assert configured_key not in str(excinfo.value)


def credential_header_names_the_adapters_send():
   """Header names in any dict literal returned by an adapter method named _headers whose
   value is computed at call time, which is how the key reaches the header; a literal or a
   module constant such as ANTHROPIC_VERSION is not credential material."""
   names = set()

   for path in sorted((APP_ROOT / "providers").rglob("*.py")):
      tree = ast.parse(path.read_text())
      module_constants = {
         target.id
         for statement in tree.body
         if isinstance(statement, ast.Assign)
         for target in statement.targets
         if isinstance(target, ast.Name)
      }

      for function in ast.walk(tree):
         is_headers_builder = isinstance(function, ast.FunctionDef) and function.name == "_headers"

         if not is_headers_builder:
            continue

         for node in ast.walk(function):
            returns_a_dict = isinstance(node, ast.Return) and isinstance(node.value, ast.Dict)

            if not returns_a_dict:
               continue

            for key_node, value_node in zip(node.value.keys, node.value.values):
               is_named_header = isinstance(key_node, ast.Constant) and isinstance(key_node.value, str)
               is_literal = isinstance(value_node, ast.Constant)
               is_module_constant = isinstance(value_node, ast.Name) and value_node.id in module_constants
               carries_runtime_value = not is_literal and not is_module_constant

               if is_named_header and carries_runtime_value:
                  names.add(key_node.value.lower())

   return names


def test_every_credential_header_an_adapter_sends_is_a_refused_value_form():
   sent = credential_header_names_the_adapters_send()

   assert "x-api-key" in sent
   assert sent <= set(detail_module.CREDENTIAL_VALUE_FORMS)


@pytest.mark.parametrize(
   "detail",
   (
      {"note": "x-api-key: whatever-was-sent"},
      {"note": "X-Api-Key whatever-was-sent"},
      {"authorization": "Bearer whatever-was-sent"},
      {"lines": ["ok", "bearer whatever-was-sent"]},
   ),
)
def test_a_value_carrying_a_credential_form_is_refused(detail):
   with pytest.raises(ValueError) as excinfo:
      bind_audit_detail(detail)

   assert "whatever-was-sent" not in str(excinfo.value)


def _is_named_call(node, name):
   if not isinstance(node, ast.Call):
      return False

   func = node.func
   names_it_directly = isinstance(func, ast.Name) and func.id == name
   names_it_as_attribute = isinstance(func, ast.Attribute) and func.attr == name

   return names_it_directly or names_it_as_attribute


def _is_json_dumps_call(node):
   if not isinstance(node, ast.Call):
      return False

   func = node.func
   is_json_attribute = (
      isinstance(func, ast.Attribute)
      and func.attr == "dumps"
      and isinstance(func.value, ast.Name)
      and func.value.id == "json"
   )

   return is_json_attribute


def _is_bound_value(node, scope):
   """A name counts as bound only when every store to it in the scope is a plain assignment
   from bind_audit_detail, so a tuple unpack, a loop target or a later reassignment spoils it."""
   if _is_named_call(node, "bind_audit_detail"):
      return True

   if not isinstance(node, ast.Name):
      return False

   store_count = 0
   bound_store_count = 0

   for candidate in ast.walk(scope):
      is_store_of_name = (
         isinstance(candidate, ast.Name)
         and candidate.id == node.id
         and isinstance(candidate.ctx, ast.Store)
      )

      if is_store_of_name:
         store_count += 1

      if not isinstance(candidate, ast.Assign):
         continue

      assigns_from_bound = _is_named_call(candidate.value, "bind_audit_detail")
      targets_name_directly = any(
         isinstance(target, ast.Name) and target.id == node.id for target in candidate.targets
      )

      if assigns_from_bound and targets_name_directly:
         bound_store_count += 1

   has_store = store_count > 0
   every_store_is_bound = store_count == bound_store_count

   return has_store and every_store_is_bound


def _detail_expression_is_bound(node, scope):
   is_none = isinstance(node, ast.Constant) and node.value is None

   if is_none:
      return True

   if isinstance(node, ast.IfExp):
      body_is_bound = _detail_expression_is_bound(node.body, scope)
      orelse_is_bound = _detail_expression_is_bound(node.orelse, scope)

      return body_is_bound and orelse_is_bound

   is_single_argument_dumps = _is_json_dumps_call(node) and len(node.args) == 1

   if not is_single_argument_dumps:
      return False

   return _is_bound_value(node.args[0], scope)


def _action_is_checked_before(action_node, scope, constructor):
   """True when scope holds `if not is_known_action(<same expression>): raise` ahead of the
   constructor, the pattern write_audit uses."""
   action_shape = ast.dump(action_node)

   for node in ast.walk(scope):
      if not isinstance(node, ast.If):
         continue

      test = node.test
      is_negated_check = (
         isinstance(test, ast.UnaryOp)
         and isinstance(test.op, ast.Not)
         and _is_named_call(test.operand, "is_known_action")
         and len(test.operand.args) == 1
      )

      if not is_negated_check:
         continue

      checks_the_same_action = ast.dump(test.operand.args[0]) == action_shape
      raises_on_unknown = any(isinstance(statement, ast.Raise) for statement in node.body)
      comes_first = node.lineno < constructor.lineno

      if checks_the_same_action and raises_on_unknown and comes_first:
         return True

   return False


def _imports_vocabulary_check(tree):
   for node in ast.walk(tree):
      is_vocabulary_import = isinstance(node, ast.ImportFrom) and node.module == "app.audit.vocabulary"

      if is_vocabulary_import and any(alias.name == "is_known_action" for alias in node.names):
         return True

   return False


def _enclosing_scopes(tree):
   parent_of = {}

   for parent in ast.walk(tree):
      for child in ast.iter_child_nodes(parent):
         parent_of[child] = parent

   def enclosing(node):
      current = parent_of.get(node)

      while current is not None:
         if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return current

         current = parent_of.get(current)

      return tree

   return enclosing


def audit_log_constructor_sites_in(source, label):
   """Each AuditLog construction in source, judged on its own: its detail keyword must be None,
   json.dumps of a bind_audit_detail call, or json.dumps of a name every assignment in the same
   function takes from bind_audit_detail; its action keyword must be checked by
   `if not is_known_action(...): raise` earlier in the same function."""
   tree = ast.parse(source)
   enclosing = _enclosing_scopes(tree)
   module_imports_check = _imports_vocabulary_check(tree)
   sites = []

   for node in ast.walk(tree):
      if not _is_named_call(node, "AuditLog"):
         continue

      scope = enclosing(node)
      keywords = {keyword.arg: keyword.value for keyword in node.keywords}
      has_splat = None in keywords
      detail_node = keywords.get("detail")
      action_node = keywords.get("action")

      detail_is_bound = detail_node is None or _detail_expression_is_bound(detail_node, scope)
      action_is_checked = (
         action_node is not None
         and module_imports_check
         and _action_is_checked_before(action_node, scope, node)
      )

      sites.append(
         {
            "location": f"{label}:{node.lineno}",
            "detail_bound": detail_is_bound and not has_splat,
            "action_checked": action_is_checked and not has_splat,
         }
      )

   return sites


def audit_log_constructor_sites():
   sites = []

   for path in sorted(APP_ROOT.rglob("*.py")):
      label = str(path.relative_to(REPO_ROOT))
      sites.extend(audit_log_constructor_sites_in(path.read_text(), label))

   return sites


def test_the_scanner_finds_the_known_constructor_sites():
   """A scanner that finds nothing would make the assertions below pass by accident."""
   locations = {site["location"] for site in audit_log_constructor_sites()}

   assert any("app/auth/service.py" in location for location in locations)
   assert any("app/content/reconcile.py" in location for location in locations)
   assert any("app/session/purge.py" in location for location in locations)
   assert any("app/review/audit.py" in location for location in locations)


def test_the_scanner_judges_each_constructor_on_its_own():
   """Positive control: a module that binds one detail does not vouch for a second
   constructor beside it, and an unchecked action is caught even where another is checked."""
   source = """
import json
from app.audit.detail import bind_audit_detail
from app.audit.vocabulary import is_known_action

def bound(detail, action):
   if not is_known_action(action):
      raise ValueError(action)

   bound_detail = bind_audit_detail(detail)
   return AuditLog(action=action, detail=json.dumps(bound_detail) if bound_detail is not None else None)

def unbound(detail, action):
   return AuditLog(action=action, detail=json.dumps(detail))

def reassigned(detail, action):
   if not is_known_action(action):
      raise ValueError(action)

   bound_detail = bind_audit_detail(detail)
   bound_detail = detail
   return AuditLog(action=action, detail=json.dumps(bound_detail))
"""
   verdicts = [
      (site["detail_bound"], site["action_checked"])
      for site in audit_log_constructor_sites_in(source, "sample")
   ]

   assert verdicts == [(True, True), (False, False), (False, True)]


def test_every_constructor_site_binds_its_detail():
   unbound = [site["location"] for site in audit_log_constructor_sites() if not site["detail_bound"]]

   assert unbound == []


def test_every_constructor_site_checks_its_action_against_the_vocabulary():
   unchecked = [site["location"] for site in audit_log_constructor_sites() if not site["action_checked"]]

   assert unchecked == []
