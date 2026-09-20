"""Tests for app/review/audit.py, the item_audit writer and the key error rate of eval 29 in
docs/plan/11-phased-delivery.md.

The 100-item operator sample does not exist yet, so the sample size is a parameter and these
tests drive a small synthetic verdict set.
"""
import json

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.review import audit

NOW = "2026-09-19T09:00:00+00:00"
LATER = "2026-09-20T09:00:00+00:00"


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

      clean_row = audit.record_item_audit_verdict(db, "ITM-0002", audit.VERDICT_CLEAN, LATER)
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

   with open_db(tmp_path) as db:
      for item_id, verdict, second_answer in verdicts:
         audit.record_item_audit_verdict(db, item_id, verdict, LATER, second_answer=second_answer)

      db.commit()

      report_path = tmp_path / "key_error_rate.json"
      measurement = audit.publish_key_error_rate(db, 5, LATER, report_path=report_path)

      assert measurement["sample_size"] == 5
      assert measurement["verdicts_recorded"] == 5
      assert measurement["verdicts_complete"] is True
      assert measurement["key_errors"] == 2
      assert measurement["key_error_rate"] == 0.4

      published = json.loads(report_path.read_text())

      assert published == measurement

      short = audit.key_error_rate(db, 6)

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
