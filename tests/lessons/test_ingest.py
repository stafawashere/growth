"""app/lessons/ingest.py and the lesson tables: the storage half of docs/lessons/BUILD-PLAN.md
Slice L1, and invariants L8 to L10 of docs/plan/15-lessons.md, Quality and evaluation. Each
invariant runs first on a fixture that breaks it, so a check that stops firing turns red."""
import json
from datetime import datetime, timezone

from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.db.migrate import apply_additive_migrations, missing_columns
from app.lessons.ingest import ingest_lessons
from tests.lessons.conftest import load_fixture
from tests.lessons.test_check_lessons import PLANTED_DRAW
from tools.check_lessons import Context

LESSON_TABLES = ("lessons", "lesson_verifications", "lesson_state", "lesson_events", "lesson_check_responses")
ATTEMPT_COLUMNS = ("attempts.preceded_by_lesson_id", "attempts.preceded_by_lesson_version")
LESSON_ID = "LSN-CON-02013"
SNAPSHOT_ID = "SNAP-LESSONS"
NOW = datetime(2026, 9, 29, 12, 0, 0, tzinfo=timezone.utc)
RETIRED_ID = "BC-ERR-02014"


def test_a_fresh_database_gets_the_five_lesson_tables(tmp_path):
   engine = models.make_engine(tmp_path / "fresh.db")
   table_names = set(inspect(engine).get_table_names())
   attempt_columns = {column["name"] for column in inspect(engine).get_columns("attempts")}

   assert set(LESSON_TABLES) <= table_names
   assert {"preceded_by_lesson_id", "preceded_by_lesson_version"} <= attempt_columns


def test_an_existing_database_gets_the_two_attempts_columns_additively(tmp_path):
   engine = create_engine(f"sqlite:///{tmp_path / 'existing.db'}")
   models.Base.metadata.create_all(engine)

   with engine.begin() as connection:
      connection.exec_driver_sql("ALTER TABLE attempts DROP COLUMN preceded_by_lesson_id")
      connection.exec_driver_sql("ALTER TABLE attempts DROP COLUMN preceded_by_lesson_version")

   added = apply_additive_migrations(engine)

   assert added == ATTEMPT_COLUMNS
   assert missing_columns(engine) == {}


def signed_off(record):
   record["status"] = "signed_off"
   record["provenance"]["signed_off_by"] = "claude-opus-5-5"
   record["provenance"]["signed_off_at"] = "2026-09-29"

   return record


def write_records(directory, *records):
   directory.mkdir(parents=True, exist_ok=True)

   for record in records:
      (directory / f"{record['id']}.json").write_text(json.dumps(record))

   return directory


def ingest_one(tmp_path, record, context, verification_dir=None):
   engine = models.make_engine(tmp_path / "growth.db")
   directory = write_records(tmp_path / "lessons", record)
   verification = verification_dir if verification_dir is not None else tmp_path / "no_verification"

   with OrmSession(engine) as db:
      results = ingest_lessons(db, directory, context.snapshot, SNAPSHOT_ID, now=NOW, context=context, verification_dir=verification)
      db.commit()

   return engine, results


def stored(engine, lesson_id=LESSON_ID):
   with OrmSession(engine) as db:
      row = db.get(models.Lesson, (lesson_id, 1))
      verifications = db.scalars(select(models.LessonVerification).where(models.LessonVerification.lesson_id == lesson_id)).all()
      audits = db.scalars(select(models.AuditLog.action).where(models.AuditLog.subject == f"lessons:{lesson_id}@1")).all()

      return row, [(row.check_type, row.outcome) for row in verifications], list(audits)


def failed_checks(verifications):
   return {check_type for check_type, outcome in verifications if outcome == "fail"}


def test_a_clean_signed_off_record_is_stored_signed_off(tmp_path, context, hand_authored):
   engine, results = ingest_one(tmp_path, signed_off(hand_authored), context)
   row, verifications, audits = stored(engine)

   assert results[0]["status"] == "signed_off"
   assert row.status == "signed_off"
   assert row.kind == "con"
   assert row.body["id"] == LESSON_ID
   assert row.read_minutes_full == hand_authored["read_minutes"]["full"]
   assert failed_checks(verifications) == set()
   assert ("delivery", "pass") in verifications
   assert audits == ["lesson_signed_off"]


def test_ingesting_twice_rewrites_in_place_and_audits_once(tmp_path, context, hand_authored):
   engine = models.make_engine(tmp_path / "growth.db")
   directory = write_records(tmp_path / "lessons", signed_off(hand_authored))

   for _ in range(2):
      with OrmSession(engine) as db:
         ingest_lessons(db, directory, context.snapshot, SNAPSHOT_ID, now=NOW, context=context, verification_dir=tmp_path)
         db.commit()

   row, verifications, audits = stored(engine)

   assert row.status == "signed_off"
   assert len(verifications) == len(set(verifications))
   assert audits == ["lesson_signed_off"]


