"""One tutor paragraph per graded free-response question, on the points it did not earn, built
from the criterion, the grader's cited rule and quote and the diagnostician's observation, and
stored so a second read of the result makes no second call."""
from app.feedback import tutor
from app.providers.base import ProviderResult, Usage
from app.providers.subscription import SubscriptionLimitReached

EXPLANATION = "Part (b) needed the sign change of g prime named at x = 3, and the work named no sign change."


class RecordingTutor:
   def __init__(self):
      self.requests = []

   def generate(self, request):
      self.requests.append(request)

      return ProviderResult(
         text=EXPLANATION,
         finish_reason="end_turn",
         usage=Usage(100, 20, None, None),
         provider="double",
         model=request.model,
      )


class LimitedTutor:
   def __init__(self):
      self.requests = []

   def generate(self, request):
      self.requests.append(request)

      raise SubscriptionLimitReached("the five-hour window is spent")


def typed_and_graded(frq_world):
   attempt_id = frq_world.open_attempt(capture_mode="typed")
   typed = frq_world.client.post(f"/attempts/{attempt_id}/typed", json={"read_back": frq_world.provider.read_back, "confidence": "unsure"})

   assert typed.status_code == 200

   return attempt_id


def frq_system_prompt():
   system, _variables = tutor.split_template(tutor.template_text(tutor.FRQ_POINTS))

   return system


def test_a_lost_point_gets_one_stored_explanation_grounded_in_its_criterion(frq_world):
   recorder = RecordingTutor()
   frq_world.settings.tutor = recorder
   frq_world.provider.grader_answers = {
      "b2": {"temp0_a": "not_earned", "temp0_b": "not_earned", "strict": "not_earned"},
   }
   attempt_id = typed_and_graded(frq_world)
   first = frq_world.client.get(f"/attempts/{attempt_id}/gradings").json()
   second = frq_world.client.get(f"/attempts/{attempt_id}/gradings").json()
   lost = [point for point in first["points"] if point["earned"] == 0]
   kept = [point for point in first["points"] if point["earned"] == 1]

   assert first["grading_state"] == "graded"
   assert [point["point_id"] for point in lost] == ["b2"]
   assert first["tutor_explanation"] == EXPLANATION
   assert second["tutor_explanation"] == EXPLANATION
   assert len(recorder.requests) == 1

   request = recorder.requests[0]
   rendered = request.messages[0].content

   assert request.role == "tutor"
   assert request.system == frq_system_prompt()
   assert lost[0]["criterion"] in rendered

   for point in kept:
      assert point["criterion"] not in rendered

   for part in first["worked_solution"]:
      for step in part["steps"]:
         assert step["text"] not in rendered


def test_a_question_with_every_point_earned_makes_no_tutor_call(frq_world):
   recorder = RecordingTutor()
   frq_world.settings.tutor = recorder
   attempt_id = typed_and_graded(frq_world)
   gradings = frq_world.client.get(f"/attempts/{attempt_id}/gradings").json()

   assert gradings["grading_state"] == "graded"
   assert gradings["tutor_explanation"] is None
   assert recorder.requests == []


def test_a_lost_point_with_the_tutor_out_of_its_window_reads_as_unavailable(frq_world):
   limited = LimitedTutor()
   frq_world.settings.tutor = limited
   frq_world.provider.grader_answers = {
      "b2": {"temp0_a": "not_earned", "temp0_b": "not_earned", "strict": "not_earned"},
   }
   attempt_id = typed_and_graded(frq_world)
   gradings = frq_world.client.get(f"/attempts/{attempt_id}/gradings").json()

   assert gradings["grading_state"] == "graded"
   assert len(limited.requests) == 1
   assert gradings["tutor_explanation"] is None
   assert gradings["tutor_unavailable"] is True
