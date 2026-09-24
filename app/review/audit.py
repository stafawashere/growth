"""The item_audit writer and the key error rate of eval 29 in docs/plan/11-phased-delivery.md.

item_audit is the operator's hand-audit verdict on a published item and is the only review_queue
kind P1 writes (docs/plan/06-architecture.md, review_queue). A key error is an item whose stated
key is mathematically wrong or whose stem the operator judged ambiguous enough to admit a second
correct answer, and the ambiguous verdict carries that second answer so the judgement stays
auditable. No pass threshold is set in P1: what is checked is that every verdict exists over the
audited sample and that the rate is published.

Eval 29 defines the rate on "a 100-item sample drawn at random from published P1 items", so the
denominator is the sample size, 100 unless a caller names another, and never the count of verdicts
recorded so far. A short set of verdicts is therefore divided by the whole sample and flagged
incomplete beside it. A verdict is per sampled item: one for an item outside the sample is refused,
and the sample is complete only when every sampled item carries exactly one verdict.
"""
import json
import random
import uuid
from collections import Counter, defaultdict

from sqlalchemy import select

from app.audit.detail import bind_audit_detail
from app.audit.vocabulary import is_known_action
from app.db import models

KIND = "item_audit"

VERDICT_KEY_WRONG = "key_wrong"
VERDICT_AMBIGUOUS = "ambiguous"
VERDICT_CLEAN = "clean"

VERDICTS = (VERDICT_KEY_WRONG, VERDICT_AMBIGUOUS, VERDICT_CLEAN)
KEY_ERROR_VERDICTS = (VERDICT_KEY_WRONG, VERDICT_AMBIGUOUS)

EVAL_29_SAMPLE_SIZE = 100


class VerdictOutsideSample(ValueError):
   pass


class VerdictAlreadyRecorded(ValueError):
   pass


def drawn_sample(sample_ids, sample_size):
   is_a_single_string = isinstance(sample_ids, str)

   if is_a_single_string:
      raise ValueError("the sample is a collection of item ids, not one string")

   listed_ids = list(sample_ids)
   sample = set(listed_ids)
   has_a_sample = sample_size > 0
   holds_each_item_once = len(sample) == len(listed_ids)
   holds_the_named_size = len(sample) == sample_size

   if not has_a_sample:
      raise ValueError(f"the key error rate needs a positive sample size, not {sample_size}")

   if not holds_each_item_once:
      raise ValueError("the sample names an item more than once")

   if not holds_the_named_size:
      raise ValueError(f"the sample holds {len(sample)} items, not the {sample_size} named")

   return sample


MAX_ITEMS_PER_UNIT = 15


def unit_cap_for(candidates, sample_size=EVAL_29_SAMPLE_SIZE, base_cap=MAX_ITEMS_PER_UNIT):
   """10's cap of 15 per unit assumes the mature bank's ten units. A population spanning fewer
   units cannot fill the sample under it (P1's three units hold at most 45 of 100), so the cap
   rises to the smallest value that can, which keeps the draw as even across units as the
   population allows. A population the base cap already fills keeps the base cap. Ruled
   2026-09-23 on the operator's delegated authority (BUILD-LEDGER.md, "Plan corrections applied").
   """
   unit_counts = Counter(row["unit"] for row in candidates)
   largest_unit = max(unit_counts.values(), default=0)
   cap = base_cap

   while True:
      reachable = sum(min(count, cap) for count in unit_counts.values())
      fills_the_sample = reachable >= sample_size
      cannot_rise_further = cap >= largest_unit
      settles = fills_the_sample or cannot_rise_further

      if settles:
         return cap

      cap += 1


def _proportional_targets(counts_by_key, sample_size):
   """Largest-remainder rounding, ties broken by key so the result is deterministic. 10's audit
   section stratifies by calculator status in proportion to the population; this generalises that
   rule to whatever population is passed in, rather than hard-coding the mature 139-archetype
   counts P1's 130 hand-authored items do not share."""
   total = sum(counts_by_key.values())
   raw = {key: sample_size * count / total for key, count in counts_by_key.items()}
   targets = {key: int(value) for key, value in raw.items()}
   remainder = sample_size - sum(targets.values())
   ranked = sorted(counts_by_key, key=lambda key: (-(raw[key] - targets[key]), key))

   for key in ranked[:remainder]:
      targets[key] += 1

   return targets


