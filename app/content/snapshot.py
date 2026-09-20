"""The immutable in-memory content graph a loaded run holds, per docs/plan/06-architecture.md."""
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Edge:
   from_id: str
   to_id: str
   type: str
   evidence_tag: str
   note: str


@dataclass(frozen=True)
class ContentSnapshot:
   skills: dict
   prerequisites: dict
   concepts: dict
   archetypes: dict
   all_archetypes: dict
   variants: dict
   errors: dict
   misconceptions: dict
   signals: dict
   scoring_points: dict
   representations: dict
   difficulty_factors: dict
   command_verbs: dict
   frq_parts: dict
   mcq_records: dict
   edges: tuple
   hard_parents: dict
   supporting_parents: dict
   hard_children: dict
   inert_top_ids: frozenset
   counts: dict
   digest: str
