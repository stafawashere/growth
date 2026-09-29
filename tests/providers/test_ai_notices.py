"""The AI call notices recorded at the provider seam (app/providers/notices.py).

Every outcome the guard can reach records one notice for the guard's user: an answer, a failure, a
refusal before the wire, a cap or pacing stop, an abandoned stream, and a call queued behind a
limit. A notice is never allowed to change the call: with the notice code raising, the result, the
exception, the accounting, the budget row and the audit rows are the same as without it.

No test here opens a socket. The wrapped providers are ReplayProvider doubles.
"""
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session as SqlSession

from app.db import models
from app.feedback import tutor
from app.grading import judge, transcribe
from app.providers import notices
from app.providers.base import (
   ImageInput,
   Message,
   Provider,
   ProviderRequest,
   RefusedBeforeWire,
   render_template,
   split_template,
)
from app.providers.call_queue import queue_call
from app.providers.guard import (
   BudgetCaps,
   BudgetStopped,
   DevSpendCapExceeded,
   DevSpendLedger,
   GuardedProvider,
   ProviderCallFailed,
   SubscriptionPaceExceeded,
   SubscriptionPacingCaps,
   SubscriptionPacingLedger,
)
from app.providers.replay import ReplayProvider
from app.providers.subscription import SubscriptionAuthFailed

USER = "USR-NOTICE-1"
MOMENT = datetime(2026, 9, 29, 10, 0, tzinfo=timezone.utc)
ROOMY_CAPS = BudgetCaps(cap_usd=1000.0)
SENTENCE = "The chain rule was applied to the outer function only, so the inner derivative is missing."
IMAGE_BYTES = b"\x89PNG\r\n\x1a\n" + bytes(range(256)) * 8

TUTOR_FIELDS = {
   "violated_step": "Differentiate the inner function 3x^2 + 1 before multiplying.",
   "observed_behavior": "The derivative of the outer function was written without the inner factor.",
   "scoring_consequence": "The answer point is lost.",
   "worked_solution": "d/dx (3x^2 + 1)^4 = 4(3x^2 + 1)^3 * 6x = 24x(3x^2 + 1)^3.",
}


def cassette(text=SENTENCE):
   return {
      "text": text,
      "finish_reason": "end_turn",
      "usage": {"input_tokens": 900, "output_tokens": 40, "cached_read_tokens": 0, "cached_write_tokens": 0},
   }


class Raising(Provider):
   def __init__(self, raised):
      self.raised = raised

   def generate(self, request):
      raise self.raised

   def stream(self, request):
      raise self.raised
      yield


def clock():
   return MOMENT


def database():
   engine = create_engine("sqlite:///:memory:")
   models.Base.metadata.create_all(engine)

   return SqlSession(engine)


def guard(db, provider, caps=ROOMY_CAPS, **options):
   return GuardedProvider(provider, db, user_id=USER, clock=clock, caps={"tutor": caps, "transcriber": caps}, **options)


def tutor_request():
   return tutor.request_for(TUTOR_FIELDS)


def transcriber_request():
   record = {
      "id": "BC-FRQ-2027-04",
      "parts": [
         {"id": "a", "prompt": "Find the slope of the tangent line at t = 2."},
         {"id": "b", "prompt": "Set up, but do not evaluate, an integral for the arc length."},
      ],
   }
   image = ImageInput(media_type="image/png", data=IMAGE_BYTES, width=1200, height=1600)

   return transcribe.request_for(record, [image])


def grader_request():
   text = judge.STANDARD_TEMPLATE.read_text()
   system, _variables = split_template(text)
   fields = {
      "point_type_id": "BC-PT-07",
      "point_type_name": "answer with supporting work",
      "earns": "a correct value with supporting work",
      "does_not_earn": "a bare value",
      "notation_requirements": "none",
      "precision_rules": "three decimal places",
      "eligibility_after_error": "no",
      "dependency": "none",
      "question_stem": "A particle moves along the x-axis.",
      "part_id": "b",
      "part_prompt": "Find the total distance travelled.",
      "criterion": "integral of |v(t)| from 0 to 3",
      "solution_skeleton": "Integrate the speed.",
      "student_work": "My whole working, line one.\nLine two of my working with 4.137.",
   }

   return ProviderRequest(
      role="grader",
      model="claude-sonnet-5",
      system=system,
      messages=(Message(role="user", content=render_template(text, fields)),),
      max_output_tokens=800,
      output_schema={"type": "object"},
   )


