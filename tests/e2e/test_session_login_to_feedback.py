"""Gate 23 of docs/plan/11-phased-delivery.md, end to end over the real HTTP application.

The property: a passkey login, a full session over the P1 subset, a confidence rating, an
elaborated feedback screen, a written error note, and a persisted skills_state change, with no
network calls outside the recorded cassettes.

Every link is driven through the routes of 06's API surface against a temporary SQLite database
built by app/main.py. The elaborated screen is the one that needs a stage-unsupported item, and no
archetype starts there at cold start, so the student works correctly through as many sessions as
the R7 counter pair needs to raise a skill from example to unsupported, and the wrong answer that
earns the elaborated screen and the error note is given on the first item served without support.
"""
import json
import socket

import pytest

from tests.e2e.conftest import CASSETTE_PATH, FIRST_DAY, NetworkCallInTest

DAYS_BETWEEN_SESSIONS = 8
MAX_SESSIONS = 12
P1_ARCHETYPES = (
   "BC-QA-01004",
   "BC-QA-01008",
   "BC-QA-01015",
   "BC-QA-02002",
   "BC-QA-02006",
   "BC-QA-02007",
   "BC-QA-02008",
   "BC-QA-02010",
   "BC-QA-02011",
   "BC-QA-03001",
   "BC-QA-03004",
   "BC-QA-03005",
   "BC-QA-03008",
)
ERROR_NOTE = "I rushed the middle step and never checked the last line against the question."


def cold_start_reachable_archetypes(world):
   """What the engine's own gating opens over the freshly seeded state, computed rather than
   typed, so the set moves with the library instead of with this file.
   """
   from sqlalchemy.orm import Session as OrmSession

   from app.engine.fringe import candidates, outer_fringe
   from app.session import repository

   context = world.settings.session_context

   with OrmSession(world.engine) as db:
      states = repository.load_states(db, world.user_id)

   available, _ = candidates(outer_fringe(states, context.graph), context.graph, context.bank)

   return {record["id"] for record in available}


def answer_for(entry, item, correctly):
   is_mcq = item["format"] == "mcq"

   if is_mcq:
      chosen = entry["key_option_id"] if correctly else entry["wrong_option_id"]

      return {"option_id": chosen}

   expression = entry["key_mathjson"] if correctly else entry["wrong_mathjson"]

   return {"mathjson": expression}


def collects_confidence(item):
   return item["stage"] != "example"


def submit(client, session_id, item, answer, today):
   return client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": answer,
         "elapsed_ms": 42000,
         "today": today.isoformat(),
      },
   )


def rate(client, session_id, attempt_id, confidence, today):
   return client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/confidence",
      json={"confidence": confidence, "today": today.isoformat()},
   )


def answer_correctly(client, session_id, item, entry, today):
   submitted = submit(client, session_id, item, answer_for(entry, item, True), today)

   assert submitted.status_code == 200, submitted.text

   attempt = submitted.json()

   assert attempt["correct"] is True

   if collects_confidence(item):
      rated = rate(client, session_id, attempt["id"], "confident", today)

      assert rated.status_code == 200, rated.text

   return attempt


def drive_the_elaborated_screen(world, client, session_id, item, entry, today):
   """The wrong answer, the rating before anything is shown, the screen, and the note."""
   submitted = submit(client, session_id, item, answer_for(entry, item, False), today)

   assert submitted.status_code == 200, submitted.text

   attempt = submitted.json()

   assert attempt["correct"] is False
   assert attempt["served_stage"] == "unsupported"
   assert attempt["confidence"] is None

   too_early = client.get(f"/sessions/{session_id}/attempts/{attempt['id']}/feedback")

   assert too_early.status_code == 409, too_early.text

   rated = rate(client, session_id, attempt["id"], "unsure", today)

   assert rated.status_code == 200, rated.text
   assert rated.json()["confidence"] == "unsure"

   shown = client.get(f"/sessions/{session_id}/attempts/{attempt['id']}/feedback")

   assert shown.status_code == 200, shown.text

   noted = client.post(
      f"/sessions/{session_id}/attempts/{attempt['id']}/error-note",
      json={"note": ERROR_NOTE},
   )

   assert noted.status_code == 200, noted.text
   assert world.attempt_error_note(attempt["id"]) == ERROR_NOTE, (
      "gate 23 wants the note written down, so the column is read back out of SQLite rather "
      "than the POST's own echo"
   )

   return {"attempt": attempt, "feedback": shown.json(), "item": item}


