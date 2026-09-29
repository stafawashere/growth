"""Blind re-solve of the stems in stems_s15v2.json, each written from its stem text alone."""
import sympy
from sympy import Rational, oo

from tools.key_recheck import series_value

n = sympy.Symbol("n", integer=True, positive=True)


def sum_from_partial_sums(partial_sum):
   return sympy.limit(partial_sum, n, oo)


def sum_of_product_series(numerator, shift):
   term = numerator / ((n + shift) * (n + shift + 1))

   return series_value(term, n, 1)


BY_SUFFIX = {
   "10021-22": lambda: sum_from_partial_sums((4 * n + 5) / (n + 6)),
   "10021-23": lambda: sum_of_product_series(7, 0),
   "10021-24": lambda: sum_from_partial_sums((9 * n + 9) / (5 * n + 4)),
   "10021-25": lambda: sum_of_product_series(1, 0),
   "10021-26": lambda: sum_of_product_series(1, 5),
   "10021-27": lambda: sum_from_partial_sums(6 - 8 * sympy.Integer(3) ** (-n)),
   "10021-28": lambda: sum_from_partial_sums((5 * n + 5) / (3 * n + 7)),
   "10021-29": lambda: sum_of_product_series(2, 0),
   "10021-30": lambda: sum_of_product_series(2, 2),
   "10021-31": lambda: sum_from_partial_sums((5 * n - 4) / (2 * n + 2)),
   "10021-32": lambda: sum_from_partial_sums(1 - 5 * sympy.Integer(4) ** (-n)),
   "10021-33": lambda: sum_of_product_series(1, 6),
   "10021-34": lambda: sum_from_partial_sums(3 - 9 * sympy.Integer(4) ** (-n)),
   "10021-35": lambda: sum_of_product_series(9, 5),
   "10021-36": lambda: sum_from_partial_sums((n - 3) / (n + 4)),
   "10021-37": lambda: sum_from_partial_sums((2 * n) / (3 * n + 3)),
   "10021-38": lambda: sum_from_partial_sums((n + 7) / (4 * n + 4)),
   "10021-39": lambda: sum_from_partial_sums(8 - 2 * Rational(3, 4) ** n),
   "10021-40": lambda: sum_from_partial_sums((n - 9) / (3 * n + 8)),
   "10021-41": lambda: sum_of_product_series(3, 4),
   "10021-42": lambda: sum_from_partial_sums((5 * n + 6) / (4 * n + 8)),
   "10021-43": lambda: sum_from_partial_sums(4 - 2 * Rational(2, 3) ** n),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