def held():
   return notices.notices_for(USER, 0)


@pytest.fixture(autouse=True)
def empty_board():
   notices.reset_notices()
   yield
   notices.reset_notices()


def test_an_answered_tutor_call_records_one_notice_with_both_briefs():
   db = database()
   result = guard(db, ReplayProvider(cassette=cassette()), provider_name="ReplayProvider").generate(tutor_request())

   assert result.text == SENTENCE

   recorded = held()

   assert len(recorded) == 1
   assert recorded[0]["role"] == "tutor"
   assert recorded[0]["outcome"] == notices.ANSWERED
   assert recorded[0]["model"] == tutor.TUTOR_MODEL
   assert recorded[0]["replayed"] is True
   assert recorded[0]["asked"].startswith("Asked the tutor to explain the step you missed: Differentiate")
   assert recorded[0]["answered"] == SENTENCE


def test_a_live_provider_name_is_not_called_a_replay():
   db = database()
   guard(db, ReplayProvider(cassette=cassette()), provider_name="anthropic").generate(tutor_request())

   assert held()[0]["replayed"] is False


def test_a_failed_call_records_a_failed_notice():
   db = database()

   with pytest.raises(ProviderCallFailed):
      guard(db, Raising(RuntimeError("socket closed")), provider_name="anthropic").generate(tutor_request())

   recorded = held()

   assert [notice["outcome"] for notice in recorded] == [notices.FAILED]
   assert "RuntimeError" in recorded[0]["answered"]
   assert "socket closed" not in recorded[0]["answered"]


def test_an_expired_sign_in_records_a_notice_that_says_so():
   db = database()
   expired = SubscriptionAuthFailed("the Claude sign-in failed on role tutor")

   with pytest.raises(ProviderCallFailed):
      guard(db, Raising(expired), provider_name="subscription").generate(tutor_request())

   recorded = held()

   assert [notice["outcome"] for notice in recorded] == [notices.FAILED]
   assert "sign-in expired" in recorded[0]["answered"]


def test_a_refusal_before_the_wire_records_a_refused_notice():
   db = database()

   with pytest.raises(RefusedBeforeWire):
      guard(db, Raising(RefusedBeforeWire("no CLI installed")), provider_name="subscription").generate(tutor_request())

   assert [notice["outcome"] for notice in held()] == [notices.REFUSED]


def test_a_cap_stop_records_a_stopped_notice():
   db = database()
   tiny = BudgetCaps(cap_usd=0.000001)

   with pytest.raises(BudgetStopped):
      guard(db, ReplayProvider(cassette=cassette()), caps=tiny).generate(tutor_request())

   recorded = held()

   assert [notice["outcome"] for notice in recorded] == [notices.STOPPED]
   assert recorded[0]["answered"] == "Nothing was sent: the tutor usd limit was reached."


def test_a_pacing_stop_records_a_stopped_notice(tmp_path):
   db = database()
   pacing = SubscriptionPacingCaps(calls_per_day={"tutor": 1}, calls_per_minute=100)
   ledger = SubscriptionPacingLedger(path=tmp_path / "pacing.json")
   paced = guard(db, ReplayProvider(cassette=cassette()), subscription_pacing=pacing, pacing_ledger=ledger)
   paced.generate(tutor_request())

   with pytest.raises(SubscriptionPaceExceeded):
      paced.generate(tutor_request())

   assert [notice["outcome"] for notice in held()] == [notices.ANSWERED, notices.STOPPED]


