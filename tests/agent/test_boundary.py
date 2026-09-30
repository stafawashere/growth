"""Memory never reaches grading, diagnosis, selection or the engine (docs/agent/architecture.md,
"Boundaries that hold everywhere" and "The memory store").

The import graph is read with ast rather than by importing, so a module that is never imported by a
test still counts. Outside app/agent and the agent's own route module, no module may import the
memory or conversation modules or name one of the four agent models; the engine, grading, the
session builder, diagnosis and feedback are listed separately so a later allowance for some other
path cannot quietly cover them. In the other direction, the memory and conversation modules import
nothing from the engine, grading, diagnosis or session packages.

The second test runs the session service over one fixed attempt sequence twice, once with
tutor_memories rows naming the very skills the attempts touch and once with the table empty, and
requires identical skills_state rows.
"""
import ast
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.auth.service import as_iso
from app.db import models
from app.engine.state import Confidence
from app.session import repository
from tests.engine.conftest_selection import ACCOUNT_CREATED_AT, build_bank, build_graph, build_states, load_fixture
from tests.session.test_service import NOW, SNAPSHOT_ID, USER_ID, World, engine_graph_from

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = REPO_ROOT / "app"
GUARDED_MODULES = ("app.agent.memory", "app.agent.conversations")
AGENT_MODEL_NAMES = ("AgentConversation", "AgentTurn", "TutorMemory", "TutorProfile")
ALLOWED_PATHS = ("app/agent/", "app/api/routes/agent.py", "app/db/models.py")
NEVER_IMPORTING_PATHS = ("app/engine/", "app/grading/", "app/session/build.py", "app/diagnosis/", "app/feedback/")
LAYERS_THE_STORE_MUST_NOT_IMPORT = ("app.engine", "app.grading", "app.diagnosis", "app.session")
ATTEMPT_SEQUENCE = (True, False, True, True, False, True, True, False)


def relative(path):
   return path.relative_to(REPO_ROOT).as_posix()


def imported_modules(tree):
   imported = set()

   for node in ast.walk(tree):
      if isinstance(node, ast.Import):
         imported.update(alias.name for alias in node.names)

      is_absolute_from = isinstance(node, ast.ImportFrom) and node.module is not None and node.level == 0

      if is_absolute_from:
         imported.add(node.module)
         imported.update(f"{node.module}.{alias.name}" for alias in node.names)

   return imported


def named_attributes(tree):
   names = set()

   for node in ast.walk(tree):
      if isinstance(node, ast.Attribute):
         names.add(node.attr)

      if isinstance(node, ast.Name):
         names.add(node.id)

   return names


def app_modules():
   for path in sorted(APP_ROOT.rglob("*.py")):
      yield relative(path), ast.parse(path.read_text())


def test_nothing_outside_the_agent_imports_the_memory_or_conversation_store():
   importers = []
   model_users = []

   for path, tree in app_modules():
      is_allowed = any(path.startswith(prefix) for prefix in ALLOWED_PATHS)
      imports_the_store = bool(imported_modules(tree) & set(GUARDED_MODULES))
      names_an_agent_model = bool(named_attributes(tree) & set(AGENT_MODEL_NAMES))
      is_never_importing = any(path.startswith(prefix) for prefix in NEVER_IMPORTING_PATHS)

      if imports_the_store and (is_never_importing or not is_allowed):
         importers.append(path)

      if names_an_agent_model and not is_allowed:
         model_users.append(path)

   assert importers == []
   assert model_users == []


def test_the_store_imports_nothing_from_the_engine_grading_diagnosis_or_session():
   reaching = {}

   for module_name in GUARDED_MODULES:
      path = REPO_ROOT / (module_name.replace(".", "/") + ".py")
      imported = imported_modules(ast.parse(path.read_text()))
      crossing = sorted(
         name for name in imported
         if any(name == layer or name.startswith(f"{layer}.") for layer in LAYERS_THE_STORE_MUST_NOT_IMPORT)
      )

      if crossing:
         reaching[module_name] = crossing

   assert reaching == {}


def memory_rows_for(skill_ids):
   stamp = as_iso(NOW)
   kinds = ("preference", "confusion", "stated_difficulty", "episode")

   return [
      models.TutorMemory(
         id=f"MEM-boundary-{index}",
         user_id=USER_ID,
         kind=kind,
         text="Likes a sketch of the graph first",
         skill_ids=list(skill_ids),
         source="conversation",
         evidence_count=3,
         last_confirmed_at=stamp,
         created_at=stamp,
         updated_at=stamp,
      )
      for index, kind in enumerate(kinds)
   ]


def skills_state_after_the_sequence(database_path, with_memory):
   fixture = load_fixture()
   engine = models.make_engine(database_path)
   archetypes = {record["id"]: record for record in fixture["archetypes"]}
   every_skill_id = sorted({skill_id for record in fixture["archetypes"] for skill_id in record["skills"]})

   with OrmSession(engine) as db:
      repository.save_states(db, USER_ID, build_states(fixture), SNAPSHOT_ID, ACCOUNT_CREATED_AT)

      if with_memory:
         db.add_all(memory_rows_for(every_skill_id))

      db.commit()

      world = World(db, fixture, build_graph(fixture), engine_graph_from(fixture), archetypes, build_bank(fixture))
      opened = world.open(seed=11)

      for is_correct in ATTEMPT_SEQUENCE:
         world.attempt(opened, {"correct": is_correct}, confidence=Confidence.UNSURE)

      db.commit()
      rows = db.execute(
         select(models.SkillState.__table__).order_by(models.SkillState.user_id, models.SkillState.skill_id)
      ).mappings().all()
      memory_count = len(db.scalars(select(models.TutorMemory.id)).all())

   return [dict(row) for row in rows], memory_count


def test_memory_rows_leave_skills_state_identical(tmp_path):
   with_memory, stored_memories = skills_state_after_the_sequence(tmp_path / "with.db", with_memory=True)
   without_memory, no_memories = skills_state_after_the_sequence(tmp_path / "without.db", with_memory=False)
   practised = [row for row in with_memory if row["observation_count"] > 0]

   assert stored_memories == 4
   assert no_memories == 0
   assert len(practised) > 0
   assert with_memory == without_memory
