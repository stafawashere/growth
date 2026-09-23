"""POST /export and GET /export/{id}: docs/plan/09-security-and-privacy.md, "Default purge 30 days
after the exam date, with an export first".

09 asks for a complete archive of everything in its data inventory table. The expectations here
come from that table, not from the exporter: every table in the SQLAlchemy metadata is seeded with a
row that names the student and a row that names a second user, and the assertions are on those
seeded rows by id and by value.

Every table in the metadata has to be accounted for. A table 09's inventory names is exported. items
is not, because 09 calls generated items "not personal data". content_snapshots, item_verifications,
review_queue and jobs are not in the inventory and name no student. A table 09 does not name at all
(one added after this was written) must be exported when its seeded row names the student through
user_id, session_id or attempt_id, and otherwise fails the accounting test until someone decides.

audit_log names no user column. 09 puts it in the inventory and gives its actor as "user
identifier, worker, or system"; in a single-student deployment an entry by the worker, the system
or the operator is part of that student's record, and an entry whose actor is another user is not.

The secret rule is 09's Audit log exclusion (any key or any part of one, the passphrase, a raw
provider response body), 06's provider_configs storage rule, and the auth layer's hashed tokens and
recovery code.
"""
import base64
import json
import stat
from pathlib import Path

import pytest
from sqlalchemy import JSON, Column, Table, Text, create_engine, select
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy.pool import StaticPool

from app.db import models
from app.export import archive as export_archive
from tests.api.conftest import world  # noqa: F401

STUDENT_TAG = "mine"
OTHER_TAG = "theirs"
OTHER_USER_ID = "USR-other"
NON_USER_ACTOR = "worker"
INVENTORY_TABLES = {
   "users",
   "passkey_credentials",
   "auth_sessions",
   "provider_configs",
   "skills_state",
   "judgments",
   "pending_probes",
   "attempts",
   "gradings",
   "diagnoses",
   "sessions",
   "budgets",
   "audit_log",
}
NOT_PERSONAL_TABLES = {"items"}
SHARED_TABLES_OUTSIDE_THE_INVENTORY = {"content_snapshots", "item_verifications", "review_queue", "jobs"}
STUDENT_LINK_COLUMNS = ("user_id", "session_id", "attempt_id")
SECRETS_NAMED_BY_09_AND_THE_AUTH_LAYER = {
   ("provider_configs", "key_ciphertext"),
   ("provider_configs", "key_nonce"),
   ("users", "recovery_code_hash"),
   ("auth_sessions", "token_hash"),
   ("auth_sessions", "reauth_token_hash"),
}
KEY_NAMED_PLAINTEXT_COLUMNS = (
   "api_key",
   "apikey",
   "provider_key",
   "session_token",
   "passphrase",
   "password",
   "raw_response_body",
)
AUDIT_ACTORS_IN_THE_STUDENTS_RECORD = ("student", NON_USER_ACTOR, "system", "operator")
USERS_TABLE = models.User.__table__
AUDIT_TABLE = models.AuditLog.__table__
ARCHIVE_FILE_MODE = 0o600
ARCHIVE_DIRECTORY_MODE = 0o700


def all_tables():
   return models.Base.metadata.sorted_tables


def secret_sentinel(tag, table_name, column_name):
   return f"SECRET-{tag}-{table_name}-{column_name}"


def filler_value(tag, table, column):
   is_secret = (table.name, column.name) in SECRETS_NAMED_BY_09_AND_THE_AUTH_LAYER
   text = secret_sentinel(tag, table.name, column.name) if is_secret else f"{tag}-{table.name}-{column.name}"

   if isinstance(column.type, JSON):
      return [text]

   python_type = column.type.python_type

   if python_type is bytes:
      return text.encode()

   if python_type is int:
      return 1

   if python_type is float:
      return 0.25

   return text


def seeded_row(tag, user_id, table):
   row = {}

   for column in table.columns:
      is_users_key = table is USERS_TABLE and column.name == "id"
      is_owner_column = column.name in ("user_id", "actor")

      if is_users_key or is_owner_column:
         row[column.name] = user_id
      elif column.name == "session_id":
         row[column.name] = f"{tag}-sessions"
      elif column.name == "attempt_id":
         row[column.name] = f"{tag}-attempts"
      elif column.name == "id":
         row[column.name] = f"{tag}-{table.name}"
      else:
         row[column.name] = filler_value(tag, table, column)

   return row


def seed_every_table(engine, tag, user_id, skip_users=False):
   with engine.begin() as connection:
      for table in all_tables():
         is_skipped = skip_users and table is USERS_TABLE

         if is_skipped:
            continue

         connection.execute(table.insert().values(**seeded_row(tag, user_id, table)))


