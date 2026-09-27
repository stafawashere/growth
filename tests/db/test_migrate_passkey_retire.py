"""The one step in app/db/migrate.py that is not additive: a database made while passkeys were the
sign-in drops passkey_credentials, after a named backup, and signs every session out in the same
transaction. The user row is kept with no password, which is the must-reset state (ruled
2026-09-27)."""
import hashlib
import logging
import sqlite3

from sqlalchemy import inspect
from sqlalchemy.orm import Session as OrmSession
from starlette.testclient import TestClient

from app.api.app import Settings, create_app
from app.auth.cookies import SESSION_COOKIE
from app.db import migrate, models
from app.db.backup import BACKUP_DIRECTORY_NAME, RETIRE_BACKUP_PREFIX

USER_ID = "USER-0001"
CREATED_AT = "2026-03-01T09:00:00+00:00"
FAR_FUTURE = "2099-01-01T00:00:00+00:00"
PASSWORD_COLUMNS = ("username", "password_hash", "failed_login_count", "locked_until")
NEW_PASSWORD = "a brand new passphrase"
SESSION_TOKEN = "session-token-from-before"


def token_hash_of(token):
   return hashlib.sha256(token.encode()).hexdigest()


def write_passkey_era_database(path, recovery_code_hash=None):
   """The current schema with the password columns taken off users and the passkey table put
   back, holding one user, one credential and one live session."""
   models.make_engine(path).dispose()
   connection = sqlite3.connect(path)

   for column_name in PASSWORD_COLUMNS:
      connection.execute(f'ALTER TABLE "users" DROP COLUMN "{column_name}"')

   connection.execute(
      "CREATE TABLE passkey_credentials (id TEXT PRIMARY KEY, user_id TEXT NOT NULL, "
      "credential_id BLOB NOT NULL UNIQUE, public_key BLOB NOT NULL, sign_count INTEGER NOT NULL, "
      "transports TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)"
   )
   connection.execute(
      "INSERT INTO users (id, display_name, exam_date, purge_after, recovery_code_hash, created_at, "
      "updated_at) VALUES (?, 'student', '2027-05-10', '2027-06-09', ?, ?, ?)",
      (USER_ID, recovery_code_hash, CREATED_AT, CREATED_AT),
   )
   connection.execute(
      "INSERT INTO passkey_credentials VALUES ('PKC-1', ?, x'01', x'02', 3, NULL, ?, ?)",
      (USER_ID, CREATED_AT, CREATED_AT),
   )
   connection.execute(
      "INSERT INTO auth_sessions (id, user_id, token_hash, expires_at, created_at, updated_at) "
      "VALUES ('AUS-1', ?, ?, ?, ?, ?)",
      (USER_ID, token_hash_of(SESSION_TOKEN), FAR_FUTURE, CREATED_AT, CREATED_AT),
   )
   connection.commit()
   connection.close()


def retire_backups(path):
   directory = path.parent / BACKUP_DIRECTORY_NAME

   if not directory.exists():
      return []

   return sorted(directory.glob(f"{RETIRE_BACKUP_PREFIX}*"))


def application_over(engine):
   settings = Settings(
      engine=engine,
      allowed_hosts=("127.0.0.1", "::1", "localhost", "testserver"),
      password_scrypt_n=2 ** 10,
      password_scrypt_r=8,
      password_scrypt_p=1,
      auth_rate_limit_count=100_000,
   )

   return create_app(settings)


def client_for(application, host="127.0.0.1"):
   return TestClient(application, client=(host, 40000), base_url="http://127.0.0.1")


def insert_session(engine, token):
   with OrmSession(engine) as db:
      db.add(
         models.AuthSession(
            id="AUS-AFTER",
            user_id=USER_ID,
            token_hash=token_hash_of(token),
            expires_at=FAR_FUTURE,
            created_at=CREATED_AT,
            updated_at=CREATED_AT,
         )
      )
      db.commit()


def test_reopening_drops_the_passkey_table_and_every_session_and_keeps_the_user(tmp_path):
   path = tmp_path / "growth.db"
   write_passkey_era_database(path)

   engine = models.make_engine(path)
   table_names = set(inspect(engine).get_table_names())
   user_columns = {column["name"] for column in inspect(engine).get_columns("users")}

   assert "passkey_credentials" not in table_names
   assert set(PASSWORD_COLUMNS) <= user_columns

   with OrmSession(engine) as db:
      user = db.get(models.User, USER_ID)

      assert user is not None
      assert user.password_hash is None
      assert user.username is None
      assert user.failed_login_count == 0
      assert db.query(models.AuthSession).count() == 0


