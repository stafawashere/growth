"""Prints a fresh recovery code for the installation's one user.

   python -m app.auth.issue_recovery_code --db var/growth.db

The way back in for an account migrated from passkeys whose recovery code is missing or spent
(ruled 2026-09-27). It rests on docs/plan/09-security-and-privacy.md treating access to the
database file as total access: whoever can run this can already read or replace every row. The new
code replaces any earlier one, is printed once and stored only as a hash, and the issue is audited.
The code is then spent at POST /auth/recovery/reset to set a password.
"""
import argparse
import sys
from pathlib import Path

from sqlalchemy.orm import Session as OrmSession

from app.auth.recovery import issue_recovery_code
from app.auth.service import sole_user, utc_now, write_audit
from app.db.models import make_engine

ISSUE_AUDIT_ACTION = "recovery_code_issued"
OPERATOR_ACTOR = "operator"


def issue_for_sole_user(engine, now=None):
   """Returns the plaintext code, or None when the installation has no user."""
   moment = now or utc_now()

   with OrmSession(engine) as db:
      user = sole_user(db)
      is_unclaimed = user is None

      if is_unclaimed:
         return None

      code = issue_recovery_code(db, user, moment)
      write_audit(db, OPERATOR_ACTOR, ISSUE_AUDIT_ACTION, f"users:{user.id}", None, moment)
      db.commit()

   return code


def main(argv=None):
   parser = argparse.ArgumentParser(description="Print a fresh recovery code for the installation's user.")
   parser.add_argument("--db", required=True, help="path to the SQLite database file")
   arguments = parser.parse_args(argv)
   database_exists = Path(arguments.db).is_file()

   if not database_exists:
      print(f"no database at {arguments.db}", file=sys.stderr)

      return 1

   engine = make_engine(arguments.db)
   code = issue_for_sole_user(engine)
   is_unclaimed = code is None

   if is_unclaimed:
      print("this installation has no user", file=sys.stderr)

      return 1

   print(code)

   return 0


if __name__ == "__main__":
   sys.exit(main())
