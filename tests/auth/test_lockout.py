"""The per-user lockout of app/auth/service.py: four free failures, then a lock that doubles from
30 seconds to a 15 minute ceiling, stored on the users row so it survives the request that set it.
An attempt made while locked counts nothing and extends nothing (ruled 2026-09-27)."""
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session as OrmSession

from app.auth import passwords, service
from tests.api.conftest import NEW_PASSWORD, PASSWORD, USERNAME, world  # noqa: F401
from tests.auth.helpers import audit_rows, lockout_state, run_together, user_row

WRONG_PASSWORD = "not the right password"
FREE_FAILURES = service.LOCKOUT_FREE_FAILURES
LOCKING_FAILURE = FREE_FAILURES + 1
START = datetime(2026, 9, 27, 12, 0, 0, tzinfo=timezone.utc)


def claimed(world):  # noqa: F811
   signed_up = world.register(world.client())

   assert signed_up.status_code == 200

   return signed_up.json()


def login_at(world, password, moment):  # noqa: F811
   """The service call the route makes, committed the way app/api/deps.py get_db commits."""
   dummy_hash = world.app.state.dummy_hashes.for_settings(world.settings)

   with OrmSession(world.engine) as db:
      outcome = service.login(db, world.settings, USERNAME, password, dummy_hash, now=moment)
      db.commit()

   return outcome


def is_session(outcome):
   return isinstance(outcome, dict) and "token" in outcome


def seconds_locked(locked_until, moment):
   return (datetime.fromisoformat(locked_until) - moment).total_seconds()


def test_five_failures_through_the_route_lock_out_even_the_correct_password(world):  # noqa: F811
   """The count must survive each 401 and be read back by the next request, not held in memory."""
   claimed(world)
   client = world.client()
   client.cookies.clear()

   for attempt in range(1, LOCKING_FAILURE + 1):
      refused = world.login(client, password=WRONG_PASSWORD)

      assert refused.status_code == 401
      assert lockout_state(world.engine)[0] == attempt

   count, locked_until = lockout_state(world.engine)

   assert count == LOCKING_FAILURE
   assert locked_until is not None

   correct = world.login(client)

   assert correct.status_code == 401
   assert correct.json() == {"detail": service.LOGIN_REFUSED_DETAIL}


def test_the_lock_is_audited_once_with_only_the_count_and_the_deadline(world):  # noqa: F811
   """The count is committed inside the reservation, but the audit row is not, so a refusal that
   raised would have get_db roll the row back and the lock would go unrecorded."""
   user_id = claimed(world)["user"]["id"]
   client = world.client()

   for _ in range(LOCKING_FAILURE + 3):
      world.login(client, password=WRONG_PASSWORD)

   rows = audit_rows(world.engine, service.LOCKOUT_ACTION)

   assert len(rows) == 1
   assert rows[0].actor == user_id
   assert rows[0].subject == f"users:{user_id}"
   assert WRONG_PASSWORD not in rows[0].detail
   assert '"failed_login_count": 5' in rows[0].detail
   assert lockout_state(world.engine)[1] in rows[0].detail


def test_attempts_while_locked_change_neither_the_count_nor_the_deadline(world):  # noqa: F811
   claimed(world)
   client = world.client()

   for _ in range(LOCKING_FAILURE):
      world.login(client, password=WRONG_PASSWORD)

   locked = lockout_state(world.engine)

   for password in (WRONG_PASSWORD, PASSWORD, WRONG_PASSWORD, PASSWORD):
      assert world.login(client, password=password).status_code == 401

   assert lockout_state(world.engine) == locked


def test_the_lock_expires_on_schedule_and_success_then_clears_the_count(world):  # noqa: F811
   claimed(world)

   for attempt in range(LOCKING_FAILURE):
      assert not is_session(login_at(world, WRONG_PASSWORD, START + timedelta(seconds=attempt)))

   locked_at = START + timedelta(seconds=FREE_FAILURES)
   count, locked_until = lockout_state(world.engine)

   assert count == LOCKING_FAILURE
   assert seconds_locked(locked_until, locked_at) == service.LOCKOUT_BASE_SECONDS

   just_before = datetime.fromisoformat(locked_until) - timedelta(seconds=1)

   assert not is_session(login_at(world, PASSWORD, just_before))
   assert lockout_state(world.engine) == (count, locked_until)

   just_after = datetime.fromisoformat(locked_until) + timedelta(seconds=1)

   assert is_session(login_at(world, PASSWORD, just_after))
   assert lockout_state(world.engine) == (0, None)