def test_a_named_backup_holding_the_passkey_table_is_written_first(tmp_path):
   path = tmp_path / "growth.db"
   write_passkey_era_database(path)

   models.make_engine(path)
   backups = retire_backups(path)

   assert len(backups) == 1
   assert "passkey_credentials" in backups[0].name

   with sqlite3.connect(backups[0]) as copied:
      credentials = copied.execute("SELECT count(*) FROM passkey_credentials").fetchone()[0]
      sessions = copied.execute("SELECT count(*) FROM auth_sessions").fetchone()[0]

   assert credentials == 1
   assert sessions == 1


def test_a_user_with_no_way_back_in_is_named_with_the_operator_command(tmp_path, caplog):
   path = tmp_path / "growth.db"
   write_passkey_era_database(path, recovery_code_hash=None)

   with caplog.at_level(logging.WARNING, logger=migrate.logger.name):
      models.make_engine(path)

   stranded = [record.getMessage() for record in caplog.records if USER_ID in record.getMessage()]

   assert len(stranded) == 1
   assert "issue_recovery_code" in stranded[0]


def test_a_user_holding_a_recovery_code_is_not_named_as_stranded(tmp_path, caplog):
   path = tmp_path / "growth.db"
   write_passkey_era_database(path, recovery_code_hash="pbkdf2_sha256$1$00$00")

   with caplog.at_level(logging.WARNING, logger=migrate.logger.name):
      models.make_engine(path)

   messages = [record.getMessage() for record in caplog.records]

   assert any("dropped passkey_credentials" in message for message in messages)
   assert [message for message in messages if USER_ID in message] == []


def test_a_second_open_retires_nothing_and_opens_no_write_transaction(tmp_path):
   path = tmp_path / "growth.db"
   write_passkey_era_database(path)
   models.make_engine(path).dispose()
   engine = models.make_engine(path)
   opened = []
   original_begin = engine.begin

   def counting_begin(*arguments, **keywords):
      opened.append(True)

      return original_begin(*arguments, **keywords)

   engine.begin = counting_begin

   assert migrate.retire_tables(engine) == ()
   assert opened == []
   assert len(retire_backups(path)) == 1


def test_a_migrated_user_cannot_log_in_until_a_recovery_reset(tmp_path):
   from app.auth.issue_recovery_code import issue_for_sole_user

   path = tmp_path / "growth.db"
   write_passkey_era_database(path)
   engine = models.make_engine(path)
   code = issue_for_sole_user(engine)
   application = application_over(engine)
   client = client_for(application)

   for guess in ("student", "migrated_student"):
      refused = client.post("/auth/login", json={"username": guess, "password": NEW_PASSWORD})

      assert refused.status_code == 401

   without_name = client.post("/auth/recovery/reset", json={"recovery_code": code, "new_password": NEW_PASSWORD})

   assert without_name.status_code == 400

   reset = client.post(
      "/auth/recovery/reset",
      json={"recovery_code": code, "new_password": NEW_PASSWORD, "username": "Migrated_Student"},
   )

   assert reset.status_code == 200

   logged_in = client_for(application).post(
      "/auth/login", json={"username": "migrated_student", "password": NEW_PASSWORD}
   )

   assert logged_in.status_code == 200


def test_a_session_for_a_user_with_no_password_is_refused(tmp_path):
   """The retire step already deleted every session; this is the second line, for a session row
   that reaches the table some other way."""
   path = tmp_path / "growth.db"
   write_passkey_era_database(path)
   engine = models.make_engine(path)
   insert_session(engine, SESSION_TOKEN)
   client = client_for(application_over(engine))
   client.cookies.set(SESSION_COOKIE, SESSION_TOKEN)

   assert client.get("/me").status_code == 401
   assert client.post("/auth/reauth", json={"password": NEW_PASSWORD}).status_code == 401


def test_status_tells_only_a_loopback_caller_that_a_password_is_needed(tmp_path):
   path = tmp_path / "growth.db"
   write_passkey_era_database(path)
   application = application_over(models.make_engine(path))

   loopback = client_for(application).get("/auth/status")
   remote = client_for(application, host="203.0.113.7").get("/auth/status")

   assert loopback.json() == {"user_exists": True, "needs_password": True}
   assert remote.json() == {"user_exists": True}
