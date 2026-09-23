"""The tutor's request configuration and its two call ceilings, from docs/plan/13-ai-engineering.md.

13's tutor row corrects the configuration to thinking disabled, effort low and 600 output tokens,
and its "A per-session ceiling" paragraph gives 09's two inferred tunables their numbers: 20 tutor
calls per session and 3 per item. Both ceilings are counted from the attempts table, so a fresh
process, a fresh ORM session or a second request sees the calls the first one spent.
"""
import json
import re
from pathlib import Path
from types import SimpleNamespace

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy.pool import StaticPool

from app.db import models
from app.engine.state import FadingStage
from app.feedback import render, tutor
from app.providers.base import ProviderResult, RefusedBeforeWire, Usage
from app.providers.guard import BudgetCaps, BudgetStopped, GuardedProvider
from tests.api.conftest import TODAY, WRONG_MATHJSON, world  # noqa: F401
from tests.api.test_routes import open_session

PLAN_13 = Path(__file__).resolve().parents[2] / "docs" / "plan" / "13-ai-engineering.md"
NOW = "2026-09-20T09:00:00+00:00"
SESSION_ID = "SES-0001"
SENTENCE = "the derivative of the product is not the product of the derivatives"


def plan_text():
   return PLAN_13.read_text()


def plan_tutor_settings():
   correction = re.search(r"The correction is three settings.*", plan_text()).group(0)
   thinking = re.search(r"`thinking: (\{.*?\})`", correction).group(1)
   output_config = re.search(r"`output_config: (\{.*?\})`", correction).group(1)
   max_output_tokens = re.search(r"`max_output_tokens` raised to (\d+)", correction).group(1)

   return json.loads(thinking), json.loads(output_config), int(max_output_tokens)


def plan_ceilings():
   sentence = re.search(
      r"The number is (\d+) tutor calls per session and (\d+) per item", plan_text()
   )

   return int(sentence.group(1)), int(sentence.group(2))


class CountingProvider:
   def __init__(self, text=SENTENCE, accountings=None):
      self.text = text
      self.calls = 0
      self.accountings = list(accountings or [])
      self.last_accounting = None

   def generate(self, request):
      self.calls += 1
      has_accounting = self.accountings != []

      if has_accounting:
         self.last_accounting = self.accountings.pop(0)

      return ProviderResult(
         text=self.text,
         finish_reason="end_turn",
         usage=Usage(input_tokens=10, output_tokens=10, cached_read_tokens=0, cached_write_tokens=0),
         provider="double",
         model=tutor.TUTOR_MODEL,
      )


class RaisingProvider:
   def __init__(self, error):
      self.error = error
      self.calls = 0

   def generate(self, request):
      self.calls += 1

      raise self.error


class StoppedProvider:
   """Stands in for a GuardedProvider refusing before the wire, so no call reaches a model."""

   def generate(self, request):
      raise BudgetStopped("tutor", "usd")


def accounting(tokens_in, cached_read, cost_usd):
   return SimpleNamespace(
      model=tutor.TUTOR_MODEL,
      tokens_in=tokens_in,
      tokens_out=40,
      tokens_cached_read=cached_read,
      tokens_cached_write=None,
      cost_usd=cost_usd,
   )


def open_engine():
   engine = create_engine(
      "sqlite://",
      connect_args={"check_same_thread": False},
      poolclass=StaticPool,
   )
   models.Base.metadata.create_all(engine)

   return engine


def make_attempt(db, attempt_id, session_id=SESSION_ID):
   attempt = models.Attempt(
      id=attempt_id,
      session_id=session_id,
      item_id="ITM-0001",
      started_at=NOW,
      submitted_at=NOW,
      transcription_confirmed=0,
      correct=0,
      served_stage=FadingStage.UNSUPPORTED.value,
      format="mcq",
      per_skill_states="{}",
      snapshot_id="SNP-0001",
      created_at=NOW,
      updated_at=NOW,
   )
   db.add(attempt)
   db.flush()

   return attempt


def make_feedback():
   payload = render.ElaboratedPayload(
      error_id="BC-ERR-0101",
      violated_step_index=1,
      violated_step="apply the product rule",
      observed_behavior="multiplied the two derivatives",
      scoring_consequence="the derivative point is not earned",
      worked_solution="differentiate each factor and combine by the product rule",
   )

   return render.Feedback(
      kind=render.FeedbackKind.ELABORATED,
      stage=FadingStage.UNSUPPORTED,
      elaborated=payload,
   )


