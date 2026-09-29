"""Blind answers for the unit 5 items in stems_s15.json, worked from each stem alone."""
import sympy
from sympy import Abs, exp, real_root

from tools.key_recheck import x

CHOICES = {
   "ITM-GEN-05003-36": [
      "f has a relative maximum at x = -2, because f' is positive before and equal to 0 at x = -2.",
      "f has a relative minimum at x = -2, because f' is equal to 0 at x = -2.",
      "f has a relative minimum at x = -2, because f' takes its smallest nearby value at x = -2.",
      "f has neither a relative minimum nor a relative maximum at x = -2, because f' does not change sign at x = -2."
   ],
   "ITM-GEN-05003-37": [
      "f has a relative maximum at x = 4, because f' changes from negative to positive at x = 4.",
      "f has a relative maximum at x = 4, because f' changes from positive to negative at x = 4.",
      "f has a relative minimum at x = 4, because f' changes from negative to positive at x = 4.",
      "f has neither a relative minimum nor a relative maximum at x = 4, because f' stays close to 0 on both sides of x = 4."
   ],
   "ITM-GEN-05003-38": [
      "f has a relative maximum at x = -3, because f' is positive before and equal to 0 at x = -3.",
      "f has a relative minimum at x = -3, because f' is equal to 0 at x = -3.",
      "f has a relative minimum at x = -3, because f' takes its smallest nearby value at x = -3.",
      "f has neither a relative minimum nor a relative maximum at x = -3, because f' does not change sign at x = -3."
   ],
   "ITM-GEN-05003-39": [
      "f has a relative maximum at x = 1, because f' is positive before and equal to 0 at x = 1.",
      "f has a relative minimum at x = 1, because f' is equal to 0 at x = 1.",
      "f has a relative minimum at x = 1, because f' takes its smallest nearby value at x = 1.",
      "f has neither a relative minimum nor a relative maximum at x = 1, because f' does not change sign at x = 1."
   ],
   "ITM-GEN-05003-40": [
      "f has a relative maximum at x = -1, because f' is positive before and equal to 0 at x = -1.",
      "f has a relative minimum at x = -1, because f' is equal to 0 at x = -1.",
      "f has a relative minimum at x = -1, because f' takes its smallest nearby value at x = -1.",
      "f has neither a relative minimum nor a relative maximum at x = -1, because f' does not change sign at x = -1."
   ],
   "ITM-GEN-05003-41": [
      "f has a relative maximum at x = -2, because f' changes from positive to negative at x = -2.",
      "f has a relative minimum at x = -2, because f' changes from negative to positive at x = -2.",
      "f has a relative minimum at x = -2, because f' changes from positive to negative at x = -2.",
      "f has neither a relative minimum nor a relative maximum at x = -2, because f' stays close to 0 on both sides of x = -2."
   ],
   "ITM-GEN-05003-42": [
      "f has a relative maximum at x = 3, because f' is positive before and equal to 0 at x = 3.",
      "f has a relative minimum at x = 3, because f' is equal to 0 at x = 3.",
      "f has a relative minimum at x = 3, because f' takes its smallest nearby value at x = 3.",
      "f has neither a relative minimum nor a relative maximum at x = 3, because f' does not change sign at x = 3."
   ],
   "ITM-GEN-05003-43": [
      "f has a relative maximum at x = -1, because f' changes from negative to positive at x = -1.",
      "f has a relative maximum at x = -1, because f' changes from positive to negative at x = -1.",
      "f has a relative minimum at x = -1, because f' changes from negative to positive at x = -1.",
      "f has neither a relative minimum nor a relative maximum at x = -1, because f' stays close to 0 on both sides of x = -1."
   ],
   "ITM-GEN-05003-44": [
      "f has a relative maximum at x = 0, because f' changes from positive to negative at x = 0.",
      "f has a relative minimum at x = 0, because f' changes from negative to positive at x = 0.",
      "f has a relative minimum at x = 0, because f' changes from positive to negative at x = 0.",
      "f has neither a relative minimum nor a relative maximum at x = 0, because f' stays close to 0 on both sides of x = 0."
   ],
   "ITM-GEN-05003-45": [
      "f has a relative maximum at x = -1, because f' changes from positive to negative at x = -1.",
      "f has a relative minimum at x = -1, because f' changes from negative to positive at x = -1.",
      "f has a relative minimum at x = -1, because f' changes from positive to negative at x = -1.",
      "f has neither a relative minimum nor a relative maximum at x = -1, because f' stays close to 0 on both sides of x = -1."
   ],
   "ITM-GEN-05003-46": [
      "f has a relative maximum at x = 4, because f' changes from negative to positive at x = 4.",
      "f has a relative maximum at x = 4, because f' changes from positive to negative at x = 4.",
      "f has a relative minimum at x = 4, because f' changes from negative to positive at x = 4.",
      "f has neither a relative minimum nor a relative maximum at x = 4, because f' stays close to 0 on both sides of x = 4."
   ],
   "ITM-GEN-05003-47": [
      "f has a relative maximum at x = -1, because f' changes from negative to positive at x = -1.",
      "f has a relative maximum at x = -1, because f' changes from positive to negative at x = -1.",
      "f has a relative minimum at x = -1, because f' changes from negative to positive at x = -1.",
      "f has neither a relative minimum nor a relative maximum at x = -1, because f' stays close to 0 on both sides of x = -1."
   ],
   "ITM-GEN-05003-48": [
      "f has a relative maximum at x = -1, because f' changes from negative to positive at x = -1.",
      "f has a relative maximum at x = -1, because f' changes from positive to negative at x = -1.",
      "f has a relative minimum at x = -1, because f' changes from negative to positive at x = -1.",
      "f has neither a relative minimum nor a relative maximum at x = -1, because f' stays close to 0 on both sides of x = -1."
   ],
   "ITM-GEN-05003-49": [
      "f has a relative maximum at x = 4, because f' is positive before and equal to 0 at x = 4.",
      "f has a relative minimum at x = 4, because f' is equal to 0 at x = 4.",
      "f has a relative minimum at x = 4, because f' takes its smallest nearby value at x = 4.",
      "f has neither a relative minimum nor a relative maximum at x = 4, because f' does not change sign at x = 4."
   ],
   "ITM-GEN-05003-50": [
      "f has a relative maximum at x = 2, because f' is positive before and equal to 0 at x = 2.",
      "f has a relative minimum at x = 2, because f' is equal to 0 at x = 2.",
      "f has a relative minimum at x = 2, because f' takes its smallest nearby value at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' does not change sign at x = 2."
   ],
   "ITM-GEN-05003-51": [
      "f has a relative maximum at x = 2, because f' changes from positive to negative at x = 2.",
      "f has a relative minimum at x = 2, because f' changes from negative to positive at x = 2.",
      "f has a relative minimum at x = 2, because f' changes from positive to negative at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' stays close to 0 on both sides of x = 2."
   ],
   "ITM-GEN-05003-52": [
      "f has a relative maximum at x = -2, because f' changes from positive to negative at x = -2.",
      "f has a relative minimum at x = -2, because f' changes from negative to positive at x = -2.",
      "f has a relative minimum at x = -2, because f' changes from positive to negative at x = -2.",
      "f has neither a relative minimum nor a relative maximum at x = -2, because f' stays close to 0 on both sides of x = -2."
   ],
   "ITM-GEN-05003-53": [
      "f has a relative maximum at x = -1, because f' is positive before and equal to 0 at x = -1.",
      "f has a relative minimum at x = -1, because f' is equal to 0 at x = -1.",
      "f has a relative minimum at x = -1, because f' takes its smallest nearby value at x = -1.",
      "f has neither a relative minimum nor a relative maximum at x = -1, because f' does not change sign at x = -1."
   ],
   "ITM-GEN-05003-54": [
      "f has a relative maximum at x = -1, because f' is positive before and equal to 0 at x = -1.",
      "f has a relative minimum at x = -1, because f' is equal to 0 at x = -1.",
      "f has a relative minimum at x = -1, because f' takes its smallest nearby value at x = -1.",
      "f has neither a relative minimum nor a relative maximum at x = -1, because f' does not change sign at x = -1."
   ],
   "ITM-GEN-05003-55": [
      "f has a relative maximum at x = -3, because f' is positive before and equal to 0 at x = -3.",
      "f has a relative minimum at x = -3, because f' is equal to 0 at x = -3.",
      "f has a relative minimum at x = -3, because f' takes its smallest nearby value at x = -3.",
      "f has neither a relative minimum nor a relative maximum at x = -3, because f' does not change sign at x = -3."
   ],
   "ITM-GEN-05003-56": [
      "f has a relative maximum at x = 1, because f' changes from negative to positive at x = 1.",
      "f has a relative maximum at x = 1, because f' changes from positive to negative at x = 1.",
      "f has a relative minimum at x = 1, because f' changes from negative to positive at x = 1.",
      "f has neither a relative minimum nor a relative maximum at x = 1, because f' stays close to 0 on both sides of x = 1."
   ],
   "ITM-GEN-05003-57": [
      "f has a relative maximum at x = 0, because f' is positive before and equal to 0 at x = 0.",
      "f has a relative minimum at x = 0, because f' is equal to 0 at x = 0.",
      "f has a relative minimum at x = 0, because f' takes its smallest nearby value at x = 0.",
      "f has neither a relative minimum nor a relative maximum at x = 0, because f' does not change sign at x = 0."
   ],
   "ITM-GEN-05014-00": [
      "The critical points of f are x = -4 and x = -1.",
      "The only critical point of f is x = -1.",
      "The only critical point of f is x = -4.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-01": [
      "The critical points of f are x = 0 and x = 6.",
      "The only critical point of f is x = 0.",
      "The only critical point of f is x = 6.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-02": [
      "The critical points of f are x = 0 and x = 4.",
      "The critical points of f are x = 0 and x = 6.",
      "The critical points of f are x = 0, x = 4 and x = 6.",
      "The only critical point of f is x = 0."
   ],
   "ITM-GEN-05014-03": [
      "The critical points of f are x = 0 and x = 4.",
      "The only critical point of f is x = 0.",
      "The only critical point of f is x = 4.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-04": [
      "The critical points of f are x = -5 and x = -1.",
      "The only critical point of f is x = -1.",
      "The only critical point of f is x = -5.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-05": [
      "The critical points of f are x = 4 and x = 6.",
      "The only critical point of f is x = 4.",
      "The only critical point of f is x = 6.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-06": [
      "The critical points of f are x = -12 and x = -2.",
      "The critical points of f are x = -12 and x = 3.",
      "The critical points of f are x = -12, x = -2 and x = 3.",
      "The only critical point of f is x = -12."
   ],
   "ITM-GEN-05014-07": [
      "The critical points of f are x = -6 and x = -5.",
      "The only critical point of f is x = -5.",
      "The only critical point of f is x = -6.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-08": [
      "The critical points of f are x = -15 and x = -1.",
      "The critical points of f are x = -15 and x = 6.",
      "The critical points of f are x = -15, x = -1 and x = 6.",
      "The only critical point of f is x = -15."
   ],
   "ITM-GEN-05014-09": [
      "The critical points of f are x = -3 and x = 6.",
      "The only critical point of f is x = -3.",
      "The only critical point of f is x = 6.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-10": [
      "The critical points of f are x = -4 and x = 0.",
      "The only critical point of f is x = -4.",
      "The only critical point of f is x = 0.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-11": [
      "The critical points of f are x = 1 and x = 16.",
      "The critical points of f are x = 1, x = 6 and x = 16.",
      "The critical points of f are x = 6 and x = 16.",
      "The only critical point of f is x = 16."
   ],
   "ITM-GEN-05014-12": [
      "The critical points of f are x = -2 and x = 1.",
      "The only critical point of f is x = -2.",
      "The only critical point of f is x = 1.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-13": [
      "The critical points of f are x = -11 and x = -2.",
      "The critical points of f are x = -11 and x = -5.",
      "The critical points of f are x = -11, x = -5 and x = -2.",
      "The only critical point of f is x = -11."
   ],
   "ITM-GEN-05014-14": [
      "The critical points of f are x = -3 and x = 1.",
      "The only critical point of f is x = -3.",
      "The only critical point of f is x = 1.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-15": [
      "The critical points of f are x = -19 and x = -5.",
      "The critical points of f are x = -19 and x = 2.",
      "The critical points of f are x = -19, x = -5 and x = 2.",
      "The only critical point of f is x = -19."
   ],
   "ITM-GEN-05014-16": [
      "The critical points of f are x = 3 and x = 9.",
      "The critical points of f are x = 3, x = 5 and x = 9.",
      "The critical points of f are x = 5 and x = 9.",
      "The only critical point of f is x = 9."
   ],
   "ITM-GEN-05014-17": [
      "The critical points of f are x = -2 and x = 5.",
      "The only critical point of f is x = -2.",
      "The only critical point of f is x = 5.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-18": [
      "The critical points of f are x = 3 and x = 12.",
      "The critical points of f are x = 3, x = 6 and x = 12.",
      "The critical points of f are x = 6 and x = 12.",
      "The only critical point of f is x = 12."
   ],
   "ITM-GEN-05014-19": [
      "The critical points of f are x = -5 and x = -1.",
      "The only critical point of f is x = -1.",
      "The only critical point of f is x = -5.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-20": [
      "The critical points of f are x = 5 and x = 6.",
      "The only critical point of f is x = 5.",
      "The only critical point of f is x = 6.",
      "f has no critical points."
   ],
   "ITM-GEN-05014-21": [
      "The critical points of f are x = -12 and x = -3.",
      "The critical points of f are x = -12 and x = -6.",
      "The critical points of f are x = -12, x = -6 and x = -3.",
      "The only critical point of f is x = -12."
   ]
}

step = sympy.Symbol("step", positive=True)
offset = sympy.Symbol("offset", positive=True)


def choice_matching(item_id, statement):
   choices = CHOICES[item_id]

   if statement not in choices:
      raise ValueError(f"{item_id}: no choice states {statement!r}")

   return statement


def number_text(value):
   return str(sympy.nsimplify(value))


def sign_word(value):
   is_positive = bool(value > 0)

   return "positive" if is_positive else "negative"


def sign_near(derivative_expression, point, side):
   """Sign of f' on the open interval between point and the nearest other zero on that side."""
   other_zeros = [root for root in sympy.solve(derivative_expression, x) if root.is_real and root != point]
   distances = [abs(root - point) for root in other_zeros]
   gap = min(distances) if distances else sympy.Integer(2)
   probe = point + side * gap / 2

   return sympy.sign(derivative_expression.subs(x, probe))


def first_derivative_test(item_id, derivative_expression, point):
   point = sympy.Integer(point)
   value_at_point = sympy.simplify(derivative_expression.subs(x, point))

   if value_at_point != 0:
      raise ValueError(f"{item_id}: f'({point}) is {value_at_point}, not a critical point")

   left_sign = sign_near(derivative_expression, point, -1)
   right_sign = sign_near(derivative_expression, point, 1)
   changes_sign = left_sign != right_sign
   rises_then_falls = changes_sign and left_sign > 0
   point_text = number_text(point)

   if not changes_sign:
      verdict = "neither a relative minimum nor a relative maximum"
      reason = f"f' does not change sign at x = {point_text}"
   else:
      verdict = "a relative maximum" if rises_then_falls else "a relative minimum"
      reason = f"f' changes from {sign_word(left_sign)} to {sign_word(right_sign)} at x = {point_text}"

   statement = f"f has {verdict} at x = {point_text}, because {reason}."

   return choice_matching(item_id, statement)


def one_sided_pieces(expression, kink):
   """The expression written without Abs or real roots on each side of the kink."""
   left_piece = expression.subs(x, kink - offset).subs(offset, kink - x)
   right_piece = expression.subs(x, kink + offset).subs(offset, x - kink)

   return left_piece, right_piece


def critical_points(expression, kink, excluded):
   """Points of the domain where f' is 0 or fails to exist; the only nonsmooth point is the kink."""
   left_piece, right_piece = one_sided_pieces(expression, kink)
   found = set()

   for piece, on_side in ((left_piece, lambda point: point < kink), (right_piece, lambda point: point > kink)):
      zeros = sympy.solve(sympy.diff(piece, x), x)

      for zero in zeros:
         is_real = zero.is_real
         is_on_side = is_real and bool(on_side(zero))
         is_in_domain = is_on_side and zero != excluded

         if is_in_domain:
            found.add(sympy.nsimplify(zero))

   kink_in_domain = kink != excluded

   if kink_in_domain:
      base_value = expression.subs(x, kink)
      quotient = (expression.subs(x, kink + step) - base_value) / step
      right_derivative = sympy.limit(quotient, step, 0, "+")
      left_derivative = sympy.limit((expression.subs(x, kink - step) - base_value) / (-step), step, 0, "+")
      both_finite = right_derivative.is_finite and left_derivative.is_finite
      is_differentiable = both_finite and sympy.simplify(right_derivative - left_derivative) == 0
      has_zero_slope = is_differentiable and sympy.simplify(right_derivative) == 0

      if not is_differentiable or has_zero_slope:
         found.add(sympy.Integer(kink))

   return sorted(found)


def critical_point_statement(item_id, expression, kink, excluded):
   points = critical_points(expression, kink, excluded)
   texts = [f"x = {number_text(point)}" for point in points]

   if not texts:
      statement = "f has no critical points."
   elif len(texts) == 1:
      statement = f"The only critical point of f is {texts[0]}."
   else:
      listed = ", ".join(texts[:-1]) + " and " + texts[-1]
      statement = f"The critical points of f are {listed}."

   return choice_matching(item_id, statement)


def absolute_over_linear(item_id, coefficient, kink, pole):
   expression = coefficient * Abs(x - kink) / (x - pole)

   return critical_point_statement(item_id, expression, kink, pole)


def cube_root_squared_over_linear(item_id, coefficient, kink, pole):
   expression = coefficient * real_root(x - kink, 3) ** 2 / (x - pole)

   return critical_point_statement(item_id, expression, kink, pole)


def extremum(suffix, derivative_expression, point):
   return lambda: first_derivative_test(f"ITM-GEN-{suffix}", derivative_expression, point)


def absolute_item(suffix, coefficient, kink, pole):
   return lambda: absolute_over_linear(f"ITM-GEN-{suffix}", coefficient, kink, pole)


def cube_root_item(suffix, coefficient, kink, pole):
   return lambda: cube_root_squared_over_linear(f"ITM-GEN-{suffix}", coefficient, kink, pole)


quadratic_free = x**2 + 1

BY_SUFFIX = {
   "05003-36": extremum("05003-36", -(x + 2) ** 2 * (x - 2) * exp(x), -2),
   "05003-37": extremum("05003-37", 2 * (x - 4) * (x + 5), 4),
   "05003-38": extremum("05003-38", -4 * (x + 3) ** 2 * (x + 2), -3),
   "05003-39": extremum("05003-39", -2 * (x - 1) ** 2 * (x - 2) * exp(x), 1),
   "05003-40": extremum("05003-40", -4 * (x + 1) ** 2 * (x - 4) * quadratic_free, -1),
   "05003-41": extremum("05003-41", 2 * (x + 2) * (x - 3) * quadratic_free, -2),
   "05003-42": extremum("05003-42", -(x - 3) ** 2 * (x - 4) * quadratic_free, 3),
   "05003-43": extremum("05003-43", -2 * (x + 1) * (x - 6) * exp(x), -1),
   "05003-44": extremum("05003-44", x * (x - 1), 0),
   "05003-45": extremum("05003-45", -3 * (x + 1) * (x + 5) * quadratic_free, -1),
   "05003-46": extremum("05003-46", 3 * (x - 4) * (x - 2) * exp(x), 4),
   "05003-47": extremum("05003-47", -x * (x + 1) * exp(x), -1),
   "05003-48": extremum("05003-48", -2 * x * (x + 1) * exp(x), -1),
   "05003-49": extremum("05003-49", -4 * (x - 4) ** 2 * (x - 5), 4),
   "05003-50": extremum("05003-50", 4 * (x - 2) ** 2 * (x + 3), 2),
   "05003-51": extremum("05003-51", -2 * (x - 2) * (x + 1) * exp(x), 2),
   "05003-52": extremum("05003-52", -(x + 2) * (x + 3) * quadratic_free, -2),
   "05003-53": extremum("05003-53", -x * (x + 1) ** 2, -1),
   "05003-54": extremum("05003-54", -2 * (x + 1) ** 2 * (x - 1) * quadratic_free, -1),
   "05003-55": extremum("05003-55", -(x + 3) ** 2 * (x - 5) * quadratic_free, -3),
   "05003-56": extremum("05003-56", (x - 1) * (x + 1), 1),
   "05003-57": extremum("05003-57", -3 * x**2 * (x - 6) * quadratic_free, 0),
   "05014-00": absolute_item("05014-00", -4, -4, -1),
   "05014-01": absolute_item("05014-01", -5, 6, 0),
   "05014-02": cube_root_item("05014-02", 3, 4, 6),
   "05014-03": absolute_item("05014-03", -4, 4, 0),
   "05014-04": absolute_item("05014-04", 3, -5, -1),
   "05014-05": absolute_item("05014-05", -3, 6, 4),
   "05014-06": cube_root_item("05014-06", 2, -2, 3),
   "05014-07": absolute_item("05014-07", 5, -5, -6),
   "05014-08": cube_root_item("05014-08", -5, -1, 6),
   "05014-09": absolute_item("05014-09", -4, -3, 6),
   "05014-10": absolute_item("05014-10", -4, -4, 0),
   "05014-11": cube_root_item("05014-11", 5, 6, 1),
   "05014-12": absolute_item("05014-12", 1, -2, 1),
   "05014-13": cube_root_item("05014-13", -3, -5, -2),
   "05014-14": absolute_item("05014-14", -4, 1, -3),
   "05014-15": cube_root_item("05014-15", 3, -5, 2),
   "05014-16": cube_root_item("05014-16", 1, 5, 3),
   "05014-17": absolute_item("05014-17", 5, -2, 5),
   "05014-18": cube_root_item("05014-18", -3, 6, 3),
   "05014-19": absolute_item("05014-19", 2, -1, -5),
   "05014-20": absolute_item("05014-20", -1, 5, 6),
   "05014-21": cube_root_item("05014-21", 5, -6, -3),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
