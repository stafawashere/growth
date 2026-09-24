"""The diagnostician's deterministic half, over the real library registries.

test_diagnosis_never_certain is the P3 gate: no misconception is ever returned at probability 1.0.
It runs every active BC-ERR in data/errors.json through diagnose() under every confidence rating
and both timings, alone and in pairs with a neighbour, so a lone candidate, the case most likely
to reach 1.0, is covered for every error that has one.
"""
from dataclasses import dataclass

import pytest

from app.content.loader import load_snapshot
from app.diagnosis import diagnose as diagnosis
from app.frq.bank import library_from_snapshot

CONFIDENCES = (None, "guess", "unsure", "confident")


@pytest.fixture(scope="module")
def library():
   return library_from_snapshot(load_snapshot("data"))


@dataclass
class Lost:
   point_id: str
   earned: int = 0
   provisional: bool = False
   part_id: str = "a"
   rule_field: str | None = "earns"


def record_for(skills):
   return {
      "id": "FRQ-TEST-01",
      "archetype_id": "BC-QA-05007",
      "skills": list(skills),
      "parts": [{"id": "a", "points": [{"point_id": "a1", "skills": list(skills)}]}],
   }


def run(library, error_ids, confidence, timed=False, signal_ids=()):
   skills = sorted({skill for error_id in error_ids for skill in library.errors[error_id].get("skills") or []}) or ["BC-SKL-05039"]
   observation = diagnosis.Observation(error_ids=list(error_ids), signal_ids=list(signal_ids))

   return diagnosis.diagnose(record_for(skills), [Lost("a1")], observation, library, confidence=confidence, timed=timed)


def test_diagnosis_never_certain(library):
   error_ids = sorted(library.errors)
   checked = 0

   for index, error_id in enumerate(error_ids):
      neighbour = error_ids[(index + 1) % len(error_ids)]

      for confidence in CONFIDENCES:
         for timed in (False, True):
            for observed in ([error_id], [error_id, neighbour]):
               result = run(library, observed, confidence, timed)
               probabilities = [entry["probability"] for entry in result["candidate_misconceptions"]]
               has_candidates = len(probabilities) > 0

               assert all(probability < 1.0 for probability in probabilities), (error_id, confidence, probabilities)

               if has_candidates:
                  assert sum(probabilities) < 1.0
                  assert result["non_conceptual_mass"] > 0

               checked += 1

   assert checked == len(error_ids) * len(CONFIDENCES) * 2 * 2
   assert len(error_ids) > 300


def test_a_lone_candidate_after_a_confident_error_still_leaves_non_conceptual_mass(library):
   lone = [
      error_id for error_id, error in sorted(library.errors.items())
      if len([m for m in error.get("possible_misconceptions") or [] if m in library.misconceptions]) == 1
   ]

   assert lone, "the library has errors with exactly one live misconception"

   result = run(library, [lone[0]], "confident")
   probability = result["candidate_misconceptions"][0]["probability"]

   assert probability == pytest.approx(1 - result["non_conceptual_mass"])
   assert probability < 1.0


def test_a_confident_error_moves_mass_toward_misconceptions_and_a_guess_away(library):
   error_id = next(error_id for error_id, error in sorted(library.errors.items()) if error.get("possible_misconceptions"))

   confident = run(library, [error_id], "confident")["non_conceptual_mass"]
   unsure = run(library, [error_id], "unsure")["non_conceptual_mass"]
   guess = run(library, [error_id], "guess")["non_conceptual_mass"]

   assert confident < unsure < guess


def test_close_hypotheses_schedule_a_probe_and_a_clear_leader_does_not(library):
   close = [
      {"kind": diagnosis.MISCONCEPTION, "id": "BC-MIS-99001", "probability": 0.40},
      {"kind": diagnosis.MISCONCEPTION, "id": "BC-MIS-04005", "probability": 0.30},
   ]
   clear = [
      {"kind": diagnosis.MISCONCEPTION, "id": "BC-MIS-99001", "probability": 0.60},
      {"kind": diagnosis.MISCONCEPTION, "id": "BC-MIS-04005", "probability": 0.10},
   ]
   rivals = {"BC-MIS-99001": ["BC-MIS-04005"]}

   probe = diagnosis.recommended_probe(close, library, rivals)

   assert probe is not None
   assert probe["archetype_id"] in library.misconceptions["BC-MIS-99001"]["exposing_archetypes"]
   assert probe["reason"] == "rival_pair"
   assert diagnosis.recommended_probe(clear, library, rivals) is None


def test_a_gap_is_traced_over_hard_edges_and_discounted_by_the_engine(library):
   child = next(skill for skill, parents in sorted(library.hard_parents.items()) if parents)
   parent = sorted(library.hard_parents[child])[0]
   observation = diagnosis.Observation(gap_skills=[child])

   weak = diagnosis.trace_gaps({child}, observation, {}, library, strengths={parent: 0.1})
   strong = diagnosis.trace_gaps({child}, observation, {}, library, strengths={parent: 0.95})

   weak_parent = next(gap for gap in weak if gap["prerequisite_id"] == parent)
   strong_parent = next(gap for gap in strong if gap["prerequisite_id"] == parent)

   assert weak_parent["depth"] == 1
   assert weak_parent["probability"] == pytest.approx(0.5 * 0.9)
   assert strong_parent["probability"] < weak_parent["probability"]
   assert all(gap["depth"] <= diagnosis.MAX_GAP_DEPTH for gap in weak)