def compose_in_fresh_session(engine, provider, attempt_id):
   with OrmSession(engine) as db:
      attempt = db.get(models.Attempt, attempt_id)
      sentence = tutor.compose_sentence(provider, make_feedback(), db=db, attempt=attempt)
      db.commit()

   return sentence


def stored_attempt(engine, attempt_id):
   with OrmSession(engine) as db:
      row = db.get(models.Attempt, attempt_id)
      db.expunge(row)

   return row


def seed_attempts(engine, attempt_ids, session_id=SESSION_ID):
   with OrmSession(engine) as db:
      for attempt_id in attempt_ids:
         make_attempt(db, attempt_id, session_id=session_id)

      db.commit()


def test_the_built_tutor_request_carries_the_three_settings_13_corrects():
   thinking, output_config, max_output_tokens = plan_tutor_settings()

   request = tutor.request_for(make_feedback().elaborated.as_prompt_fields())

   assert request.provider_options["thinking"] == thinking
   assert request.provider_options["output_config"] == output_config
   assert request.max_output_tokens == max_output_tokens


def test_the_ceilings_are_the_numbers_13_gives_09s_tunables():
   per_session, per_item = plan_ceilings()

   assert tutor.TUTOR_CALLS_PER_SESSION == per_session
   assert tutor.TUTOR_CALLS_PER_ITEM == per_item


def test_every_call_that_reaches_the_provider_is_counted_on_the_attempt():
   engine = open_engine()
   seed_attempts(engine, ["ATT-0001"])

   compose_in_fresh_session(engine, CountingProvider(text=""), "ATT-0001")
   compose_in_fresh_session(engine, RaisingProvider(RuntimeError("chain exhausted")), "ATT-0001")
   compose_in_fresh_session(engine, CountingProvider(), "ATT-0001")

   assert stored_attempt(engine, "ATT-0001").tutor_calls == 3


def test_a_budget_stop_before_the_wire_is_not_counted():
   engine = open_engine()
   seed_attempts(engine, ["ATT-0001"])

   with OrmSession(engine) as db:
      attempt = db.get(models.Attempt, "ATT-0001")

      try:
         tutor.compose_sentence(StoppedProvider(), make_feedback(), db=db, attempt=attempt)
      except BudgetStopped:
         db.commit()

   assert stored_attempt(engine, "ATT-0001").tutor_calls == 0


def test_each_calls_accounting_is_added_onto_the_attempt_null_aware():
   engine = open_engine()
   seed_attempts(engine, ["ATT-0001"])
   provider = CountingProvider(
      text="",
      accountings=[accounting(1200, None, 0.004), accounting(174, 1100, 0.002)],
   )

   compose_in_fresh_session(engine, provider, "ATT-0001")
   after_first = stored_attempt(engine, "ATT-0001")

   assert after_first.tutor_tokens_in == 1200
   assert after_first.tutor_tokens_cached_read is None
   assert after_first.tutor_cost_usd == 0.004

   compose_in_fresh_session(engine, provider, "ATT-0001")
   after_second = stored_attempt(engine, "ATT-0001")

   assert after_second.tutor_tokens_in == 1374
   assert after_second.tutor_tokens_cached_read == 1100
   assert abs(after_second.tutor_cost_usd - 0.006) < 1e-12


def test_a_stale_accounting_from_an_earlier_call_is_not_added_twice():
   engine = open_engine()
   seed_attempts(engine, ["ATT-0001"])
   provider = CountingProvider(text="", accountings=[accounting(1200, 1100, 0.004)])

   compose_in_fresh_session(engine, provider, "ATT-0001")
   compose_in_fresh_session(engine, provider, "ATT-0001")
   stored = stored_attempt(engine, "ATT-0001")

   assert stored.tutor_calls == 2
   assert stored.tutor_tokens_in == 1200
   assert stored.tutor_tokens_cached_read == 1100


