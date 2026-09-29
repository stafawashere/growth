"""GET /progress/pace over the real graph, the blueprint weights and the account's exam date."""
from app.progress import pace
from tests.api.conftest import TODAY


def test_pace_refuses_a_request_without_a_session_cookie(world):
   assert world.client().get("/progress/pace").status_code == 401


def test_a_new_account_gets_no_verdict_and_the_whole_graph_as_remaining_work(world):
   client = world.client()
   world.register(client)

   exam_date = client.get("/settings").json()["exam_date"]
   response = client.get("/progress/pace", params={"today": TODAY.isoformat()})
   payload = response.json()
   graph_skills = world.settings.session_context.graph.skills

   assert response.status_code == 200
   assert payload["verdict"] == pace.TOO_EARLY
   assert payload["exam_date"] == exam_date
   assert payload["skills"]["total"] == len(graph_skills)
   assert payload["skills"]["held"] == 0
   assert abs(payload["skills"]["remaining_weighted"] - len(graph_skills)) < 0.01
