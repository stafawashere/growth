"""The Desmos fluency routes against the contract in docs/calculator/build-plan.md, over the conftest
application: a drill served and answered once, the two verdicts, the exam's budgets, the measured
payload and skills_state untouched by any of it (invariant C0)."""
from sqlalchemy import select, text
from sqlalchemy.orm import Session as OrmSession

from app.assessment.shape import part_shape
from app.calculator_drills import service
from app.calculator.check import check_value
from app.db import models

OTHER_USER_ID = "USR-other"
INTEGRAL = "integral"
INTEGRAL_TEMPLATE = "CDT-integral-01"
UNSUPPORTED_SETUP = ["NotAHead", 1]
MAX_DRAWS_FOR_A_SHORT_ENTRY = 20


def signed_in(world):
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]

   return client, user_id


def serve(client, capability=INTEGRAL, **fields):
   response = client.post("/calculator/drills", json={"capability": capability, **fields})

   assert response.status_code == 200, response.text

   return response.json()


def task_of(world, drill_id):
   with OrmSession(world.engine) as db:
      return service.rebuilt_task(db.get(models.CalculatorDrill, drill_id))


def answer(client, drill_id, value, setup=None, elapsed_ms=1000):
   return client.post(
      f"/calculator/drills/{drill_id}/answer",
      json={"value": value, "setup_mathjson": setup, "elapsed_ms": elapsed_ms, "desmos_open": True},
   )


def rounded_and_truncated(world, drill_id):
   task = task_of(world, drill_id)
   verdict = check_value("", task.value_key)

   return verdict.rounded, verdict.truncated


def drill_with_a_nonzero_third_place(world, client):
   """A truncated form ending in 0, such as 15.300, makes the two-place entry 15.30 an accepted
   answer under the rule, so a short entry is only short when the third place is not 0."""
   for _ in range(MAX_DRAWS_FOR_A_SHORT_ENTRY):
      drill = serve(client, template_id=INTEGRAL_TEMPLATE)
      rounded, truncated = rounded_and_truncated(world, drill["drill_id"])
      has_nonzero_third_place = not truncated.endswith("0")

      if has_nonzero_third_place:
         return drill, rounded, truncated

   raise AssertionError("no draw with a nonzero third place")


def skills_state_rows(world):
   with world.engine.connect() as connection:
      return connection.execute(text("SELECT * FROM skills_state ORDER BY user_id, skill_id")).all()


def expected_budgets():
   return {key: part_shape(key).budget_seconds_per_question for key in ("I-B", "II-A")}


def test_a_served_drill_carries_the_contract_fields_and_never_the_keys(world):
   client, user_id = signed_in(world)
   drill = serve(client)

   assert set(drill) == {
      "drill_id", "template_id", "capability", "card_id", "prompt", "function_tex", "unit",
      "radian_sensitive", "desmos_url", "served_at",
   }
   assert drill["capability"] == INTEGRAL
   assert drill["template_id"].startswith("CDT-integral-")
   assert drill["desmos_url"] == service.DESMOS_COLLEGE_BOARD_URL

   rounded, truncated = rounded_and_truncated(world, drill["drill_id"])

   assert rounded not in str(drill)
   assert truncated not in str(drill)

   with OrmSession(world.engine) as db:
      row = db.get(models.CalculatorDrill, drill["drill_id"])
      audit_actions = db.scalars(select(models.AuditLog.action).where(models.AuditLog.actor == user_id)).all()

   assert row.user_id == user_id
   assert row.submitted_at is None
   assert rounded not in row.draw
   assert "calculator_drill_served" in audit_actions


def test_a_correct_rounded_value_and_an_equivalent_setup(world):
   client, _ = signed_in(world)
   drill = serve(client, template_id=INTEGRAL_TEMPLATE)
   task = task_of(world, drill["drill_id"])
   rounded, truncated = rounded_and_truncated(world, drill["drill_id"])
   response = answer(client, drill["drill_id"], rounded, setup=task.setup_key)
   payload = response.json()

   assert response.status_code == 200
   assert payload["value"] == {"correct": True, "reason": None, "rounded": rounded, "truncated": truncated}
   assert payload["setup"]["shown"] is True
   assert payload["setup"]["correct"] is True
   assert payload["setup"]["reason"] is None
   assert payload["setup"]["key_latex"] != ""
   assert payload["budget_seconds"] == expected_budgets()


def test_the_value_verdicts_for_truncated_short_and_wrong_entries(world):
   client, _ = signed_in(world)
   outcomes = {}

   for label in ("truncated", "short", "wrong"):
      drill, rounded, truncated = drill_with_a_nonzero_third_place(world, client)
      entries = {"truncated": truncated, "short": truncated[:-1], "wrong": f"{float(rounded) + 0.5:.3f}"}
      outcomes[label] = answer(client, drill["drill_id"], entries[label], setup=UNSUPPORTED_SETUP).json()

   assert outcomes["truncated"]["value"]["correct"] is True
   assert outcomes["short"]["value"]["correct"] is False
   assert outcomes["short"]["value"]["reason"] == "not_three_places"
   assert outcomes["wrong"]["value"]["correct"] is False
   assert outcomes["wrong"]["value"]["reason"] == "outside_tolerance"
   assert outcomes["wrong"]["setup"]["shown"] is True
   assert outcomes["wrong"]["setup"]["correct"] is None
   assert outcomes["wrong"]["setup"]["reason"] == "unsupported"