def test_the_hand_authored_draft_is_stored_and_not_signed_off(tmp_path, context, hand_authored):
   engine, results = ingest_one(tmp_path, hand_authored, context)
   row, _, audits = stored(engine)

   assert row.status == "draft"
   assert audits == []


def test_l8_a_record_citing_an_inactive_id_is_stale(tmp_path, context, hand_authored):
   record = signed_off(hand_authored)
   key_idea = next(section for section in record["sections"] if section["type"] == "key_ideas")
   key_idea["text"] = key_idea["text"] + f" See {RETIRED_ID}."
   engine, _ = ingest_one(tmp_path, record, context)
   row, verifications, audits = stored(engine)

   assert row.status == "stale"
   assert ("stale", "fail") in verifications
   assert audits == ["lesson_stale"]


def test_l8_a_record_whose_sources_moved_is_stale(tmp_path, context, hand_authored):
   record = signed_off(hand_authored)
   record["source_digest"] = "0" * 64
   engine, _ = ingest_one(tmp_path, record, context)
   row, _, audits = stored(engine)

   assert row.status == "stale"
   assert audits == ["lesson_stale"]


def planted(file_name, hand_authored):
   """A red fixture with the current source digest, so the one planted defect is all it carries."""
   record = signed_off(load_fixture(file_name))
   record["source_digest"] = hand_authored["source_digest"]

   return record


def test_l9_a_worked_step_that_does_not_follow_is_not_signed_off(tmp_path, context, hand_authored):
   engine, _ = ingest_one(tmp_path, planted("red_step_equivalence.json", hand_authored), context)
   row, verifications, audits = stored(engine)

   assert row.status == "draft"
   assert "step_equivalence" in failed_checks(verifications)
   assert audits == []


def verification_file(directory, verdicts):
   directory.mkdir(parents=True, exist_ok=True)
   payload = {"resolve": {"all_agree": all(agree for _, agree in verdicts), "verdicts": [{"id": problem_id, "agree": agree} for problem_id, agree in verdicts]}}
   (directory / f"{LESSON_ID}.json").write_text(json.dumps(payload))

   return directory


def test_l9_a_key_without_an_agreeing_re_solve_is_not_signed_off(tmp_path, context, hand_authored):
   verdicts = [(f"{LESSON_ID}#ex-1", True), (f"{LESSON_ID}#ex-2", False), (f"{LESSON_ID}#chk-1", True), (f"{LESSON_ID}#chk-2", True)]
   directory = verification_file(tmp_path / "verification", verdicts)
   engine, _ = ingest_one(tmp_path, signed_off(hand_authored), context, verification_dir=directory)
   row, verifications, _ = stored(engine)

   assert row.status == "draft"
   assert "resolve" in failed_checks(verifications)


def test_l9_every_key_agreeing_keeps_the_record_signed_off(tmp_path, context, hand_authored):
   verdicts = [(f"{LESSON_ID}#{block}", True) for block in ("ex-1", "ex-2", "chk-1", "chk-2", "chk-3")]
   directory = verification_file(tmp_path / "verification", verdicts)
   engine, _ = ingest_one(tmp_path, signed_off(hand_authored), context, verification_dir=directory)
   row, verifications, _ = stored(engine)

   assert row.status == "signed_off"
   assert ("resolve", "pass") in verifications


def test_l10_a_draw_equal_to_a_published_item_is_not_signed_off(tmp_path, snapshot, hand_authored):
   bank = tmp_path / "content" / "items_planted"
   bank.mkdir(parents=True)
   twin = {"id": "ITM-PLANTED-00", "archetype_id": "BC-QA-02008", "parameter_draw": PLANTED_DRAW}
   (bank / "ITM-PLANTED-00.json").write_text(json.dumps(twin))
   planted_context = Context(snapshot, content_dir=tmp_path / "content")
   engine, _ = ingest_one(tmp_path, planted("red_draw_exclusion.json", hand_authored), planted_context)
   row, verifications, _ = stored(engine)

   assert row.status == "draft"
   assert "draw_exclusion" in failed_checks(verifications)


def test_a_record_failing_the_schema_is_not_stored(tmp_path, context):
   engine, results = ingest_one(tmp_path, signed_off(load_fixture("red_schema__delivery.json")), context)
   row, verifications, _ = stored(engine)

   assert results[0]["status"] is None
   assert row is None
   assert failed_checks(verifications) == {"schema"}


def test_a_pooled_lint_gives_the_serial_findings_in_record_order(context, monkeypatch):
   from app.lessons import ingest

   records = [load_fixture("red_style.json"), load_fixture("resolve/LSN-CON-02013.json"), load_fixture("red_error_blocks.json")]
   serial = ingest.lint_records(records, context.snapshot, context)
   monkeypatch.setattr(ingest, "PARALLEL_LINT_MIN_RECORDS", 1)
   monkeypatch.setattr(ingest, "PARALLEL_LINT_WORKERS_MAX", 2)
   pooled = ingest.lint_records(records, context.snapshot, None)

   assert [findings for findings, _ in pooled] == [findings for findings, _ in serial]
   assert "style" in pooled[0][0]
   assert pooled[1][0] == {}
