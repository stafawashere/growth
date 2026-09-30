"""Subscription pacing for the live tutor agent's two roles, docs/agent/architecture.md "Roles,
models, caps and the chain": agent at 80 calls a day and 6 a minute, memory at 10 and 2. A role
missing from the default tables would fall to the generic 20 a day and 4 a minute, which would
cut a day of agent conversation to a quarter, and a variable the reader skips would leave the
operator unable to move either number.
"""
from app.providers.guard import pacing_caps_from_environment


def test_the_agent_roles_carry_their_own_pacing_defaults():
   pacing = pacing_caps_from_environment({})

   assert (pacing.daily_cap_for("agent"), pacing.minute_cap_for("agent")) == (80, 6)
   assert (pacing.daily_cap_for("memory"), pacing.minute_cap_for("memory")) == (10, 2)


def test_the_four_agent_pacing_variables_override_the_defaults():
   pacing = pacing_caps_from_environment(
      {
         "GROWTH_SUBSCRIPTION_AGENT_CALLS_PER_DAY": "40",
         "GROWTH_SUBSCRIPTION_MEMORY_CALLS_PER_DAY": "3",
         "GROWTH_SUBSCRIPTION_AGENT_CALLS_PER_MINUTE": "9",
         "GROWTH_SUBSCRIPTION_MEMORY_CALLS_PER_MINUTE": "1",
      }
   )

   assert (pacing.daily_cap_for("agent"), pacing.minute_cap_for("agent")) == (40, 9)
   assert (pacing.daily_cap_for("memory"), pacing.minute_cap_for("memory")) == (3, 1)


def test_the_existing_roles_keep_their_pacing():
   pacing = pacing_caps_from_environment({})

   assert (pacing.daily_cap_for("tutor"), pacing.minute_cap_for("tutor")) == (60, 4)
   assert (pacing.daily_cap_for("grader"), pacing.minute_cap_for("grader")) == (120, 12)
