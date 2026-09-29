"""The lesson payloads carry calculator_work, true when a worked example belongs to a calculator
archetype, so the reader can offer the Calculator destination beside it
(docs/calculator/build-plan.md, Slice 3, the lesson link)."""
from tests.api.test_lessons_routes import LESSON_ID, store_lesson

WORKED_EXAMPLE_ARCHETYPE = "BC-QA-02008"


def flags(client):
   lesson = client.get(f"/lessons/{LESSON_ID}").json()
   planned = client.get(f"/lessons/{LESSON_ID}/plan", params={"band": "mid"}).json()

   return lesson["calculator_work"], planned["calculator_work"]


def test_calculator_work_follows_the_worked_examples_archetype(world):
   store_lesson(world, "signed_off")
   client = world.client()
   world.register(client)
   archetypes = world.settings.session_context.archetypes
   archetypes[WORKED_EXAMPLE_ARCHETYPE] = {"id": WORKED_EXAMPLE_ARCHETYPE, "calculator_status": "either"}

   assert flags(client) == (False, False)

   archetypes[WORKED_EXAMPLE_ARCHETYPE] = {"id": WORKED_EXAMPLE_ARCHETYPE, "calculator_status": "calculator"}

   assert flags(client) == (True, True)
