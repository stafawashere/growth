"""The per-role model choice, docs/plan/14-token-economy.md "Per role model choice".

Operator's instruction of 2026-09-23: the AI engine uses Anthropic Claude models only. This table
is the single place the application reads a role's model from; tools/cost_model.py
CLAUDE_ONLY_ROLE_MODELS prices the same choice, and tests/providers/test_model_routing.py asserts
the two agree role by role, so the two cannot drift apart silently.

P1 wires only the tutor (app/feedback/tutor.py TUTOR_MODEL), so this table is ahead of the code
for every other role today. That is deliberate: the table is what a role reads from when it is
built, not a record of what is already wired.
"""
from app.providers.guard import ROLES

ROLE_MODELS = {
   "tutor": "claude-sonnet-5",
   "grader": "claude-sonnet-5",
   "transcriber": "claude-sonnet-5",
   "diagnostician": "claude-sonnet-5",
   "generator": "claude-opus-5-5",
   "verifier": "claude-haiku-4-5",
}


def model_for(role):
   return ROLE_MODELS[role]


assert set(ROLE_MODELS) == set(ROLES), "ROLE_MODELS must name every role in app.providers.guard.ROLES"
