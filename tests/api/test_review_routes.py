"""Route tests for GET /review-queue and POST /review-queue/{id}/resolve."""
import json

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.items import ingest
from app.review import audit

NOW = "2026-03-01T09:00:00+00:00"
LATER = "2026-03-01T10:00:00+00:00"


def insert_row(world, row_id, kind, ref_id, opened_at, resolved_at=None, resolution=None):
   with OrmSession(world.engine) as db:
      db.add(
         models.ReviewQueue(
            id=row_id,
            kind=kind,
            ref_id=ref_id,
            opened_at=opened_at,
            resolved_at=resolved_at,
            resolution=json.dumps(resolution) if resolution is not None else None,
            visible_to_student=0,
            created_at=opened_at,
            updated_at=opened_at,
         )
      )
      db.commit()


def test_review_queue_lists_open_rows(world):
   client = world.client()
   world.register(client)
   insert_row(world, "RVQ-open-1", "item_audit", "ITM-0001", NOW)
   insert_row(world, "RVQ-open-2", "item_verification_disagreement", "ITM-0002", LATER)
   insert_row(world, "RVQ-closed", "item_audit", "ITM-0003", NOW, resolved_at=LATER, resolution={"verdict": "clean"})

   fetched = client.get("/review-queue")

   assert fetched.status_code == 200

   rows = fetched.json()
   ids = [row["id"] for row in rows]

   assert ids == ["RVQ-open-1", "RVQ-open-2"]
   assert rows[0]["kind"] == "item_audit"
   assert rows[0]["ref_id"] == "ITM-0001"
   assert rows[0]["opened_at"] == NOW
   assert rows[0]["visible_to_student"] == 0
   assert "resolved_at" not in rows[0]


def test_review_queue_requires_the_cookie(world):
   client = world.client()
   world.register(client)
   client.cookies.clear()

   assert client.get("/review-queue").status_code == 401


def test_resolve_records_the_operator_verdict(world):
   client = world.client()
   world.register(client)
   world.settings.key_audit_sample_ids = ["ITM-0010"]
   insert_row(world, "RVQ-audit-1", "item_audit", "ITM-0010", NOW)

   resolved = client.post(
      "/review-queue/RVQ-audit-1/resolve",
      json={"verdict": audit.VERDICT_KEY_WRONG},
   )

   assert resolved.status_code == 200
   assert resolved.json()["resolved_at"] is not None
   assert resolved.json()["resolution"]["verdict"] == audit.VERDICT_KEY_WRONG

   with OrmSession(world.engine) as db:
      row = db.get(models.ReviewQueue, "RVQ-audit-1")

      assert row.resolved_at is not None
      assert json.loads(row.resolution)["verdict"] == audit.VERDICT_KEY_WRONG

      rate = audit.key_error_rate(db, ["ITM-0010"], sample_size=1)

      assert rate["verdicts_recorded"] == 1
      assert rate["key_errors"] == 1

      entries = db.query(models.AuditLog).filter(models.AuditLog.subject == "review_queue:RVQ-audit-1").all()

      assert len(entries) == 1
      assert entries[0].action == "review_queue_item_resolved"

   insert_row(world, "RVQ-disagreement-1", "item_verification_disagreement", "ITM-0011", NOW)
   generic_resolved = client.post(
      "/review-queue/RVQ-disagreement-1/resolve",
      json={"resolution": "operator confirmed the symbolic mismatch is real"},
   )

   assert generic_resolved.status_code == 200
   assert generic_resolved.json()["resolved_at"] is not None

   with OrmSession(world.engine) as db:
      row = db.get(models.ReviewQueue, "RVQ-disagreement-1")

      assert row.resolved_at is not None

      entries = db.query(models.AuditLog).filter(
         models.AuditLog.subject == "review_queue:RVQ-disagreement-1"
      ).all()

      assert len(entries) == 1


def test_resolve_refuses_an_unknown_row(world):
   client = world.client()
   world.register(client)

   resolved = client.post("/review-queue/RVQ-does-not-exist/resolve", json={"verdict": "clean"})

   assert resolved.status_code == 404


def test_resolve_refuses_a_row_already_resolved(world):
   client = world.client()
   world.register(client)
   insert_row(
      world,
      "RVQ-already",
      "item_audit",
      "ITM-0020",
      NOW,
      resolved_at=LATER,
      resolution={"verdict": "clean", "second_answer": None},
   )

   resolved = client.post(
      "/review-queue/RVQ-already/resolve",
      json={"verdict": audit.VERDICT_CLEAN},
   )

   assert resolved.status_code == 409


