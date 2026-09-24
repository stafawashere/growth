"""Each agent-drafted Unit 2 item's stem, written as the SymPy computation of the answer it asks for.

Read by tools/key_recheck.py. Every entry was written from the stem text alone, never from the
stored key, so a match is evidence that the key answers the stem. An edited stem needs its entry
rewritten the same way before the recheck can pass again. app/items/ingest.py loads only .json
records, so this file never reaches the bank.

The difference-quotient stems are limits taken directly, with the stem's increment renamed x. The
product and quotient stems replace f and g by polynomials carrying only the stated value and
derivative at the point, which is all the derivative there depends on; a stated tangent line
supplies g's value and slope.
"""
import sympy
from sympy import E, Rational, cos, exp, ln, pi, sin, sqrt, tan

from tools.key_recheck import derivative, function_with_values, limit_at, x

ITEM_PREFIX = "ITM-AGT-"


def derivative_at(combine, point, f_value, f_slope, g_value, g_slope):
   f = function_with_values(point, [f_value, f_slope])
   g = function_with_values(point, [g_value, g_slope])

   return derivative(combine(f, g)).subs(x, point)


def derivative_with_tangent_line(combine, point, f_value, f_slope, g_tangent_line):
   g_value = g_tangent_line.subs(x, point)
   g_slope = derivative(g_tangent_line).subs(x, point)

   return derivative_at(combine, point, f_value, f_slope, g_value, g_slope)


def product(f, g):
   return f * g


def ratio(f, g):
   return f / g


BY_SUFFIX = {
   "02003-00": lambda: limit_at(((3 + x)**2 - 9) / x, 0),
   "02003-01": lambda: limit_at(((-4 + x)**2 - 16) / x, 0),
   "02003-02": lambda: limit_at(((2 + x)**3 - 8) / x, 0),
   "02003-03": lambda: limit_at(((Rational(1, 2) + x)**2 - Rational(1, 4)) / x, 0),
   "02003-04": lambda: limit_at(((-1 + x)**4 - 1) / x, 0),
   "02003-05": lambda: limit_at(((Rational(1, 2) + x)**3 - Rational(1, 8)) / x, 0),
   "02003-06": lambda: limit_at((sin(pi / 6 + x) - Rational(1, 2)) / x, 0),
   "02003-07": lambda: limit_at((sin(pi / 3 + x) - sqrt(3) / 2) / x, 0),
   "02003-08": lambda: limit_at((sin(pi / 4 + x) - sqrt(2) / 2) / x, 0),
   "02003-09": lambda: limit_at((cos(pi / 6 + x) - sqrt(3) / 2) / x, 0),
   "02003-10": lambda: limit_at((cos(pi / 4 + x) - sqrt(2) / 2) / x, 0),
   "02003-11": lambda: limit_at((tan(pi / 6 + x) - sqrt(3) / 3) / x, 0),
   "02003-12": lambda: limit_at((exp(ln(2) + x) - 2) / x, 0),
   "02003-13": lambda: limit_at((exp(ln(3) + x) - 3) / x, 0),
   "02003-14": lambda: limit_at((exp(1 + x) - E) / x, 0),
   "02003-15": lambda: limit_at(((1 + x)**2 + 3*(1 + x) - 4) / x, 0),
   "02003-16": lambda: limit_at((sin(pi / 2 + x) - 1) / x, 0),
   "02003-17": lambda: limit_at(((5 + x)**2 - 25) / x, 0),
   "02003-18": lambda: limit_at(((x + 1)**2 - 9) / (x - 2), 2),
   "02003-19": lambda: limit_at((sqrt(x + 4) - 3) / (x - 5), 5),

   "02009-00": lambda: derivative_at(product, 2, -2, 2, -3, 4),
   "02009-01": lambda: derivative_at(product, 4, -4, 2, 3, 2),
   "02009-02": lambda: derivative_at(product, 4, -1, 4, 2, 4),
   "02009-03": lambda: derivative_at(product, 1, 3, -2, 3, 1),
   "02009-04": lambda: derivative_at(product, 2, 3, -1, -1, 4),
   "02009-05": lambda: derivative_at(ratio, 4, 3, 2, -3, 4),
   "02009-06": lambda: derivative_at(ratio, 4, 1, 3, -1, 4),
   "02009-07": lambda: derivative_at(ratio, -1, 1, 6, -3, 2),
   "02009-08": lambda: derivative_at(ratio, 4, 2, 3, 3, 1),
   "02009-09": lambda: derivative_at(ratio, 3, -4, 4, -3, 7),

   "02009-10": lambda: derivative_with_tangent_line(product, 2, -4, -3, 2*x - 7),
   "02009-11": lambda: derivative_with_tangent_line(product, 3, 2, -3, 2*x - 2),
   "02009-12": lambda: derivative_with_tangent_line(ratio, 1, -4, 4, 2*x),
   "02009-13": lambda: derivative_with_tangent_line(ratio, 2, 5, -1, x),

   "02009-14": lambda: derivative_at(product, 3, 6, -1, 13, -2),
   "02009-15": lambda: derivative_at(product, 5, 9, 2, 12, 2),
   "02009-16": lambda: derivative_at(ratio, 3, 50, -3, 3, 2),
   "02009-17": lambda: derivative_at(ratio, 5, 40, 18, 7, -1),

   "02009-18": lambda: derivative_at(lambda f, g: f*g - 3*f, 1, -2, 6, -1, 1),
   "02009-19": lambda: derivative_at(lambda f, g: f/g + x**2, -1, -1, -3, 2, -1),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