def seed_non_user_audit_row(engine):
   row = seeded_row("system", NON_USER_ACTOR, AUDIT_TABLE)

   with engine.begin() as connection:
      connection.execute(AUDIT_TABLE.insert().values(**row))


def audit_row_id(label):
   return f"AUD-{label}"


def seed_audit_actors(engine, user_id):
   actor_for_label = {
      "student": user_id,
      NON_USER_ACTOR: NON_USER_ACTOR,
      "system": "system",
      "operator": "operator",
      "other": OTHER_USER_ID,
   }

   with engine.begin() as connection:
      for label, actor in actor_for_label.items():
         row = seeded_row(label, actor, AUDIT_TABLE)
         row["id"] = audit_row_id(label)
         connection.execute(AUDIT_TABLE.insert().values(**row))


def names_the_student(table):
   column_names = {column.name for column in table.columns}

   return any(name in column_names for name in STUDENT_LINK_COLUMNS)


def expected_exported_tables():
   expected = set()

   for table in all_tables():
      is_in_inventory = table.name in INVENTORY_TABLES
      is_named_by_09 = table.name in NOT_PERSONAL_TABLES | SHARED_TABLES_OUTSIDE_THE_INVENTORY | INVENTORY_TABLES
      is_later_student_table = not is_named_by_09 and names_the_student(table)

      if is_in_inventory or is_later_student_table:
         expected.add(table.name)

   return expected


def primary_key_of(table, row):
   return tuple(row[column.name] for column in table.primary_key.columns)


def as_exported(value):
   if isinstance(value, bytes):
      return base64.b64encode(value).decode()

   return value


def expected_export_row(table, seeded):
   return {
      name: as_exported(value)
      for name, value in seeded.items()
      if (table.name, name) not in SECRETS_NAMED_BY_09_AND_THE_AUTH_LAYER
   }


def registered_student(world):
   client = world.client()
   registered = world.register(client)

   assert registered.status_code == 200

   return client, registered.json()["user"]["id"]


def fresh_reauth_token(world, client):
   finished = world.reauth(client)

   assert finished.status_code == 200

   return finished.json()["reauth_token"]


def produce(world, client):
   token = fresh_reauth_token(world, client)
   produced = client.post("/export", json={"reauth_token": token})

   assert produced.status_code == 200, produced.text

   return produced.json()


def fetch_archive(client, export_id):
   fetched = client.get(f"/export/{export_id}")

   assert fetched.status_code == 200

   return fetched


def export_jobs(engine):
   with OrmSession(engine) as db:
      return db.scalars(select(models.Job).where(models.Job.type == "export")).all()


def export_audit_rows(engine):
   with OrmSession(engine) as db:
      return db.scalars(
         select(models.AuditLog).where(models.AuditLog.action == "export_produced")
      ).all()


def archives_on_disk(engine):
   database_directory = Path(engine.url.database).resolve().parent

   return sorted(path.name for path in database_directory.rglob("*.json"))


def test_every_table_in_the_schema_is_accounted_for_by_09():
   named_by_09 = INVENTORY_TABLES | NOT_PERSONAL_TABLES | SHARED_TABLES_OUTSIDE_THE_INVENTORY
   unaccounted = []

   for table in all_tables():
      is_named = table.name in named_by_09
      is_linked = names_the_student(table)
      is_unaccounted = not is_named and not is_linked

      if is_unaccounted:
         unaccounted.append(table.name)

   assert unaccounted == []


def test_export_requires_a_fresh_reauthentication_and_burns_a_wrong_one(world):
   client, user_id = registered_student(world)

   missing = client.post("/export", json={})

   assert missing.status_code == 401

   token = fresh_reauth_token(world, client)
   wrong = client.post("/export", json={"reauth_token": "not-the-token"})

   assert wrong.status_code == 401

   replayed = client.post("/export", json={"reauth_token": token})

   assert replayed.status_code == 401
   assert export_jobs(world.engine) == []
   assert export_audit_rows(world.engine) == []

   anonymous = world.client().post("/export", json={"reauth_token": token})

   assert anonymous.status_code == 401


