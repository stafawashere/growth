"""docs/plan/06-architecture.md, "Data model": the 14 P1 tables, the two passkey tables,
diagnoses, which 11 P2 scope item 9 puts in use in P2, the six tables of the P7 evaluation
harness (11 P7 scope items 4 to 6), and gradings, which 11 P3 scope item 10 puts in use in P3,
with frq_images for the photographs 06's image routes store, and the three P5 assessment tables
(11 P5 scope items 1, 2 and 5)."""
from sqlalchemy import inspect

from app.db.models import Base, make_engine

P1_TABLE_NAMES = {
   "users",
   "provider_configs",
   "content_snapshots",
   "skills_state",
   "items",
   "item_verifications",
   "sessions",
   "judgments",
   "attempts",
   "pending_probes",
   "review_queue",
   "jobs",
   "budgets",
   "audit_log",
   "passkey_credentials",
   "auth_sessions",
}

P2_TABLE_NAMES = P1_TABLE_NAMES | {"diagnoses"}

P7_TABLE_NAMES = P2_TABLE_NAMES | {
   "experiments",
   "experiment_assignments",
   "checkpoints",
   "checkpoint_scores",
   "probe_administrations",
   "probe_responses",
}

P3_TABLE_NAMES = {"gradings", "frq_images"}

P5_TABLE_NAMES = {"assessment_parts", "assessment_responses", "mock_results"}


def test_models_create_all(tmp_path):
   engine = make_engine(tmp_path / "p1.sqlite")
   inspector = inspect(engine)
   table_names = set(inspector.get_table_names())

   assert table_names == P7_TABLE_NAMES | P3_TABLE_NAMES | P5_TABLE_NAMES

   gradings_columns = {column["name"] for column in inspector.get_columns("gradings")}
   assert gradings_columns == {
      "id",
      "attempt_id",
      "part_id",
      "point_id",
      "point_type_id",
      "decided_by",
      "earned",
      "samples",
      "agreement",
      "provisional",
      "rationale",
      "rule_field",
      "evidence_quote",
      "eligibility_note",
      "deterministic_check",
      "rereads",
      "created_at",
      "updated_at",
   }

   for table_name in sorted((P7_TABLE_NAMES - P2_TABLE_NAMES) | P5_TABLE_NAMES):
      columns = {column["name"] for column in inspector.get_columns(table_name)}
      assert "user_id" in columns, table_name

   diagnoses_columns = {column["name"] for column in inspector.get_columns("diagnoses")}
   assert diagnoses_columns == {
      "id",
      "attempt_id",
      "observed_errors",
      "misconception_hypotheses",
      "non_conceptual_causes",
      "prerequisite_gap",
      "mastery_states",
      "matched_signal",
      "probe_scheduled",
      "diagnosed_by",
      "created_at",
      "updated_at",
   }

   attempts_columns = {column["name"] for column in inspector.get_columns("attempts")}
   assert {"error_note", "self_explanation", "snapshot_id"} <= attempts_columns
   assert {"p_split", "p_compensatory"} <= attempts_columns
   assert "experiment_arms" in attempts_columns

   items_options_column = Base.metadata.tables["items"].columns["options"]
   assert items_options_column.type.__class__.__name__ == "JSON"

   skills_state_table = Base.metadata.tables["skills_state"]
   primary_key_columns = {column.name for column in skills_state_table.primary_key.columns}
   assert primary_key_columns == {"user_id", "skill_id"}

   skills_state_columns = {column["name"] for column in inspector.get_columns("skills_state")}
   assert "unaided_success_count" in skills_state_columns