def test_a_developer_spend_stop_records_a_stopped_notice(tmp_path):
   db = database()
   ledger = DevSpendLedger(path=tmp_path / "dev.json")
   tracked = guard(db, ReplayProvider(cassette=cassette()), dev_spend_track=True, dev_spend_cap=0.0, dev_spend_ledger=ledger)

   with pytest.raises(DevSpendCapExceeded):
      tracked.generate(tutor_request())

   assert [notice["outcome"] for notice in held()] == [notices.STOPPED]


def test_a_finished_stream_records_an_answer_and_an_abandoned_one_records_an_interruption():
   db = database()
   streaming = guard(db, ReplayProvider(cassette=cassette()))

   assert list(streaming.stream(tutor_request())) == [SENTENCE]

   abandoned = streaming.stream(tutor_request())
   next(abandoned)
   abandoned.close()

   assert [notice["outcome"] for notice in held()] == [notices.ANSWERED, notices.INTERRUPTED]


def test_a_queued_call_records_a_queued_notice():
   db = database()
   queue_call(db, USER, "ATT-1", tutor_request(), reason="subscription_limit_reached", now=MOMENT)
   queue_call(db, USER, "ATT-1", tutor_request(), reason="subscription_limit_reached", now=MOMENT)

   recorded = held()

   assert [notice["outcome"] for notice in recorded] == [notices.QUEUED]
   assert "subscription limit reached" in recorded[0]["answered"]


def test_a_transcriber_brief_names_the_pages_and_parts_and_carries_no_image_or_template():
   db = database()
   answer = '{"parts": [{"part_id": "a", "lines": [], "answer": "3"}, {"part_id": "b", "lines": [], "answer": "x"}], "unreadable": []}'
   guard(db, ReplayProvider(cassette=cassette(answer))).generate(transcriber_request())
   recorded = held()[0]
   system, _variables = split_template(transcribe.TEMPLATE_PATH.read_text())

   assert recorded["asked"] == "Asked to read 1 photographed page for question BC-FRQ-2027-04, parts a, b."
   assert recorded["answered"] == "Returned a transcription of 2 parts."

   for brief in (recorded["asked"], recorded["answered"]):
      assert len(brief) <= notices.BRIEF_LIMIT
      assert "PNG" not in brief
      assert "\\x" not in brief
      assert system.strip()[:40] not in brief


def test_a_grader_brief_summarises_the_decision_and_leaves_out_the_student_work():
   db = database()
   answer = '{"decision": "earned", "evidence_quote": "My whole working, line one.", "rule_field": "earns", "rule_cited": "x", "eligibility_note": ""}'
   request = grader_request()
   grading = GuardedProvider(ReplayProvider(cassette=cassette(answer)), db, user_id=USER, clock=clock, caps={"grader": ROOMY_CAPS})
   grading.generate(request)
   recorded = held()[0]

   assert recorded["asked"] == "Asked whether your work on part (b) earns the point for answer with supporting work."
   assert recorded["answered"] == "Judged the point earned, citing the earns rule."
   assert "My whole working" not in recorded["asked"] + recorded["answered"]
   assert request.messages[0].content[:30] not in recorded["asked"]


def test_every_brief_is_cut_to_the_limit():
   db = database()
   long_answer = "word " * 400
   long_fields = dict(TUTOR_FIELDS, violated_step="step " * 400)
   guard(db, ReplayProvider(cassette=cassette(long_answer))).generate(tutor.request_for(long_fields))
   recorded = held()[0]

   for brief in (recorded["asked"], recorded["answered"]):
      assert notices.BRIEF_LIMIT - len("step ") <= len(brief) <= notices.BRIEF_LIMIT
      assert brief.endswith(notices.ELLIPSIS)


def test_an_unrecognised_message_falls_back_to_a_role_sentence_rather_than_prompt_text():
   db = database()
   request = ProviderRequest(
      role="tutor",
      model="claude-sonnet-5",
      system="system text",
      messages=(Message(role="user", content="Raw prompt text the notice must not repeat."),),
      max_output_tokens=100,
   )
   guard(db, ReplayProvider(cassette=cassette())).generate(request)

   assert held()[0]["asked"] == "Asked the tutor for a feedback sentence on your answer."