def test_each_further_failure_doubles_the_lock_up_to_fifteen_minutes_and_never_beyond(world):  # noqa: F811
   claimed(world)
   moment = START
   durations = []

   for _ in range(LOCKING_FAILURE + 8):
      login_at(world, WRONG_PASSWORD, moment)
      count, locked_until = lockout_state(world.engine)
      is_locked = locked_until is not None

      if is_locked:
         durations.append(seconds_locked(locked_until, moment))
         moment = datetime.fromisoformat(locked_until) + timedelta(seconds=1)
      else:
         moment = moment + timedelta(seconds=1)

   assert durations[:6] == [30, 60, 120, 240, 480, 900]
   assert set(durations[6:]) == {service.LOCKOUT_MAX_SECONDS}
   assert lockout_state(world.engine)[0] == service.lockout_count_cap(world.settings)

   after_the_last_lock = moment

   assert is_session(login_at(world, PASSWORD, after_the_last_lock))


def test_parallel_wrong_guesses_get_no_more_real_checks_than_the_free_budget(world, monkeypatch):  # noqa: F811
   """Forty threads hold a request each at once. Reading the count, then writing it, would let
   all of them past the lock check before any wrote; the reservation UPDATE lets five through."""
   claimed(world)
   stored = user_row(world.engine).password_hash
   real_checks = []
   real_verify = passwords.verify_password

   def spy(password, stored_hash):
      is_real_check = stored_hash == stored

      if is_real_check:
         real_checks.append(password)

      return real_verify(password, stored_hash)

   monkeypatch.setattr(passwords, "verify_password", spy)
   calls = [
      (lambda: world.login(world.client(), password=WRONG_PASSWORD).status_code)
      for _ in range(40)
   ]

   statuses = run_together(calls)

   assert set(statuses) == {401}
   assert len(real_checks) == LOCKING_FAILURE
   assert lockout_state(world.engine)[0] == LOCKING_FAILURE
   assert len(audit_rows(world.engine, service.LOCKOUT_ACTION)) == 1


def test_a_wrong_reauth_password_counts_toward_the_same_lock(world):  # noqa: F811
   client = world.client()
   world.register(client)

   for attempt in range(1, LOCKING_FAILURE + 1):
      assert world.reauth(client, password=WRONG_PASSWORD).status_code == 401
      assert lockout_state(world.engine)[0] == attempt

   refused = world.reauth(client)

   assert refused.status_code == 401
   assert "reauth_token" not in refused.json()
   assert world.login(world.client()).status_code == 401


def test_a_correct_login_clears_earlier_failures(world):  # noqa: F811
   claimed(world)
   client = world.client()

   for _ in range(FREE_FAILURES):
      world.login(client, password=WRONG_PASSWORD)

   assert lockout_state(world.engine) == (FREE_FAILURES, None)
   assert world.login(client).status_code == 200
   assert lockout_state(world.engine) == (0, None)

   for _ in range(FREE_FAILURES):
      world.login(client, password=WRONG_PASSWORD)

   assert lockout_state(world.engine) == (FREE_FAILURES, None)


def test_a_recovery_reset_clears_the_lock(world):  # noqa: F811
   code = claimed(world)["recovery_code"]
   client = world.client()

   for _ in range(LOCKING_FAILURE):
      world.login(client, password=WRONG_PASSWORD)

   assert lockout_state(world.engine)[1] is not None
   assert world.recover(client, code, new_password=NEW_PASSWORD).status_code == 200
   assert lockout_state(world.engine) == (0, None)
   assert world.login(world.client(), password=NEW_PASSWORD).status_code == 200
