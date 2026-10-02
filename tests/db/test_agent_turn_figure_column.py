"""agent_turns.figure (docs/agent/drawing-design.md, Storage, privacy and logs) is additive and
nullable: a database created before it gains it through apply_additive_migrations, and a turn
already in the table reads back with no figure.
"""
from sqlalchemy import create_engine, inspect

from app.db.migrate import apply_additive_migrations
from app.db.models import Base

OLD_TURN = {
   "id": "ATN-OLD",
   "conversation_id": "ACV-OLD",
   "user_id": "USR-OLD",
   "role": "agent",
   "text": "An older reply.",
   "created_at": "2026-09-20T10:00:00+00:00",
   "updated_at": "2026-09-20T10:00:00+00:00",
}


def test_an_old_agent_turns_table_gains_a_null_figure_column(tmp_path):
   engine = create_engine(f"sqlite:///{tmp_path / 'old.db'}")
   Base.metadata.create_all(engine)

   with engine.begin() as connection:
      connection.exec_driver_sql('ALTER TABLE "agent_turns" DROP COLUMN "figure"')
      names = ", ".join(OLD_TURN)
      placeholders = ", ".join(f":{name}" for name in OLD_TURN)
      connection.exec_driver_sql(f"INSERT INTO agent_turns ({names}) VALUES ({placeholders})", OLD_TURN)

   assert "figure" not in {column["name"] for column in inspect(engine).get_columns("agent_turns")}

   added = apply_additive_migrations(engine)

   with engine.connect() as connection:
      figure = connection.exec_driver_sql("SELECT figure FROM agent_turns WHERE id = 'ATN-OLD'").scalar_one()

   assert added == ("agent_turns.figure",)
   assert figure is None
