"""docs/plan/09-security-and-privacy.md, "Audit log": the action comes from a controlled vocabulary.

The plan states the vocabulary in prose, which makes it controlled in the plan and uncontrolled in
the code, where any string reaches the column. app/audit/vocabulary.py is the enumeration and the
three audit writers refuse anything outside it.

The first test walks app/ and reads the action literal out of every write_audit call and every
AuditLog construction, so a new call site with an unlisted action fails here rather than raising at
runtime in whatever phase added it. A hand-copied list of the names would not catch that, because
the copy and the code drift apart without either one noticing.
"""
import ast
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.audit.vocabulary import AUDIT_ACTIONS, is_known_action
from app.auth.service import write_audit
from app.db import models

APP_ROOT = Path(__file__).resolve().parents[2] / "app"


def module_constants(tree):
   """Two call sites pass a module constant rather than a literal, so the scanner resolves them."""
   constants = {}

   for node in tree.body:
      if not isinstance(node, ast.Assign):
         continue

      is_single_name = len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
      is_string = isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)

      if is_single_name and is_string:
         constants[node.targets[0].id] = node.value.value

   return constants


def resolve(node, constants):
   is_literal = isinstance(node, ast.Constant) and isinstance(node.value, str)

   if is_literal:
      return node.value

   is_named_constant = isinstance(node, ast.Name) and node.id in constants

   if is_named_constant:
      return constants[node.id]

   return None


def action_argument(call, names, constants):
   for keyword in call.keywords:
      if keyword.arg == "action":
         return resolve(keyword.value, constants)

   is_write_audit = isinstance(call.func, ast.Name) and call.func.id in names
   is_attribute_call = isinstance(call.func, ast.Attribute) and call.func.attr in names
   names_the_writer = is_write_audit or is_attribute_call
   has_positional_action = len(call.args) >= 3

   if names_the_writer and has_positional_action:
      return resolve(call.args[2], constants)

   return None


def written_actions():
   writers = {"write_audit", "_write_audit_entry"}
   constructors = {"AuditLog"}
   found = {}

   for path in sorted(APP_ROOT.rglob("*.py")):
      tree = ast.parse(path.read_text())
      constants = module_constants(tree)

      for node in ast.walk(tree):
         if not isinstance(node, ast.Call):
            continue

         is_writer_call = (
            isinstance(node.func, ast.Name) and node.func.id in writers | constructors
         )
         is_qualified_call = (
            isinstance(node.func, ast.Attribute) and node.func.attr in writers | constructors
         )

         if not (is_writer_call or is_qualified_call):
            continue

         action = action_argument(node, writers, constants)

         if action is not None:
            found[action] = f"{path.relative_to(APP_ROOT.parent)}:{node.lineno}"

   return found


def test_every_action_the_application_writes_is_in_the_vocabulary():
   found = written_actions()

   assert found != {}

   unlisted = {action: where for action, where in found.items() if not is_known_action(action)}

   assert unlisted == {}


def test_the_scanner_sees_the_writers_it_is_meant_to_see():
   """A scanner that finds nothing would make the test above pass by accident."""
   found = written_actions()

   assert "passkey_registered" in found
   assert "purge" in found
   assert "coverage_gap_fail_closed" in found
   assert "budget_hard_stop" in found


def test_an_unknown_action_is_refused(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      with pytest.raises(ValueError):
         write_audit(db, "USER-0001", "not_a_recorded_action", "users:USER-0001", None)


def test_a_refused_action_leaves_nothing_staged(tmp_path):
   """No rollback here: a rollback would discard the row whether or not the writer added it,
   which is what made the first version of this test unable to fail."""
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      try:
         write_audit(db, "USER-0001", "not_a_recorded_action", "users:USER-0001", None)
      except ValueError:
         pass

      staged = [row for row in db.new if isinstance(row, models.AuditLog)]

      assert staged == []
      assert db.scalars(select(models.AuditLog)).all() == []


def test_a_known_action_is_accepted():
   assert is_known_action("purge")
   assert not is_known_action("purge_everything")


def test_the_vocabulary_is_sorted_and_unique():
   assert list(AUDIT_ACTIONS) == sorted(set(AUDIT_ACTIONS))
