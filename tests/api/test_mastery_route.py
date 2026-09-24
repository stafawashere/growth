"""GET /progress/mastery, the map the progress screen draws, over the student's skills_state."""
import json

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.progress import mastery
from tests.api.conftest import TODAY


def nodes_of(payload):
   return {node["skill_id"]: node for unit in payload["units"] for node in unit["nodes"]}


def test_mastery_refuses_a_request_without_a_session_cookie(world):
   assert world.client().get("/progress/mastery").status_code == 401


def test_mastery_refuses_an_unreadable_day(world):
   client = world.client()
   world.register(client)

   assert client.get("/progress/mastery", params={"today": "not-a-day"}).status_code == 422


def test_the_map_draws_every_graph_skill_from_the_stored_states(world):
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]

   graph_skills = set(world.settings.session_context.graph.skills)

   with OrmSession(world.engine) as db:
      rows = {
         row.skill_id: row
         for row in db.query(models.SkillState).filter(models.SkillState.user_id == user_id)
      }
      drawn = sorted(skill_id for skill_id in rows if skill_id in graph_skills)
      observed_id = next(skill_id for skill_id in drawn if not rows[skill_id].mastered)
      decayed_id = next(skill_id for skill_id in drawn if skill_id != observed_id)
      decayed = rows[decayed_id]
      decayed.mastered = 1
      decayed.stability = 1.0
      decayed.difficulty = 5.0
      decayed.last_practised_at = "2025-12-01T09:00:00+00:00"
      decayed.success_days = json.dumps(["2025-12-01"])
      db.commit()

   response = client.get("/progress/mastery", params={"today": TODAY.isoformat()})
   nodes = nodes_of(response.json())

   assert response.status_code == 200
   assert set(nodes) == graph_skills
   assert nodes[observed_id]["state"] == mastery.IN_PROGRESS
   assert nodes[decayed_id]["state"] == mastery.FADING
   assert nodes[decayed_id]["days_since_success"] == (TODAY - TODAY.replace(year=2025, month=12, day=1)).days
