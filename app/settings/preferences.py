"""The queue settings behind GET and PUT /settings: the exam date, the purge date and desired retention.

docs/plan/06-architecture.md stores exam_date and purge_after on users and defaults purge_after to
exam_date plus 30 days. docs/plan/09-security-and-privacy.md makes the purge date editable and
says an extension is an explicit act rather than a default, so a changed exam date does not move
the purge date; only a request that names purge_after does. Desired retention is read from the
engine and is never written here. 08's queue settings also name a daily minute target, which has
no column in 06 and so is not served.

The if-then plan of 01's "Implementation intention and queue-bound streak" is kept on users as one
line of the student's own words, read and written through /settings/study-plan so the queue
settings payload stays as it was. An empty plan clears it.
"""
from datetime import date

from app.engine import constants

EDITABLE_DATES = ("exam_date", "purge_after")


class SettingsRefused(ValueError):
   pass


def settings_view(user, today):
   return {
      "exam_date": user.exam_date,
      "purge_after": user.purge_after,
      "desired_retention": constants.desired_retention(today),
   }


def validated_iso_date(name, value):
   is_text = isinstance(value, str)

   if not is_text:
      raise SettingsRefused(f"{name} must be an ISO date such as 2027-05-10")

   try:
      parsed = date.fromisoformat(value)
   except ValueError as unreadable:
      raise SettingsRefused(f"{name} must be an ISO date such as 2027-05-10") from unreadable

   is_canonical = parsed.isoformat() == value

   if not is_canonical:
      raise SettingsRefused(f"{name} must be an ISO date such as 2027-05-10")

   return value


def validated_dates(fields):
   unknown = sorted(set(fields) - set(EDITABLE_DATES))

   if unknown:
      raise SettingsRefused(f"only {', '.join(EDITABLE_DATES)} can be changed here, not {', '.join(unknown)}")

   named = {name: fields[name] for name in EDITABLE_DATES if name in fields}

   if not named:
      raise SettingsRefused(f"name at least one of {', '.join(EDITABLE_DATES)}")

   return {name: validated_iso_date(name, value) for name, value in named.items()}


def update_dates(db, user, fields, timestamp):
   for name, value in validated_dates(fields).items():
      setattr(user, name, value)

   user.updated_at = timestamp
   db.flush()
   db.refresh(user)

   return user


STUDY_PLAN_LIMIT = 280


def study_plan_view(user):
   return {"study_plan": user.study_plan}


def validated_study_plan(value):
   is_text = isinstance(value, str)

   if not is_text:
      raise SettingsRefused("study_plan must be text")

   plan = value.strip()
   is_too_long = len(plan) > STUDY_PLAN_LIMIT

   if is_too_long:
      raise SettingsRefused(f"an if-then plan is at most {STUDY_PLAN_LIMIT} characters")

   return plan if plan != "" else None


def update_study_plan(db, user, value, timestamp):
   user.study_plan = validated_study_plan(value)
   user.updated_at = timestamp
   db.flush()

   return user
