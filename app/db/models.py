"""The 14 P1 tables from docs/plan/06-architecture.md, "Data model", plus the two the passkey
layer of docs/plan/09-security-and-privacy.md needs and 06 leaves unlisted: passkey_credentials
and auth_sessions.

gradings and diagnoses are not P1 tables: they arrive with the grader and the
diagnostician in P3, per docs/plan/11-phased-delivery.md.
"""
from sqlalchemy import JSON, Integer, LargeBinary, Text, event, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
   pass


class User(Base):
   __tablename__ = "users"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   display_name: Mapped[str | None] = mapped_column(Text, nullable=True)
   exam_date: Mapped[str] = mapped_column(Text, nullable=False, default="2027-05-10")
   purge_after: Mapped[str | None] = mapped_column(Text, nullable=True)
   recovery_code_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class ProviderConfig(Base):
   __tablename__ = "provider_configs"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   user_id: Mapped[str] = mapped_column(Text, nullable=False)
   provider: Mapped[str] = mapped_column(Text, nullable=False)
   enabled: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   key_ciphertext: Mapped[bytes | None] = mapped_column(nullable=True)
   key_nonce: Mapped[bytes | None] = mapped_column(nullable=True)
   base_url: Mapped[str | None] = mapped_column(Text, nullable=True)
   model_map: Mapped[str | None] = mapped_column(Text, nullable=True)
   options: Mapped[str | None] = mapped_column(Text, nullable=True)
   last_verified_at: Mapped[str | None] = mapped_column(Text, nullable=True)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class ContentSnapshot(Base):
   __tablename__ = "content_snapshots"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   loaded_at: Mapped[str] = mapped_column(Text, nullable=False)
   library_commit: Mapped[str | None] = mapped_column(Text, nullable=True)
   digest: Mapped[str] = mapped_column(Text, nullable=False)
   counts: Mapped[str] = mapped_column(Text, nullable=False)
   status: Mapped[str] = mapped_column(Text, nullable=False)
   rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class SkillState(Base):
   __tablename__ = "skills_state"

   user_id: Mapped[str] = mapped_column(Text, primary_key=True)
   skill_id: Mapped[str] = mapped_column(Text, primary_key=True)
   snapshot_id: Mapped[str] = mapped_column(Text, nullable=False)
   beta: Mapped[float] = mapped_column(nullable=False)
   credited_successes: Mapped[float] = mapped_column(nullable=False, default=0.0)
   credited_failures: Mapped[float] = mapped_column(nullable=False, default=0.0)
   stability: Mapped[float | None] = mapped_column(nullable=True)
   difficulty: Mapped[float | None] = mapped_column(nullable=True)
   last_practised_at: Mapped[str | None] = mapped_column(Text, nullable=True)
   fading_stage: Mapped[str] = mapped_column(Text, nullable=False)
   observation_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   credited_observation_count: Mapped[int] = mapped_column(
      Integer, nullable=False, default=0, server_default=text("0")
   )
   distinct_archetypes_succeeded: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
   success_days: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
   mastered: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   mastered_at: Mapped[str | None] = mapped_column(Text, nullable=True)
   hypercorrection_due: Mapped[str | None] = mapped_column(Text, nullable=True)
   consecutive_successes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   consecutive_failures: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   concept_opener_done: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   unaided_success_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class Item(Base):
   __tablename__ = "items"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   archetype_id: Mapped[str] = mapped_column(Text, nullable=False)
   variant_id: Mapped[str | None] = mapped_column(Text, nullable=True)
   snapshot_id: Mapped[str] = mapped_column(Text, nullable=False)
   parameter_draw: Mapped[str] = mapped_column(Text, nullable=False)
   stem: Mapped[str] = mapped_column(Text, nullable=False)
   figure_spec: Mapped[str | None] = mapped_column(Text, nullable=True)
   options: Mapped[list | None] = mapped_column(JSON, nullable=True)
   answer_key: Mapped[str] = mapped_column(Text, nullable=False)
   worked_solution: Mapped[str] = mapped_column(Text, nullable=False)
   calculator_status: Mapped[str] = mapped_column(Text, nullable=False)
   representation: Mapped[str] = mapped_column(Text, nullable=False)
   difficulty_settings: Mapped[str] = mapped_column(Text, nullable=False)
   skills: Mapped[str] = mapped_column(Text, nullable=False)
   provenance: Mapped[str] = mapped_column(Text, nullable=False)
   status: Mapped[str] = mapped_column(Text, nullable=False)
   dedupe_minhash: Mapped[str] = mapped_column(Text, nullable=False)
   dedupe_embedding: Mapped[bytes | None] = mapped_column(nullable=True)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class ItemVerification(Base):
   __tablename__ = "item_verifications"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   item_id: Mapped[str] = mapped_column(Text, nullable=False)
   check_type: Mapped[str] = mapped_column(Text, nullable=False)
   outcome: Mapped[str] = mapped_column(Text, nullable=False)
   detail: Mapped[str | None] = mapped_column(Text, nullable=True)
   model_id: Mapped[str | None] = mapped_column(Text, nullable=True)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class Session(Base):
   __tablename__ = "sessions"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   user_id: Mapped[str] = mapped_column(Text, nullable=False)
   mode: Mapped[str] = mapped_column(Text, nullable=False)
   sub_mode: Mapped[str | None] = mapped_column(Text, nullable=True)
   started_at: Mapped[str] = mapped_column(Text, nullable=False)
   ended_at: Mapped[str | None] = mapped_column(Text, nullable=True)
   queue: Mapped[str] = mapped_column(Text, nullable=False)
   updates_mastery: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
   snapshot_id: Mapped[str] = mapped_column(Text, nullable=False)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class Judgment(Base):
   __tablename__ = "judgments"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   user_id: Mapped[str] = mapped_column(Text, nullable=False)
   session_id: Mapped[str] = mapped_column(Text, nullable=False)
   scope: Mapped[str] = mapped_column(Text, nullable=False)
   scope_id: Mapped[str] = mapped_column(Text, nullable=False)
   predicted_retention: Mapped[float] = mapped_column(nullable=False)
   made_at: Mapped[str] = mapped_column(Text, nullable=False)
   outcome_attempt_id: Mapped[str | None] = mapped_column(Text, nullable=True)
   outcome_correct: Mapped[int | None] = mapped_column(Integer, nullable=True)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class Attempt(Base):
   __tablename__ = "attempts"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   session_id: Mapped[str] = mapped_column(Text, nullable=False)
   item_id: Mapped[str] = mapped_column(Text, nullable=False)
   started_at: Mapped[str] = mapped_column(Text, nullable=False)
   submitted_at: Mapped[str | None] = mapped_column(Text, nullable=True)
   response: Mapped[str | None] = mapped_column(Text, nullable=True)
   confidence: Mapped[str | None] = mapped_column(Text, nullable=True)
   elapsed_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
   image_ids: Mapped[str | None] = mapped_column(Text, nullable=True)
   transcription: Mapped[str | None] = mapped_column(Text, nullable=True)
   transcription_confirmed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   correct: Mapped[int | None] = mapped_column(Integer, nullable=True)
   p_split: Mapped[float | None] = mapped_column(nullable=True)
   p_compensatory: Mapped[float | None] = mapped_column(nullable=True)
   served_stage: Mapped[str] = mapped_column(Text, nullable=False)
   format: Mapped[str] = mapped_column(Text, nullable=False)
   per_skill_states: Mapped[str] = mapped_column(Text, nullable=False)
   error_note: Mapped[str | None] = mapped_column(Text, nullable=True)
   self_explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
   tutor_sentence: Mapped[str | None] = mapped_column(Text, nullable=True)
   tutor_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
   tutor_cost_usd: Mapped[float | None] = mapped_column(nullable=True)
   tutor_tokens_in: Mapped[int | None] = mapped_column(Integer, nullable=True)
   tutor_tokens_cached_read: Mapped[int | None] = mapped_column(Integer, nullable=True)
   tutor_cached_read_reported_calls: Mapped[int] = mapped_column(
      Integer, nullable=False, default=0, server_default=text("0")
   )
   snapshot_id: Mapped[str] = mapped_column(Text, nullable=False)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class PendingProbe(Base):
   __tablename__ = "pending_probes"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   user_id: Mapped[str] = mapped_column(Text, nullable=False)
   archetype_id: Mapped[str] = mapped_column(Text, nullable=False)
   diagnosis_id: Mapped[str] = mapped_column(Text, nullable=False)
   enqueued_at: Mapped[str] = mapped_column(Text, nullable=False)
   expires_at: Mapped[str] = mapped_column(Text, nullable=False)
   served_at: Mapped[str | None] = mapped_column(Text, nullable=True)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class ReviewQueue(Base):
   __tablename__ = "review_queue"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   kind: Mapped[str] = mapped_column(Text, nullable=False)
   ref_id: Mapped[str] = mapped_column(Text, nullable=False)
   opened_at: Mapped[str] = mapped_column(Text, nullable=False)
   resolved_at: Mapped[str | None] = mapped_column(Text, nullable=True)
   resolution: Mapped[str | None] = mapped_column(Text, nullable=True)
   visible_to_student: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class Job(Base):
   __tablename__ = "jobs"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   type: Mapped[str] = mapped_column(Text, nullable=False)
   payload: Mapped[str] = mapped_column(Text, nullable=False)
   idempotency_key: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
   state: Mapped[str] = mapped_column(Text, nullable=False)
   attempts_made: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   lease_expires_at: Mapped[str | None] = mapped_column(Text, nullable=True)
   not_before: Mapped[str] = mapped_column(Text, nullable=False)
   last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
   priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class Budget(Base):
   __tablename__ = "budgets"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   user_id: Mapped[str] = mapped_column(Text, nullable=False)
   role: Mapped[str] = mapped_column(Text, nullable=False)
   day: Mapped[str] = mapped_column(Text, nullable=False)
   tokens_in: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   tokens_out: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   tokens_cached_read: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   tokens_cached_write: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   cost_usd: Mapped[float] = mapped_column(nullable=False, default=0.0)
   cap_tokens: Mapped[float | None] = mapped_column(nullable=True)
   cap_usd: Mapped[float | None] = mapped_column(nullable=True)
   hard_stopped: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   settled_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
   cached_read_reported_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
   cached_write_reported_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
   stopped_by: Mapped[str | None] = mapped_column(Text, nullable=True)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class AuditLog(Base):
   __tablename__ = "audit_log"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   at: Mapped[str] = mapped_column(Text, nullable=False)
   actor: Mapped[str] = mapped_column(Text, nullable=False)
   action: Mapped[str] = mapped_column(Text, nullable=False)
   subject: Mapped[str] = mapped_column(Text, nullable=False)
   detail: Mapped[str | None] = mapped_column(Text, nullable=True)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class PasskeyCredential(Base):
   """A registered authenticator, per docs/plan/09-security-and-privacy.md, "Registration"."""

   __tablename__ = "passkey_credentials"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   user_id: Mapped[str] = mapped_column(Text, nullable=False)
   credential_id: Mapped[bytes] = mapped_column(LargeBinary, nullable=False, unique=True)
   public_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
   sign_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   transports: Mapped[str | None] = mapped_column(Text, nullable=True)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


