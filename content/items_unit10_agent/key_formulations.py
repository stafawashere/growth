"""Each agent-drafted unit 10 item's stem, written as the SymPy computation of the answer it asks for.

Read by tools/key_recheck.py. Every entry was written from the stem text alone, never from the
stored key, so a match is evidence that the key answers the stem. An edited stem needs its entry
rewritten the same way before the recheck can pass again. app/items/ingest.py loads only .json
records, so this file never reaches the bank.
"""
import sympy
from sympy import Rational, atan, cos, exp, factorial, ln, oo, sin, sqrt

from tools.key_recheck import (
   definite_integral,
   first_omitted_term,
   function_with_values,
   lagrange_error_bound,
   radius_of_convergence,
   series_value,
   taylor_from_derivatives,
   taylor_from_relation,
   taylor_polynomial,
   x,
   y,
)

n = sympy.Symbol("n", integer=True, nonnegative=True)
t, c, slope_symbol, shift = sympy.symbols("t c slope_symbol shift")

ITEM_PREFIX = "ITM-AGT-"

PARTIAL_SUM_LAST_INDEX = 40
DERIVATIVE_SERIES_ORDER = 30


def telescoping_value(leading, first):
   """The sum from first to infinity of leading(n) - leading(n + 1)."""
   return leading(first) - sympy.limit(leading(n), n, oo)


def geometric_closed_form(term, first):
   ratio = sympy.simplify(sympy.powsimp(term.subs(n, n + 1) / term, force=True))

   if ratio.has(n):
      raise ValueError(f"not geometric, ratio {ratio}")

   return sympy.simplify(term.subs(n, first) / (1 - ratio))


def constant_for_sum(term, first, target):
   return sympy.solve(sympy.Eq(c * series_value(term, n, first), target), c)


def improper_from_index(general_term, first):
   return definite_integral(general_term.subs(n, x), first, oo)


def alternating_bound_after(term, at, first, count):
   return first_omitted_term(term.subs(x, at), n, first + count - 1)


def least_terms_within(term, at, first, tolerance, search_limit=10000):
   """The least N whose alternating series error bound, the first omitted term, is at most tolerance."""
   at_point = term.subs(x, at)

   for count in range(1, search_limit):
      bound = first_omitted_term(at_point, n, first + count - 1)
      is_within = bool(bound <= tolerance)

      if is_within:
         return count

   raise ValueError(f"no partial sum within {tolerance}")


def max_abs_on_interval(expression, left, right):
   stationary = sympy.solve(sympy.diff(expression, x), x)
   critical = [point for point in stationary if point.is_real and bool(point >= left) and bool(point <= right)]
   candidates = [left, right] + critical

   return max(sympy.Abs(expression.subs(x, point)) for point in candidates)


def lagrange_bound_for(function, center, at, degree):
   next_derivative = sympy.diff(function, x, degree + 1)
   left, right = sorted([sympy.nsimplify(center), sympy.nsimplify(at)])
   bound = max_abs_on_interval(next_derivative, left, right)

   return lagrange_error_bound(bound, at, center, degree)


def taylor_from_second_order(rhs, center, value, slope, degree):
   """f'' = rhs(x, y, slope_symbol), with y standing for f and slope_symbol for f'."""
   at_center = {x: center, y: value, slope_symbol: slope}
   values = [sympy.nsimplify(value), sympy.nsimplify(slope)]
   current = rhs

   for _ in range(degree - 1):
      values.append(sympy.simplify(current.subs(at_center)))
      current = sympy.diff(current, x) + sympy.diff(current, y) * slope_symbol + sympy.diff(current, slope_symbol) * rhs

   return taylor_from_derivatives(values, center)


def taylor_value(values, center, degree, at):
   return taylor_from_derivatives(values[:degree + 1], center).subs(x, at)


def product_polynomial(factor, polynomial, degree):
   return taylor_polynomial(factor * polynomial, 0, degree)


def product_with_values(factor, center, values, degree):
   return taylor_polynomial(factor * function_with_values(center, values), center, degree)


def composed_polynomial(polynomial, inner, degree):
   return taylor_polynomial(polynomial.subs(x, inner), 0, degree)


