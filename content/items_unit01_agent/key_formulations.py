"""Each agent-drafted Unit 1 item's stem, written as the SymPy computation of the answer it asks for.

Read by tools/key_recheck.py. Every entry was written from the stem text alone, never from the
stored key, so a match is evidence that the key answers the stem. An edited stem needs its entry
rewritten the same way before the recheck can pass again. app/items/ingest.py loads only .json
records, so this file never reaches the bank.

The composition stems name f, g and h only through tabulated values, so their limits are built
from those values with the limit theorems: a continuous outer function passes the limit through,
and a jump in the outer function is resolved only when the inner argument is x itself approaching
from a stated side. When the side of approach cannot be read off the stem, every candidate is
returned. The asymptote stems return every x at which a one-sided limit is infinite.
"""
import itertools

import sympy
from sympy import Abs, ln, oo

from tools.key_recheck import x

ITEM_PREFIX = "ITM-AGT-"


class StatedFunction:
   """A function known through values at points, an optional formula, and optional jumps given
   as {point: (left_limit, right_limit)}."""

   def __init__(self, values=None, formula=None, jumps=None):
      self.values = values or {}
      self.formula = formula
      self.jumps = jumps or {}

   def value(self, point):
      if self.formula is not None:
         return self.formula.subs(x, point)

      return sympy.Integer(self.values[point])

   def limits(self, point, side):
      """Possible limits of this function at an argument tending to point. side is "+" or "-"
      when the argument is x itself approaching from that side, "+-" for a two-sided limit in x,
      and None when the argument is an inner function whose side of approach is unknown."""
      has_jump = point in self.jumps

      if not has_jump:
         return {self.value(point)}

      left_limit, right_limit = self.jumps[point]

      if side == "+":
         return {sympy.Integer(right_limit)}

      if side == "-":
         return {sympy.Integer(left_limit)}

      return {sympy.Integer(left_limit), sympy.Integer(right_limit)}


def tabulated(pairs):
   return StatedFunction(values=dict(enumerate(pairs)))


def composition_limits(functions, chain, point, side):
   """Possible limits of the composition named by chain (outermost first, "fgh" is f(g(h(x))))."""
   candidates = {(sympy.Integer(point), side)}

   for name in reversed(chain):
      stated = functions[name]
      candidates = {(limit, None) for argument, approach in candidates for limit in stated.limits(argument, approach)}

   return {limit for limit, _ in candidates}


def combination_limit(functions, point, combine, chains, side="+-"):
   """The limit of combine(*chain limits), taking the quotient theorem only with a nonzero
   denominator (combine raises ZeroDivisionError otherwise)."""
   per_chain = [sorted(composition_limits(functions, chain, point, side), key=float) for chain in chains]
   results = []

   for chosen in itertools.product(*per_chain):
      results.append(sympy.nsimplify(combine(*chosen)))

   distinct = list(dict.fromkeys(results))

   return distinct[0] if len(distinct) == 1 else distinct


def quotient(numerator, denominator):
   denominator_is_zero = denominator == 0

   if denominator_is_zero:
      raise ZeroDivisionError("limit of the denominator is 0")

   return sympy.Rational(numerator) / denominator


def three_tables(f_values, g_values, h_values):
   return {"f": tabulated(f_values), "g": tabulated(g_values), "h": tabulated(h_values)}


def with_jump_in_g(f_values, g_values, h_values, jump_point, left_limit, right_limit):
   functions = three_tables(f_values, [0] * 5, h_values)
   g_known = {index: value for index, value in enumerate(g_values) if value is not None}
   functions["g"] = StatedFunction(values=g_known, jumps={jump_point: (left_limit, right_limit)})

   return functions


def with_formula_f(formula, g_values, h_values):
   functions = three_tables([0] * 5, g_values, h_values)
   functions["f"] = StatedFunction(formula=formula)

   return functions


def vertical_asymptotes(expression, denominators=(), log_arguments=()):
   """Every x at which a one-sided limit of expression is infinite, checked at each real zero of
   the denominators as written and of the log arguments."""
   candidates = set()

   for factor in list(denominators) + list(log_arguments):
      candidates.update(root for root in sympy.solve(factor, x) if root.is_real)

   asymptotes = []

   for candidate in sorted(candidates):
      one_sided = [sympy.limit(expression, x, candidate, direction) for direction in ("+", "-")]
      is_infinite = any(limit in (oo, -oo, sympy.zoo) for limit in one_sided)

      if is_infinite:
         asymptotes.append(candidate)

   return asymptotes


def rational_asymptotes(numerator, denominator):
   return vertical_asymptotes(numerator / denominator, denominators=[denominator])


def log_plus_rational_asymptotes(log_argument, numerator, denominator):
   expression = ln(Abs(log_argument)) + numerator / denominator

   return vertical_asymptotes(expression, denominators=[denominator], log_arguments=[log_argument])


