"""Each agent-drafted P1 item's stem, written as the SymPy computation of the answer it asks for.

Read by tools/key_recheck.py and tests/items/test_key_recheck.py. Every entry was written from the
stem text alone, never from the stored key, so a match is evidence that the key answers the stem.
An edited stem needs its entry rewritten the same way before the recheck can pass again.
app/items/ingest.py loads only .json records, so this file never reaches the bank.
"""
import sympy
from sympy import E, Interval, Rational, cos, cot, csc, exp, ln, oo, pi, sec, sin, sqrt, tan

from tools.key_recheck import (
   continuity_value,
   continuous_domain,
   derivative,
   derivative_by_definition,
   horizontal_tangent_points,
   implicit_second_derivative,
   implicit_slope,
   integer_sum_of_interval_containing,
   limit_at,
   second_derivative_along_solution,
   tangent_line,
   vertical_tangent_points,
   x,
   y,
)

t, s, theta = sympy.symbols("t s theta")
k, a, b = sympy.symbols("k a b")

ITEM_PREFIX = "ITM-AGT-"


def piecewise_interval_sum(left, right, joint, left_open, anchor):
   """The integer sum over the continuous interval holding anchor, for a function given by left
   below joint and right from joint on, continuous at joint only when the two sides meet."""
   left_domain = continuous_domain(left, Interval.open(-oo, joint) if left_open else Interval(-oo, joint))
   right_domain = continuous_domain(right, Interval(joint, oo))
   meets_at_joint = sympy.simplify(sympy.limit(left, x, joint, "-") - right.subs(x, joint)) == 0
   domain = left_domain.union(right_domain)

   if not meets_at_joint:
      domain = domain - sympy.FiniteSet(joint)

   return integer_sum_of_interval_containing(domain, anchor)


def slope_where_y_exceeds_one():
   curve = x**2 + 3*x*y - y**2 - 3*x**2
   heights = [height for height in sympy.solve(curve.subs(x, 1), y) if height.is_real and height > 1]

   return [implicit_slope(curve).subs({x: 1, y: height}) for height in heights]


def larger(values):
   return max(values)


def smaller(values):
   return min(values)


def heights(points):
   return sorted({point[1] for point in points})


def abscissas(points):
   return sorted({point[0] for point in points})


