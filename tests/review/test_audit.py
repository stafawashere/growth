"""Tests for app/review/audit.py, the item_audit writer and the key error rate of eval 29 in
docs/plan/11-phased-delivery.md.

The 100-item operator sample does not exist yet, so these tests draw a small synthetic sample and
name its size.
"""
import json
import re
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.review import audit

NOW = "2026-09-19T09:00:00+00:00"
LATER = "2026-09-20T09:00:00+00:00"
ROOT = Path(__file__).resolve().parents[2]
FIVE_ITEM_SAMPLE = ["ITM-0001", "ITM-0002", "ITM-0003", "ITM-0004", "ITM-0005"]


def open_db(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   return OrmSession(engine)


def test_item_audit_verdict_recorded(tmp_path):
   with open_db(tmp_path) as db:
      audit.open_item_audit(db, "ITM-0001", NOW)
      row = audit.record_item_audit_verdict(
         db,
         "ITM-0001",
         audit.VERDICT_AMBIGUOUS,
         LATER,
         sample_ids=FIVE_ITEM_SAMPLE,
         second_answer="2x + C",
      )
      db.commit()

      assert row.kind == "item_audit"
      assert row.ref_id == "ITM-0001"
      assert row.resolved_at == LATER

      resolution = json.loads(row.resolution)

      assert resolution["verdict"] == audit.VERDICT_AMBIGUOUS
      assert resolution["second_answer"] == "2x + C"

      entries = db.query(models.AuditLog).all()

      assert len(entries) == 1
      assert entries[0].action == "review_queue_item_resolved"
      assert entries[0].subject == f"review_queue:{row.id}"

      clean_row = audit.record_item_audit_verdict(
         db, "ITM-0002", audit.VERDICT_CLEAN, LATER, sample_ids=FIVE_ITEM_SAMPLE
      )
      db.commit()

      assert json.loads(clean_row.resolution)["second_answer"] is None


def test_key_error_rate_published_over_the_recorded_verdicts(tmp_path):
   verdicts = [
      ("ITM-0001", audit.VERDICT_KEY_WRONG, None),
      ("ITM-0002", audit.VERDICT_AMBIGUOUS, "x^2 + C"),
      ("ITM-0003", audit.VERDICT_CLEAN, None),
      ("ITM-0004", audit.VERDICT_CLEAN, None),
      ("ITM-0005", audit.VERDICT_CLEAN, None),
   ]
   sample_ids = FIVE_ITEM_SAMPLE

   with open_db(tmp_path) as db:
      for item_id, verdict, second_answer in verdicts:
         audit.record_item_audit_verdict(
            db, item_id, verdict, LATER, sample_ids=sample_ids, second_answer=second_answer
         )

      db.commit()

      report_path = tmp_path / "key_error_rate.json"
      measurement = audit.publish_key_error_rate(
         db, sample_ids, LATER, report_path=report_path, sample_size=5
      )

      assert measurement["sample_size"] == 5
      assert measurement["verdicts_recorded"] == 5
      assert measurement["verdicts_complete"] is True
      assert measurement["key_errors"] == 2
      assert measurement["key_error_rate"] == 0.4

      published = json.loads(report_path.read_text())

      assert published == measurement

      short = audit.key_error_rate(db, sample_ids + ["ITM-0006"], sample_size=6)

      assert short["verdicts_complete"] is False
      assert short["verdicts_recorded"] == 5


def test_an_indeterminate_verification_row_stays_out_of_the_audit_sample(tmp_path):
   """Only the operator's item_audit verdicts count towards the published key error rate."""
   with open_db(tmp_path) as db:
      db.add(
         models.ReviewQueue(
            id="RVQ-9001",
            kind="item_verification_disagreement",
            ref_id="ITM-9001",
            opened_at=NOW,
            resolved_at=NOW,
            resolution="checked by hand",
            visible_to_student=0,
            created_at=NOW,
            updated_at=NOW,
         )
      )
      db.commit()

      assert audit.recorded_verdicts(db) == []


def test_an_incomplete_sample_publishes_no_rate(tmp_path):
   """Exit criterion 4 asks for a rate measured over the whole audited sample, so a short set of
   verdicts is flagged incomplete and carries no rate, neither divided by the sample nor by the
   verdicts that happen to exist."""
   verdicts = [
      ("ITM-0001", audit.VERDICT_KEY_WRONG, None),
      ("ITM-0002", audit.VERDICT_AMBIGUOUS, "x^2 + C"),
      ("ITM-0003", audit.VERDICT_CLEAN, None),
      ("ITM-0004", audit.VERDICT_CLEAN, None),
      ("ITM-0005", audit.VERDICT_CLEAN, None),
   ]
   sample_ids = [f"ITM-{number:04d}" for number in range(1, 11)]

   with open_db(tmp_path) as db:
      for item_id, verdict, second_answer in verdicts:
         audit.record_item_audit_verdict(
            db, item_id, verdict, LATER, sample_ids=sample_ids, second_answer=second_answer
         )

      db.flush()

      measurement = audit.key_error_rate(db, sample_ids, sample_size=10)

      assert measurement["verdicts_recorded"] == 5
      assert measurement["verdicts_complete"] is False
      assert measurement["key_errors"] == 2
      assert measurement["key_error_rate"] is None


def test_the_default_sample_size_is_the_one_eval_29_names(tmp_path):
   plan_text = (ROOT / "docs" / "plan" / "11-phased-delivery.md").read_text()
   named_sizes = set(re.findall(r"On a (\d+)-item sample", plan_text))

   assert len(named_sizes) == 1

   named_size = int(named_sizes.pop())
   sample_ids = [f"ITM-{number:04d}" for number in range(1, named_size + 1)]

   with open_db(tmp_path) as db:
      measurement = audit.key_error_rate(db, sample_ids)

      with pytest.raises(ValueError):
         audit.key_error_rate(db, sample_ids[:-1])

   assert measurement["sample_size"] == named_size


def test_a_sample_size_of_zero_is_refused(tmp_path):
   with open_db(tmp_path) as db:
      with pytest.raises(ValueError):
         audit.key_error_rate(db, [], sample_size=0)


def test_a_row_of_another_kind_is_not_resolved_as_an_item_audit(tmp_path):
   with open_db(tmp_path) as db:
      row = models.ReviewQueue(
         id="RVQ-9002",
         kind="item_verification_disagreement",
         ref_id="ITM-9002",
         opened_at=NOW,
         resolved_at=None,
         resolution=None,
         visible_to_student=0,
         created_at=NOW,
         updated_at=NOW,
      )
      db.add(row)
      db.flush()

      with pytest.raises(ValueError):
         audit.resolve_item_audit_row(db, row, audit.VERDICT_CLEAN, LATER)

      assert row.resolved_at is None
      assert db.query(models.AuditLog).count() == 0


def test_a_resolved_item_audit_row_is_not_resolved_again(tmp_path):
   with open_db(tmp_path) as db:
      row = audit.open_item_audit(db, "ITM-9003", NOW)
      audit.resolve_item_audit_row(db, row, audit.VERDICT_CLEAN, NOW)

      with pytest.raises(ValueError):
         audit.resolve_item_audit_row(db, row, audit.VERDICT_KEY_WRONG, LATER)

      db.expire_all()
      stored = db.execute(
         select(models.ReviewQueue.resolved_at, models.ReviewQueue.resolution)
         .where(models.ReviewQueue.id == row.id)
      ).one()

      assert stored.resolved_at == NOW
      assert json.loads(stored.resolution)["verdict"] == audit.VERDICT_CLEAN
      assert db.query(models.AuditLog).count() == 1


def test_a_verdict_outside_the_sample_is_refused(tmp_path):
   with open_db(tmp_path) as db:
      with pytest.raises(audit.VerdictOutsideSample):
         audit.record_item_audit_verdict(
            db, "ITM-0099", audit.VERDICT_KEY_WRONG, LATER, sample_ids=FIVE_ITEM_SAMPLE
         )

      db.flush()

      assert issubclass(audit.VerdictOutsideSample, ValueError)
      assert db.query(models.ReviewQueue).count() == 0
      assert db.query(models.AuditLog).count() == 0


def test_verdicts_beyond_the_sample_neither_complete_it_nor_lift_the_rate_above_one(tmp_path):
   """A row resolved through the review queue carries neither the sample check nor the one-verdict
   rule, so a second verdict on a sampled item and a verdict outside the sample can both sit in
   the table. Neither may
   complete the sample or count towards the rate."""
   sample_ids = ["ITM-0001", "ITM-0002"]

   with open_db(tmp_path) as db:
      for item_id in sample_ids:
         audit.record_item_audit_verdict(
            db, item_id, audit.VERDICT_KEY_WRONG, LATER, sample_ids=sample_ids
         )

      duplicate_row = audit.open_item_audit(db, "ITM-0001", NOW)
      audit.resolve_item_audit_row(db, duplicate_row, audit.VERDICT_KEY_WRONG, LATER)

      outside_row = audit.open_item_audit(db, "ITM-0099", NOW)
      audit.resolve_item_audit_row(db, outside_row, audit.VERDICT_KEY_WRONG, LATER)
      db.flush()

      verdicts_on_first_item = [
         verdict for verdict in audit.recorded_verdicts(db) if verdict["item_id"] == "ITM-0001"
      ]

      assert len(verdicts_on_first_item) == 2

      measurement = audit.key_error_rate(db, sample_ids, sample_size=2)

   assert measurement["sample_size"] == 2
   assert measurement["verdicts_complete"] is False
   assert measurement["duplicate_item_ids"] == ["ITM-0001"]
   assert measurement["verdicts_outside_sample"] == 1
   assert measurement["key_errors"] == 1
   assert measurement["key_error_rate"] is None


def test_a_second_verdict_on_an_audited_item_is_refused(tmp_path):
   sample_ids = ["ITM-0001", "ITM-0002"]

   with open_db(tmp_path) as db:
      audit.record_item_audit_verdict(db, "ITM-0001", audit.VERDICT_CLEAN, LATER, sample_ids=sample_ids)
      db.flush()

      with pytest.raises(audit.VerdictAlreadyRecorded):
         audit.record_item_audit_verdict(
            db, "ITM-0001", audit.VERDICT_KEY_WRONG, LATER, sample_ids=sample_ids
         )

      db.flush()
      verdicts_on_first_item = [
         verdict for verdict in audit.recorded_verdicts(db) if verdict["item_id"] == "ITM-0001"
      ]

   assert [verdict["verdict"] for verdict in verdicts_on_first_item] == [audit.VERDICT_CLEAN]


def test_a_complete_sample_publishes_its_rate(tmp_path):
   sample_ids = ["ITM-0001", "ITM-0002"]

   with open_db(tmp_path) as db:
      audit.record_item_audit_verdict(db, "ITM-0001", audit.VERDICT_KEY_WRONG, LATER, sample_ids=sample_ids)
      audit.record_item_audit_verdict(db, "ITM-0002", audit.VERDICT_CLEAN, LATER, sample_ids=sample_ids)
      db.flush()

      measurement = audit.key_error_rate(db, sample_ids, sample_size=2)

   assert measurement["verdicts_complete"] is True
   assert measurement["key_error_rate"] == 0.5


def _synthetic_candidates(count=200, units=10):
   statuses = ["no_calculator"] * 5 + ["either"] * 3 + ["calculator"] * 2

   return [
      {
         "item_id": f"ITM-{index:04d}",
         "unit": f"BC-UNIT-{(index % units) + 1:02d}",
         "calculator_status": statuses[index % len(statuses)],
      }
      for index in range(count)
   ]


def test_draw_key_audit_sample_is_deterministic_for_a_seed():
   candidates = _synthetic_candidates()

   first = audit.draw_key_audit_sample(candidates, rng_seed=2026, sample_size=100)
   second = audit.draw_key_audit_sample(candidates, rng_seed=2026, sample_size=100)

   assert first == second
   assert len(first) == 100
   assert len(set(first)) == 100


def test_draw_key_audit_sample_changes_with_the_seed():
   candidates = _synthetic_candidates()

   drawn_2026 = audit.draw_key_audit_sample(candidates, rng_seed=2026, sample_size=100)
   drawn_7 = audit.draw_key_audit_sample(candidates, rng_seed=7, sample_size=100)

   assert drawn_2026 != drawn_7


def test_draw_key_audit_sample_never_exceeds_the_per_unit_cap():
   candidates = _synthetic_candidates(count=200, units=10)

   drawn = audit.draw_key_audit_sample(candidates, rng_seed=2026, sample_size=100, max_per_unit=15)
   by_unit = {row["item_id"]: row["unit"] for row in candidates}
   unit_counts = {}

   for item_id in drawn:
      unit = by_unit[item_id]
      unit_counts[unit] = unit_counts.get(unit, 0) + 1

   assert all(count <= 15 for count in unit_counts.values())


def test_draw_key_audit_sample_refuses_a_population_smaller_than_the_sample():
   candidates = _synthetic_candidates(count=50)

   with pytest.raises(ValueError):
      audit.draw_key_audit_sample(candidates, rng_seed=2026, sample_size=100)


def test_draw_key_audit_sample_refuses_when_the_unit_cap_makes_the_size_unreachable():
   candidates = _synthetic_candidates(count=150, units=1)

   with pytest.raises(ValueError):
      audit.draw_key_audit_sample(candidates, rng_seed=2026, sample_size=100, max_per_unit=15)