def test_the_per_item_ceiling_refuses_the_next_call_from_a_fresh_session():
   engine = open_engine()
   seed_attempts(engine, ["ATT-0001"])
   silent = CountingProvider(text="")

   for _call in range(tutor.TUTOR_CALLS_PER_ITEM):
      compose_in_fresh_session(engine, silent, "ATT-0001")

   late = CountingProvider()
   sentence = compose_in_fresh_session(engine, late, "ATT-0001")

   assert sentence is None
   assert late.calls == 0
   assert stored_attempt(engine, "ATT-0001").tutor_calls == tutor.TUTOR_CALLS_PER_ITEM


def test_the_per_session_ceiling_refuses_a_new_attempt_once_the_session_sum_is_reached():
   engine = open_engine()
   per_session = tutor.TUTOR_CALLS_PER_SESSION
   per_item = tutor.TUTOR_CALLS_PER_ITEM
   full_attempts = per_session // per_item
   attempt_ids = [f"ATT-{index:04d}" for index in range(full_attempts + 2)]
   seed_attempts(engine, attempt_ids)
   seed_attempts(engine, ["ATT-OTHER"], session_id="SES-OTHER")
   silent = CountingProvider(text="")

   for attempt_id in attempt_ids[:full_attempts]:
      for _call in range(per_item):
         compose_in_fresh_session(engine, silent, attempt_id)

   remainder = per_session - full_attempts * per_item

   for _call in range(remainder):
      compose_in_fresh_session(engine, silent, attempt_ids[full_attempts])

   with OrmSession(engine) as db:
      spent = db.scalar(
         select(func.sum(models.Attempt.tutor_calls)).where(models.Attempt.session_id == SESSION_ID)
      )

   assert spent == per_session

   late = CountingProvider()
   sentence = compose_in_fresh_session(engine, late, attempt_ids[-1])

   assert sentence is None
   assert late.calls == 0

   other_session = CountingProvider()
   compose_in_fresh_session(engine, other_session, "ATT-OTHER")

   assert other_session.calls == 1


def test_a_lowered_ceiling_binds_on_the_next_call(monkeypatch):
   engine = open_engine()
   seed_attempts(engine, ["ATT-0001"])
   compose_in_fresh_session(engine, CountingProvider(text=""), "ATT-0001")
   monkeypatch.setattr(tutor, "TUTOR_CALLS_PER_ITEM", 1)
   late = CountingProvider()

   compose_in_fresh_session(engine, late, "ATT-0001")

   assert late.calls == 0


def answer_for(item):
   is_mcq = item["format"] == "mcq"

   if is_mcq:
      return {"option_id": "B"}

   return {"form": "symbolic", "mathjson": WRONG_MATHJSON}


def test_the_twenty_first_tutor_call_in_a_session_never_reaches_the_provider(world):
   """Through the real feedback route. The silent tutor returns an empty sentence, so nothing is
   cached and every read of the feedback screen asks again, which is the case the ceilings bound.
   """
   silent = CountingProvider(text="")
   world.settings.tutor = silent
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   per_session = tutor.TUTOR_CALLS_PER_SESSION
   per_item = tutor.TUTOR_CALLS_PER_ITEM
   reads = 0
   attempt_ids = []

   while reads <= per_session:
      item = client.get(f"/sessions/{session_id}/next").json()["item"]

      assert item is not None

      attempted = client.post(
         f"/sessions/{session_id}/attempts",
         json={
            "item_id": item["id"],
            "answer": answer_for(item),
            "elapsed_ms": 90000,
            "today": TODAY.isoformat(),
            "confidence": "confident",
         },
      )

      assert attempted.status_code == 200

      attempt_id = attempted.json()["id"]
      attempt_ids.append(attempt_id)

      for _read in range(per_item):
         is_past_the_ceiling = reads > per_session

         if is_past_the_ceiling:
            break

         feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")
         reads += 1

         assert feedback.status_code == 200
         assert feedback.json()["sentence"] is None
         assert feedback.json()["tutor_unavailable"] is False

   assert reads == per_session + 1
   assert silent.calls == per_session

   with OrmSession(world.engine) as db:
      spent = db.scalar(
         select(func.sum(models.Attempt.tutor_calls)).where(models.Attempt.session_id == session_id)
      )

   assert spent == per_session


class RefusingAdapter:
   """An adapter whose request never left, behind the real guard, the way the feedback route
   wires the tutor."""

   def __init__(self):
      self.calls = 0

   def generate(self, request):
      self.calls += 1

      raise RefusedBeforeWire("no key configured")

   def stream(self, request):
      raise RefusedBeforeWire("no key configured")


