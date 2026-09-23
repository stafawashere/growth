"""app/providers/model_routing.py ROLE_MODELS and tools/cost_model.py CLAUDE_ONLY_ROLE_MODELS
price the same operator decision, docs/plan/14-token-economy.md "Per role model choice", in two
places for two different readers. If one is edited and the other is not, the app would serve a
model the cost model never priced, silently. This is the test that catches that.
"""
from app.providers.guard import ROLES
from app.providers.model_routing import ROLE_MODELS
from tools.cost_model import CLAUDE_ONLY_ROLE_MODELS


def test_every_role_names_a_model():
   assert set(ROLE_MODELS) == set(ROLES)


def test_the_app_table_and_the_cost_model_agree_on_every_role():
   for role in ROLES:
      assert ROLE_MODELS[role] == CLAUDE_ONLY_ROLE_MODELS[role], role


def test_no_role_is_routed_to_a_non_anthropic_model():
   for role, model in ROLE_MODELS.items():
      assert model.startswith("claude-"), f"{role} is routed to {model!r}, not a Claude model"


def test_the_tutor_path_reads_its_model_from_the_shared_table():
   from app.feedback.tutor import TUTOR_MODEL

   assert TUTOR_MODEL == ROLE_MODELS["tutor"]
