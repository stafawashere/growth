"""Each agent-drafted unit 7 item's stem, written as the SymPy computation of the answer it asks for.

Read by tools/key_recheck.py. Every entry was written from the stem text alone, never from the
stored key, so a match is evidence that the key answers the stem. An edited stem needs its entry
rewritten the same way before the recheck can pass again. app/items/ingest.py loads only .json
records, so this file never reaches the bank.
"""
import sympy
from sympy import E, Rational, cos, exp, ln, oo, pi, sec, sin, sqrt

from tools.key_recheck import definite_integral, euler_approximation, particular_solutions, x, y

u = sympy.symbols("u")
k = sympy.symbols("k")

ITEM_PREFIX = "ITM-AGT-"


def solution_value(slope_field, start_x, start_y, at):
   return [sympy.simplify(solution.subs(x, at)) for solution in particular_solutions(slope_field, start_x, start_y)]


def euler_to(slope_field, start_x, start_y, target_x, steps):
   step = (sympy.nsimplify(target_x) - start_x) / steps

   return euler_approximation(slope_field, start_x, start_y, step, steps)


def accumulated_position(rate, start_t, start_value, at):
   return sympy.simplify(start_value + definite_integral(rate, start_t, at, variable=u))


def right_endpoint_where_undefined(slope_field, start_x, start_y, search_width=20):
   endpoints = []

   for solution in particular_solutions(slope_field, start_x, start_y):
      as_ratio = sympy.together(solution.rewrite(sympy.sin).rewrite(sympy.cos))
      denominator = sympy.fraction(as_ratio)[1]
      to_the_right = sympy.Interval.open(start_x, start_x + search_width)
      poles = sympy.solveset(denominator, x, to_the_right)
      endpoints.append(sympy.simplify(sympy.Min(*poles)))

   return endpoints


def finite_endpoint_where_solution_vanishes(slope_field, start_x, start_y):
   endpoints = []

   for solution in particular_solutions(slope_field, start_x, start_y):
      zeros = [zero for zero in sympy.solve(solution, x) if zero.is_real]
      nearest_zero = min(zeros, key=lambda zero: abs(float(zero - start_x)))
      endpoints.append(sympy.simplify(nearest_zero))

   return endpoints


def exponential_rate(equation_in_k, condition):
   roots = sympy.solve(equation_in_k, k)

   return [root for root in roots if root.is_real and bool(condition(root))]


def characteristic(second, first, zeroth):
   return second * k**2 + first * k + zeroth


