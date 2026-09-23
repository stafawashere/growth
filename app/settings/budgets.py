"""Per-role caps and today's usage, and the cap change behind PUT /settings/budgets.

docs/plan/07-ai-provider-layer.md, "Budget caps": each role has a daily cap in tokens and in
dollars, stored in budgets with one row per user per role per day, and settings shows today's
usage against the cap per role. A change is written onto today's row for the role, which is
created when the role has none yet, and app/providers/guard.py's caps_in_force carries it into
later days, so the screen and the guard read the cap from the same place. The budget_cap_changed
entry 09 requires is the record of the change and the flag that the stored caps, not the startup
ones, are in force for the role; its values are never read back as the cap.

A change names one unit or both. A unit the request does not name keeps the value in force,
because 07 gives every role a cap in both units and a change to one is not a request to drop the
other. A unit named as null is cleared, and a change that would leave no cap in either unit is
refused, because the guard refuses a role with no cap. NaN and Infinity are refused too: the JSON
parser behind the route accepts both, an infinite cap is no cap under another name, and NaN would
be stored as none and written into the audit detail as a token JSON does not allow.

A change clears hard_stopped and stopped_by on today's row only when it is a raise above the day's
spend (13, "A cap that is raised after a stop"), decided by app/providers/guard.py's
apply_cap_change so the route and the guard agree. A lowered cap keeps the stop even when it still
sits above the spend, because 07's hard-stop table says no further calls today.
"""
import math

from app.auth.service import as_iso, write_audit
from app.db import models
from app.providers.guard import (
   CAP_CHANGED_ACTION,
   ROLES,
   BudgetCaps,
   apply_cap_change,
   caps_in_force,
   create_budget_row,
   find_budget_row,
)

CAP_UNITS = ("cap_usd", "cap_tokens")
USAGE_FIELDS = ("cost_usd", "tokens_in", "tokens_out", "tokens_cached_read", "tokens_cached_write")


class CapRefused(ValueError):
   pass


def caps_as_dict(caps):
   has_caps = caps is not None

   if not has_caps:
      return {"cap_usd": None, "cap_tokens": None}

   return {"cap_usd": caps.cap_usd, "cap_tokens": caps.cap_tokens}


def validated_cap(name, value):
   if value is None:
      return None

   is_number = isinstance(value, (int, float)) and not isinstance(value, bool)

   if not is_number:
      raise CapRefused(f"{name} must be a number or null")

   is_finite = math.isfinite(value)

   if not is_finite:
      raise CapRefused(f"{name} must be a finite number")

   is_negative = value < 0

   if is_negative:
      raise CapRefused(f"{name} must not be negative")

   return float(value)


def requested_units(role, fields):
   """The units the request names, validated. Nothing here reads the database."""
   is_known_role = role in ROLES

   if not is_known_role:
      raise CapRefused(f"role must be one of {', '.join(ROLES)}")

   named = {unit: validated_cap(unit, fields[unit]) for unit in CAP_UNITS if unit in fields}

   if not named:
      raise CapRefused("name cap_usd, cap_tokens or both")

   return named


def merged_caps(current, named):
   merged = dict(caps_as_dict(current), **named)
   leaves_no_cap = merged["cap_usd"] is None and merged["cap_tokens"] is None

   if leaves_no_cap:
      raise CapRefused("a role needs a cap in dollars, in tokens or in both")

   return BudgetCaps(cap_tokens=merged["cap_tokens"], cap_usd=merged["cap_usd"])


def change_cap(db, user_id, role, fields, configured, now):
   named = requested_units(role, fields)
   day = now.date().isoformat()
   before = caps_in_force(db, user_id, role, day, configured)
   after = merged_caps(before, named)
   timestamp = as_iso(now)
   row = find_budget_row(db, user_id, role, day)

   if row is None:
      row = create_budget_row(db, user_id, role, day, after, timestamp)

   apply_cap_change(row, after)
   row.updated_at = timestamp
   db.flush()

   write_audit(
      db,
      user_id,
      CAP_CHANGED_ACTION,
      f"budgets:{row.id}",
      {"role": role, "before": caps_as_dict(before), "after": caps_as_dict(after)},
      now=now,
   )

   return row


def role_view(db, user_id, role, day, configured):
   caps = caps_as_dict(caps_in_force(db, user_id, role, day, configured))
   row = find_budget_row(db, user_id, role, day)
   has_row = row is not None
   usage = {field: getattr(row, field) if has_row else 0 for field in USAGE_FIELDS}
   hard_stopped = has_row and row.hard_stopped == 1

   return {"role": role, **caps, **usage, "hard_stopped": hard_stopped}


def month_to_date_usd(db, user_id, day):
   month_prefix = day[:len("YYYY-MM")]
   rows = db.query(models.Budget).filter(
      models.Budget.user_id == user_id,
      models.Budget.day.startswith(month_prefix),
      models.Budget.day <= day,
   )

   return sum(row.cost_usd for row in rows)


def budgets_view(db, user_id, configured, now):
   day = now.date().isoformat()

   return {
      "day": day,
      "roles": [role_view(db, user_id, role, day, configured) for role in ROLES],
      "month_to_date_usd": month_to_date_usd(db, user_id, day),
   }