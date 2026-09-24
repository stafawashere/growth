"""docs/plan/06-architecture.md, "Data model": the 14 P1 tables, the two passkey tables, and
diagnoses, which 11 P2 scope item 9 puts in use in P2. gradings stays out until P3."""
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


def test_models_create_all(tmp_path):
   engine = make_engine(tmp_path / "p1.sqlite")
   inspector = inspect(engine)
   table_names = set(inspector.get_table_names())

   assert table_names == P2_TABLE_NAMES
   assert "gradings" not in table_names

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

   items_options_column = Base.metadata.tables["items"].columns["options"]
   assert items_options_column.type.__class__.__name__ == "JSON"

   skills_state_table = Base.metadata.tables["skills_state"]
   primary_key_columns = {column.name for column in skills_state_table.primary_key.columns}
   assert primary_key_columns == {"user_id", "skill_id"}

   skills_state_columns = {column["name"] for column in inspector.get_columns("skills_state")}
   assert "unaided_success_count" in skills_state_columns