def power_terms(expression, center, order):
   shifted = sympy.expand(expression.subs(x, center + shift))
   expansion = sympy.expand(sympy.series(shifted, shift, 0, order).removeO())

   return {power: expansion.coeff(shift, power) for power in range(order)}


def first_nonzero_terms(expression, count, center=0):
   order = count + 2

   while order <= 400:
      coefficients = power_terms(expression, center, order)
      nonzero = [(power, value) for power, value in sorted(coefficients.items()) if value != 0]
      has_enough = len(nonzero) >= count

      if has_enough:
         return sum(value * (x - center) ** power for power, value in nonzero[:count])

      order *= 2

   raise ValueError(f"fewer than {count} nonzero terms found")


def coefficient_of(expression, power, center=0):
   return power_terms(expression, center, power + 1)[power]


def partial_sum(term, first=0):
   return sum(term.subs(n, index) for index in range(first, PARTIAL_SUM_LAST_INDEX + 1))


def series_terms(term, count, first=0, center=0):
   return first_nonzero_terms(partial_sum(term, first), count, center)


def series_coefficient(term, power, first=0, center=0):
   return coefficient_of(partial_sum(term, first), power, center)


def derivative_series_terms(term, count, first=0, center=0):
   return first_nonzero_terms(sympy.diff(partial_sum(term, first), x), count, center)


def integral_series_terms(term, count, first=0):
   integrand = partial_sum(term, first).subs(x, t)

   return first_nonzero_terms(sympy.integrate(integrand, (t, 0, x)), count)


def derivative_series_radius(term, center=0):
   return radius_of_convergence(sympy.diff(term, x), n, center)


def antiderivative_series_terms(derivative_expression, value_at_zero, count):
   derivative_series = sympy.series(derivative_expression, x, 0, DERIVATIVE_SERIES_ORDER).removeO()
   integrated = value_at_zero + sympy.integrate(derivative_series.subs(x, t), (t, 0, x))

   return first_nonzero_terms(integrated, count)


