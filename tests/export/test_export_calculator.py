"""A drill served and answered through the routes is in the student's export archive, keys
excluded because they are never stored (docs/calculator/architecture.md, Purge, export and
retention)."""
from tests.api.conftest import world  # noqa: F401
from tests.export.test_export import fetch_archive, produce, registered_student


def test_an_answered_drill_is_in_the_archive(world):
   client, user_id = registered_student(world)
   drill = client.post("/calculator/drills", json={"capability": "zero"}).json()
   answered = client.post(
      f"/calculator/drills/{drill['drill_id']}/answer",
      json={"value": "2.5", "setup_mathjson": None, "elapsed_ms": 1500, "desmos_open": False},
   )

   assert answered.status_code == 200

   archive = fetch_archive(client, produce(world, client)["id"]).json()
   rows = archive["tables"]["calculator_drills"]

   assert [row["id"] for row in rows] == [drill["drill_id"]]
   assert rows[0]["user_id"] == user_id
   assert rows[0]["value_entered"] == "2.5"
   assert rows[0]["submitted_at"] is not None
   assert rows[0]["desmos_url"] == drill["desmos_url"]
