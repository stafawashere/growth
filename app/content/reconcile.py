"""snapshot_reload reconciliation, per docs/plan/06-architecture.md
"Library updates and retired IDs".
"""
import json
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timezone

from app.audit.detail import bind_audit_detail
from app.audit.vocabulary import is_known_action
from app.db.models import AuditLog, SkillState as SkillStateRow
from app.engine.state import FadingStage, SkillState as EngineSkillState
from app.engine.update import evaluate_mastery


class ReloadRefused(Exception):
   pass


@dataclass
class ReloadReport:
   kept: list = field(default_factory=list)
   rewritten: list = field(default_factory=list)
   merged: list = field(default_factory=list)
   orphaned: list = field(default_factory=list)
   notes: list = field(default_factory=list)


FADING_STAGE_ORDER = {"example": 0, "completion": 1, "unsupported": 2}


def _now_iso():
   return datetime.now(timezone.utc).isoformat()


def _load_str_list(text):
   return json.loads(text) if text else []


def _parse_datetime(value):
   return datetime.fromisoformat(value) if value else None


def _parse_date(value):
   return date.fromisoformat(value)


def _row_to_engine_state(row):
   return EngineSkillState(
      skill_id=row.skill_id,
      beta=row.beta,
      c=row.credited_successes,
      f=row.credited_failures,
      stability=row.stability,
      difficulty=row.difficulty,
      last_practised_at=_parse_datetime(row.last_practised_at),
      fading_stage=FadingStage(row.fading_stage),
      observation_count=row.observation_count,
      unaided_success_count=row.unaided_success_count,
      distinct_archetypes_succeeded=set(_load_str_list(row.distinct_archetypes_succeeded)),
      success_days={_parse_date(day) for day in _load_str_list(row.success_days)},
      mastered=bool(row.mastered),
   )


def _write_audit_entry(db_session, actor, action, old_id, new_id):
   if not is_known_action(action):
      raise ValueError(f"{action!r} is not in the audit_log vocabulary")

   timestamp = _now_iso()
   bound_detail = bind_audit_detail({"old_id": old_id, "new_id": new_id})
   entry = AuditLog(
      id=uuid.uuid4().hex,
      at=timestamp,
      actor=actor,
      action=action,
      subject=old_id,
      detail=json.dumps(bound_detail),
      created_at=timestamp,
      updated_at=timestamp,
   )
   db_session.add(entry)


def _merge_into(existing_row, old_row, today, report):
   most_recent_practice = max(
      (value for value in (existing_row.last_practised_at, old_row.last_practised_at) if value),
      default=None,
   )
   merged_archetypes = set(_load_str_list(existing_row.distinct_archetypes_succeeded)) | set(
      _load_str_list(old_row.distinct_archetypes_succeeded)
   )
   merged_days = set(_load_str_list(existing_row.success_days)) | set(
      _load_str_list(old_row.success_days)
   )
   existing_stability = existing_row.stability or 0.0
   old_stability = old_row.stability or 0.0
   has_stability = existing_row.stability is not None or old_row.stability is not None
   old_wins_stability = old_stability > existing_stability
   merged_stability = None
   merged_difficulty = existing_row.difficulty

   if has_stability:
      merged_stability = old_stability if old_wins_stability else existing_stability
      merged_difficulty = old_row.difficulty if old_wins_stability else existing_row.difficulty

   merged_fading_order = min(
      FADING_STAGE_ORDER[existing_row.fading_stage],
      FADING_STAGE_ORDER[old_row.fading_stage],
   )
   merged_fading_stage = next(
      stage for stage, order in FADING_STAGE_ORDER.items() if order == merged_fading_order
   )
   merged_hypercorrection_due = max(
      (value for value in (existing_row.hypercorrection_due, old_row.hypercorrection_due) if value),
      default=None,
   )
   merged_concept_opener_done = int(
      bool(existing_row.concept_opener_done) or bool(old_row.concept_opener_done)
   )

   existing_row.credited_successes = existing_row.credited_successes + old_row.credited_successes
   existing_row.credited_failures = existing_row.credited_failures + old_row.credited_failures
   existing_row.stability = merged_stability
   existing_row.difficulty = merged_difficulty
   existing_row.observation_count = max(existing_row.observation_count, old_row.observation_count)
   existing_row.distinct_archetypes_succeeded = json.dumps(sorted(merged_archetypes))
   existing_row.success_days = json.dumps(sorted(merged_days))
   existing_row.unaided_success_count = (
      existing_row.unaided_success_count + old_row.unaided_success_count
   )
   existing_row.last_practised_at = most_recent_practice
   existing_row.fading_stage = merged_fading_stage
   existing_row.hypercorrection_due = merged_hypercorrection_due
   existing_row.concept_opener_done = merged_concept_opener_done
   existing_row.consecutive_successes = 0
   existing_row.consecutive_failures = 0
   existing_row.mastered = int(bool(existing_row.mastered) or bool(old_row.mastered))

   recomputed = evaluate_mastery(_row_to_engine_state(existing_row), today)
   existing_row.mastered = int(recomputed)

   if recomputed and not existing_row.mastered_at:
      existing_row.mastered_at = today.isoformat()
   elif not recomputed:
      existing_row.mastered_at = None

   existing_row.updated_at = _now_iso()
   report.notes.append(
      f"{existing_row.user_id}/{existing_row.skill_id}: consecutive_successes and "
      f"consecutive_failures reset to 0 on merge, not summed or maxed (inferred, plan silent)"
   )


def reconcile_skills_state(db_session, new_snapshot, ids_registry, today, snapshot_row_id, actor="worker"):
   active_ids = set(new_snapshot.skills) | set(new_snapshot.prerequisites)
   report = ReloadReport()
   rows = db_session.query(SkillStateRow).all()

   for row in rows:
      is_active = row.skill_id in active_ids

      if is_active:
         row.snapshot_id = snapshot_row_id
         row.updated_at = _now_iso()
         report.kept.append((row.user_id, row.skill_id))
         continue

      tombstone = ids_registry.get(row.skill_id)
      is_tombstone = tombstone is not None and tombstone.get("status") == "retired"

      if not is_tombstone:
         raise ReloadRefused(
            f"skills_state row {row.user_id}/{row.skill_id} is neither active in the new "
            f"snapshot nor tombstoned in data/ids.json"
         )

      successor_id = tombstone.get("superseded_by")

      if successor_id is None:
         row.snapshot_id = snapshot_row_id
         row.updated_at = _now_iso()
         report.orphaned.append((row.user_id, row.skill_id))
         _write_audit_entry(db_session, actor, "skill_orphaned", row.skill_id, None)
         continue

      successor_is_active = successor_id in active_ids

      if not successor_is_active:
         raise ReloadRefused(
            f"tombstone for {row.skill_id} names superseded_by {successor_id!r}, "
            f"which is not active in the new snapshot"
         )

      existing_successor = db_session.get(SkillStateRow, (row.user_id, successor_id))

      if existing_successor is None:
         old_skill_id = row.skill_id
         row.skill_id = successor_id
         row.snapshot_id = snapshot_row_id
         row.updated_at = _now_iso()
         report.rewritten.append((old_skill_id, successor_id))
         _write_audit_entry(db_session, actor, "skill_rewritten", old_skill_id, successor_id)
      else:
         old_skill_id = row.skill_id
         _merge_into(existing_successor, row, today, report)
         existing_successor.snapshot_id = snapshot_row_id
         db_session.delete(row)
         report.merged.append((old_skill_id, successor_id))
         _write_audit_entry(db_session, actor, "skill_merged", old_skill_id, successor_id)

   db_session.flush()

   return report
