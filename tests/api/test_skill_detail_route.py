"""GET /progress/skills/{skill_id}: one node of the mastery map opened, with the state the map gives
it and the prerequisites it is built on."""
from tests.api.conftest import world  # noqa: F401


def a_node(client):
   units = client.get("/progress/mastery").json()["units"]

   return units[0]["nodes"][0]


def test_the_detail_carries_the_state_the_map_gives_the_same_skill(world):  # noqa: F811
   client = world.client()
   world.register(client)
   node = a_node(client)

   detail = client.get(f"/progress/skills/{node['skill_id']}")

   assert detail.status_code == 200
   assert detail.json()["skill_id"] == node["skill_id"]
   assert detail.json()["name"] == node["name"]
   assert detail.json()["state"] == node["state"]


def test_the_prerequisites_are_the_graphs_parents_of_the_skill(world):  # noqa: F811
   client = world.client()
   world.register(client)
   graph = world.settings.session_context.graph
   skill_id = next(skill for skill in graph.skills if graph.hard_parents.get(skill) or graph.supporting_parents.get(skill))
   expected = set(graph.hard_parents.get(skill_id, ())) | set(graph.supporting_parents.get(skill_id, ()))

   detail = client.get(f"/progress/skills/{skill_id}").json()
   listed = {entry["id"] for entry in detail["prerequisites"]}

   assert listed == expected

   for entry in detail["prerequisites"]:
      is_skill = entry["id"] in graph.skills

      assert (entry["state"] is not None) == is_skill


def test_an_unknown_skill_is_not_found_and_a_stranger_is_refused(world):  # noqa: F811
   client = world.client()
   world.register(client)

   assert client.get("/progress/skills/BC-SKL-99999").status_code == 404
   assert world.client().get("/progress/skills/BC-SKL-01024").status_code == 401