BY_SUFFIX = {
   "07003-00": lambda: particular_solutions(2*x*y, 0, 3),
   "07003-01": lambda: particular_solutions(3*x**2*y, 0, -2),
   "07003-02": lambda: particular_solutions(x*y, 2, 5),
   "07003-03": lambda: particular_solutions(-4*x*y, 0, Rational(1, 2)),
   "07003-04": lambda: particular_solutions(6*x**2*y, 1, -4),
   "07003-05": lambda: solution_value(2*x*y, 1, 7, 2),
   "07003-06": lambda: particular_solutions(y*cos(x), 0, 4),
   "07003-07": lambda: particular_solutions(y*sin(x), 0, 2),
   "07003-08": lambda: particular_solutions(3*y*cos(x), 0, -5),
   "07003-09": lambda: particular_solutions(y*sec(x)**2, 0, 3),
   "07003-10": lambda: particular_solutions(x*y**2, 0, 2),
   "07003-11": lambda: particular_solutions(3*x**2*y**2, 0, 1),
   "07003-12": lambda: particular_solutions(2*x*y**2, 0, -1),
   "07003-13": lambda: solution_value(4*x*y**2, 0, Rational(1, 3), Rational(1, 2)),
   "07003-14": lambda: particular_solutions(x*exp(-y), 0, 0),
   "07003-15": lambda: particular_solutions(x**2*exp(-y), 0, ln(3)),
   "07003-16": lambda: particular_solutions(exp(x - y), 0, ln(2)),
   "07003-17": lambda: particular_solutions(2*x*y / (x**2 + 1), 1, 4),
   "07003-18": lambda: particular_solutions(x*y / (x**2 + 4), 0, 6),
   "07003-19": lambda: particular_solutions(y*cos(x) / (sin(x) + 2), 0, -2),
   "07003-20": lambda: particular_solutions(x / y, 0, -3),
   "07003-21": lambda: particular_solutions(3*x**2 / y, 1, 2),
   "07003-22": lambda: particular_solutions(x**2 / y**2, 0, 2),

   "07004-00": lambda: euler_to(x + y, 0, 1, 1, 2),
   "07004-01": lambda: euler_to(x*y, 1, 2, 2, 2),
   "07004-02": lambda: euler_to(-x**2 + y, 0, 3, 1, 2),
   "07004-03": lambda: euler_to(2*x - y, 1, 3, 2, 2),
   "07004-04": lambda: euler_to(-x + y**2, 0, 1, Rational(1, 2), 2),
   "07004-05": lambda: euler_to(x - 2*y, 2, 3, 3, 2),
   "07004-06": lambda: euler_to(y*(x + 1), 0, 2, 1, 2),
   "07004-07": lambda: euler_to(x**2 + y, -1, 2, 0, 2),
   "07004-08": lambda: euler_to(y / x, 1, 3, 2, 2),
   "07004-09": lambda: euler_to(x*y**2, 0, 1, 1, 2),
   "07004-10": lambda: euler_to(-x + 3*y, 0, -1, 1, 2),
   "07004-11": lambda: euler_to(x + y, 2, 1, 1, 2),
   "07004-12": lambda: euler_to(x*y, 2, 3, 1, 2),
   "07004-13": lambda: euler_to(1 - y, 0, 4, Rational(3, 2), 3),
   "07004-14": lambda: euler_to(x + y, 0, 2, 1, 3),
   "07004-15": lambda: euler_to(-x + 2*y, 1, 1, 2, 3),
   "07004-16": lambda: euler_to(x - y, 0, 0, Rational(3, 2), 3),
   "07004-17": lambda: euler_to(x*y - 1, 0, 2, 1, 2),
   "07004-18": lambda: euler_to(2*x + y, 3, -1, 2, 2),
   "07004-19": lambda: euler_to(x*y + 1, 0, 1, -1, 2),

   "07007-00": lambda: exponential_rate(characteristic(1, 1, -12), lambda root: root > 0),
   "07007-01": lambda: exponential_rate(characteristic(1, -3, -10), lambda root: root < 0),
   "07007-02": lambda: exponential_rate(characteristic(1, 3, -10), lambda root: root > 0),
   "07007-03": lambda: exponential_rate(characteristic(1, 1, -6), lambda root: sympy.limit(exp(root*x), x, oo) == 0),
   "07007-04": lambda: exponential_rate(characteristic(1, 2, -8), lambda root: 5*exp(root) < 5),
   "07007-05": lambda: exponential_rate(characteristic(1, -3, -10), lambda root: exp(root) > 1),
   "07007-06": lambda: exponential_rate(characteristic(1, 2, -15), lambda root: 2*exp(root) > 2),
   "07007-07": lambda: exponential_rate(characteristic(1, -6, 8), lambda root: exp(root) > E**3),
   "07007-08": lambda: exponential_rate(characteristic(1, -8, 12), lambda root: sympy.And(root > 0, root < 4)),
   "07007-09": lambda: exponential_rate(characteristic(1, 6, 8), lambda root: exp(root) > exp(-3)),
   "07007-10": lambda: exponential_rate(characteristic(1, -4, -12), lambda root: sympy.limit(exp(root*x), x, oo) == oo),
   "07007-11": lambda: exponential_rate(characteristic(2, 1, -6), lambda root: root > 0),
   "07007-12": lambda: exponential_rate(characteristic(2, -5, -3), lambda root: sympy.limit(exp(root*x), x, oo) == 0),
   "07007-13": lambda: exponential_rate(characteristic(3, 5, -2), lambda root: exp(root) > 1),
   "07007-14": lambda: exponential_rate(characteristic(2, 1, -15), lambda root: 4*exp(root) > 4),
   "07007-15": lambda: exponential_rate(characteristic(3, -4, -4), lambda root: exp(root) < 1),
   "07007-16": lambda: exponential_rate(characteristic(2, 5, -3), lambda root: root > 0),
   "07007-17": lambda: exponential_rate(characteristic(2, 3, -9), lambda root: exp(root) < exp(-1)),

   "07011-00": lambda: accumulated_position(3*u**2 - 4*u + 1, 0, 5, 2),
   "07011-01": lambda: accumulated_position(4*u**3 - 6*u, 0, -3, 2),
   "07011-02": lambda: accumulated_position(2*sin(u), 0, 1, pi / 3),
   "07011-03": lambda: accumulated_position(exp(2*u), 0, 1, ln(3)),
   "07011-04": lambda: accumulated_position(1 / (u + 1), 0, 3, -1 + E),
   "07011-05": lambda: accumulated_position(3*u**2 + 2, 1, 4, 3),
   "07011-06": lambda: accumulated_position(6*cos(3*u), 0, -2, pi / 9),

   "07011-07": lambda: right_endpoint_where_undefined(2*(1 + y**2), 0, 1),
   "07011-08": lambda: right_endpoint_where_undefined(3*(1 + y**2), 0, -1),
   "07011-09": lambda: right_endpoint_where_undefined(Rational(1, 2)*(1 + y**2), 1, sqrt(3)),
   "07011-10": lambda: right_endpoint_where_undefined(2*(1 + y**2), 1, 0),
   "07011-11": lambda: right_endpoint_where_undefined(4*(1 + y**2), 0, -sqrt(3)),

   "07011-12": lambda: finite_endpoint_where_solution_vanishes(x / y, 5, 3),
   "07011-13": lambda: finite_endpoint_where_solution_vanishes(x / y, 13, -5),
   "07011-14": lambda: finite_endpoint_where_solution_vanishes(x / y, 10, 6),
   "07011-15": lambda: finite_endpoint_where_solution_vanishes(x / y, 3, 2),
   "07011-16": lambda: finite_endpoint_where_solution_vanishes(x / y, -2, 1),
   "07011-17": lambda: finite_endpoint_where_solution_vanishes(x / y, 4, -2),
   "07011-18": lambda: finite_endpoint_where_solution_vanishes(x / y, -17, 8),

   "07011-19": lambda: particular_solutions(2*x*(y - 3), 0, 1),
   "07011-20": lambda: particular_solutions(-4*x*(y + 1), 0, -3),
   "07011-21": lambda: particular_solutions(6*x*(y - 2), 0, 0),
   "07011-22": lambda: particular_solutions(2*(y - 5)*cos(x), 0, 2),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