BY_SUFFIX = {
   "01003-00": lambda: combination_limit(
      three_tables([3, 3, 2, 3, 4], [4, 1, 4, 0, 4], [3, 0, 0, 2, 1]), 2, lambda fgh: fgh, ["fgh"]),
   "01003-01": lambda: combination_limit(
      three_tables([0, 3, 2, 4, 2], [1, 3, 1, 3, 2], [0, 4, 1, 3, 0]), 1, lambda gfh: gfh, ["gfh"]),
   "01003-02": lambda: combination_limit(
      three_tables([0, 1, 1, 0, 4], [3, 2, 3, 3, 1], [4, 2, 4, 2, 2]), 1, lambda hgf: hgf, ["hgf"]),
   "01003-03": lambda: combination_limit(
      three_tables([1, 2, 2, 0, 0], [4, 1, 1, 3, 1], [0, 3, 2, 2, 0]), 3, lambda gfh: gfh, ["gfh"]),
   "01003-04": lambda: combination_limit(
      three_tables([2, 4, 0, 1, 0], [4, 3, 2, 0, 3], [4, 3, 2, 1, 2]), 1,
      lambda fg, gh, hf: 3*fg + gh + 3*hf, ["fg", "gh", "hf"]),
   "01003-05": lambda: combination_limit(
      three_tables([4, 4, 3, 4, 4], [1, 2, 2, 2, 4], [3, 2, 0, 0, 1]), 2,
      lambda fg, gh, hf: 3*fg + 2*gh + hf, ["fg", "gh", "hf"]),
   "01003-06": lambda: combination_limit(
      three_tables([2, 2, 2, 1, 4], [1, 1, 4, 2, 1], [4, 4, 1, 3, 4]), 3,
      lambda fg, hf, gh: fg - 2*hf - gh, ["fg", "hf", "gh"]),
   "01003-07": lambda: combination_limit(
      three_tables([4, 2, 3, 1, 3], [2, 1, 2, 2, 2], [3, 1, 0, 1, 0]), 3,
      lambda gh, fg, hf: 3*gh - 2*fg + hf, ["gh", "fg", "hf"]),
   "01003-08": lambda: combination_limit(
      three_tables([4, 0, 2, 2, 1], [2, 1, 3, 4, 2], [4, 1, 0, 4, 4]), 2,
      lambda hf, fg, gh: quotient(hf + fg, gh), ["hf", "fg", "gh"]),
   "01003-09": lambda: combination_limit(
      three_tables([2, 1, 4, 0, 2], [4, 0, 2, 3, 1], [4, 0, 4, 0, 1]), 2,
      lambda fg, hf, gh: quotient(fg + hf, gh), ["fg", "hf", "gh"]),
   "01003-10": lambda: combination_limit(
      three_tables([3, 4, 4, 4, 3], [4, 3, 4, 4, 2], [0, 1, 1, 1, 1]), 1,
      lambda fg, hf, gh: quotient(fg + hf, gh), ["fg", "hf", "gh"]),
   "01003-11": lambda: combination_limit(
      three_tables([1, 4, 2, 2, 0], [4, 1, 2, 4, 3], [1, 0, 4, 1, 2]), 1,
      lambda gh, hf, fg: quotient(gh + hf, fg), ["gh", "hf", "fg"]),

   "01003-12": lambda: combination_limit(
      with_jump_in_g([1, 1, 3, 4, 2], [4, 4, None, 0, 4], [3, 4, 4, 1, 2], 2, 1, 4), 2,
      lambda hf, gh, fg: 3*hf + 2*gh + 3*fg, ["hf", "gh", "fg"], side="+"),
   "01003-13": lambda: combination_limit(
      with_jump_in_g([3, 1, 3, 3, 4], [1, 1, None, 4, 3], [4, 4, 1, 4, 0], 2, 1, 2), 2,
      lambda hf, fg, gh: 3*hf + fg - gh, ["hf", "fg", "gh"], side="-"),
   "01003-14": lambda: combination_limit(
      with_jump_in_g([3, 3, 4, 0, 1], [3, None, 0, 4, 3], [3, 3, 3, 3, 0], 1, 0, 1), 1,
      lambda hf, fg, gh: 3*hf - 2*fg + 3*gh, ["hf", "fg", "gh"], side="+"),
   "01003-15": lambda: combination_limit(
      with_jump_in_g([0, 2, 0, 0, 0], [2, 0, 1, None, 1], [4, 2, 1, 2, 0], 3, 0, 2), 3,
      lambda fg, hf, gh: fg + hf - gh, ["fg", "hf", "gh"], side="-"),

   "01003-16": lambda: combination_limit(
      with_formula_f(x**2 - 3*x + 2, [3, 4, 1, 1, 3], [3, 0, 3, 0, 0]), 2,
      lambda fg, hf, gh: 2*fg + 2*hf + 3*gh, ["fg", "hf", "gh"]),
   "01003-17": lambda: combination_limit(
      with_formula_f(x**2 - x + 2, [1, 0, 4, 2, 2], [0, 0, 1, 2, 4]), 1,
      lambda fg, gh, hf: 3*fg - 2*gh - hf, ["fg", "gh", "hf"]),
   "01003-18": lambda: combination_limit(
      with_formula_f(x**2 - 3*x + 2, [2, 2, 1, 2, 3], [4, 4, 1, 4, 3]), 2,
      lambda gh, fg, hf: 2*gh + fg + hf, ["gh", "fg", "hf"]),
   "01003-19": lambda: combination_limit(
      with_formula_f(x**2 - 3*x + 2, [1, 2, 0, 0, 2], [1, 1, 3, 1, 4]), 3,
      lambda fg, gh, hf: 2*fg - 2*gh - hf, ["fg", "gh", "hf"]),

   "01009-00": lambda: rational_asymptotes(
      (x**2 + 8*x + 15) * (x**2 - 4*x + 3), (x**2 - 9) * (x**2 + 9*x + 20)),
   "01009-01": lambda: rational_asymptotes(
      (x**2 - 9) * (x**2 - 16), (x**2 - 7*x + 12) * (x**2 + 5*x + 6)),
   "01009-02": lambda: rational_asymptotes(
      (x**2 + 9*x + 20) * (x**2 + 3*x + 2), (x**2 + 6*x + 8) * (x**2 + x - 20)),
   "01009-03": lambda: rational_asymptotes(
      (x**2 - 9*x + 18) * (x**2 + 4*x + 3), (x**2 - 3*x - 18) * (x**2 + x - 12)),
   "01009-04": lambda: rational_asymptotes(
      (x**2 + 2*x - 15) * (x**2 - 6*x + 8), (x**2 - 7*x + 12) * (x**2 + 8*x + 15)),
   "01009-05": lambda: rational_asymptotes(
      (x**2 + 2*x - 3) * (x**2 - 7*x + 10), (x**2 - 6*x + 5) * (x**2 - 9)),
   "01009-06": lambda: rational_asymptotes(
      (x**2 + 3*x - 10) * (x**2 + 5*x + 6), (x**2 + x - 6) * (x**2 + 2*x - 15)),
   "01009-07": lambda: rational_asymptotes(
      (x**2 + 3*x + 2) * (x**2 - 3*x - 18), (x**2 - 5*x - 6) * (x**2 - 4) * (x - 2)),
   "01009-08": lambda: rational_asymptotes(
      (x**2 - 4*x + 3) * (x**2 + 8*x + 15), (x**2 + 4*x - 5) * (x**2 - 2*x - 3) * (x + 1)),
   "01009-09": lambda: rational_asymptotes(
      (x**2 - 11*x + 30) * (x**2 - 9), (x**2 - 3*x - 18) * (x**2 - 6*x + 5) * (x - 1)),
   "01009-10": lambda: rational_asymptotes(
      (x**2 + 6*x + 8) * (x**2 + x - 20), (x**2 + 9*x + 20) * (x**2 - x - 6) * (x - 3)),
   "01009-11": lambda: rational_asymptotes(
      (x**2 - 2*x - 8) * (x**2 - x - 30), (x**2 - 4*x - 12) * (x**2 - 3*x - 4) * (x + 1)),

   "01009-12": lambda: log_plus_rational_asymptotes(
      x + 3, (x**2 - 2*x - 8) * (x**2 - 1), (x**2 - 5*x + 4) * (x + 1)),
   "01009-13": lambda: log_plus_rational_asymptotes(
      x - 1, (x**2 - 25) * (x**2 - x - 2), (x**2 + 3*x - 10) * (x + 1)),
   "01009-14": lambda: log_plus_rational_asymptotes(
      x - 2, (x**2 - x - 12) * (x**2 - 11*x + 30), (x**2 - 3*x - 18) * (x - 5)),
   "01009-15": lambda: log_plus_rational_asymptotes(
      x - 4, (x**2 - 2*x - 15) * (x**2 - 4), (x**2 - 7*x + 10) * (x + 2)),

   "01009-16": lambda: rational_asymptotes(
      (2*x + 2) * (x**2 + 7*x + 12), (x**2 + 5*x + 4) * (x**2 + 8*x + 15)),
   "01009-17": lambda: rational_asymptotes(
      (-2*x - 10) * (x**2 + x - 12), (x**2 + 2*x - 15) * (x**2 - x - 20)),
   "01009-18": lambda: rational_asymptotes(
      (3*x + 15) * (x**2 - 7*x + 12), (x**2 + x - 20) * (x**2 - 8*x + 15)),
   "01009-19": lambda: rational_asymptotes(
      (-2*x - 10) * (x**2 - 7*x + 6), (x**2 + 4*x - 5) * (x**2 - 9*x + 18)),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