BY_SUFFIX = {
   "01004-00": lambda: limit_at((x**2 - x - 6) / (x**2 - 9), 3),
   "01004-01": lambda: limit_at((x**2 + 2*x - 3) / (x**2 + 4*x + 3), -3),
   "01004-02": lambda: limit_at((x - sqrt(x + 12)) / (x - 4), 4),
   "01004-03": lambda: limit_at((cos(x)**2 + cos(x) - 2) / (cos(x)**2 - 1), 0),
   "01004-04": lambda: limit_at((x - 2) / (x - sqrt(x + 2)), 2),
   "01004-05": lambda: limit_at((x**2 + x - 6) / (x**2 - 4), 2),
   "01004-06": lambda: limit_at((x**2 - 7*x + 10) / (x**2 - x - 2), 2),
   "01004-07": lambda: limit_at((x - 6 / (x + 1)) / (x - 2), 2),
   "01004-08": lambda: limit_at((x + 2 / (x - 3)) / (x - 1), 1),
   "01004-09": lambda: limit_at((sin(x)**2 - 3*sin(x) + 2) / (sin(x)**2 + 2*sin(x) - 3), pi / 2),

   "01008-00": lambda: continuity_value(k, [2*x + 3, k**2 - k*x - 1], [(1, 2*k**2 - 4*k - 1)]),
   "01008-01": lambda: continuity_value(k, [4 - 3*x, k**2 + x + 3], [(-2, 7 + 4*k - k**2)]),
   "01008-02": lambda: continuity_value(k, [k**2*x + 2, 3*k*x], [(1, 2*k**2 + k - 4)]),
   "01008-03": lambda: continuity_value(a, [7 - x**2, a*x + b, 4*sqrt(x) + a], [1, 4], [a, b]),
   "01008-04": lambda: continuity_value(b, [exp(x) + a, b*x + 3, a*x**2 + x - a], [0, 2], [a, b]),
   "01008-05": lambda: continuity_value(k, [k**2*sin(x), cos(x) + k + 20], [(pi / 2, 2*k**2 - 3*k - 10)]),
   "01008-06": lambda: continuity_value(k, [(x**2 - 16) / (x - 4), k**2 + x], [(4, 2*k**2 + 2*k - 4)]),
   "01008-07": lambda: continuity_value(b, [(x**2 - 1) / (x - 1), a*x**2 + b, 6*x + 11 - a], [1, 3], [a, b]),
   "01008-08": lambda: continuity_value(a, [a*3**x + b, 3*x + 5, 2*b*x + a], [0, 1], [a, b]),
   "01008-09": lambda: continuity_value(k, [k**2 + ln(x), k*x + 6], [(1, 2*k**2 + 3*k + 2)]),

   "01015-00": lambda: integer_sum_of_interval_containing(continuous_domain(sqrt(x + 5) / (x**2 - 2*x - 8)), 0),
   "01015-01": lambda: integer_sum_of_interval_containing(continuous_domain((x + 4) / ((x + 1) * (x**2 - 6*x + 8))), 0),
   "01015-02": lambda: integer_sum_of_interval_containing(continuous_domain(ln(x + 3) / (x**2 - 7*x + 10)), 0),
   "01015-03": lambda: piecewise_interval_sum((x + 21) / (x**2 + 4*x + 3), 3 / (6 - x), 3, True, 0),
   "01015-04": lambda: integer_sum_of_interval_containing(continuous_domain(sqrt(12 - 3*x) / ((x - 1) * (x**2 - 16))), 2),
   "01015-05": lambda: integer_sum_of_interval_containing(continuous_domain((x**2 - 1) / ((x**2 + 5*x + 4) * (x - 3))), 0),
   "01015-06": lambda: integer_sum_of_interval_containing(continuous_domain((x + 3) / (x**2 + 5*x - 6), Interval(-4, 6)), 0),
   "01015-07": lambda: integer_sum_of_interval_containing(continuous_domain(ln(25 - x**2) / (x + 2)), 0),
   "01015-08": lambda: piecewise_interval_sum(sqrt(x + 8) / (x + 4), 3 * sqrt(17 - x) / (25 - 5*x), 1, True, 0),
   "01015-09": lambda: integer_sum_of_interval_containing(continuous_domain((x + 1) / ((x - 2) * sqrt(20 + x - x**2))), 0),

   "02002-00": lambda: derivative_by_definition(3*x**2 - 5*x),
   "02002-01": lambda: derivative_by_definition(x**2 + 4*x).subs(x, 3),
   "02002-02": lambda: derivative_by_definition(5 - 2*x**2),
   "02002-03": lambda: derivative_by_definition(sqrt(x + 3)).subs(x, 6),
   "02002-04": lambda: derivative_by_definition(1 / (3*x + 1)),
   "02002-05": lambda: derivative_by_definition(x**3 - 2*x).subs(x, -1),
   "02002-06": lambda: derivative_by_definition(sqrt(2*x + 5)),
   "02002-07": lambda: derivative_by_definition(4 / x).subs(x, 2),
   "02002-08": lambda: derivative_by_definition(x / (x + 1)),
   "02002-09": lambda: limit_at(((2*x**2 + 1) - (2*3**2 + 1)) / (x - 3), 3),

   "02006-00": lambda: derivative(5*x**4 - 3*x**2 + 8*x - 6),
   "02006-01": lambda: derivative(3*x**2 + 6*sqrt(x) - 4),
   "02006-02": lambda: derivative(4 / x**2 + 2*x**3 + 9),
   "02006-03": lambda: derivative(x**3 - 12 / x + 5).subs(x, 2),
   "02006-04": lambda: derivative(2*x**5 - 3 / x + 7*x, x, 2),
   "02006-05": lambda: derivative(6 * sympy.cbrt(x**2) + x**4 - 10),
   "02006-06": lambda: derivative(-2 / sqrt(x) + 5*x**2 + 1),
   "02006-07": lambda: derivative(8*sqrt(t) - 4 / t**2 + 3*t, t).subs(t, 4),
   "02006-08": lambda: derivative(x**4 - 6*x**2 + 2 / x + 3, x, 2).subs(x, 1),
   "02006-09": lambda: derivative(3 / s**4 - 10 * (s**2)**Rational(1, 5) + 2, s),

   "02007-00": lambda: derivative(5*cos(x) + 3*exp(x)),
   "02007-01": lambda: derivative(x**3 - 4*cos(x) + exp(x)),
   "02007-02": lambda: derivative(2*cos(x) + 7*ln(x) - exp(x)),
   "02007-03": lambda: derivative(3*cos(x) - 2*exp(x)).subs(x, pi / 2),
   "02007-04": lambda: derivative(2*ln(x) + 3*cos(x) + exp(x)).subs(x, pi / 6),
   "02007-05": lambda: derivative(exp(x) - 2*cos(x) + 3*ln(x)),
   "02007-06": lambda: derivative(5*exp(t) - 3*cos(t) + t**4, t),
   "02007-07": lambda: derivative(6*cos(x) - exp(x)).subs(x, pi / 6),
   "02007-08": lambda: derivative(3*ln(x) - 4*sin(x) + 2*cos(x) + exp(x)),
   "02007-09": lambda: derivative(7*exp(x) + cos(x) - 2*ln(x)),

   "02008-00": lambda: derivative(exp(x) * (x - 1) / (x + 1)),
   "02008-01": lambda: derivative(x**2 * cos(x) / (x + 1)).subs(x, pi),
   "02008-02": lambda: derivative((x + 1) / (x * exp(x))),
   "02008-03": lambda: derivative(x**2 * exp(x) / 4),
   "02008-04": lambda: derivative(x**2 * exp(x) / (x**2 + 1)),
   "02008-05": lambda: derivative(exp(x) * sin(x) / (1 + cos(x))),
   "02008-06": lambda: derivative(x * exp(x) / (x + 1)).subs(x, 1),
   "02008-07": lambda: derivative(t**2 * exp(t) / (t + 1), t),
   "02008-08": lambda: derivative((x**2 - 3) * x / (2*x + 1)).subs(x, 1),
   "02008-09": lambda: derivative(ln(x) * x / (x + 2)),

   "02010-00": lambda: derivative(cot(x) + csc(x)),
   "02010-01": lambda: derivative(3*csc(x) - 2*cot(x)),
   "02010-02": lambda: derivative(x * cot(x)).subs(x, pi / 6),
   "02010-03": lambda: derivative(tan(x) + cot(x)),
   "02010-04": lambda: derivative(csc(t) * cot(t), t),
   "02010-05": lambda: derivative(csc(x) - 2*cot(x)).subs(x, pi / 6),
   "02010-06": lambda: derivative(x**2 * cot(x)),
   "02010-07": lambda: derivative(6*tan(x) - sec(x)),
   "02010-08": lambda: derivative(sec(theta) * tan(theta), theta),
   "02010-09": lambda: derivative(4*cot(x) + tan(x)).subs(x, pi / 6),

   "02011-00": lambda: tangent_line(x**3 - x**2 + 4, -1),
   "02011-01": lambda: tangent_line(x * exp(x + 2), -2),
   "02011-02": lambda: tangent_line(x**2 / (x + 3), -2),
   "02011-03": lambda: tangent_line(sqrt(x + 10), -6).subs(x, Rational(-56, 10)),
   "02011-04": lambda: tangent_line(2*x**2 - 5*x + 1, -1),
   "02011-05": lambda: tangent_line((x + 1) * cos(x), -pi / 2),
   "02011-06": lambda: tangent_line(x**3 + 2*x**2 - x, 1),
   "02011-07": lambda: tangent_line(x * ln(x), E),
   "02011-08": lambda: tangent_line(3*x / (x**2 + 1), 2),
   "02011-09": lambda: tangent_line(exp(2*x + 4) + 3*x, -2).subs(x, Rational(-19, 10)),

   "03001-00": lambda: derivative(x * sin(5*x)**3),
   "03001-01": lambda: derivative(x**2 * exp(3*x)),
   "03001-02": lambda: derivative(x * sqrt(1 + x**3)).subs(x, 2),
   "03001-03": lambda: derivative(cos(2*x) / x),
   "03001-04": lambda: derivative(x * ln(cos(x**2))),
   "03001-05": lambda: derivative(x * exp(sin(3*x))).subs(x, pi / 3),
   "03001-06": lambda: derivative(x * (x**2 + 1)**5),
   "03001-07": lambda: derivative(x / sqrt(2*x + 1)).subs(x, 4),
   "03001-08": lambda: derivative(x * sqrt(ln(x**2 + 1))),
   "03001-09": lambda: derivative(exp(2*x) * sin(x)**2).subs(x, pi / 6),

   "03004-00": lambda: implicit_slope(x**2 + 4*x*y + y**3 - 10),
   "03004-01": lambda: implicit_slope(y*sin(x) + y**2 - 4*x),
   "03004-02": lambda: implicit_slope(x*y + y**2 - x**3 - 5).subs({x: 1, y: 2}),
   "03004-03": slope_where_y_exceeds_one,
   "03004-04": lambda: implicit_slope(x**2 - 3*x*y + y**2 - 3*x + 4).subs({x: 1, y: 2}),
   "03004-05": lambda: implicit_slope(3*x**2 - 2*x*y + y**3 - y - 8).subs({x: 2, y: 1}),
   "03004-06": lambda: implicit_slope(y**2 - 5*x*y - 4*x**3),
   "03004-07": lambda: implicit_slope(2*x**3 + x*y**2 - 7*y),
   "03004-08": lambda: implicit_slope(x**2*y + y**3 - 10).subs({x: 1, y: 2}),
   "03004-09": lambda: implicit_slope(x*y**2 + 3*y - 2*x**2),

   "03005-00": lambda: heights(horizontal_tangent_points((x**2 + 2*x) * (y**2 - 2*y - 8) - 5, quadrant=2)),
   "03005-01": lambda: abscissas(vertical_tangent_points((x**2 - 8*x + 12) * (6*y - y**2 - 8) - 12, quadrant=1)),
   "03005-02": lambda: abscissas(horizontal_tangent_points(y**2 - (x**3 - 12*x + 11))),
   "03005-03": lambda: heights(horizontal_tangent_points((x**2 + 4*x + 3) * (y**2 + 4*y + 3) + 3, quadrant=3)),
   "03005-04": lambda: larger(heights(horizontal_tangent_points((x**2 - 2*x) * (y**2 + 6*y + 5) - 3))),
   "03005-05": lambda: abscissas(vertical_tangent_points((x**2 - 4*x + 1) * (y**2 + 2*y) + 9, quadrant=4)),
   "03005-06": lambda: larger(abscissas(vertical_tangent_points((x**2 - 8*x + 7) * (1 - y**2) + 5))),
   "03005-07": lambda: smaller(abscissas(vertical_tangent_points((x**2 - 10*x + 21) * (y**2 + 4*y + 3) - 3))),
   "03005-08": lambda: abscissas(vertical_tangent_points((x**2 + 6*x + 5) * (2*y - y**2) - 12, quadrant=2)),
   "03005-09": lambda: smaller(heights(horizontal_tangent_points((y**2 + 6*y + 7) * (1 - x**2) + 1))),

   "03008-00": lambda: derivative(x**3 * ln(x), x, 2),
   "03008-01": lambda: derivative(x * exp(2*x), x, 3).subs(x, 1),
   "03008-02": lambda: second_derivative_along_solution(x**2 + y**2).subs({x: 1, y: 2}),
   "03008-03": lambda: second_derivative_along_solution(x*y + 2*x).subs({x: 2, y: -1}),
   "03008-04": lambda: implicit_second_derivative(x**2 + x*y + y**2 - 7).subs({x: 1, y: 2}),
   "03008-05": lambda: derivative(x**2 * exp(2*x), x, 3),
   "03008-06": lambda: derivative(x * exp(-x), x, 2),
   "03008-07": lambda: second_derivative_along_solution(x*y + x**2),
   "03008-08": lambda: second_derivative_along_solution(x**2 * y).subs({x: -2, y: 1}),
   "03008-09": lambda: second_derivative_along_solution(x * y**2).subs({x: 2, y: 1}),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
