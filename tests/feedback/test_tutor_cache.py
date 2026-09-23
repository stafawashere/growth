"""The composed sentence is cached on the attempt, so re-reading the feedback screen neither
spends a second tutor call against the budget cap of docs/plan/07-ai-provider-layer.md nor shows
a different sentence than the one the student already read.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy.pool import StaticPool

from app.db import models
from app.engine.state import FadingStage
from app.feedback import render, tutor
from app.providers.base import ProviderResult, Usage

NOW = "2026-09-20T09:00:00+00:00"


class CountingProvider:
   """Counts calls so the no-second-call assertion rests on a number, not on a mock's memory."""

   def __init__(self, text="the derivative of the product is not the product of the derivatives"):
      self.text = text
      self.calls = 0

   def generate(self, request):
      self.calls += 1

      return ProviderResult(
         text=self.text,
         finish_reason="end_turn",
         usage=Usage(
            input_tokens=10,
            output_tokens=10,
            cached_read_tokens=0,
            cached_write_tokens=0,
         ),
         provider="double",
         model=tutor.TUTOR_MODEL,
      )


class FailingProvider:
   def __init__(self):
      self.calls = 0

   def generate(self, request):
      self.calls += 1

      raise RuntimeError("the tutor chain is exhausted")


def open_engine():
   engine = create_engine(
      "sqlite://",
      connect_args={"check_same_thread": False},
      poolclass=StaticPool,
   )
   models.Base.metadata.create_all(engine)

   return engine


def make_attempt(db, attempt_id="ATT-0001"):
   attempt = models.Attempt(
      id=attempt_id,
      session_id="SES-0001",
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


def test_the_first_call_stores_the_sentence_on_the_attempt():
   engine = open_engine()

   with OrmSession(engine) as db:
      attempt = make_attempt(db)
      provider = CountingProvider()

      sentence = tutor.compose_sentence(provider, make_feedback(), db=db, attempt=attempt)

      assert sentence == provider.text
      assert provider.calls == 1
      assert attempt.tutor_sentence == provider.text


def test_a_cached_sentence_is_returned_without_a_second_provider_call():
   engine = open_engine()

   with OrmSession(engine) as db:
      attempt = make_attempt(db)
      provider = CountingProvider()

      first = tutor.compose_sentence(provider, make_feedback(), db=db, attempt=attempt)
      second = tutor.compose_sentence(provider, make_feedback(), db=db, attempt=attempt)

      assert second == first
      assert provider.calls == 1


def test_no_provider_stores_nothing_and_returns_no_sentence():
   engine = open_engine()

   with OrmSession(engine) as db:
      attempt = make_attempt(db)

      sentence = tutor.compose_sentence(None, make_feedback(), db=db, attempt=attempt)

      assert sentence is None
      assert attempt.tutor_sentence is None


def test_a_provider_failure_stores_nothing_and_returns_no_sentence():
   engine = open_engine()

   with OrmSession(engine) as db:
      attempt = make_attempt(db)
      failing = FailingProvider()

      sentence = tutor.compose_sentence(failing, make_feedback(), db=db, attempt=attempt)

      assert sentence is None
      assert attempt.tutor_sentence is None
      assert failing.calls == 1


def test_an_empty_sentence_is_not_cached_and_is_composed_again():
   """An empty string is a provider that said nothing, not a sentence the student read, so it
   falls under the degradation rule rather than being stored as the answer."""
   engine = open_engine()

   with OrmSession(engine) as db:
      attempt = make_attempt(db)
      silent = CountingProvider(text="")

      sentence = tutor.compose_sentence(silent, make_feedback(), db=db, attempt=attempt)

      assert sentence is None
      assert attempt.tutor_sentence is None

      speaking = CountingProvider()
      second = tutor.compose_sentence(speaking, make_feedback(), db=db, attempt=attempt)

      assert second == speaking.text
      assert speaking.calls == 1


def test_the_cached_sentence_is_read_back_through_a_fresh_session():
   engine = open_engine()
   provider = CountingProvider()

   with OrmSession(engine) as db:
      attempt = make_attempt(db)
      tutor.compose_sentence(provider, make_feedback(), db=db, attempt=attempt)
      db.commit()

   with OrmSession(engine) as fresh_db:
      stored = fresh_db.get(models.Attempt, "ATT-0001")

      sentence = tutor.compose_sentence(provider, make_feedback(), db=fresh_db, attempt=stored)

      assert sentence == provider.text
      assert provider.calls == 1


def test_without_a_session_and_attempt_the_function_behaves_as_before():
   provider = CountingProvider()

   sentence = tutor.compose_sentence(provider, make_feedback())

   assert sentence == provider.text
   assert provider.calls == 1