def test_export_holds_the_students_seeded_rows_and_no_other_users(world):
   client, user_id = registered_student(world)
   seed_every_table(world.engine, STUDENT_TAG, user_id, skip_users=True)
   seed_every_table(world.engine, OTHER_TAG, OTHER_USER_ID)

   produced = produce(world, client)
   fetched = fetch_archive(client, produced["id"])

   assert fetched.headers["content-type"].startswith("application/json")

   archive = fetched.json()
   exported_tables = archive["tables"]

   assert archive["user"]["id"] == user_id
   assert set(exported_tables) == expected_exported_tables()
   assert NOT_PERSONAL_TABLES.isdisjoint(exported_tables)
   assert SHARED_TABLES_OUTSIDE_THE_INVENTORY.isdisjoint(exported_tables)

   for table in all_tables():
      is_exported = table.name in exported_tables

      if not is_exported:
         continue

      exported_by_key = {primary_key_of(table, row): row for row in exported_tables[table.name]}
      other_row = seeded_row(OTHER_TAG, OTHER_USER_ID, table)

      assert primary_key_of(table, other_row) not in exported_by_key, table.name

      is_users = table is USERS_TABLE

      if is_users:
         assert list(exported_by_key) == [(user_id,)]
         continue

      student_row = seeded_row(STUDENT_TAG, user_id, table)
      student_key = primary_key_of(table, student_row)

      assert student_key in exported_by_key, table.name
      assert exported_by_key[student_key] == expected_export_row(table, student_row), table.name


def test_export_carries_the_students_audit_record_and_not_another_users(world):
   client, user_id = registered_student(world)
   seed_audit_actors(world.engine, user_id)

   produced = produce(world, client)
   exported_ids = {row["id"] for row in fetch_archive(client, produced["id"]).json()["tables"]["audit_log"]}

   for label in AUDIT_ACTORS_IN_THE_STUDENTS_RECORD:
      assert audit_row_id(label) in exported_ids, label

   assert audit_row_id("other") not in exported_ids


def test_export_reaches_a_later_table_keyed_by_attempt_id(world):
   later_gradings = Table(
      "export_later_gradings",
      models.Base.metadata,
      Column("id", Text, primary_key=True),
      Column("attempt_id", Text, nullable=False),
   )

   try:
      later_gradings.create(world.engine)
      client, user_id = registered_student(world)
      seed_every_table(world.engine, STUDENT_TAG, user_id, skip_users=True)
      seed_every_table(world.engine, OTHER_TAG, OTHER_USER_ID)

      with world.engine.begin() as connection:
         connection.execute(later_gradings.delete())
         connection.execute(later_gradings.insert().values(id="GRD-mine", attempt_id=f"{STUDENT_TAG}-attempts"))
         connection.execute(later_gradings.insert().values(id="GRD-theirs", attempt_id=f"{OTHER_TAG}-attempts"))
         connection.execute(later_gradings.insert().values(id="GRD-orphan", attempt_id="ATT-nobody"))

      produced = produce(world, client)
      exported_tables = fetch_archive(client, produced["id"]).json()["tables"]
   finally:
      models.Base.metadata.remove(later_gradings)

   assert [row["id"] for row in exported_tables["export_later_gradings"]] == ["GRD-mine"]


def test_export_carries_no_secret_column_or_value(world):
   later_secrets = Table(
      "export_later_secrets",
      models.Base.metadata,
      Column("id", Text, primary_key=True),
      Column("user_id", Text, nullable=False),
      Column("note", Text, nullable=True),
      *[Column(name, Text, nullable=True) for name in KEY_NAMED_PLAINTEXT_COLUMNS],
   )

   try:
      later_secrets.create(world.engine)
      client, user_id = registered_student(world)
      seed_every_table(world.engine, STUDENT_TAG, user_id, skip_users=True)

      with world.engine.begin() as connection:
         connection.execute(later_secrets.delete())
         plaintext = {name: f"PLAINTEXT-{name}" for name in KEY_NAMED_PLAINTEXT_COLUMNS}
         connection.execute(
            later_secrets.insert().values(id="SEC-mine", user_id=user_id, note="kept", **plaintext)
         )
         connection.execute(
            USERS_TABLE.update()
            .where(USERS_TABLE.c.id == user_id)
            .values(recovery_code_hash=secret_sentinel(STUDENT_TAG, "users", "recovery_code_hash"))
         )

      produced = produce(world, client)
      fetched = fetch_archive(client, produced["id"])
   finally:
      models.Base.metadata.remove(later_secrets)

   raw = fetched.text
   exported_tables = fetched.json()["tables"]

   for table_name, column_name in SECRETS_NAMED_BY_09_AND_THE_AUTH_LAYER:
      rows = exported_tables[table_name]
      sentinel = secret_sentinel(STUDENT_TAG, table_name, column_name)
      sentinel_base64 = base64.b64encode(sentinel.encode()).decode()

      assert len(rows) > 0, table_name
      assert all(column_name not in row for row in rows), (table_name, column_name)
      assert sentinel not in raw, (table_name, column_name)
      assert sentinel_base64 not in raw, (table_name, column_name)

   assert exported_tables["export_later_secrets"] == [{"id": "SEC-mine", "user_id": user_id, "note": "kept"}]

   for name in KEY_NAMED_PLAINTEXT_COLUMNS:
      assert f"PLAINTEXT-{name}" not in raw, name


