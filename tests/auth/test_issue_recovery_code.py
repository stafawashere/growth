"""python -m app.auth.issue_recovery_code: the operator's way back in for a user whose recovery code
is missing or spent (ruled 2026-09-27)."""
from app.auth import issue_recovery_code
from tests.api.conftest import NEW_PASSWORD, world  # noqa: F401
from tests.auth.helpers import audit_rows


def database_path(world):  # noqa: F811
   return world.engine.url.database


def test_the_printed_code_is_accepted_by_a_reset_and_the_old_code_is_not(world, capsys):  # noqa: F811
   old_code = world.register(world.client()).json()["recovery_code"]

   exit_code = issue_recovery_code.main(["--db", database_path(world)])
   printed = capsys.readouterr().out.strip()

   assert exit_code == 0
   assert printed != old_code
   assert world.recover(world.client(), old_code).status_code == 401
   assert world.recover(world.client(), printed, new_password=NEW_PASSWORD).status_code == 200


def test_issuing_a_code_is_audited_as_the_operator_without_the_code(world, capsys):  # noqa: F811
   user_id = world.register(world.client()).json()["user"]["id"]

   issue_recovery_code.main(["--db", database_path(world)])
   printed = capsys.readouterr().out.strip()
   rows = audit_rows(world.engine, issue_recovery_code.ISSUE_AUDIT_ACTION)

   assert len(rows) == 1
   assert rows[0].actor == "operator"
   assert rows[0].subject == f"users:{user_id}"
   assert printed not in (rows[0].detail or "")


def test_an_installation_with_no_user_prints_no_code(world, capsys):  # noqa: F811
   exit_code = issue_recovery_code.main(["--db", database_path(world)])
   captured = capsys.readouterr()

   assert exit_code == 1
   assert captured.out == ""
   assert "no user" in captured.err


def test_a_missing_database_file_is_not_created(tmp_path, capsys):
   missing = tmp_path / "absent.db"

   exit_code = issue_recovery_code.main(["--db", str(missing)])

   assert exit_code == 1
   assert missing.exists() is False
