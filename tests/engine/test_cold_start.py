"""Eval 27 from docs/plan/11-phased-delivery.md, P1: the cold-start p_A_knowledge distribution.

The test asserts only that the distribution computes over all 139 active archetypes and is
finite everywhere. The 0.3 floor on the 90th percentile is a merge gate on the published number,
so the percentiles are printed for the pull request rather than asserted here.
"""
import csv
import json
import math
from pathlib import Path

from app.engine import prior
from app.engine.state import SkillState

ROOT = Path(__file__).resolve().parents[2]


def load_active_archetypes():
   records = json.loads((ROOT / "data" / "archetypes.json").read_text())["archetypes"]

   return {record["id"]: record for record in records if record.get("status", "active") == "active"}


def load_hard_parents():
   hard_parents = {}

   with (ROOT / "data" / "prereq_edges.csv").open() as handle:
      for edge in csv.DictReader(handle):
         is_hard = edge["type"] == "hard_prerequisite"

         if is_hard:
            hard_parents.setdefault(edge["to"], set()).add(edge["from"])

   return hard_parents


def percentile(sorted_values, fraction):
   index = int(fraction * (len(sorted_values) - 1))

   return sorted_values[index]


def eval_cold_start_pA_distribution(capsys):
   archetypes = load_active_archetypes()
   hard_parents = load_hard_parents()
   skills = {skill for record in archetypes.values() for skill in record["skills"]}
   states = {skill: SkillState(skill, beta=prior.beta_for_skill(skill, archetypes)) for skill in skills}

   split = sorted(prior.p_knowledge(record, states, hard_parents) for record in archetypes.values())
   compensatory = sorted(prior.p_compensatory(record, states) for record in archetypes.values())

   assert len(split) == 139
   assert all(math.isfinite(value) for value in split)
   assert all(0.0 <= value <= 1.0 for value in split)

   with capsys.disabled():
      print(
         "\neval_cold_start_pA_distribution split p10/p50/p90:",
         round(percentile(split, 0.1), 3), round(percentile(split, 0.5), 3), round(percentile(split, 0.9), 3),
         "compensatory p10/p50/p90:",
         round(percentile(compensatory, 0.1), 3), round(percentile(compensatory, 0.5), 3), round(percentile(compensatory, 0.9), 3),
      )
