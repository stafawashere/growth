"""Invariant C0 of docs/calculator/architecture.md as a property: any sequence of calculator card
reads, drill serves, drill answers and measured reads leaves every learning table as it was, and
the only tables it writes are calculator_drills and audit_log.

auth_sessions is left out of the comparison because every signed-in request may renew its own
cookie session there (app/api/deps.py), which is the sign-in layer and not a calculator event.
Every other table holds a seeded row naming the student, so an unchanged table is a table that
had something to change.
"""
from hypothesis import HealthCheck, given, settings, strategies as st
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.calculator_drills import service
from app.db import models
from tests.api.conftest import world  # noqa: F401
from tests.export.test_export import all_tables, seeded_row

C0_TABLES = (
   "skills_state",
   "attempts",
   "sessions",
   "judgments",
   "diagnoses",
   "pending_probes",
   "gradings",
   "experiment_assignments",
   "assessment_parts",
   "assessment_responses",
)
CALCULATOR_WRITES = ("calculator_drills", "audit_log")
SIGN_IN_BOOKKEEPING = ("auth_sessions",)
NOT_SEEDED = ("users", "calculator_drills")
OTHER_USER_ID = "USR-other"
UNSUPPORTED_SETUP = ["NotAHead", 1]
PROPERTY = settings(
   max_examples=25,
   deadline=None,
   suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)

capabilities = st.sampled_from(["plot", "zero", "derivative", "integral", "intersection", "value", "mixed"])
serve_events = st.tuples(st.just("serve"), capabilities)
answer_events = st.tuples(
   st.just("answer"),
   st.sampled_from(["latest", "foreign", "unknown"]),
   st.sampled_from(["", "1.000", "not a number", "12.3", "-0.5"]),
   st.sampled_from([None, UNSUPPORTED_SETUP]),
   st.integers(min_value=0, max_value=10_000_000),
   st.booleans(),
)
read_events = st.tuples(st.sampled_from(["measured", "cards", "card"]))
event_sequences = st.lists(st.one_of(serve_events, answer_events, read_events), min_size=1, max_size=4)


def table_contents(engine):
   contents = {}

   with engine.connect() as connection:
      for table in all_tables():
         ordering = list(table.primary_key.columns)
         contents[table.name] = connection.execute(select(table).order_by(*ordering)).all()

   return contents


def prepared(world):
   """The student, the seeded rows and another user's drill, built once per world because the
   installation admits one sign-up."""
   ready = getattr(world, "calculator_ready", None)

   if ready is not None:
      return ready

   client = world.client()
   user_id = world.register(client).json()["user"]["id"]

   with world.engine.begin() as connection:
      for table in all_tables():
         if table.name in NOT_SEEDED:
            continue

         connection.execute(table.insert().values(**seeded_row("mine", user_id, table)))

   with OrmSession(world.engine) as db:
      foreign = service.serve(db, OTHER_USER_ID, "integral")
      db.commit()

   world.calculator_ready = {"client": client, "user_id": user_id, "foreign": foreign["drill_id"], "served": []}

   return world.calculator_ready


def run(event, ready):
   client = ready["client"]
   kind = event[0]

   if kind == "serve":
      response = client.post("/calculator/drills", json={"capability": event[1]})
      assert response.status_code == 200, response.text
      ready["served"].append(response.json()["drill_id"])
      return

   if kind == "answer":
      _, target, value, setup, elapsed_ms, desmos_open = event
      has_served = len(ready["served"]) > 0
      targets = {
         "latest": ready["served"][-1] if has_served else "cdr-none",
         "foreign": ready["foreign"],
         "unknown": "cdr-none",
      }
      body = {"value": value, "setup_mathjson": setup, "elapsed_ms": elapsed_ms, "desmos_open": desmos_open}
      response = client.post(f"/calculator/drills/{targets[target]}/answer", json=body)
      assert response.status_code in (200, 404, 409), response.text
      return

   paths = {"measured": "/calculator/measured", "cards": "/calculator/cards", "card": "/calculator/cards/CCD-zero-01"}
   assert client.get(paths[kind]).status_code == 200


@PROPERTY
@given(events=event_sequences)
def test_calculator_events_leave_every_learning_table_unchanged(world, events):
   ready = prepared(world)
   before = table_contents(world.engine)

   for event in events:
      run(event, ready)

   after = table_contents(world.engine)
   changed = {name for name in before if before[name] != after[name]}

   for name in C0_TABLES:
      assert len(before[name]) > 0, name
      assert after[name] == before[name], name

   assert changed <= set(CALCULATOR_WRITES + SIGN_IN_BOOKKEEPING)


def test_the_comparison_sees_a_write_to_a_learning_table(world):
   """The property's positive control: the same snapshot notices a skills_state change."""
   ready = prepared(world)
   before = table_contents(world.engine)

   with OrmSession(world.engine) as db:
      row = db.scalars(select(models.SkillState).where(models.SkillState.user_id == ready["user_id"])).first()
      row.beta = row.beta + 0.5
      db.commit()

   after = table_contents(world.engine)

   assert before["skills_state"] != after["skills_state"]