class AuthSession(Base):
   """A cookie session and the short-lived re-authentication token it may carry.

   Both tokens are stored as sha256 hashes; the raw values exist only in the response that issues
   them and in the client cookie or request body that returns them.
   """

   __tablename__ = "auth_sessions"

   id: Mapped[str] = mapped_column(Text, primary_key=True)
   user_id: Mapped[str] = mapped_column(Text, nullable=False)
   token_hash: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
   expires_at: Mapped[str] = mapped_column(Text, nullable=False)
   reauth_token_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
   reauth_expires_at: Mapped[str | None] = mapped_column(Text, nullable=True)
   created_at: Mapped[str] = mapped_column(Text, nullable=False)
   updated_at: Mapped[str] = mapped_column(Text, nullable=False)


def make_engine(path):
   from sqlalchemy import create_engine

   from app.db.migrate import apply_additive_migrations, repair_wrapped_stems

   engine = create_engine(f"sqlite:///{path}")

   @event.listens_for(engine, "connect")
   def _enable_wal(dbapi_connection, connection_record):
      cursor = dbapi_connection.cursor()
      cursor.execute("PRAGMA journal_mode=WAL")
      cursor.close()

   Base.metadata.create_all(engine)

   apply_additive_migrations(engine)
   repair_wrapped_stems(engine)

   return engine