def test_a_missing_setup_is_recorded_as_not_shown(world):
   client, _ = signed_in(world)
   drill = serve(client)
   rounded, _ = rounded_and_truncated(world, drill["drill_id"])
   payload = answer(client, drill["drill_id"], rounded).json()

   assert payload["setup"]["shown"] is False
   assert payload["setup"]["correct"] is None
   assert payload["setup"]["reason"] == "missing"

   with OrmSession(world.engine) as db:
      row = db.get(models.CalculatorDrill, drill["drill_id"])

   assert row.setup_shown == 0
   assert row.setup_reason == "missing"
   assert row.value_correct == 1


def test_a_second_answer_is_refused_and_leaves_the_first(world):
   client, _ = signed_in(world)
   drill = serve(client)
   rounded, _ = rounded_and_truncated(world, drill["drill_id"])
   first = answer(client, drill["drill_id"], rounded)
   second = answer(client, drill["drill_id"], "0.000")

   assert first.status_code == 200
   assert second.status_code == 409

   with OrmSession(world.engine) as db:
      row = db.get(models.CalculatorDrill, drill["drill_id"])

   assert row.value_entered == rounded


def test_another_users_drill_and_an_unknown_drill_are_404(world):
   client, _ = signed_in(world)

   with OrmSession(world.engine) as db:
      foreign = service.serve(db, OTHER_USER_ID, INTEGRAL)
      db.commit()

   assert answer(client, foreign["drill_id"], "1.000").status_code == 404
   assert answer(client, "cdr-missing", "1.000").status_code == 404

   with OrmSession(world.engine) as db:
      row = db.get(models.CalculatorDrill, foreign["drill_id"])

   assert row.submitted_at is None


def test_a_bad_body_is_422(world):
   client, _ = signed_in(world)
   drill = serve(client)

   assert client.post("/calculator/drills", json={"capability": "graphing"}).status_code == 422
   assert client.post("/calculator/drills", json={"capability": "zero", "template_id": INTEGRAL_TEMPLATE}).status_code == 422
   assert client.post(f"/calculator/drills/{drill['drill_id']}/answer", json={"value": "1.000"}).status_code == 422
   assert answer(client, drill["drill_id"], "1.000", elapsed_ms=-1).status_code == 422


def test_the_routes_need_a_session(world):
   client = world.client()

   assert client.get("/calculator/cards").status_code == 401
   assert client.post("/calculator/drills", json={"capability": INTEGRAL}).status_code == 401
   assert client.get("/calculator/measured").status_code == 401


def test_elapsed_time_is_bounded_by_the_time_since_serving(world):
   client, _ = signed_in(world)
   drill = serve(client)
   payload = answer(client, drill["drill_id"], "1.000", elapsed_ms=10_000_000).json()

   assert payload["elapsed_ms"] < 10_000_000
   assert payload["elapsed_ms"] >= service.ELAPSED_GRACE_MS


def test_measured_says_null_under_three_and_the_median_at_three(world):
   client, _ = signed_in(world)
   elapsed_values = (100, 300, 200)

   for count, elapsed_ms in enumerate(elapsed_values, start=1):
      drill = serve(client)
      rounded, _ = rounded_and_truncated(world, drill["drill_id"])
      answer(client, drill["drill_id"], rounded if count != 2 else "0.000", elapsed_ms=elapsed_ms)
      measured = client.get("/calculator/measured").json()
      integral = next(entry for entry in measured["capabilities"] if entry["capability"] == INTEGRAL)

      if count < 3:
         assert integral["median_ms"] is None

   serve(client)
   measured = client.get("/calculator/measured").json()
   integral = next(entry for entry in measured["capabilities"] if entry["capability"] == INTEGRAL)

   assert [entry["capability"] for entry in measured["capabilities"]] == ["plot", "zero", "derivative", "integral", "intersection", "value"]
   assert integral["median_ms"] == 200
   assert integral["served"] == 4
   assert integral["answered"] == 3
   assert integral["value_correct"]["numerator"] == 2
   assert integral["value_correct"]["denominator"] == 3
   assert integral["setup_shown"]["numerator"] == 0
   assert integral["setup_correct"]["denominator"] == 0
   assert measured["budget_seconds"] == expected_budgets()
   assert len(measured["recent"]) == 3
   assert [entry["elapsed_ms"] for entry in measured["recent"]] == [200, 300, 100]
   assert measured["recent"][0]["function_tex"].startswith("R(t)")


def test_the_cards_are_served_without_sources_or_library_ids(world):
   client, _ = signed_in(world)
   cards = client.get("/calculator/cards").json()["cards"]
   integral = client.get("/calculator/cards/CCD-integral-01").json()

   assert "CCD-integral-01" in {card["id"] for card in cards}
   assert "sources" not in integral
   assert "evidence_tag" not in integral
   assert "BC-ERR" not in str(integral)
   assert integral["bluebook_note"] is None
   assert client.get("/calculator/cards/CCD-missing").status_code == 404


def test_skills_state_is_byte_identical_across_a_served_and_answered_drill(world):
   client, user_id = signed_in(world)
   before = skills_state_rows(world)
   drill = serve(client)
   rounded, _ = rounded_and_truncated(world, drill["drill_id"])
   answer(client, drill["drill_id"], rounded, setup=UNSUPPORTED_SETUP)
   after = skills_state_rows(world)

   assert len(before) > 0
   assert before == after