def draw_key_audit_sample(candidates, rng_seed, sample_size=EVAL_29_SAMPLE_SIZE, max_per_unit=MAX_ITEMS_PER_UNIT):
   """Draws the key-audit sample docs/plan/10-quality-and-evaluation.md describes: stratified by
   unit so no unit contributes more than max_per_unit items, and by calculator_status in
   proportion to the population offered. Deterministic for a given rng_seed and candidate set.

   candidates: an iterable of {"item_id", "unit", "calculator_status"} for every eligible
   (published, in P1 hand-authored) item. Ordering does not matter; candidates are sorted by
   item_id before the seeded shuffle so the draw does not depend on query order.
   """
   ordered = sorted(candidates, key=lambda row: row["item_id"])
   total = len(ordered)

   if total < sample_size:
      raise ValueError(f"only {total} candidate items are offered; the audit needs {sample_size}")

   rng = random.Random(rng_seed)
   by_status = defaultdict(list)

   for row in ordered:
      by_status[row["calculator_status"]].append(row)

   for rows in by_status.values():
      rng.shuffle(rows)

   status_counts = {status: len(rows) for status, rows in by_status.items()}
   targets = _proportional_targets(status_counts, sample_size)

   selected = []
   leftover = []
   unit_counts = Counter()

   for status in sorted(by_status):
      target = targets[status]
      taken = 0

      for row in by_status[status]:
         fits_the_unit_cap = unit_counts[row["unit"]] < max_per_unit

         if taken < target and fits_the_unit_cap:
            selected.append(row)
            unit_counts[row["unit"]] += 1
            taken += 1
         else:
            leftover.append(row)

   rng.shuffle(leftover)

   for row in leftover:
      if len(selected) >= sample_size:
         break

      fits_the_unit_cap = unit_counts[row["unit"]] < max_per_unit

      if fits_the_unit_cap:
         selected.append(row)
         unit_counts[row["unit"]] += 1

   if len(selected) < sample_size:
      raise ValueError(
         f"only {len(selected)} items honour the {max_per_unit}-per-unit cap; {sample_size} were requested"
      )

   return sorted(row["item_id"] for row in selected[:sample_size])


def refuse_outside_sample(item_id, sample_ids):
   is_sampled = item_id in set(sample_ids)

   if not is_sampled:
      raise VerdictOutsideSample(f"{item_id} is not in the drawn audit sample")


def new_id(prefix):
   return f"{prefix}-{uuid.uuid4().hex}"


def open_item_audit(db, item_id, now):
   row = models.ReviewQueue(
      id=new_id("RVQ"),
      kind=KIND,
      ref_id=item_id,
      opened_at=now,
      resolved_at=None,
      resolution=None,
      visible_to_student=0,
      created_at=now,
      updated_at=now,
   )
   db.add(row)
   db.flush()

   return row


def open_row_for(db, item_id):
   statement = (
      select(models.ReviewQueue)
      .where(models.ReviewQueue.kind == KIND)
      .where(models.ReviewQueue.ref_id == item_id)
      .where(models.ReviewQueue.resolved_at.is_(None))
   )

   return db.scalars(statement).first()


def write_resolution_audit_entry(db, row, verdict, now, actor):
   action = "review_queue_item_resolved"

   if not is_known_action(action):
      raise ValueError(f"{action!r} is not in the audit_log vocabulary")

   entry = models.AuditLog(
      id=new_id("AUD"),
      at=now,
      actor=actor,
      action=action,
      subject=f"review_queue:{row.id}",
      detail=json.dumps(bind_audit_detail({"kind": row.kind, "ref_id": row.ref_id, "verdict": verdict})),
      created_at=now,
      updated_at=now,
   )
   db.add(entry)


def refuse_unusable_verdict(item_id, verdict, second_answer):
   is_known_verdict = verdict in VERDICTS

   if not is_known_verdict:
      raise ValueError(f"unknown item audit verdict: {verdict!r}")

   is_ambiguous = verdict == VERDICT_AMBIGUOUS
   has_second_answer = second_answer is not None
   missing_second_answer = is_ambiguous and not has_second_answer

   if missing_second_answer:
      raise ValueError(f"ambiguous verdict on {item_id} needs the second answer the operator found")