def compose_through_the_guard(engine, adapter, attempt_id):
   with OrmSession(engine) as db:
      guarded = GuardedProvider(
         adapter,
         db,
         user_id="USR-1",
         caps={"tutor": BudgetCaps(cap_usd=1000.0)},
         provider_name="double",
      )
      attempt = db.get(models.Attempt, attempt_id)
      sentence = tutor.compose_sentence(guarded, make_feedback(), db=db, attempt=attempt)
      db.commit()

   return sentence


def test_a_call_refused_before_the_wire_does_not_use_up_the_items_ceiling():
   engine = open_engine()
   seed_attempts(engine, ["ATT-0001"])
   refusing = RefusingAdapter()

   for _call in range(tutor.TUTOR_CALLS_PER_ITEM):
      assert compose_through_the_guard(engine, refusing, "ATT-0001") is None

   assert refusing.calls == tutor.TUTOR_CALLS_PER_ITEM
   assert stored_attempt(engine, "ATT-0001").tutor_calls == 0

   answering = CountingProvider()
   sentence = compose_in_fresh_session(engine, answering, "ATT-0001")

   assert sentence == SENTENCE
   assert answering.calls == 1
   assert stored_attempt(engine, "ATT-0001").tutor_calls == 1


def test_a_call_that_raised_after_the_wire_through_the_guard_is_counted():
   engine = open_engine()
   seed_attempts(engine, ["ATT-0001"])

   compose_through_the_guard(engine, RaisingProvider(RuntimeError("connection reset mid body")), "ATT-0001")

   assert stored_attempt(engine, "ATT-0001").tutor_calls == 1


def test_the_attempt_counts_the_calls_whose_accounting_reported_a_cached_read():
   """06, attempts: tutor_tokens_cached_read sums the calls that reported, so a served item whose
   calls reported for some and not others is told apart only by this count. A reported zero is a
   report."""
   engine = open_engine()
   seed_attempts(engine, ["ATT-0001"])
   provider = CountingProvider(
      text="",
      accountings=[accounting(1200, None, 0.004), accounting(174, 1100, 0.002), accounting(174, 0, 0.002)],
   )

   for _call in range(3):
      compose_in_fresh_session(engine, provider, "ATT-0001")

   stored = stored_attempt(engine, "ATT-0001")

   assert stored.tutor_calls == 3
   assert stored.tutor_cached_read_reported_calls == 2
   assert stored.tutor_tokens_cached_read == 1100


def fail_before_the_wire_then_answer(engine, monkeypatch, patch_failure):
   """Each failure is tried as many times as the item ceiling allows. None of them reached the
   provider, so none may use up the ceiling, and the answering call after them must go through."""
   silent_adapter = CountingProvider()

   with monkeypatch.context() as patch:
      patch_failure(patch)

      for _call in range(tutor.TUTOR_CALLS_PER_ITEM):
         assert compose_through_the_guard(engine, silent_adapter, "ATT-0001") is None

   assert silent_adapter.calls == 0
   assert stored_attempt(engine, "ATT-0001").tutor_calls == 0

   answering = CountingProvider()
   sentence = compose_through_the_guard(engine, answering, "ATT-0001")

   assert sentence == SENTENCE
   assert answering.calls == 1
   assert stored_attempt(engine, "ATT-0001").tutor_calls == 1


def test_an_unpriced_model_refused_by_the_guard_does_not_use_up_the_items_ceiling(monkeypatch):
   engine = open_engine()
   seed_attempts(engine, ["ATT-0001"])

   def route_to_an_unpriced_model(patch):
      patch.setattr(tutor, "TUTOR_MODEL", "claude-unpriced-model")

   fail_before_the_wire_then_answer(engine, monkeypatch, route_to_an_unpriced_model)


def test_a_missing_template_does_not_use_up_the_items_ceiling(monkeypatch, tmp_path):
   engine = open_engine()
   seed_attempts(engine, ["ATT-0001"])

   def remove_the_template(patch):
      patch.setattr(tutor, "TEMPLATE_PATH", tmp_path / "missing_template.md")

   fail_before_the_wire_then_answer(engine, monkeypatch, remove_the_template)