def test_resolve_refuses_an_unknown_verdict(world):
   """An unknown verdict is a bad request, not a crash out of the audit writer."""
   client = world.client()
   world.register(client)
   world.settings.key_audit_sample_ids = ["ITM-0009"]
   row_id = "RVQ-verdict-1"
   insert_row(world, row_id, "item_audit", "ITM-0009", NOW)
   refused = client.post(f"/review-queue/{row_id}/resolve", json={"verdict": "bogus"})

   assert refused.status_code == 400

   empty = client.post(f"/review-queue/{row_id}/resolve", json={})

   assert empty.status_code == 400


def test_resolving_an_item_audit_without_a_configured_sample_is_refused(world):
   client = world.client()
   world.register(client)
   insert_row(world, "RVQ-no-sample", "item_audit", "ITM-0050", NOW)

   refused = client.post(
      "/review-queue/RVQ-no-sample/resolve",
      json={"verdict": audit.VERDICT_CLEAN},
   )

   assert refused.status_code == 400

   with OrmSession(world.engine) as db:
      row = db.get(models.ReviewQueue, "RVQ-no-sample")

      assert row.resolved_at is None


def test_resolving_an_item_audit_outside_the_sample_is_refused(world):
   client = world.client()
   world.register(client)
   world.settings.key_audit_sample_ids = ["ITM-0060"]
   insert_row(world, "RVQ-outside-sample", "item_audit", "ITM-0061", NOW)

   refused = client.post(
      "/review-queue/RVQ-outside-sample/resolve",
      json={"verdict": audit.VERDICT_CLEAN},
   )

   assert refused.status_code == 400

   with OrmSession(world.engine) as db:
      row = db.get(models.ReviewQueue, "RVQ-outside-sample")

      assert row.resolved_at is None


def test_a_second_verdict_on_an_already_audited_item_through_a_new_row_is_refused(world):
   client = world.client()
   world.register(client)
   world.settings.key_audit_sample_ids = ["ITM-0070"]
   insert_row(
      world,
      "RVQ-audited-already",
      "item_audit",
      "ITM-0070",
      NOW,
      resolved_at=LATER,
      resolution={"verdict": audit.VERDICT_CLEAN, "second_answer": None},
   )
   insert_row(world, "RVQ-second-attempt", "item_audit", "ITM-0070", LATER)

   refused = client.post(
      "/review-queue/RVQ-second-attempt/resolve",
      json={"verdict": audit.VERDICT_KEY_WRONG},
   )

   assert refused.status_code == 400

   with OrmSession(world.engine) as db:
      row = db.get(models.ReviewQueue, "RVQ-second-attempt")

      assert row.resolved_at is None


def test_resolving_a_row_logs_the_row_own_kind(world):
   """09 records a review queue item resolved, and the entry has to say which kind of row it was."""
   client = world.client()
   world.register(client)
   insert_row(world, "RVQ-kind-1", ingest.REVIEW_KIND, "ITM-0030", NOW)

   resolved = client.post(
      "/review-queue/RVQ-kind-1/resolve",
      json={"resolution": "operator settled the comparison by hand"},
   )

   assert resolved.status_code == 200

   with OrmSession(world.engine) as db:
      entries = db.query(models.AuditLog).filter(
         models.AuditLog.subject == "review_queue:RVQ-kind-1"
      ).all()

      assert len(entries) == 1
      assert json.loads(entries[0].detail)["kind"] == ingest.REVIEW_KIND


def test_resolving_an_item_audit_resolves_exactly_the_named_row(world):
   client = world.client()
   world.register(client)
   world.settings.key_audit_sample_ids = ["ITM-0040"]
   insert_row(world, "RVQ-same-item-first", audit.KIND, "ITM-0040", NOW)
   insert_row(world, "RVQ-same-item-second", audit.KIND, "ITM-0040", LATER)

   resolved = client.post(
      "/review-queue/RVQ-same-item-second/resolve",
      json={"verdict": audit.VERDICT_CLEAN},
   )

   assert resolved.status_code == 200

   with OrmSession(world.engine) as db:
      named_row = db.get(models.ReviewQueue, "RVQ-same-item-second")
      other_row = db.get(models.ReviewQueue, "RVQ-same-item-first")

      assert named_row.resolved_at is not None
      assert json.loads(named_row.resolution)["verdict"] == audit.VERDICT_CLEAN
      assert other_row.resolved_at is None
      assert other_row.resolution is None

      entries = db.query(models.AuditLog).filter(
         models.AuditLog.action == "review_queue_item_resolved"
      ).all()

      assert [entry.subject for entry in entries] == ["review_queue:RVQ-same-item-second"]
