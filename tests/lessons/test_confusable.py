"""app/lessons/confusable.py: confusable_sets is deterministic over a snapshot and every set
lies within one unit, holds 2 to DECISION_SET_MAX active skills and is ordered by id (L18)."""
from types import SimpleNamespace

from app.lessons import constants
from app.lessons.confusable import confusable_sets


def skill(unit, *confused):
   return {"unit": unit, "confusable_with": list(confused)}


def stub(skills):
   return SimpleNamespace(skills=skills)


def test_sets_are_the_same_on_every_call_and_in_any_insertion_order(snapshot):
   first = confusable_sets(snapshot)
   second = confusable_sets(snapshot)
   reversed_skills = dict(reversed(list(snapshot.skills.items())))
   reordered = confusable_sets(stub(reversed_skills))

   assert first == second
   assert first == reordered


def test_every_real_set_is_in_one_unit_of_active_skills_within_the_size_bounds(snapshot):
   sets = confusable_sets(snapshot)

   assert len(sets) > 0

   for members in sets:
      units = {snapshot.skills[skill_id]["unit"] for skill_id in members}
      is_sorted = list(members) == sorted(members)

      assert len(units) == 1
      assert 2 <= len(members) <= constants.DECISION_SET_MAX
      assert is_sorted

   assert sets == sorted(sets)


def test_a_reference_is_read_in_both_directions():
   skills = {"S1": skill("U1", "S3"), "S2": skill("U1", "S3"), "S3": skill("U1")}

   assert confusable_sets(stub(skills)) == [("S1", "S2", "S3")]


def test_a_reference_that_leaves_the_unit_joins_nothing():
   skills = {"S1": skill("U1", "S2"), "S2": skill("U2")}

   assert confusable_sets(stub(skills)) == []


def test_a_reference_to_a_skill_that_is_not_active_is_ignored():
   skills = {"S1": skill("U1", "S9", "S2"), "S2": skill("U1")}

   assert confusable_sets(stub(skills)) == [("S1", "S2")]


def test_a_component_larger_than_the_cap_is_dropped_not_split():
   count = constants.DECISION_SET_MAX + 1
   names = [f"S{index}" for index in range(count)]
   skills = {name: skill("U1", *names[index + 1:index + 2]) for index, name in enumerate(names)}

   assert confusable_sets(stub(skills)) == []


def test_sets_are_ordered_by_id():
   skills = {
      "S5": skill("U1", "S6"),
      "S6": skill("U1"),
      "S1": skill("U1", "S2"),
      "S2": skill("U1"),
   }

   assert confusable_sets(stub(skills)) == [("S1", "S2"), ("S5", "S6")]