def drain_session(client, world, session_id, today, screens):
   """Serve, answer and rate every queued item until the queue is empty.

   Every item is answered correctly except the ones that earn the elaborated screen: the first
   unsupported item, which R29 serves as a short answer, and the first unsupported item served as
   an MCQ, which is the one whose chosen distractor carries a BC-ERR id for the screen to name.
   """
   served = []

   while True:
      offered = client.get(f"/sessions/{session_id}/next")

      assert offered.status_code == 200, offered.text

      item = offered.json()["item"]
      is_drained = item is None

      if is_drained:
         break

      entry = world.answers[item["id"]]
      served.append(item)
      is_unsupported = item["stage"] == "unsupported"
      is_a_new_screen = item["format"] not in screens
      earns_a_screen = is_unsupported and is_a_new_screen

      if earns_a_screen:
         screens[item["format"]] = drive_the_elaborated_screen(
            world, client, session_id, item, entry, today
         )
      else:
         answer_correctly(client, session_id, item, entry, today)

   return served


def test_session_login_to_feedback(world):
   client = world.client()
   registered = world.register(client)

   assert registered.status_code == 200, registered.text
   assert registered.json()["seeded_skill_states"] == 618

   cold_start_reachable = cold_start_reachable_archetypes(world)
   seeded_states = world.skill_state_rows()
   logged_out = client.post("/auth/logout")

   assert logged_out.status_code == 200, logged_out.text

   logged_in = world.login(client)

   assert logged_in.status_code == 200, logged_in.text

   identified = client.get("/me")

   assert identified.status_code == 200, identified.text
   assert identified.json()["id"] == world.user_id

   screens = {}
   all_served = []
   today = FIRST_DAY

   for _session_index in range(MAX_SESSIONS):
      opened = client.post("/sessions", json={"mode": "learning", "today": today.isoformat()})

      assert opened.status_code == 200, opened.text

      session_id = opened.json()["id"]
      served = drain_session(client, world, session_id, today, screens)
      all_served.extend(served)
      emptied = client.get(f"/sessions/{session_id}")

      assert emptied.status_code == 200, emptied.text
      assert emptied.json()["remaining"] == []

      closed = client.post(
         f"/sessions/{session_id}/close", json={"today": today.isoformat()}
      )

      assert closed.status_code == 200, closed.text
      assert closed.json()["ended_at"] is not None

      has_both_screens = len(screens) == 2

      if has_both_screens:
         break

      today = today.fromordinal(today.toordinal() + DAYS_BETWEEN_SESSIONS)

   assert len(all_served) > 0
   assert sorted(screens) == ["mcq", "short_answer"], (
      "gate 23 needs the elaborated screen at stage unsupported in both served formats, and "
      f"only these arrived: {sorted(screens)}"
   )

   served_archetypes = sorted({item["archetype_id"] for item in all_served})
   outside_the_subset = [
      archetype_id
      for archetype_id in served_archetypes
      if archetype_id not in P1_ARCHETYPES
   ]

   assert outside_the_subset == [], (
      "gate 23 runs over the P1 subset, which scope item 2 of docs/plan/11-phased-delivery.md "
      f"fixes as the 13 archetypes listed here, and these were served instead: {outside_the_subset}"
   )

   reachable = cold_start_reachable
   never_served = sorted(reachable - set(served_archetypes))

   opened_more_than_one = len(reachable) > 1

   assert opened_more_than_one, (
      "gate 23's archetype check is only worth making when the cold-start state opens more than "
      f"one archetype, and it opened {sorted(reachable)}"
   )
   assert never_served == [], (
      "membership in the 13 is a subset check and a regression that serves one archetype passes "
      "it, so gate 23 also asserts that every archetype the engine's own gating opens at cold "
      f"start was actually served, and these never were: {never_served}"
   )

   cassette = json.loads(CASSETTE_PATH.read_text())

   for screen in screens.values():
      feedback = screen["feedback"]

      assert feedback["kind"] == "elaborated"
      assert feedback["stage"] == "unsupported"
      assert feedback["confidence"] == "unsure"
      assert feedback["elaborated"]["violated_step"] != ""
      assert feedback["elaborated"]["worked_solution"] != ""
      assert feedback["sentence"] == cassette["text"]

   named = screens["mcq"]["feedback"]["elaborated"]
   chosen_error_path = world.answers[screens["mcq"]["item"]["id"]]["wrong_error_path"]

   assert named["error_id"] == chosen_error_path
   assert named["observed_behavior"] != ""
   assert named["scoring_consequence"] != ""

   changed_skills = [
      skill_id
      for skill_id, row in world.skill_state_rows().items()
      if row != seeded_states[skill_id]
   ]

   assert len(changed_skills) > 0

   wrongly_answered_skill = screens["mcq"]["item"]["skills"][0]

   assert wrongly_answered_skill in changed_skills

   before = seeded_states[wrongly_answered_skill]
   after = world.skill_state_rows()[wrongly_answered_skill]

   assert after["observation_count"] > before["observation_count"]
   assert after["fading_stage"] != before["fading_stage"]


def test_the_socket_ban_itself_fails_a_network_call(forbid_network):
   """The no-network half of gate 23 is only worth asserting if the ban can fire."""
   with pytest.raises(NetworkCallInTest):
      socket.socket(socket.AF_INET, socket.SOCK_STREAM)
