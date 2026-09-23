"""Per-skill mastery state, the D2 state vector from docs/plan/02-adaptive-engine.md.

Column names drop the _k suffix per the P1 conventions in docs/plan/11-phased-delivery.md.
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum


class MasteryState(str, Enum):
   MASTERED = "mastered"
   PARTIAL_PROCEDURAL = "partial_procedural"
   PARTIAL_CONCEPTUAL = "partial_conceptual"
   PARTIAL_UNSPECIFIED = "partial_unspecified"
   PREREQUISITE_GAP = "prerequisite_gap"
   NOTATION_ONLY = "notation_only"
   NOT_MASTERED = "not_mastered"
   NOT_ATTEMPTED = "not_attempted"


PARTIAL_STATES = frozenset({
   MasteryState.PARTIAL_PROCEDURAL,
   MasteryState.PARTIAL_CONCEPTUAL,
   MasteryState.PARTIAL_UNSPECIFIED,
})


class FadingStage(str, Enum):
   EXAMPLE = "example"
   COMPLETION = "completion"
   UNSUPPORTED = "unsupported"


FADING_ORDER = (FadingStage.EXAMPLE, FadingStage.COMPLETION, FadingStage.UNSUPPORTED)


class Confidence(str, Enum):
   GUESS = "guess"
   UNSURE = "unsure"
   CONFIDENT = "confident"


class ResponseFormat(str, Enum):
   MCQ = "mcq"
   SHORT_ANSWER = "short_answer"


@dataclass
class SkillState:
   skill_id: str
   beta: float = 0.0
   c: float = 0.0
   f: float = 0.0
   stability: float | None = None
   difficulty: float | None = None
   last_practised_at: datetime | None = None
   fading_stage: FadingStage = FadingStage.EXAMPLE
   observation_count: int = 0
   credited_observation_count: int = 0
   unaided_success_count: int = 0
   distinct_archetypes_succeeded: set[str] = field(default_factory=set)
   success_days: set[date] = field(default_factory=set)
   mastered: bool = False
   mastered_at: datetime | None = None
   hypercorrection_due: date | None = None
   consecutive_successes: int = 0
   consecutive_failures: int = 0
   concept_opener_done: bool = False

   @classmethod
   def seeded_mastered(cls, skill_id, created_at):
      """A BC-PRQ row or an out-of-subgraph parent: assumed mastered until a diagnosed gap (R15)."""
      return cls(
         skill_id=skill_id,
         beta=0.0,
         fading_stage=FadingStage.UNSUPPORTED,
         mastered=True,
         mastered_at=created_at,
      )


@dataclass
class PendingProbe:
   archetype_id: str
   diagnosis_id: str
   enqueued_at: datetime
   served_at: datetime | None = None