def budget_columns(db):
   return [
      (row.role, row.tokens_in, row.tokens_out, row.cost_usd, row.settled_calls, row.hard_stopped, row.stopped_by)
      for row in db.scalars(select(models.Budget)).all()
   ]


def audit_columns(db):
   """The budget row's id is random per database, so it is named by its role in the subject."""
   named = {f"budgets:{row.id}": f"budgets:{row.role}" for row in db.scalars(select(models.Budget)).all()}

   return [
      (row.action, row.actor, named.get(row.subject, row.subject), row.detail)
      for row in db.scalars(select(models.AuditLog)).all()
   ]


def run_every_outcome():
   """One answer, one failure and one cap stop, each through a fresh guard on its own database.
   Returns what a caller and the stores could observe."""
   observed = []

   answering_db = database()
   answering = guard(answering_db, ReplayProvider(cassette=cassette()))
   result = answering.generate(tutor_request())
   observed.append((result, answering.last_accounting, budget_columns(answering_db), audit_columns(answering_db)))

   failing_db = database()
   failing = guard(failing_db, Raising(RuntimeError("socket closed")))

   try:
      failing.generate(tutor_request())
   except ProviderCallFailed as failed:
      raised = (type(failed), str(failed), failed.__cause__, failed.__context__)

   observed.append((raised, failing.last_accounting, budget_columns(failing_db), audit_columns(failing_db)))

   stopped_db = database()
   stopped = guard(stopped_db, ReplayProvider(cassette=cassette()), caps=BudgetCaps(cap_usd=0.000001))

   try:
      stopped.generate(tutor_request())
   except BudgetStopped as stop:
      raised = (type(stop), str(stop), stop.__cause__, stop.__context__, stop.caps)

   observed.append((raised, stopped.last_accounting, budget_columns(stopped_db), audit_columns(stopped_db)))

   streaming_db = database()
   streaming = guard(streaming_db, ReplayProvider(cassette=cassette()))
   abandoned = streaming.stream(tutor_request())
   next(abandoned)
   abandoned.close()
   observed.append((streaming.last_accounting, budget_columns(streaming_db)))

   return observed


def test_a_notice_that_raises_changes_nothing_about_the_call(monkeypatch):
   untouched = run_every_outcome()

   assert len(held()) == 4

   notices.reset_notices()

   def broken(*args, **kwargs):
      raise RuntimeError("the notice board is broken")

   monkeypatch.setattr(notices.BOARD, "record", broken)
   monkeypatch.setattr(notices, "asked_brief", broken)

   with_broken_notices = run_every_outcome()

   assert with_broken_notices == untouched
   assert held() == []


def test_a_record_call_that_raises_is_swallowed_by_the_guard(monkeypatch):
   def broken(*args, **kwargs):
      raise RuntimeError("record_call itself is broken")

   monkeypatch.setattr(notices, "record_call", broken)
   db = database()
   result = guard(db, ReplayProvider(cassette=cassette())).generate(tutor_request())

   assert result.text == SENTENCE


def test_the_board_keeps_a_bounded_buffer_per_user():
   board = notices.NoticeBoard(per_user=3)

   for index in range(5):
      board.record("USR-A", {"index": index})

   board.record("USR-B", {"index": 99})

   assert [notice["index"] for notice in board.since("USR-A", 0)] == [2, 3, 4]
   assert [notice["index"] for notice in board.since("USR-B", 0)] == [99]
   assert board.since("USR-A", 5) == []


def test_record_call_and_record_queued_never_raise_themselves(monkeypatch):
   def broken(*args, **kwargs):
      raise RuntimeError("the notice board is broken")

   monkeypatch.setattr(notices.BOARD, "record", broken)

   assert notices.record_call(USER, "anthropic", tutor_request(), raised=RuntimeError("x")) is None
   assert notices.record_queued(USER, tutor_request(), "subscription_limit_reached") is None
