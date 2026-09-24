"""The diagnoses table in use (docs/plan/11 P2 scope item 9; 06 "diagnoses").

P2 has no diagnostician, so each row records what the R12 and R26 rule decided and nothing it
did not: the chosen distractor's BC-ERR path as the observed error, the per-skill mastery_state,
and empty hypothesis lists rather than invented ones. The misconception distribution, the
non-conceptual causes, the matched signal and the probe arrive with P3's diagnostician, which
writes into the same table with diagnosed_by naming the model.
"""
import json
import uuid

from app.db import models
from app.engine.state import MasteryState

DIAGNOSED_BY_RULE = "rule_r12_r26"


def write_rule_diagnosis(db, attempt_id, per_skill_states, graded_answer, written_at):
   error_path = graded_answer.get("error_path")
   observed_errors = [error_path] if error_path else []
   stamp = written_at.isoformat()
   row = models.Diagnosis(
      id=f"DGN-{uuid.uuid4().hex}",
      attempt_id=attempt_id,
      observed_errors=json.dumps(observed_errors),
      misconception_hypotheses=json.dumps([]),
      non_conceptual_causes=json.dumps([]),
      prerequisite_gap=None,
      mastery_states=json.dumps(
         {skill: MasteryState(state).value for skill, state in per_skill_states.items()}
      ),
      matched_signal=None,
      probe_scheduled=None,
      diagnosed_by=DIAGNOSED_BY_RULE,
      created_at=stamp,
      updated_at=stamp,
   )
   db.add(row)
   db.flush()

   return row
