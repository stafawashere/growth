"""Exam-weight priors as a hard constraint on the assembled set (docs/plan/11 P2 scope item 5).

The weights are read from research/exam/exam-blueprint.md, "Unit weighting on the
multiple-choice section", which owns them; nothing here restates a band. Each unit's prior is its
BC band midpoint. The CED publishes no unit weighting for free response, and every band is a
range that constrains rather than fixes a form, so the prior is a quota rather than a score term.

The quota: among the units open to the candidates in hand, unit u's share of the set is its
midpoint over the open units' midpoints, and a candidate from u is allowed only while u holds
fewer than ceil(share_u * (n + 1)) of the n items the constraint has already counted. The open
units' ceilings sum to at least n + 1 while their counts sum to at most n, so some open unit is
always below its ceiling and the constraint never empties a candidate set on its own.
"""
import math
import re
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

BLUEPRINT_PATH = Path(__file__).resolve().parents[2] / "research" / "exam" / "exam-blueprint.md"

SECTION_HEADING = "## Unit weighting on the multiple-choice section"

ROW_PATTERN = re.compile(r"^\|\s*(BC-UNIT-\d{2})\s*\|.*\|\s*(\d+)\s+to\s+(\d+)%\s*\|\s*$")


class BlueprintUnreadable(RuntimeError):
   pass


def section_lines(text):
   lines = text.splitlines()

   try:
      start = lines.index(next(line for line in lines if line.startswith(SECTION_HEADING)))
   except StopIteration as missing:
      raise BlueprintUnreadable(f"no section starting {SECTION_HEADING!r}") from missing

   section = []

   for line in lines[start + 1:]:
      starts_next_section = line.startswith("## ")

      if starts_next_section:
         break

      section.append(line)

   return section


def parse_bc_bands(text):
   """The BC column is the last column of the table, so each row's last band is the BC band."""
   bands = {}

   for line in section_lines(text):
      match = ROW_PATTERN.match(line.strip())

      if match is None:
         continue

      unit_id = match.group(1)
      low = int(match.group(2))
      high = int(match.group(3))
      bands[unit_id] = (low, high)

   is_empty = len(bands) == 0

   if is_empty:
      raise BlueprintUnreadable("the unit weighting table has no BC band rows")

   return bands


@lru_cache(maxsize=1)
def bc_bands(path=BLUEPRINT_PATH):
   return parse_bc_bands(Path(path).read_text())


def band_midpoints(path=BLUEPRINT_PATH):
   """Exact halves, so the quota arithmetic below has no rounding to reason about."""
   return {unit_id: Fraction(low + high, 2) for unit_id, (low, high) in bc_bands(path).items()}


def open_unit_shares(open_units, midpoints):
   weighted = {unit_id: Fraction(midpoints.get(unit_id, 0)) for unit_id in open_units}
   total = sum(weighted.values())
   has_weight = total > 0

   if not has_weight:
      return {unit_id: Fraction(1, len(weighted)) for unit_id in weighted}

   return {unit_id: weight / total for unit_id, weight in weighted.items()}


def unit_ceiling(share, counted):
   return math.ceil(share * (counted + 1))


def filter_exam_weight(records, unit_counts, midpoints=None):
   """The candidates whose unit is still below its quota ceiling among the open units."""
   if unit_counts is None:
      return list(records)

   has_candidates = len(records) > 0

   if not has_candidates:
      return []

   weights = midpoints if midpoints is not None else band_midpoints()
   open_units = sorted({record["primary_unit"] for record in records})
   shares = open_unit_shares(open_units, weights)
   counted = sum(unit_counts.values())

   return [
      record
      for record in records
      if unit_counts.get(record["primary_unit"], 0) < unit_ceiling(shares[record["primary_unit"]], counted)
   ]
