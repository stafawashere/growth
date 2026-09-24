"""The D3 interleaving window and the representation-translation floor (docs/plan/02, Item
selection algorithm, filter_interleaving and pick_variant; docs/plan/11 P2 scope item 4).

Every served set is read as sliding windows of 10 consecutive items, blocks 1 to 3 in order. Two
rules are strict and can end a block: no more than 2 consecutive items share a primary skill, as
in P1. The other four bind whenever some candidate can meet them and are otherwise recorded as a
shortfall naming the rule, which is the plan's own "once 2 units are open" clause applied to each
of them: a window needs at least 4 primary skills, at least 2 units, at most 3 items from one
archetype family, and at least 20 percent representation translations.

A window shorter than 10 is held to what a full window could still reach: with 10 - L slots left
it needs max(0, minimum - (10 - L)) skills or units, so a set never walks into a window it cannot
complete. The translation floor also holds on every short prefix at floor(0.20 * L), which is 1
from the fifth item and 2 in a full window.

A translation archetype carries two BC-REP ids that data/taxonomies.json lists as a conversion
pair, source to a different target. Self-pairs such as graph of f to graph of f' are left out,
because an archetype carrying one representation cannot show whether a given item asks for the
translation.
"""
import math
import re
from dataclasses import dataclass

from app.engine import constants
from app.engine.prior import primary_skill

WINDOW = 10

PAIR_PATTERN = re.compile(r"^(BC-REP-\d+)\s*->\s*(BC-REP-\d+)")

STRICT_RULES = ("max_consecutive",)
SOFT_RULES = ("block_skills", "block_units", "family_cap", "translation_floor")


@dataclass(frozen=True)
class InterleaveRules:
   max_consecutive: bool = True
   block_skills: bool = True
   block_units: bool = True
   family_cap: bool = True
   translation_floor: bool = True


FULL_RULES = InterleaveRules()

MAX_TWO_ONLY = InterleaveRules(
   block_skills=False,
   block_units=False,
   family_cap=False,
   translation_floor=False,
)


def conversion_pairs_from(representations):
   """(source, target) pairs with source != target, from the BC-REP records' conversion_pairs."""
   pairs = set()

   for record in representations:
      for text in record.get("conversion_pairs", ()):
         match = PAIR_PATTERN.match(text)

         if match is None:
            continue

         source, target = match.group(1), match.group(2)
         is_self_pair = source == target

         if not is_self_pair:
            pairs.add((source, target))

   return frozenset(pairs)


def is_translation(record, pairs):
   carried = list(record.get("representations") or ())

   return any(
      (source, target) in pairs
      for source in carried
      for target in carried
      if source != target
   )


def required_in_window(length, minimum):
   return max(0, minimum - (WINDOW - length))


def required_translations(length):
   share_floor = math.floor(constants.MIN_TRANSLATION_SHARE * length + 1e-9)
   full_window = math.ceil(constants.MIN_TRANSLATION_SHARE * WINDOW - 1e-9)

   return max(share_floor, required_in_window(length, full_window))


def window_with(history_records, candidate):
   return history_records[-(WINDOW - 1):] + [candidate]


def breaks_max_consecutive(history_records, candidate):
   limit = constants.MAX_CONSECUTIVE_SAME_SKILL
   tail = history_records[-limit:]
   is_full_tail = len(tail) == limit
   candidate_skill = primary_skill(candidate)
   repeats_tail = all(primary_skill(record) == candidate_skill for record in tail)

   return is_full_tail and repeats_tail


def meets_skills(history_records, candidate):
   window = window_with(history_records, candidate)
   distinct = {primary_skill(record) for record in window}

   return len(distinct) >= required_in_window(len(window), constants.MIN_SKILLS_PER_10)


def meets_units(history_records, candidate):
   window = window_with(history_records, candidate)
   distinct = {record["primary_unit"] for record in window}

   return len(distinct) >= required_in_window(len(window), constants.MIN_UNITS_PER_10)


def meets_family_cap(history_records, candidate):
   window = window_with(history_records, candidate)
   same_family = [record for record in window if record["family"] == candidate["family"]]

   return len(same_family) <= constants.MAX_FAMILY_PER_10


def meets_translation_floor(history_records, candidate, pairs):
   window = window_with(history_records, candidate)
   translations = [record for record in window if is_translation(record, pairs)]

   return len(translations) >= required_translations(len(window))


def soft_checks(pairs):
   return {
      "block_skills": meets_skills,
      "block_units": meets_units,
      "family_cap": meets_family_cap,
      "translation_floor": lambda history_records, candidate: meets_translation_floor(
         history_records, candidate, pairs
      ),
   }


def history_records_of(history, graph):
   return [graph.archetypes[item["archetype_id"]] for item in history]


def window_filter(records, history, graph, rules=FULL_RULES):
   """The candidates every applicable rule allows, and the soft rules no candidate could meet.

   Strict rules filter unconditionally, so an empty result ends the block. Each soft rule, in
   the order of SOFT_RULES, narrows the set when at least one remaining candidate meets it, and
   otherwise leaves the set as it is and is returned as a shortfall.
   """
   past = history_records_of(history, graph)
   allowed = list(records)

   if rules.max_consecutive:
      allowed = [record for record in allowed if not breaks_max_consecutive(past, record)]

   has_candidates = len(allowed) > 0

   if not has_candidates:
      return [], ()

   checks = soft_checks(graph.conversion_pairs)
   shortfalls = []

   for rule_name in SOFT_RULES:
      is_enabled = getattr(rules, rule_name)

      if not is_enabled:
         continue

      meeting = [record for record in allowed if checks[rule_name](past, record)]
      can_meet = len(meeting) > 0

      if can_meet:
         allowed = meeting
      else:
         shortfalls.append(rule_name)

   return allowed, tuple(shortfalls)


def window_violations(served_records, pairs):
   """Every rule a served sequence breaks, as (position, rule) with position the index of the
   item that completed the offending window. Independent of window_filter: it reads only the
   sequence, so a filter bug cannot hide from it.
   """
   violations = []
   checks = soft_checks(pairs)

   for position, record in enumerate(served_records):
      past = served_records[:position]

      if breaks_max_consecutive(past, record):
         violations.append((position, "max_consecutive"))

      for rule_name in SOFT_RULES:
         if not checks[rule_name](past, record):
            violations.append((position, rule_name))

   return violations