def resolve_item_audit_row(db, row, verdict, now, second_answer=None, actor="operator"):
   """Resolves exactly the row given, so two open audits of one item never stand in for each other."""
   is_item_audit = row.kind == KIND

   if not is_item_audit:
      raise ValueError(f"review queue row {row.id} is a {row.kind} row, not an item audit")

   is_already_resolved = row.resolved_at is not None

   if is_already_resolved:
      raise ValueError(f"review queue row {row.id} is already resolved")

   refuse_unusable_verdict(row.ref_id, verdict, second_answer)

   row.resolution = json.dumps({"verdict": verdict, "second_answer": second_answer})
   row.resolved_at = now
   row.updated_at = now

   write_resolution_audit_entry(db, row, verdict, now, actor)
   db.flush()

   return row


def resolved_row_for(db, item_id):
   statement = (
      select(models.ReviewQueue)
      .where(models.ReviewQueue.kind == KIND)
      .where(models.ReviewQueue.ref_id == item_id)
      .where(models.ReviewQueue.resolved_at.is_not(None))
   )

   return db.scalars(statement).first()


def refuse_second_verdict(db, item_id):
   already_audited = resolved_row_for(db, item_id) is not None

   if already_audited:
      raise VerdictAlreadyRecorded(f"{item_id} already carries its audit verdict")


def record_item_audit_verdict(db, item_id, verdict, now, *, sample_ids, second_answer=None, actor="operator"):
   """Gate 29 asks for one verdict per sampled item, so a second one is refused rather than
   written beside the first, where it would leave the sample incomplete for good."""
   refuse_outside_sample(item_id, sample_ids)
   refuse_unusable_verdict(item_id, verdict, second_answer)
   refuse_second_verdict(db, item_id)

   row = open_row_for(db, item_id)
   has_open_row = row is not None

   if not has_open_row:
      row = open_item_audit(db, item_id, now)

   return resolve_item_audit_row(db, row, verdict, now, second_answer=second_answer, actor=actor)


def recorded_verdicts(db):
   statement = (
      select(models.ReviewQueue)
      .where(models.ReviewQueue.kind == KIND)
      .where(models.ReviewQueue.resolution.is_not(None))
      .order_by(models.ReviewQueue.ref_id)
   )
   rows = db.scalars(statement).all()

   return [
      {"item_id": row.ref_id, **json.loads(row.resolution)} for row in rows
   ]


def key_error_rate(db, sample_ids, sample_size=EVAL_29_SAMPLE_SIZE):
   sample = drawn_sample(sample_ids, sample_size)
   verdicts_by_item_id = {}
   verdicts_outside_sample = 0

   for verdict in recorded_verdicts(db):
      is_sampled = verdict["item_id"] in sample

      if not is_sampled:
         verdicts_outside_sample += 1
         continue

      verdicts_by_item_id.setdefault(verdict["item_id"], []).append(verdict)

   single_verdict_by_item_id = {
      item_id: verdicts[0]
      for item_id, verdicts in verdicts_by_item_id.items()
      if len(verdicts) == 1
   }
   duplicate_item_ids = sorted(
      item_id for item_id, verdicts in verdicts_by_item_id.items() if len(verdicts) > 1
   )

   key_errors = len([
      verdict
      for verdict in single_verdict_by_item_id.values()
      if verdict["verdict"] in KEY_ERROR_VERDICTS
   ])
   verdicts_recorded = sum(len(verdicts) for verdicts in verdicts_by_item_id.values())
   is_complete = len(single_verdict_by_item_id) == len(sample)
   measured_rate = key_errors / len(sample) if is_complete else None

   return {
      "sample_size": len(sample),
      "verdicts_recorded": verdicts_recorded,
      "verdicts_complete": is_complete,
      "duplicate_item_ids": duplicate_item_ids,
      "verdicts_outside_sample": verdicts_outside_sample,
      "key_errors": key_errors,
      "key_error_rate": measured_rate,
   }


def publish_key_error_rate(db, sample_ids, now, report_path=None, sample_size=EVAL_29_SAMPLE_SIZE):
   measurement = key_error_rate(db, sample_ids, sample_size=sample_size)
   measurement["measured_at"] = now

   has_report_path = report_path is not None

   if has_report_path:
      report_path.write_text(json.dumps(measurement, indent=2))

   return measurement
