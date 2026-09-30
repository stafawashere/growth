"""What the calculator drills measured, per capability (docs/calculator/architecture.md, Pacing and
progress integration). A sibling of app/progress/pace.py that reads calculator_drills alone;
nothing here reaches pace_verdict, the learning metrics, the mastery map or fluent.
"""
import statistics

from sqlalchemy import select

from app.calculator.registry import CAPABILITIES
from app.calculator_drills.service import budget_seconds, rebuilt_task
from app.db import models
from app.progress.learning_metrics import value

MEDIAN_FLOOR = 3
RECENT_LIMIT = 20
ANSWERED_DRILLS = "answered drills"
SETUPS_SHOWN = "answered drills with a setup shown"


def as_bool(flag):
   return None if flag is None else bool(flag)


def capability_measure(capability, rows):
   answered = [row for row in rows if row.submitted_at is not None]
   answered_count = len(answered)
   value_correct = sum(1 for row in answered if row.value_correct == 1)
   shown = [row for row in answered if row.setup_shown == 1]
   setup_correct = sum(1 for row in shown if row.setup_correct == 1)
   has_enough_for_a_median = answered_count >= MEDIAN_FLOOR
   median_ms = round(statistics.median(row.elapsed_ms for row in answered)) if has_enough_for_a_median else None

   return {
      "capability": capability,
      "served": len(rows),
      "answered": answered_count,
      "value_correct": value("results accurate to three places", value_correct, answered_count, ANSWERED_DRILLS),
      "setup_shown": value("setup shown", len(shown), answered_count, ANSWERED_DRILLS),
      "setup_correct": value("setup equivalent to the key", setup_correct, len(shown), SETUPS_SHOWN),
      "median_ms": median_ms,
   }


def recent_entry(row):
   """function_tex is not stored, so the task is rebuilt from its draw, as the answer does."""
   return {
      "drill_id": row.id,
      "capability": row.capability,
      "function_tex": rebuilt_task(row).function_tex,
      "value_correct": row.value_correct == 1,
      "setup_correct": as_bool(row.setup_correct),
      "setup_shown": row.setup_shown == 1,
      "elapsed_ms": row.elapsed_ms,
      "submitted_at": row.submitted_at,
   }


def measured(db, user_id):
   rows = db.scalars(select(models.CalculatorDrill).where(models.CalculatorDrill.user_id == user_id)).all()
   by_capability = {capability: [] for capability in CAPABILITIES}

   for row in rows:
      by_capability.setdefault(row.capability, []).append(row)

   answered = [row for row in rows if row.submitted_at is not None]
   newest_first = sorted(answered, key=lambda row: (row.submitted_at, row.id), reverse=True)[:RECENT_LIMIT]

   return {
      "capabilities": [capability_measure(capability, by_capability[capability]) for capability in CAPABILITIES],
      "budget_seconds": budget_seconds(),
      "recent": [recent_entry(row) for row in newest_first],
   }
