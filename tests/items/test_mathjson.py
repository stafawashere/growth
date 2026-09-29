"""app/items/mathjson.py: the heads lesson records need (sets, tuples, intervals, calculus
operators, relations) and from_sympy, the inverse lesson transcription uses. Every distinct
expression string in the lesson designs round-trips (docs/lessons/BUILD-PLAN.md, The design to
record path, step 2)."""
import glob
from pathlib import Path

import pytest
import sympy

from app.items import verify
from app.items.mathjson import UnsupportedMathJSON, from_sympy, to_sympy
from tools.check_lesson_designs import Design, parse_expression

ROOT = Path(__file__).resolve().parents[2]


def design_paths():
   concept = sorted(glob.glob(str(ROOT / "docs" / "lessons" / "unit-*" / "LSN-*.md")))
   decision = sorted(glob.glob(str(ROOT / "docs" / "lessons" / "decisions" / "LSN-*.md")))

   return concept + decision


def step_strings(record):
   found = []

   for example in record.get("worked_examples") or []:
      found.extend(step.get("expr") for step in example.get("steps") or [])
      found.append((example.get("answer") or {}).get("expr"))

   for block in record.get("common_errors") or []:
      found.append((block.get("wrong_step") or {}).get("expr"))
      found.append((block.get("right_step") or {}).get("expr"))

   for check in record.get("checks") or []:
      found.extend(step.get("expr") for step in check.get("steps") or [])
      found.append((check.get("key") or {}).get("expr"))
      found.extend(option.get("expr") for option in check.get("options") or [])

   return [text for text in found if isinstance(text, str)]


def design_expressions():
   strings = set()

   for path in design_paths():
      record = Design(Path(path), Path(path).read_text()).record or {}
      strings.update(step_strings(record))

   parsed = []

   for text in sorted(strings):
      try:
         parsed.append((text, parse_expression(text)))
      except Exception:
         continue

   return parsed


def round_trips(expression):
   back = to_sympy(from_sympy(expression))

   if back == expression:
      return True

   return verify.equivalence(back, expression) == "equivalent"


def test_every_design_expression_round_trips():
   expressions = design_expressions()
   failures = [text for text, expression in expressions if not round_trips(expression)]

   assert len(expressions) > 1000
   assert failures == []


def test_a_pair_key_reads_as_a_set_of_equations():
   mathjson = ["Set", ["Equal", "k", 5], ["Equal", "m", -3]]
   expected = sympy.FiniteSet(sympy.Eq(sympy.Symbol("k"), 5), sympy.Eq(sympy.Symbol("m"), -3))

   assert to_sympy(mathjson) == expected
   assert to_sympy(from_sympy(expected)) == expected


def test_list_and_tuple_read_as_tuples():
   assert to_sympy(["Tuple", 1, "x"]) == sympy.Tuple(1, sympy.Symbol("x"))
   assert to_sympy(["List", 1, 2]) == sympy.Tuple(1, 2)


def test_intervals_unions_and_set_differences():
   half_open = ["Interval", ["Open", -3], "PositiveInfinity"]
   union = ["Union", ["Interval", "NegativeInfinity", ["Open", 2]], ["Interval", ["Open", 2], 5]]
   difference = ["SetMinus", ["Interval", -3, 4], ["Set", 2]]

   assert to_sympy(half_open) == sympy.Interval.open(-3, sympy.oo)
   assert to_sympy(union) == sympy.Union(sympy.Interval.open(-sympy.oo, 2), sympy.Interval.Lopen(2, 5))
   assert to_sympy(difference) == sympy.Complement(sympy.Interval(-3, 4), sympy.FiniteSet(2))


def test_infinities_and_nan_are_constants_not_symbols():
   assert to_sympy("PositiveInfinity") is sympy.oo
   assert to_sympy("NegativeInfinity") is -sympy.oo
   assert to_sympy("NaN") is sympy.nan
   assert from_sympy(sympy.nan) == "NaN"


def test_calculus_operators_round_trip():
   x, t = sympy.symbols("x t")
   f = sympy.Function("f")
   cases = (
      sympy.Integral(2 * t + 4, (t, 1, 4)),
      sympy.Integral(sympy.cos(x), x),
      sympy.Derivative(x ** 3, x),
      sympy.Limit(sympy.sin(x) / x, x, 0, "+"),
      sympy.Sum(1 / t ** 2, (t, 1, sympy.oo)),
      f(x) + 1,
      sympy.Gt(x, 2),
   )

   for expression in cases:
      assert to_sympy(from_sympy(expression)) == expression


def test_an_unknown_sympy_class_is_refused():
   with pytest.raises(UnsupportedMathJSON):
      from_sympy(sympy.Matrix([[1, 2]]))
