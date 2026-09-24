"""Blind answers for the generated unit 10 items in stems_H.json, written from the stems alone.

Written by claude-opus-5-5, a blind solver working on the operator's delegation of 2026-09-24,
without sight of any key, worked solution, template or candidate record. Numeric and expression
items return SymPy values computed from the stem's numbers. Statement items work the mathematics
(limits, ratios, endpoint behaviour, integrals) and assemble the one correct choice's text from
the computed values, so a wrong computation yields text that matches no choice.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

import sympy
from sympy import Rational, atan, cos, exp, factorial, ln, oo, sin, sqrt

from tools.key_recheck import (
   first_omitted_term,
   lagrange_error_bound,
   radius_of_convergence,
   series_value,
   taylor_from_derivatives,
   taylor_from_relation,
   taylor_polynomial,
   x,
   y,
)

n = sympy.Symbol("n", integer=True, positive=True)
t, shift = sympy.symbols("t shift")

DERIVATIVE_SERIES_ORDER = 30
SERIES_CHECK_ORDER = 14


def tex(value):
   return sympy.latex(sympy.nsimplify(value))


def power_of_n(power):
   if power == 1:
      return "n"

   if power == Rational(1, 2):
      return "\\sqrt{n}"

   return f"n^{{{tex(power)}}}"


def interval_text(left, right, left_closed, right_closed):
   left_relation = "\\le" if left_closed else "<"
   right_relation = "\\le" if right_closed else "<"

   return f"{tex(left)} {left_relation} x {right_relation} {tex(right)}"


def endpoint_converges(endpoint_sign, power):
   """Whether the sum of endpoint_sign**n / n**power converges."""
   is_absolutely_convergent = power > 1
   is_alternating_and_shrinking = endpoint_sign == -1 and power > 0

   return is_absolutely_convergent or is_alternating_and_shrinking


def is_decreasing_from(expression, variable, start):
   if sympy.is_decreasing(expression, sympy.Interval(start, oo), variable):
      return True

   offset = sympy.Symbol("offset", nonnegative=True)
   slope = sympy.diff(expression, variable).subs(variable, start + offset)

   return bool(sympy.simplify(slope).is_negative)


# BC-QA-10001: name a test the series meets and its verdict


def named_test_verdict(term, first):
   magnitude = sympy.Abs(term)
   is_alternating = term.has(sympy.Pow(-1, n))

   if not is_alternating:
      term_limit = sympy.limit(term, n, oo)
      has_nonzero_limit = term_limit != 0

      if has_nonzero_limit:
         return f"The series diverges by the nth term test, because \\( \\lim_{{n\\to\\infty}} a_n = {tex(term_limit)} \\ne 0 \\)."

   if is_alternating:
      size = sympy.simplify(term / sympy.Pow(-1, n))
      size_shrinks = is_decreasing_from(size.subs(n, x), x, first) and sympy.limit(size, n, oo) == 0

      if not size_shrinks:
         raise ValueError("alternating series test conditions fail")

      return "The series converges by the alternating series test, because \\( |a_n| \\) decreases to 0."

   log_slope = sympy.simplify(n * sympy.diff(term, n) / term)
   is_p_series = not log_slope.has(n)

   if is_p_series:
      power = -log_slope

      if power > 1:
         return f"The series converges by the p-series test, because \\( p = {tex(power)} > 1 \\)."

      return f"The series diverges by the p-series test, because \\( p = {tex(power)} \\le 1 \\)."

   consecutive_ratio = sympy.simplify(term.subs(n, n + 1) / term)
   is_geometric = not consecutive_ratio.has(n)

   if is_geometric:
      if sympy.Abs(consecutive_ratio) < 1:
         return f"The series converges by the geometric series test, because \\( r = {tex(consecutive_ratio)} < 1 \\)."

      return f"The series diverges by the geometric series test, because \\( r = {tex(consecutive_ratio)} > 1 \\)."

   ratio_limit = sympy.limit(sympy.Abs(consecutive_ratio), n, oo)

   if ratio_limit < 1:
      return f"The series converges by the ratio test, because \\( \\lim_{{n\\to\\infty}} \\left|\\frac{{a_{{n+1}}}}{{a_n}}\\right| = {tex(ratio_limit)} < 1 \\)."

   raise ValueError(f"no conclusive test for {magnitude}")


# BC-QA-10004: direct comparison or alternating series test with conditions verified


def alternating_series_verdict(size, first):
   decreases = is_decreasing_from(size.subs(n, x), x, first)
   tends_to_zero = sympy.limit(size, n, oo) == 0
   conditions_hold = decreases and tends_to_zero

   if not conditions_hold:
      raise ValueError("alternating series test conditions fail")

   return "The series converges by the alternating series test, because \\( |a_n| \\) decreases to 0."


def bounded_above_convergent(coefficient, power, added_constant, first):
   """a_n = coefficient / (n**power + added_constant) lies strictly between 0 and coefficient / n**power."""
   term = coefficient / (n**power + added_constant)
   comparison = coefficient / n**power
   gap = sympy.simplify(comparison - term)
   bound_holds = coefficient > 0 and added_constant > 0 and bool(gap.subs(n, first) > 0)

   if not bound_holds or power <= 1:
      raise ValueError("direct comparison for convergence does not apply")

   bound = f"\\frac{{{tex(coefficient)}}}{{{power_of_n(power)}}}"

   return f"The series converges by the direct comparison test, because \\( 0 < a_n < {bound} \\text{{ and }} p = {tex(power)} > 1 \\)."


def bounded_below_divergent(term, power, first):
   excess = sympy.simplify(term - 1 / n**power)
   is_nonnegative_everywhere = bool(excess.is_nonnegative)

   if not is_nonnegative_everywhere or power > 1:
      raise ValueError("direct comparison for divergence does not apply")

   bound = f"\\frac{{1}}{{{power_of_n(power)}}}"

   return f"The series diverges by the direct comparison test, because \\( a_n \\ge {bound} \\text{{ and }} p = {tex(power)} \\le 1 \\)."


# BC-QA-10006: limit comparison with 1/n**p


def limit_comparison_verdict(term, power, absolute):
   size = sympy.simplify(term / sympy.Pow(-1, n)) if absolute else term
   ratio_limit = sympy.limit(size * n**power, n, oo)
   is_positive_finite = ratio_limit.is_positive and ratio_limit.is_finite

   if not is_positive_finite:
      raise ValueError("limit comparison inconclusive")

   numerator = "|a_n|" if absolute else "a_n"
   comparison_sum = "\\frac{1}{n}" if power == 1 else f"\\frac{{1}}{{n^{{{power}}}}}"
   comparison_behaviour = "converges" if power > 1 else "diverges"

   if absolute:
      verdict = "converges absolutely"
   else:
      verdict = comparison_behaviour

   limit_part = f"\\lim_{{n\\to\\infty}} \\frac{{{numerator}}}{{1/n^{{{power}}}}} = {tex(ratio_limit)}"

   return f"\\( \\sum a_n \\) {verdict}, because \\( {limit_part} \\) is positive and finite and \\( \\sum {comparison_sum} \\) {comparison_behaviour}."


# BC-QA-10013: interval of convergence of c (sign)^n (x - center)^n / (base^n n^power)


def interval_of_convergence(sign, center, base, power):
   right_endpoint_sign = sign
   left_endpoint_sign = -sign
   left = center - base
   right = center + base
   left_closed = endpoint_converges(left_endpoint_sign, power)
   right_closed = endpoint_converges(right_endpoint_sign, power)

   return f"The interval of convergence is \\( {interval_text(left, right, left_closed, right_closed)} \\)."


# BC-QA-10014: radius of convergence


def radius_statement(term, center):
   radii = radius_of_convergence(term, n, center)

   if len(radii) != 1:
      raise ValueError(f"radius not unique: {radii}")

   return f"\\( R = {tex(radii[0])} \\)"


# BC-QA-10015: behaviour at one endpoint of sign^n (x - center)^n / (base^n (n**power + added))


def size_text(power, added_constant):
   if added_constant == 0:
      return f"\\frac{{1}}{{{power_of_n(power)}}}"

   return f"\\frac{{1}}{{{power_of_n(power)} + {tex(added_constant)}}}"


def endpoint_verdict(sign, center, base, power, added_constant, side):
   at = center + base if side == "right" else center - base
   endpoint_sign = sign if side == "right" else -sign
   prefix = f"At \\( x = {tex(at)} \\) the series"
   size = 1 / (n**power + added_constant)
   is_alternating = endpoint_sign == -1

   if is_alternating:
      alternating_series_verdict(size, 1)

      return f"{prefix} converges by the alternating series test, because the sizes \\( {size_text(power, added_constant)} \\) decrease to 0."

   is_plain_p_series = added_constant == 0
   converges = power > 1

   if is_plain_p_series and converges:
      return f"{prefix} converges by the p-series test, because \\( p = {tex(power)} > 1 \\)."

   if is_plain_p_series:
      return f"{prefix} diverges by the p-series test, because \\( p = {tex(power)} \\le 1 \\)."

   comparison = f"\\( \\sum \\frac{{1}}{{{power_of_n(power)}}} \\)"

   if converges:
      return f"{prefix} converges by direct comparison with {comparison}, because \\( p = {tex(power)} > 1 \\)."

   ratio_limit = sympy.limit(size * n**power, n, oo)

   if ratio_limit != 1:
      raise ValueError("unexpected limit comparison value")

   return f"{prefix} diverges by limit comparison with {comparison}, because \\( p = {tex(power)} \\le 1 \\)."


# BC-QA-10020: does the Taylor series converge to f at a given point


def taylor_convergence_at(kind, center, radius, at):
   """kind "log": sum (-1)^(n+1) ((x - center)/radius)^n / n, whose value is c ln(1 + (x - center)/radius).
   kind "geometric": sum ((x - center)/radius)^n."""
   left = center - radius
   right = center + radius
   is_log = kind == "log"
   left_closed = False
   right_closed = is_log
   interval = interval_text(left, right, left_closed, right_closed)
   is_interior = left < at < right
   is_endpoint = at in (left, right)

   if is_interior:
      raise ValueError("interior point, no endpoint question")

   if not is_endpoint:
      return f"No, because \\( x = {tex(at)} \\) lies outside the open interval \\( {interval_text(left, right, False, False)} \\)."

   included = (at == right and right_closed) or (at == left and left_closed)

   if included:
      return f"Yes, because \\( x = {tex(at)} \\) is an endpoint that the interval of convergence \\( {interval} \\) includes."

   return f"No, because \\( x = {tex(at)} \\) is an endpoint that the interval of convergence \\( {interval} \\) excludes."


# BC-QA-10005: integral test


def integral_test_verdict(function, first):
   is_positive = bool(function.subs(x, first) > 0) and sympy.limit(function, x, oo) >= 0
   decreases = is_decreasing_from(function, x, first)
   conditions_hold = is_positive and decreases

   if not conditions_hold:
      raise ValueError("integral test conditions fail")

   improper_value = sympy.integrate(function, (x, first, oo))
   verdict = "diverges" if improper_value == oo else "converges"
   conditions = f"f is positive, decreasing and continuous on \\( [{first}, \\infty) \\)"
   limit_part = f"\\lim_{{b\\to\\infty}} \\int_{{{first}}}^{{b}} f(x)\\,dx = {sympy.latex(improper_value)}"

   return f"\\( \\sum a_n \\) {verdict}, because {conditions} and \\( {limit_part} \\)."


# BC-QA-10016: first terms and general term of a Maclaurin series, checked before the text is returned


def maclaurin_statement(function, general_term, text):
   expansion = sympy.series(function, x, 0, SERIES_CHECK_ORDER).removeO()
   index = sympy.Symbol("k", integer=True, nonnegative=True)
   from_general = sum(general_term.subs(n, index_value) for index_value in range(SERIES_CHECK_ORDER))
   truncated = sympy.series(from_general, x, 0, SERIES_CHECK_ORDER).removeO()
   agrees = sympy.expand(expansion - truncated) == 0

   if not agrees:
      raise ValueError("general term does not reproduce the series")

   return text


# BC-QA-10018: term-by-term derivative and its interval


def derivative_series_statement(coefficient, sign, center, base, center_text):
   original = coefficient * sign**n * (x - center)**n / (n**2 * base**n)
   claimed = coefficient * sign**n * (x - center)**(n - 1) / (n * base**n)
   matches = sympy.simplify(sympy.diff(original, x) - claimed) == 0

   if not matches:
      raise ValueError("derivative term mismatch")

   interval = interval_text(
      center - base,
      center + base,
      endpoint_converges(-sign, 1),
      endpoint_converges(sign, 1),
   )
   sign_text = " (-1)^{n}" if sign == -1 else ""
   term_text = f"\\frac{{{coefficient}{sign_text} \\left({center_text}\\right)^{{n-1}}}}{{n \\cdot {base}^{{n}}}}"

   return f"\\( f^{{\\prime}}(x) = \\sum_{{n=1}}^{{\\infty}} {term_text} \\), converging for \\( {interval} \\)."


# Numeric and expression archetypes


def geometric_closed_form(term, first):
   ratio = sympy.simplify(sympy.powsimp(term.subs(n, n + 1) / term, force=True))

   if ratio.has(n):
      raise ValueError(f"not geometric, ratio {ratio}")

   return sympy.simplify(term.subs(n, first) / (1 - ratio))


def alternating_error_bound(term, at, last_index):
   return first_omitted_term(term.subs(x, at), n, last_index)


def lagrange_bound(derivative_bound, center, at, degree):
   return lagrange_error_bound(derivative_bound, at, center, degree)


def taylor_from_table(values, center, degree):
   return taylor_from_derivatives(values[:degree + 1], center)


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
         return sum(value * (x - center)**power for power, value in nonzero[:count])

      order *= 2

   raise ValueError(f"fewer than {count} nonzero terms found")


def antiderivative_series_terms(derivative_expression, value_at_zero, count):
   derivative_series = sympy.series(derivative_expression, x, 0, DERIVATIVE_SERIES_ORDER).removeO()
   integrated = value_at_zero + sympy.integrate(derivative_series.subs(x, t), (t, 0, x))

   return first_nonzero_terms(integrated, count)


ALT = sympy.Pow(-1, n)
COSINE_TERM = ALT * x**(2 * n) / factorial(2 * n)
ARCTAN_TERM = ALT * x**(2 * n + 1) / (2 * n + 1)
EXP_NEGATIVE_TERM = ALT * x**n / factorial(n)

BY_SUFFIX = {
   "10001-00": lambda: named_test_verdict(n / 4**n, 1),
   "10001-01": lambda: named_test_verdict(2 * ALT / n**Rational(2, 3), 2),
   "10001-02": lambda: named_test_verdict((n - 4) / (3 * n + 4), 2),
   "10001-03": lambda: named_test_verdict(4 / n**Rational(2, 3), 2),
   "10001-04": lambda: named_test_verdict(4 / sqrt(n), 2),
   "10001-05": lambda: named_test_verdict((2 * n + 5) / (2 * n + 6), 1),
   "10001-06": lambda: named_test_verdict(2**n / factorial(n), 2),
   "10001-07": lambda: named_test_verdict(n**3 / 3**n, 2),
   "10001-08": lambda: named_test_verdict(5 * 3**n / 5**n, 2),
   "10001-09": lambda: named_test_verdict(4 * ALT / n, 1),
   "10001-10": lambda: named_test_verdict(n**3 / 3**n, 1),
   "10001-11": lambda: named_test_verdict(7 / n**Rational(2, 3), 1),
   "10001-12": lambda: named_test_verdict(3 / n**Rational(1, 3), 2),
   "10001-13": lambda: named_test_verdict(9 / n, 2),
   "10001-14": lambda: named_test_verdict(4 / n**Rational(2, 3), 1),
   "10001-15": lambda: named_test_verdict(5 * 3**n / 7**n, 1),
   "10001-16": lambda: named_test_verdict(6 * 3**n / 4**n, 2),
   "10001-17": lambda: named_test_verdict(5 / n**Rational(1, 3), 2),
   "10001-18": lambda: named_test_verdict(8 * ALT / n**Rational(2, 3), 1),
   "10001-19": lambda: named_test_verdict(7 * 2**n / 7**n, 2),
   "10001-20": lambda: named_test_verdict(4 / n**2, 1),
   "10001-21": lambda: named_test_verdict(6 / n**Rational(3, 2), 1),

   "10002-00": lambda: series_value(1 / ((n + 4) * (n + 5)), n, 2),
   "10002-01": lambda: series_value(Rational(-2, 5)**n, n, 3),
   "10002-02": lambda: series_value(5 / ((n + 3) * (n + 4)), n, 2),
   "10002-03": lambda: series_value(6 * Rational(2, 5)**n, n, 2),
   "10002-04": lambda: series_value(4 / ((n + 3) * (n + 4)), n, 3),

   "10003-00": lambda: geometric_closed_form(5 * ALT * x**(2 * n) / 7**n, 2),
   "10003-01": lambda: geometric_closed_form(7 * ALT * (x + 2)**n / 2**n, 2),
   "10003-02": lambda: geometric_closed_form(2 * (x + 2)**(2 * n) / 4**n, 1),
   "10003-03": lambda: geometric_closed_form(5 * (x - 2)**(2 * n) / 3**n, 1),
   "10003-04": lambda: geometric_closed_form(6 * (x - 1)**n / 4**n, 1),

   "10004-00": lambda: bounded_above_convergent(2, Rational(5, 2), 4, 2),
   "10004-01": lambda: alternating_series_verdict(1 / (sqrt(n) + 2), 1),
   "10004-02": lambda: bounded_above_convergent(2, Rational(5, 2), 5, 2),
   "10004-03": lambda: alternating_series_verdict(6 / (n + 7), 1),
   "10004-04": lambda: bounded_above_convergent(3, Rational(3, 2), 6, 1),
   "10004-05": lambda: bounded_above_convergent(7, Rational(5, 2), 3, 1),
   "10004-06": lambda: bounded_above_convergent(4, 2, 3, 1),
   "10004-07": lambda: bounded_below_divergent((n**Rational(2, 3) + 2) / n**Rational(4, 3), Rational(2, 3), 2),
   "10004-08": lambda: alternating_series_verdict(1 / (n**Rational(2, 3) + 8), 2),
   "10004-09": lambda: bounded_below_divergent((sqrt(n) + 2) / n, Rational(1, 2), 1),
   "10004-10": lambda: bounded_above_convergent(9, 4, 4, 1),
   "10004-11": lambda: bounded_above_convergent(8, 3, 2, 1),
   "10004-12": lambda: bounded_above_convergent(8, Rational(5, 2), 6, 1),
   "10004-13": lambda: alternating_series_verdict(7 / (sqrt(n) + 1), 2),
   "10004-14": lambda: bounded_above_convergent(9, 3, 9, 2),
   "10004-15": lambda: bounded_above_convergent(5, 4, 5, 1),
   "10004-16": lambda: alternating_series_verdict(5 / (sqrt(n) + 5), 1),
   "10004-17": lambda: bounded_above_convergent(5, 2, 6, 2),
   "10004-18": lambda: bounded_below_divergent((n + 3) / n**2, 1, 2),
   "10004-19": lambda: bounded_below_divergent((sqrt(n) + 2) / n, Rational(1, 2), 1),
   "10004-20": lambda: bounded_above_convergent(4, Rational(3, 2), 5, 2),
   "10004-21": lambda: bounded_below_divergent((n**Rational(2, 3) + 1) / n**Rational(4, 3), Rational(2, 3), 2),

   "10005-00": lambda: integral_test_verdict(10 * x / (x**2 + 10)**2, 2),
   "10005-01": lambda: integral_test_verdict(x * exp(-15 * x**2), 5),
   "10005-02": lambda: integral_test_verdict(15 * x / (x**2 + 6)**2, 5),
   "10005-03": lambda: integral_test_verdict(4 * x**2 / (x**3 + 3), 2),
   "10005-04": lambda: integral_test_verdict(6 * x**2 / (x**3 + 4), 5),

   "10006-00": lambda: limit_comparison_verdict(ALT * (5 * n**2 + 6) / (3 * n**5 + 3), 3, True),
   "10006-01": lambda: limit_comparison_verdict((4 * n + 1) / (n**4 + 2), 3, False),
   "10006-02": lambda: limit_comparison_verdict((2 * n + 5) / (4 * n**2 + 2), 1, False),
   "10006-03": lambda: limit_comparison_verdict((2 * n**2 + 2) / (6 * n**5 + 9), 3, False),
   "10006-04": lambda: limit_comparison_verdict(ALT * (2 * n**2 + 6) / (6 * n**4 + 7), 2, True),
   "10006-05": lambda: limit_comparison_verdict((n**2 + 6) / (4 * n**3 + 1), 1, False),
   "10006-06": lambda: limit_comparison_verdict((6 * n**2 + 5) / (4 * n**4 + 2), 2, False),
   "10006-07": lambda: limit_comparison_verdict((3 * n**2 + 2) / (n**3 + 1), 1, False),
   "10006-08": lambda: limit_comparison_verdict(ALT * (n**2 + 3) / (4 * n**5 + 2), 3, True),
   "10006-09": lambda: limit_comparison_verdict(ALT * (5 * n + 5) / (4 * n**3 + 4), 2, True),
   "10006-10": lambda: limit_comparison_verdict(ALT * (4 * n + 7) / (5 * n**3 + 2), 2, True),
   "10006-11": lambda: limit_comparison_verdict((3 * n + 5) / (2 * n**3 + 8), 2, False),
   "10006-12": lambda: limit_comparison_verdict(ALT * (3 * n**2 + 6) / (5 * n**4 + 1), 2, True),
   "10006-13": lambda: limit_comparison_verdict((6 * n + 9) / (3 * n**4 + 3), 3, False),
   "10006-14": lambda: limit_comparison_verdict((2 * n**2 + 3) / (n**4 + 7), 2, False),
   "10006-15": lambda: limit_comparison_verdict((n + 3) / (4 * n**2 + 1), 1, False),
   "10006-16": lambda: limit_comparison_verdict((4 * n**2 + 6) / (n**4 + 9), 2, False),
   "10006-17": lambda: limit_comparison_verdict((4 * n**2 + 2) / (6 * n**4 + 9), 2, False),
   "10006-18": lambda: limit_comparison_verdict((4 * n + 1) / (3 * n**2 + 3), 1, False),
   "10006-19": lambda: limit_comparison_verdict(ALT * (3 * n + 9) / (2 * n**4 + 3), 3, True),
   "10006-20": lambda: limit_comparison_verdict((5 * n**2 + 7) / (3 * n**3 + 4), 1, False),
   "10006-21": lambda: limit_comparison_verdict((2 * n**2 + 1) / (3 * n**3 + 2), 1, False),

   "10008-00": lambda: alternating_error_bound(3 * COSINE_TERM, Rational(3, 4), 1),
   "10008-01": lambda: alternating_error_bound(5 * ARCTAN_TERM, Rational(5, 8), 6),
   "10008-02": lambda: alternating_error_bound(6 * EXP_NEGATIVE_TERM, Rational(3, 4), 3),
   "10008-03": lambda: alternating_error_bound(6 * ARCTAN_TERM, Rational(5, 6), 4),
   "10008-04": lambda: alternating_error_bound(9 * ARCTAN_TERM, Rational(4, 7), 1),

   "10009-00": lambda: lagrange_bound(7, 2, Rational(3, 2), 2),
   "10009-01": lambda: lagrange_bound(12, -2, Rational(-5, 4), 3),
   "10009-02": lambda: lagrange_bound(12, 1, Rational(5, 3), 3),
   "10009-03": lambda: lagrange_bound(11, -2, Rational(-5, 4), 3),
   "10009-04": lambda: lagrange_bound(5, -2, Rational(-7, 3), 3),

   "10010-00": lambda: taylor_from_relation(-x * y + 3, 0, -4, 3),
   "10010-01": lambda: taylor_from_relation(-x * y + 2, 1, -4, 3),
   "10010-02": lambda: taylor_from_relation(x * y, -1, 3, 2),
   "10010-03": lambda: taylor_from_relation(2 * x * y - 2, -1, 2, 3),
   "10010-04": lambda: taylor_from_relation(-2 * x * y - 3, -1, -3, 2),

   "10011-00": lambda: taylor_from_table([3, -5, -8, 5, -2], 2, 3),
   "10011-01": lambda: taylor_from_table([4, 7, 8, 4, 4], 0, 3),
   "10011-02": lambda: taylor_from_table([2, 3, -8, -6, 6], 1, 2),
   "10011-03": lambda: taylor_from_table([1, 4, -9, 4, 4], 2, 3),
   "10011-04": lambda: taylor_from_table([-7, -6, -8, -7, 2], 1, 2),

   "10012-00": lambda: taylor_polynomial(7 * x**3 / (1 - 3 * x), 0, 6),
   "10012-01": lambda: taylor_polynomial(3 * x**3 / (1 + x / 2), 0, 5),
   "10012-02": lambda: taylor_polynomial(9 * x**3 * exp(2 * x), 0, 5),
   "10012-03": lambda: taylor_polynomial(4 * x**2 * sin(x / 4), 0, 7),
   "10012-04": lambda: taylor_polynomial(11 * x**2 * sin(3 * x), 0, 9),

   "10013-00": lambda: interval_of_convergence(-1, 4, 4, 1),
   "10013-01": lambda: interval_of_convergence(-1, 4, 4, 0),
   "10013-02": lambda: interval_of_convergence(-1, 3, 2, 0),
   "10013-03": lambda: interval_of_convergence(-1, -2, 3, 2),
   "10013-04": lambda: interval_of_convergence(1, 4, 3, 0),
   "10013-05": lambda: interval_of_convergence(-1, 4, 5, 0),
   "10013-06": lambda: interval_of_convergence(-1, -1, 2, 2),
   "10013-07": lambda: interval_of_convergence(1, 3, 2, 1),
   "10013-08": lambda: interval_of_convergence(1, 0, 3, Rational(1, 2)),
   "10013-09": lambda: interval_of_convergence(1, 2, 3, Rational(1, 2)),
   "10013-10": lambda: interval_of_convergence(1, 0, 5, 0),
   "10013-11": lambda: interval_of_convergence(1, -2, 4, 0),
   "10013-12": lambda: interval_of_convergence(1, 1, 5, 2),
   "10013-13": lambda: interval_of_convergence(-1, 4, 3, 1),
   "10013-14": lambda: interval_of_convergence(1, 4, 4, 1),
   "10013-15": lambda: interval_of_convergence(1, 3, 5, 1),
   "10013-16": lambda: interval_of_convergence(1, -1, 3, 0),
   "10013-17": lambda: interval_of_convergence(-1, -4, 3, 0),
   "10013-18": lambda: interval_of_convergence(-1, -4, 4, Rational(1, 2)),
   "10013-19": lambda: interval_of_convergence(-1, -3, 5, 2),
   "10013-20": lambda: interval_of_convergence(-1, 4, 5, 2),
   "10013-21": lambda: interval_of_convergence(-1, -1, 6, 1),

   "10014-00": lambda: radius_statement(4 * 8**n * (x - 3)**n / n, 3),
   "10014-01": lambda: radius_statement(3 * n**2 * (x - 4)**n / 3**n, 4),
   "10014-02": lambda: radius_statement(2 * n * (x - 2)**n / 6**n, 2),
   "10014-03": lambda: radius_statement(4 * (x - 2)**(2 * n) / (8**n * n), 2),
   "10014-04": lambda: radius_statement(4 * 7**n * (x - 5)**n / n**2, 5),

   "10015-00": lambda: endpoint_verdict(1, 2, 5, Rational(1, 3), 0, "right"),
   "10015-01": lambda: endpoint_verdict(1, -3, 3, Rational(3, 2), 4, "left"),
   "10015-02": lambda: endpoint_verdict(-1, 3, 5, Rational(3, 2), 0, "left"),
   "10015-03": lambda: endpoint_verdict(-1, -2, 5, 2, 0, "right"),
   "10015-04": lambda: endpoint_verdict(1, 1, 5, Rational(3, 2), 0, "right"),
   "10015-05": lambda: endpoint_verdict(-1, 1, 4, Rational(1, 2), 6, "left"),
   "10015-06": lambda: endpoint_verdict(-1, 4, 4, Rational(1, 2), 3, "right"),
   "10015-07": lambda: endpoint_verdict(-1, 1, 2, 2, 2, "left"),
   "10015-08": lambda: endpoint_verdict(1, 5, 4, Rational(1, 3), 4, "left"),
   "10015-09": lambda: endpoint_verdict(-1, 5, 3, Rational(1, 2), 4, "right"),
   "10015-10": lambda: endpoint_verdict(1, 3, 3, Rational(3, 2), 0, "right"),
   "10015-11": lambda: endpoint_verdict(-1, -2, 3, Rational(3, 2), 2, "left"),
   "10015-12": lambda: endpoint_verdict(1, 2, 3, 2, 0, "left"),
   "10015-13": lambda: endpoint_verdict(-1, -1, 5, Rational(1, 3), 0, "left"),
   "10015-14": lambda: endpoint_verdict(-1, 2, 4, Rational(1, 3), 0, "left"),
   "10015-15": lambda: endpoint_verdict(1, -4, 4, 2, 0, "left"),
   "10015-16": lambda: endpoint_verdict(1, 3, 2, Rational(3, 2), 0, "left"),
   "10015-17": lambda: endpoint_verdict(-1, 1, 3, Rational(3, 2), 0, "right"),
   "10015-18": lambda: endpoint_verdict(1, -5, 5, Rational(1, 2), 6, "right"),
   "10015-19": lambda: endpoint_verdict(1, -3, 2, Rational(3, 2), 0, "left"),
   "10015-20": lambda: endpoint_verdict(-1, -3, 5, Rational(3, 2), 3, "left"),
   "10015-21": lambda: endpoint_verdict(-1, 4, 3, 1, 5, "right"),

   "10016-00": lambda: maclaurin_statement(
      4 * x**3 / (1 - 7 * x),
      4 * 7**n * x**(n + 3),
      "\\( 4 x^{3} + 28 x^{4} + 196 x^{5} + 1372 x^{6} + \\cdots + 4 \\cdot 7^{n} x^{n+3} + \\cdots \\)",
   ),
   "10016-01": lambda: maclaurin_statement(
      5 * sin(5 * x),
      5 * ALT * 5**(2 * n + 1) * x**(2 * n + 1) / factorial(2 * n + 1),
      "\\( 25 x - \\frac{625}{6} x^{3} + \\frac{3125}{24} x^{5} - \\frac{78125}{1008} x^{7} + \\cdots + \\frac{5 \\cdot (-1)^{n} 5^{2n+1} x^{2n+1}}{(2n+1)!} + \\cdots \\)",
   ),
   "10016-02": lambda: maclaurin_statement(
      3 * exp(7 * x),
      3 * 7**n * x**n / factorial(n),
      "\\( 3 + 21 x + \\frac{147}{2} x^{2} + \\cdots + \\frac{3 \\cdot 7^{n} x^{n}}{n!} + \\cdots \\)",
   ),
   "10016-03": lambda: maclaurin_statement(
      5 / (1 - 7 * x),
      5 * 7**n * x**n,
      "\\( 5 + 35 x + 245 x^{2} + 1715 x^{3} + \\cdots + 5 \\cdot 7^{n} x^{n} + \\cdots \\)",
   ),
   "10016-04": lambda: maclaurin_statement(
      3 * sin(2 * x),
      3 * ALT * 2**(2 * n + 1) * x**(2 * n + 1) / factorial(2 * n + 1),
      "\\( 6 x - 4 x^{3} + \\frac{4}{5} x^{5} - \\frac{8}{105} x^{7} + \\cdots + \\frac{3 \\cdot (-1)^{n} 2^{2n+1} x^{2n+1}}{(2n+1)!} + \\cdots \\)",
   ),

   "10017-00": lambda: first_nonzero_terms(7 * exp(-3 * x**4), 4),
   "10017-01": lambda: first_nonzero_terms(4 * sin(4 * x**3), 3),
   "10017-02": lambda: first_nonzero_terms(8 * sin(-4 * x**4), 4),
   "10017-03": lambda: first_nonzero_terms(9 * exp(-3 * x**3), 4),
   "10017-04": lambda: first_nonzero_terms(13 * sin(2 * x**2), 4),

   "10018-00": lambda: derivative_series_statement(12, 1, -2, 2, "x + 2"),
   "10018-01": lambda: derivative_series_statement(7, -1, 3, 5, "x - 3"),
   "10018-02": lambda: derivative_series_statement(7, -1, -3, 2, "x + 3"),
   "10018-03": lambda: derivative_series_statement(11, 1, 1, 4, "x - 1"),
   "10018-04": lambda: derivative_series_statement(4, -1, -4, 6, "x + 4"),

   "10019-00": lambda: antiderivative_series_terms(5 / (1 + 3 * x**2), -6, 4),
   "10019-01": lambda: antiderivative_series_terms(8 / (1 - 3 * x**2), 1, 5),
   "10019-02": lambda: antiderivative_series_terms(1 / (1 - 4 * x**2), -6, 4),
   "10019-03": lambda: antiderivative_series_terms(3 / (1 + 3 * x), -1, 4),
   "10019-04": lambda: antiderivative_series_terms(6 / (1 - 4 * x**2), 2, 4),

   "10020-00": lambda: taylor_convergence_at("log", -3, 6, 3),
   "10020-01": lambda: taylor_convergence_at("log", 1, 1, 0),
   "10020-02": lambda: taylor_convergence_at("log", 1, 4, 5),
   "10020-03": lambda: taylor_convergence_at("log", -4, 2, -2),
   "10020-04": lambda: taylor_convergence_at("log", -2, 2, -4),
   "10020-05": lambda: taylor_convergence_at("log", 0, 1, 1),
   "10020-06": lambda: taylor_convergence_at("log", 0, 5, 5),
   "10020-07": lambda: taylor_convergence_at("geometric", 1, 4, -3),
   "10020-08": lambda: taylor_convergence_at("log", -3, 3, 0),
   "10020-09": lambda: taylor_convergence_at("geometric", -4, 1, -5),
   "10020-10": lambda: taylor_convergence_at("log", -4, 5, 1),
   "10020-11": lambda: taylor_convergence_at("log", -4, 1, -5),
   "10020-12": lambda: taylor_convergence_at("geometric", 4, 5, -1),
   "10020-13": lambda: taylor_convergence_at("log", 0, 4, 4),
   "10020-14": lambda: taylor_convergence_at("log", -1, 1, -2),
   "10020-15": lambda: taylor_convergence_at("log", 3, 6, 9),
   "10020-16": lambda: taylor_convergence_at("log", 4, 5, -1),
   "10020-17": lambda: taylor_convergence_at("log", -4, 6, -10),
   "10020-18": lambda: taylor_convergence_at("log", 4, 3, 7),
   "10020-19": lambda: taylor_convergence_at("log", 4, 2, 6),
   "10020-20": lambda: taylor_convergence_at("log", 2, 1, 1),
   "10020-21": lambda: taylor_convergence_at("log", 0, 2, -2),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