BY_SUFFIX = {
   "10002-00": lambda: series_value(3 * Rational(2, 5)**n, n, 1),
   "10002-01": lambda: series_value(Rational(1, 3)**n, n, 2),
   "10002-02": lambda: series_value(2**(n + 1) / 3**n, n, 1),
   "10002-03": lambda: series_value((-1)**n * 4 / 3**n, n, 1),
   "10002-04": lambda: series_value(5 / 4**n, n, 2),
   "10002-05": lambda: series_value(3**n / 2**(2*n), n, 1),
   "10002-06": lambda: series_value(7 / 10**n, n, 1),
   "10002-07": lambda: series_value(2**(n - 1) / 3**(n + 1), n, 1),
   "10002-08": lambda: series_value((-2)**n / factorial(n), n, 0),
   "10002-09": lambda: series_value((-1)**n * 3**n / factorial(n), n, 0),
   "10002-10": lambda: series_value((-1)**n / (2**n * factorial(n)), n, 0),
   "10002-11": lambda: series_value((-1)**n * 4**n / (3**n * factorial(n)), n, 0),
   "10002-12": lambda: series_value((-1)**n * 5**n / factorial(n), n, 0),
   "10002-13": lambda: series_value(3**n / factorial(n), n, 1),
   "10002-14": lambda: series_value((-1)**n * 2**n / factorial(n), n, 1),
   "10002-15": lambda: series_value(2 / (n * (n + 2)), n, 1),
   "10002-16": lambda: series_value(1 / (n**2 - 1), n, 2),
   "10002-17": lambda: telescoping_value(lambda index: 1 / sqrt(index), 1),
   "10002-18": lambda: -telescoping_value(lambda index: atan(index), 1),
   "10002-19": lambda: series_value(4 / ((2*n - 1) * (2*n + 1)), n, 1),

   "10003-00": lambda: series_value(2**(2*n) / 5**n, n, 1),
   "10003-01": lambda: series_value(3**(2*n) / 10**n, n, 1),
   "10003-02": lambda: series_value(1 / 3**(2*n), n, 2),
   "10003-03": lambda: series_value(2**(2*n) / 3**(2*n), n, 1),
   "10003-04": lambda: series_value(5 * (-1)**n / 4**n, n, 1),
   "10003-05": lambda: series_value(2**n / 3**(n + 1), n, 2),
   "10003-06": lambda: series_value(3 * (-2)**n / 5**n, n, 1),
   "10003-07": lambda: geometric_closed_form((-1)**n * x**(2*n) / 4**n, 0),
   "10003-08": lambda: geometric_closed_form((-1)**n * (x - 2)**n / 3**n, 0),
   "10003-09": lambda: geometric_closed_form((-1)**n * 2**n * x**(2*n), 0),
   "10003-10": lambda: geometric_closed_form(3 * (-1)**n * (x + 1)**n / 2**n, 0),
   "10003-11": lambda: geometric_closed_form((-1)**n * x**(2*n + 1) / 9**n, 0),
   "10003-12": lambda: geometric_closed_form((x / 3)**n, 1),
   "10003-13": lambda: geometric_closed_form(2 * (x - 1)**n / 5**n, 1),
   "10003-14": lambda: geometric_closed_form(x**(2*n) / 4**n, 2),
   "10003-15": lambda: geometric_closed_form(3**n * (x + 2)**n, 1),
   "10003-16": lambda: geometric_closed_form((-1)**(n + 1) * x**n / 2**n, 1),
   "10003-17": lambda: constant_for_sum(3**(2*n) / 10**n, 1, 27),
   "10003-18": lambda: constant_for_sum(2**(2*n) / 9**n, 1, 8),
   "10003-19": lambda: constant_for_sum((-1)**n / 2**n, 1, 2),

   "10005-00": lambda: improper_from_index(1 / n**2, 2),
   "10005-01": lambda: improper_from_index(1 / n**3, 2),
   "10005-02": lambda: improper_from_index(exp(-n), 1),
   "10005-03": lambda: improper_from_index(1 / (n**2 + 1), 1),
   "10005-04": lambda: improper_from_index(1 / (n * (n + 1)), 1),
   "10005-05": lambda: improper_from_index(n * exp(-n**2), 1),
   "10005-06": lambda: improper_from_index(n / (n**2 + 1)**2, 1),
   "10005-07": lambda: improper_from_index(1 / (n * ln(n)**2), 3),
   "10005-08": lambda: improper_from_index(2**(-n), 1),
   "10005-09": lambda: improper_from_index(1 / (n + 2)**2, 1),
   "10005-10": lambda: improper_from_index(1 / (4*n**2 - 1), 1),
   "10005-11": lambda: improper_from_index(1 / (n**2 + 4), 2),
   "10005-12": lambda: improper_from_index(1 / n**2, 4),
   "10005-13": lambda: improper_from_index(exp(-2*n), 1),
   "10005-14": lambda: improper_from_index(1 / (n + 2)**3, 1),
   "10005-15": lambda: improper_from_index(n**2 * exp(-n**3), 1),
   "10005-16": lambda: improper_from_index(ln(n) / n**2, 2),
   "10005-17": lambda: improper_from_index(1 / (n * (n + 2)), 1),
   "10005-18": lambda: improper_from_index(1 / n**Rational(3, 2), 4),
   "10005-19": lambda: improper_from_index(1 / (n**2 + 3), 1),

   "10008-00": lambda: alternating_bound_after((-1)**(n + 1) * (x - 1)**n / (n * 3**n), 2, 1, 3),
   "10008-01": lambda: alternating_bound_after((-1)**(n + 1) * (x - 2)**n / (n * 4**n), 3, 1, 2),
   "10008-02": lambda: alternating_bound_after((-1)**(n + 1) * (x + 1)**n / (n * 5**n), 1, 1, 3),
   "10008-03": lambda: alternating_bound_after((-1)**(n + 1) * (x - 3)**n / (n**2 * 2**n), 4, 1, 4),
   "10008-04": lambda: alternating_bound_after((-1)**(n + 1) * (x - 1)**n / ((n + 1) * 4**n), 3, 1, 3),
   "10008-05": lambda: alternating_bound_after((-1)**(n + 1) * (x - 2)**n / (n * 3**n), 4, 1, 4),
   "10008-06": lambda: alternating_bound_after((-1)**(n + 1) * (x - 5)**n / (n**2 * 6**n), 7, 1, 2),
   "10008-07": lambda: alternating_bound_after((-1)**(n + 1) * (x - 1)**n / ((2*n - 1) * 2**n), 2, 1, 3),
   "10008-08": lambda: alternating_bound_after((-1)**(n + 1) * (x - 4)**n / (n * 10**n), 5, 1, 3),
   "10008-09": lambda: alternating_bound_after((-1)**(n + 1) * (x + 3)**n / ((n + 1) * 2**n), -2, 1, 4),
   "10008-10": lambda: alternating_bound_after((-1)**n * x**(2*n + 1) / factorial(2*n + 1), Rational(1, 2), 0, 2),
   "10008-11": lambda: alternating_bound_after((-1)**n * x**(2*n + 1) / factorial(2*n + 1), 1, 0, 3),
   "10008-12": lambda: alternating_bound_after((-1)**n * x**(2*n + 1) / factorial(2*n + 1), Rational(1, 3), 0, 2),
   "10008-13": lambda: alternating_bound_after((-1)**n * x**(2*n) / factorial(2*n), Rational(1, 2), 0, 3),
   "10008-14": lambda: alternating_bound_after((-1)**n * x**(2*n) / factorial(2*n), 1, 0, 2),
   "10008-15": lambda: alternating_bound_after((-1)**n * x**(2*n) / factorial(2*n), Rational(2, 5), 0, 3),
   "10008-16": lambda: least_terms_within((-1)**(n + 1) * (x - 1)**n / (n * 5**n), 3, 1, Rational(1, 100)),
   "10008-17": lambda: least_terms_within((-1)**(n + 1) * (x - 1)**n / (n * 4**n), 2, 1, Rational(1, 1000)),
   "10008-18": lambda: least_terms_within((-1)**(n + 1) * (x - 4)**n / (n**2 * 10**n), 6, 1, Rational(1, 1000)),
   "10008-19": lambda: least_terms_within((-1)**(n + 1) * (x - 1)**n / (n * 2**n), Rational(3, 2), 1, Rational(1, 1000)),

   "10009-00": lambda: lagrange_error_bound(12, Rational(5, 2), 2, 3),
   "10009-01": lambda: lagrange_error_bound(6, Rational(6, 5), 1, 2),
   "10009-02": lambda: lagrange_error_bound(10, Rational(1, 2), 0, 4),
   "10009-03": lambda: lagrange_error_bound(9, Rational(5, 2), 3, 2),
   "10009-04": lambda: lagrange_error_bound(48, Rational(-1, 2), -1, 3),
   "10009-05": lambda: lagrange_error_bound(4, Rational(4, 3), 1, 1),
   "10009-06": lambda: lagrange_error_bound(5, Rational(1, 10), 0, 3),
   "10009-07": lambda: lagrange_error_bound(2, Rational(17, 4), 4, 2),
   "10009-08": lambda: lagrange_error_bound(15, Rational(8, 5), 2, 3),
   "10009-09": lambda: lagrange_error_bound(12, Rational(-1, 2), 0, 2),
   "10009-10": lambda: lagrange_error_bound(100, Rational(26, 5), 5, 3),
   "10009-11": lambda: lagrange_error_bound(20, Rational(1, 2), 1, 4),
   "10009-12": lambda: lagrange_error_bound(6, Rational(-7, 4), -2, 1),
   "10009-13": lambda: lagrange_error_bound(10, Rational(3, 10), 0, 2),
   "10009-14": lambda: lagrange_bound_for(ln(x), 1, Rational(1, 2), 2),
   "10009-15": lambda: lagrange_bound_for(1 / x, 1, Rational(4, 5), 2),
   "10009-16": lambda: lagrange_bound_for(exp(2*x), 0, Rational(1, 2), 2),
   "10009-17": lambda: lagrange_bound_for(1 / x, 2, Rational(3, 2), 2),
   "10009-18": lambda: lagrange_bound_for(exp(-x), 0, Rational(-1, 2), 2),
   "10009-19": lambda: lagrange_bound_for(ln(x), 2, Rational(3, 2), 2),

   "10010-00": lambda: taylor_from_relation(x + y**2, 0, 2, 2),
   "10010-01": lambda: taylor_from_relation(x*y + 1, 0, 1, 2),
   "10010-02": lambda: taylor_from_relation(2*x - y**2, 0, -1, 3),
   "10010-03": lambda: taylor_from_relation(x*y, 1, 2, 2),
   "10010-04": lambda: taylor_from_relation(y**2 - 4*x, 0, 3, 2),
   "10010-05": lambda: taylor_from_relation(x**2 + y**3, 0, -1, 2),
   "10010-06": lambda: taylor_from_relation(x - y**2, 2, 2, 2),
   "10010-07": lambda: taylor_from_relation(x * y**2, 0, 2, 3),
   "10010-08": lambda: taylor_from_relation(1 + x*y, 0, -2, 3),
   "10010-09": lambda: taylor_from_relation(x * y**2, -1, 1, 2),
   "10010-10": lambda: taylor_from_relation(y**2 - x, 0, 1, 3),
   "10010-11": lambda: taylor_from_relation(x*y - 1, 1, 2, 2),
   "10010-12": lambda: taylor_from_second_order(x*slope_symbol + y**2, 0, 1, 2, 3),
   "10010-13": lambda: taylor_from_second_order(slope_symbol**2 + x*y, 0, 2, -1, 3),
   "10010-14": lambda: taylor_from_second_order(x*slope_symbol, 1, 1, 3, 3),
   "10010-15": lambda: taylor_from_second_order(2*y**2 - x, 0, -1, 2, 3),
   "10010-16": lambda: taylor_from_second_order(x*y + slope_symbol**2, 2, 1, 1, 3),
   "10010-17": lambda: taylor_from_second_order(x**2 + y**2, -1, 2, 3, 3),
   "10010-18": lambda: taylor_from_relation(1 - x*y, 0, 1, 3),
   "10010-19": lambda: taylor_from_relation(2*x + y**2, 0, 1, 3),

   "10011-00": lambda: taylor_from_derivatives([3, -2, 4], 0),
   "10011-01": lambda: taylor_from_derivatives([1, 2, -6, 12], 0),
   "10011-02": lambda: taylor_from_derivatives([5, -1, 3], 2),
   "10011-03": lambda: taylor_from_derivatives([0, 4, -2, 9], 1),
   "10011-04": lambda: taylor_from_derivatives([2, 0, 6], -1),
   "10011-05": lambda: taylor_from_derivatives([-1, 3, 2, -12], 0),
   "10011-06": lambda: taylor_from_derivatives([4, -2, -1], 3),
   "10011-07": lambda: taylor_value([2, -1, 6, -18, 24], 0, 3, Rational(1, 2)),
   "10011-08": lambda: taylor_value([3, 2, -4, 12], 1, 2, Rational(3, 2)),
   "10011-09": lambda: taylor_value([-1, 4, 6, -6, 10], 2, 3, Rational(3, 2)),
   "10011-10": lambda: taylor_value([5, -3, 8, 24, -48], 0, 3, Rational(1, 2)),
   "10011-11": lambda: taylor_from_derivatives([1, 3, -2], -2),
   "10011-12": lambda: taylor_value([2, Rational(1, 4), Rational(-1, 32), Rational(3, 256)], 4, 2, 5),
   "10011-13": lambda: taylor_value([0, 1, -1, 2, -6], 1, 3, Rational(3, 2)),
   "10011-14": lambda: taylor_value([1, -1, 1, -1, 1], 0, 3, Rational(1, 2)),
   "10011-15": lambda: taylor_from_derivatives([2, 0, -4, 6], 3),
   "10011-16": lambda: taylor_from_derivatives([-3, 5, 2, 0], -1),
   "10011-17": lambda: taylor_from_derivatives([4, 0, -6, 0], 0),
   "10011-18": lambda: taylor_value([1, -3, 8, -12], 2, 2, 1),
   "10011-19": lambda: taylor_value([-2, 1, 3, 4, -5], 5, 3, 6),

   "10012-00": lambda: product_polynomial(exp(x), 2 - x + 3*x**2, 2),
   "10012-01": lambda: product_polynomial(sin(x), 1 + 2*x + x**2 - x**3, 3),
   "10012-02": lambda: product_polynomial(cos(x), 3 - x + 2*x**2, 2),
   "10012-03": lambda: product_polynomial(1 / (1 - 2*x), 1 - 3*x + x**2 + 2*x**3, 3),
   "10012-04": lambda: product_polynomial(exp(2*x), 1 - x + 4*x**2, 2),
   "10012-05": lambda: product_polynomial(sin(2*x), 3 + x - 2*x**2 + 5*x**3, 3),
   "10012-06": lambda: product_polynomial(exp(-x), 2 + 4*x + x**2 - x**3, 3),
   "10012-07": lambda: product_polynomial(cos(2*x), 1 + x + x**2 + x**3, 3),
   "10012-08": lambda: product_polynomial(1 / (1 + x), 2 + x - x**2, 2),
   "10012-09": lambda: product_polynomial(exp(x), -1 + x + 2*x**2 + x**3, 3),
   "10012-10": lambda: product_polynomial(sin(x), 4 - 2*x + x**2 + 5*x**3, 3),
   "10012-11": lambda: product_with_values(x, 1, [2, -1, 3, 4], 2),
   "10012-12": lambda: product_with_values(x**2, 1, [1, 2, -2, 6], 2),
   "10012-13": lambda: product_with_values(x, 2, [-1, 3, 1, -2], 2),
   "10012-14": lambda: product_with_values(x + 1, 1, [3, 1, -4, 2], 2),
   "10012-15": lambda: product_with_values(x**2, -1, [2, 1, 4, 0], 2),
   "10012-16": lambda: composed_polynomial(1 - 2*x + 3*x**2 - x**3 + 2*x**4, 2*x, 3),
   "10012-17": lambda: composed_polynomial(2 + x - x**2 + 4*x**3, -3*x, 2),
   "10012-18": lambda: composed_polynomial(3 - x + 2*x**2 + x**3 - 4*x**4, x / 2, 3),
   "10012-19": lambda: composed_polynomial(-2 + 4*x + x**2 - 3*x**3, 3*x, 2),

   "10014-00": lambda: radius_of_convergence(2**(2*n) * (x - 1)**(2*n) / (n + 1), n, 1),
   "10014-01": lambda: radius_of_convergence((x + 2)**n / (3**(2*n) * n), n, -2),
   "10014-02": lambda: radius_of_convergence(2**n * (x - 3)**(2*n) / 5**(n + 1), n, 3),
   "10014-03": lambda: radius_of_convergence(2**(2*n) * x**(2*n + 1) / (3**(n + 1) * n), n, 0),
   "10014-04": lambda: radius_of_convergence((-1)**n * 3**(n + 1) * (x - 4)**(2*n) / n, n, 4),
   "10014-05": lambda: radius_of_convergence((x + 1)**(2*n) / (9**n * (2*n + 1)), n, -1),
   "10014-06": lambda: radius_of_convergence(5**(2*n) * (x - 2)**n / n**3, n, 2),
   "10014-07": lambda: radius_of_convergence((x + 3)**(3*n) / 8**n, n, -3),
   "10014-08": lambda: radius_of_convergence(4**n * (x - 5)**(2*n + 1) / 9**n, n, 5),
   "10014-09": lambda: radius_of_convergence(3**(2*n + 1) * x**(2*n) / 2**n, n, 0),
   "10014-10": lambda: radius_of_convergence((-1)**n * n * (x + 4)**(2*n) / 2**(3*n), n, -4),
   "10014-11": lambda: radius_of_convergence(7**(n + 2) * (x - 6)**(2*n) / (n + 1), n, 6),
   "10014-12": lambda: radius_of_convergence(2**n * x**(3*n + 1) / 27**(n + 1), n, 0),
   "10014-13": lambda: radius_of_convergence(3**n * (x + 5)**(2*n) / 4**(2*n), n, -5),
   "10014-14": lambda: radius_of_convergence((x - 2)**(2*n) / (6**n * n**2), n, 2),
   "10014-15": lambda: radius_of_convergence(10**n * (x + 1)**n / (3**(2*n) * n), n, -1),
   "10014-16": lambda: radius_of_convergence((-1)**n * 2**(3*n) * (x - 3)**n / 5**(n + 1), n, 3),
   "10014-17": lambda: radius_of_convergence(4**n * x**(2*n + 1) / 5**(2*n), n, 0),
   "10014-18": lambda: radius_of_convergence(2**n * (x - 1)**n / (3**n * n**2), n, 1),
   "10014-19": lambda: radius_of_convergence((-1)**n * (x + 2)**(2*n + 1) / 2**(4*n), n, -2),

   "10016-00": lambda: series_terms((-1)**n / (n + 1) * x**(2*n), 3),
   "10016-01": lambda: series_terms(x**(2*n + 1) / factorial(n), 3),
   "10016-02": lambda: series_terms((-1)**n * (n + 1) / 3**n * x**n, 4),
   "10016-03": lambda: series_terms((-1)**n / (2*n + 1) * x**(2*n + 1), 3),
   "10016-04": lambda: series_terms(2**n / factorial(n) * x**(n + 1), 3),
   "10016-05": lambda: series_terms((-1)**n / 2**n * x**(3*n), 3),
   "10016-06": lambda: series_terms((-1)**n * 3**n / factorial(2*n) * x**(2*n), 3),
   "10016-07": lambda: series_terms((n + 1) / 2**n * x**(2*n), 3),
   "10016-08": lambda: series_terms((-1)**(n + 1) / n * x**n, 4, first=1),
   "10016-09": lambda: series_terms((-1)**n / (n + 2) * (x - 1)**n, 3, center=1),
   "10016-10": lambda: series_coefficient((-1)**n * (n + 1) / 3**n * x**(2*n), 6),
   "10016-11": lambda: series_coefficient((-1)**n / (n + 1) * x**(3*n), 9),
   "10016-12": lambda: series_coefficient((n + 1) / 2**n * x**(2*n + 1), 7),
   "10016-13": lambda: series_coefficient((-1)**n * 2**n / (n + 1) * x**(n + 2), 5),
   "10016-14": lambda: series_coefficient((-1)**n / factorial(n) * x**(2*n), 6),
   "10016-15": lambda: series_coefficient((-1)**n * (n + 1) / 4**n * (x - 2)**(2*n), 6, center=2),
   "10016-16": lambda: derivative_series_terms(x**n / 3**n, 3),
   "10016-17": lambda: derivative_series_terms((-1)**n / (n + 1) * x**(2*n), 3),
   "10016-18": lambda: integral_series_terms((-1)**n / 2**n * x**(2*n), 3),
   "10016-19": lambda: derivative_series_terms(2**n / factorial(n) * x**(n + 1), 3),

   "10017-00": lambda: first_nonzero_terms(3 * exp(-2*x), 3),
   "10017-01": lambda: first_nonzero_terms(x * sin(2*x), 3),
   "10017-02": lambda: first_nonzero_terms(2 * cos(3*x), 3),
   "10017-03": lambda: first_nonzero_terms(5*x**2 / (1 + x**2), 4),
   "10017-04": lambda: first_nonzero_terms(4 / (1 - 3*x), 3),
   "10017-05": lambda: first_nonzero_terms(2*x * exp(-x**2), 3),
   "10017-06": lambda: first_nonzero_terms(3 * sin(x**2), 3),
   "10017-07": lambda: first_nonzero_terms(x**3 * cos(2*x**2), 3),
   "10017-08": lambda: first_nonzero_terms(6*x / (1 + 2*x), 3),
   "10017-09": lambda: coefficient_of(x**2 * exp(3*x), 5),
   "10017-10": lambda: coefficient_of(4 * cos(x / 2), 4),
   "10017-11": lambda: coefficient_of(3*x * sin(2*x), 4),
   "10017-12": lambda: coefficient_of(5*x**3 / (1 - 2*x**2), 9),
   "10017-13": lambda: coefficient_of(2 * exp(-x**3), 6),
   "10017-14": lambda: first_nonzero_terms(8 * exp(x / 2), 4),
   "10017-15": lambda: first_nonzero_terms(x**2 * cos(3*x), 3),
   "10017-16": lambda: first_nonzero_terms(-2*x * sin(x**2), 3),
   "10017-17": lambda: first_nonzero_terms(3 / (1 + x), 4),
   "10017-18": lambda: coefficient_of(2*x / (1 + 4*x**2), 7),
   "10017-19": lambda: coefficient_of(5 * exp(2*x), 4),

   "10018-00": lambda: derivative_series_terms(x**n / 2**n, 3),
   "10018-01": lambda: derivative_series_terms((-1)**n / (2*n + 1) * x**(2*n), 3),
   "10018-02": lambda: derivative_series_terms(x**n / factorial(n), 4),
   "10018-03": lambda: derivative_series_terms((-1)**n / factorial(2*n) * x**(2*n), 3),
   "10018-04": lambda: derivative_series_terms((n + 1) * x**n, 3),
   "10018-05": lambda: derivative_series_terms((-1)**n / 3**n * (x - 2)**n, 3, center=2),
   "10018-06": lambda: derivative_series_terms(2**n / factorial(n) * x**n, 3),
   "10018-07": lambda: derivative_series_terms((-1)**n / 2**n * x**(3*n), 3),
   "10018-08": lambda: derivative_series_terms((x - 1)**n / (n + 1), 3, center=1),
   "10018-09": lambda: derivative_series_terms((-1)**n / (n + 1)**2 * x**n, 3),
   "10018-10": lambda: derivative_series_terms(x**(2*n) / factorial(n), 3),
   "10018-11": lambda: derivative_series_terms((-1)**n * (n + 1) / 2**n * (x + 1)**n, 3, center=-1),
   "10018-12": lambda: derivative_series_terms(3**n / factorial(2*n) * x**(2*n), 3),
   "10018-13": lambda: derivative_series_terms(x**n / (factorial(n) * 2**n), 3),
   "10018-14": lambda: derivative_series_radius(x**(2*n) / 9**n),
   "10018-15": lambda: derivative_series_radius(n / 4**n * x**(2*n)),
   "10018-16": lambda: derivative_series_radius((-1)**n / (16**n * (2*n + 1)) * x**(2*n + 1)),
   "10018-17": lambda: derivative_series_radius(x**(3*n) / 8**n),
   "10018-18": lambda: derivative_series_radius((x - 1)**(2*n) / (25**n * (n + 1)), 1),
   "10018-19": lambda: derivative_series_radius(n**2 / 27**n * x**(3*n)),

   "10019-00": lambda: antiderivative_series_terms(x / (1 + x**2), 2, 4),
   "10019-01": lambda: antiderivative_series_terms(x * exp(-x**2), 0, 3),
   "10019-02": lambda: antiderivative_series_terms(sin(x), 3, 3),
   "10019-03": lambda: antiderivative_series_terms(exp(-x**2), 0, 3),
   "10019-04": lambda: antiderivative_series_terms(x**2 / (1 + x**3), 1, 3),
   "10019-05": lambda: antiderivative_series_terms(x * cos(x), 1, 3),
   "10019-06": lambda: antiderivative_series_terms(2*x / (1 - x**2), -1, 4),
   "10019-07": lambda: antiderivative_series_terms(x / (1 - x), 0, 3),
   "10019-08": lambda: antiderivative_series_terms(x * sin(x), 2, 3),
   "10019-09": lambda: antiderivative_series_terms(3*x**2 * exp(x**3), 1, 3),
   "10019-10": lambda: antiderivative_series_terms(x / (1 + 4*x**2), 0, 3),
   "10019-11": lambda: antiderivative_series_terms(sin(2*x), 1, 4),
   "10019-12": lambda: antiderivative_series_terms(x**2 * cos(x), -2, 4),
   "10019-13": lambda: antiderivative_series_terms(4*x**3 / (1 + x**4), 0, 3),
   "10019-14": lambda: antiderivative_series_terms(exp(x**2), 3, 4),
   "10019-15": lambda: antiderivative_series_terms(x**3 / (1 - x**2), 5, 3),
   "10019-16": lambda: antiderivative_series_terms(x * exp(x), 1, 3),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
