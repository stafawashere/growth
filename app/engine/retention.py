"""Per-skill retrievability at a moment in time, the R_k that scheduling and mastery condition 6 read.

R_k is derived on read, never stored (docs/plan/02, Mastery state schema). A skill with no memory
state has R_k = 1 (R1).
"""
from datetime import date, datetime

from app.engine import fsrs


def elapsed_days(last_practised_at, today):
   has_no_history = last_practised_at is None

   if has_no_history:
      return 0.0

   is_datetime = isinstance(last_practised_at, datetime)
   last_day = last_practised_at.date() if is_datetime else last_practised_at
   is_today_datetime = isinstance(today, datetime)
   today_day = today.date() if is_today_datetime else today

   return max((today_day - last_day).days, 0)


def retrievability_of_state(state, today):
   return fsrs.retrievability(
      state.stability,
      elapsed_days(state.last_practised_at, today),
      difficulty=state.difficulty,
   )


def current_retrievability(states, today):
   """Map every skill id to its R_k today; the map the selection functions consume."""
   return {skill_id: retrievability_of_state(state, today) for skill_id, state in states.items()}