def test_export_writes_a_done_job_an_audit_entry_and_an_owner_only_file(world):
   client, user_id = registered_student(world)
   produced = produce(world, client)
   jobs = export_jobs(world.engine)
   audit_rows = export_audit_rows(world.engine)

   assert [job.id for job in jobs] == [produced["id"]]
   assert jobs[0].state == produced["status"] == "done"
   assert jobs[0].created_at == produced["created_at"]
   assert json.loads(jobs[0].payload)["user_id"] == user_id
   assert [(row.actor, row.subject) for row in audit_rows] == [(user_id, f"jobs:{produced['id']}")]

   database_directory = Path(world.engine.url.database).resolve().parent
   archive_name = json.loads(jobs[0].payload)["archive"]
   stored = [path for path in database_directory.rglob("*.json") if path.name == archive_name]
   fetched = fetch_archive(client, produced["id"])

   assert len(stored) == 1
   assert stored[0].read_bytes() == fetched.content
   assert stat.S_IMODE(stored[0].stat().st_mode) == ARCHIVE_FILE_MODE
   assert stat.S_IMODE(stored[0].parent.stat().st_mode) == ARCHIVE_DIRECTORY_MODE


def test_a_second_export_replaces_the_first(world):
   client, user_id = registered_student(world)
   first = produce(world, client)
   first_archive = json.loads(export_jobs(world.engine)[0].payload)["archive"]
   second = produce(world, client)
   second_archive = json.loads(export_jobs(world.engine)[0].payload)["archive"]

   assert [job.id for job in export_jobs(world.engine)] == [second["id"]]
   assert archives_on_disk(world.engine) == [second_archive]
   assert first_archive != second_archive
   assert client.get(f"/export/{first['id']}").status_code == 404
   assert client.get(f"/export/{second['id']}").status_code == 200
   assert len(export_audit_rows(world.engine)) == 2


def refuse_archive_write(path, text):
   raise OSError("disk full")


def refuse_commit(self):
   raise RuntimeError("database is locked")


@pytest.mark.parametrize("failure_point", ["archive_write", "commit"])
def test_a_failed_export_leaves_the_previous_one_whole(world, monkeypatch, failure_point):
   client, user_id = registered_student(world)
   first = produce(world, client)
   first_bytes = fetch_archive(client, first["id"]).content
   first_archives = archives_on_disk(world.engine)
   token = fresh_reauth_token(world, client)

   if failure_point == "archive_write":
      monkeypatch.setattr(export_archive, "write_archive_file", refuse_archive_write)
   else:
      monkeypatch.setattr(OrmSession, "commit", refuse_commit)

   with pytest.raises((OSError, RuntimeError)):
      client.post("/export", json={"reauth_token": token})

   monkeypatch.undo()

   assert [job.id for job in export_jobs(world.engine)] == [first["id"]]
   assert archives_on_disk(world.engine) == first_archives
   assert fetch_archive(client, first["id"]).content == first_bytes


def test_export_answers_503_without_spending_the_token_on_an_in_memory_database(world):
   memory_engine = create_engine(
      "sqlite://",
      poolclass=StaticPool,
      connect_args={"check_same_thread": False},
   )
   models.Base.metadata.create_all(memory_engine)
   world.app.state.engine = memory_engine
   world.settings.engine = memory_engine
   client, user_id = registered_student(world)
   token = fresh_reauth_token(world, client)

   refused = client.post("/export", json={"reauth_token": token})
   fetched = client.get("/export/JOB-any")

   with OrmSession(memory_engine) as db:
      auth_session = db.scalars(
         select(models.AuthSession).where(models.AuthSession.user_id == user_id)
      ).one()
      export_job_count = len(db.scalars(select(models.Job)).all())

   assert refused.status_code == 503
   assert fetched.status_code == 503
   assert auth_session.reauth_token_hash is not None
   assert export_job_count == 0


def test_get_export_is_scoped_to_its_owner(world):
   from app.auth.service import utc_now

   client, user_id = registered_student(world)
   seed_every_table(world.engine, OTHER_TAG, OTHER_USER_ID)

   with OrmSession(world.engine) as db:
      directory = export_archive.archive_directory_for(world.engine)
      other_job = export_archive.produce_export(db, directory, OTHER_USER_ID, utc_now())
      other_id = other_job.id
      db.commit()

   assert [job.id for job in export_jobs(world.engine)] == [other_id]
   assert client.get(f"/export/{other_id}").status_code == 404
   assert client.get("/export/JOB-unknown").status_code == 404
   assert client.get(f"/export/{OTHER_TAG}-jobs").status_code == 404
   assert world.client().get(f"/export/{other_id}").status_code == 401