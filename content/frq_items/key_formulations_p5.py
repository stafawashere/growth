"""Blind SymPy formulations of every checked point in the 16 new free-response questions of P5,
written on 2026-09-24 by a separate Claude agent given only the stems and part prompts
(tools/frq_key_recheck.py stems), on the operator's delegation. Calculator answers are exact
expressions (unevaluated integrals) or roots found by sympy.nsolve at 50 digits. Run with:
python3 tools/frq_key_recheck.py check content/frq_items content/frq_items/key_formulations.py, which merges this file
"""
import sympy

x, y, t, k, theta = sympy.symbols("x y t k theta")

PRECISION = 50

fprime_04008 = sympy.sqrt(x**3 + 1)

f_05006 = x**3 - 9 * x**2 + 24 * x
g_05006 = sympy.integrate(f_05006.subs(x, t) - 20, (t, 0, x))

slope_05007 = y * (x**2 - 2 * x - 3)
second_05007 = sympy.diff(slope_05007, x) + sympy.diff(slope_05007, y) * slope_05007

inflow_06005 = 30 + 12 * sympy.sin(sympy.pi * t / 6)
drain_06005 = 3 * t
water_06005 = 200 + sympy.integrate(inflow_06005 - drain_06005, (t, 0, t))

f_07003_early = (t**2 + 1) ** 2
f_07003_late = 100 / t**2

slope_07004 = y - 2 * x

temperature_08001 = 50 + 20 * sympy.exp(-((t - 14) ** 2) / 25)
average_08001 = sympy.Integral(temperature_08001, (t, 0, 24)) / 24

f_08008 = 6 * x - x**2
g_08008 = x**2 - 2 * x

f_08012 = 4 * x * sympy.exp(-x)

velocity_x_09005 = sympy.sqrt(1 + t**3)
velocity_y_09005 = 4 - sympy.exp(t**2 / 4)

r_09012 = 1 + 2 * sympy.sin(theta)

outer_09013 = 4 * sympy.sin(theta)
inner_09013 = 1 + theta

cars_99008 = 120 + 80 * sympy.sin(t**2 / 12)
fee_99008 = 12 - sympy.Rational(8, 10) * t


def euler(slope, start_x, start_y, step, steps):
   current_x = sympy.nsimplify(start_x)
   current_y = sympy.nsimplify(start_y)
   step = sympy.nsimplify(step)

   for _ in range(steps):
      current_y = current_y + step * slope.subs({x: current_x, y: current_y})
      current_x = current_x + step

   return current_y


def root(equation, variable, guess):
   return sympy.nsolve(equation, variable, guess, prec=PRECISION)


def average_crossing_08001():
   average_value = average_08001.doit().evalf(PRECISION)

   return root(temperature_08001 - average_value, t, 9)


def running_average_crossing_08001():
   running_integral = sympy.integrate(temperature_08001, (t, 0, x))

   return root(running_integral / x - 55, x, 12)


def crossings_08012():
   p = root(f_08012 - 1, x, sympy.Rational(3, 10))
   q = root(f_08012 - 1, x, 2)

   return p, q


def volume_about_line_08012():
   p, q = crossings_08012()

   return sympy.pi * sympy.Integral((f_08012 - 1) ** 2, (x, p, q))


def half_volume_radius_08012():
   partial_volume = sympy.pi * sympy.integrate(f_08012**2, (x, 0, k))

   return root(partial_volume - 2 * sympy.pi, k, sympy.Rational(13, 10))


def highest_y_09005():
   turning_time = 2 * sympy.sqrt(sympy.log(4))

   return 1 + sympy.Integral(velocity_y_09005, (t, 2, turning_time))


def time_at_x_seven_09005():
   travelled = sympy.Integral(velocity_x_09005, (t, 2, x))

   return root(4 + travelled - 7, x, sympy.Rational(27, 10))


def intersections_09013():
   alpha = root(outer_09013 - inner_09013, theta, sympy.Rational(34, 100))
   beta = root(outer_09013 - inner_09013, theta, sympy.Rational(22, 10))

   return alpha, beta


def area_r_09013():
   alpha, beta = intersections_09013()

   return sympy.Integral((outer_09013**2 - inner_09013**2) / 2, (theta, alpha, beta))


def area_s_09013():
   _alpha, beta = intersections_09013()

   return sympy.Integral((inner_09013**2 - outer_09013**2) / 2, (theta, beta, sympy.pi))


def splitting_ray_09013():
   alpha, _beta = intersections_09013()
   half_area = area_r_09013().evalf(PRECISION) / 2
   partial_area = sympy.Integral((outer_09013**2 - inner_09013**2) / 2, (theta, alpha, x))

   return root(partial_area - half_area, x, sympy.Rational(12, 10))


def taylor_10010():
   derivative_values = {0: sympy.Integer(2)}
   derivative_values[1] = 1 * derivative_values[0] - 3

   for order in range(1, 4):
      derivative_values[order + 1] = 1 * derivative_values[order] + order * derivative_values[order - 1]

   return derivative_values


def taylor_polynomial_10010(degree):
   derivative_values = taylor_10010()

   return sum(derivative_values[order] * (x - 1) ** order / sympy.factorial(order) for order in range(degree + 1))


def garage_fill_time_99008():
   entered = sympy.Integral(cars_99008, (t, 0, x))

   return root(entered - 500, x, 4)


FORMULATIONS = {
   "FRQ-AGT-04008-01:a1": lambda: fprime_04008.subs(x, 2),
   "FRQ-AGT-04008-01:a3": lambda: 5 + fprime_04008.subs(x, 2) * sympy.Rational(2, 10),
   "FRQ-AGT-04008-01:b1": lambda: sympy.diff(fprime_04008, x),
   "FRQ-AGT-04008-01:c1": lambda: 5 + 2 * fprime_04008.subs(x, 2),
   "FRQ-AGT-04008-01:c2": lambda: 2 * 5 + (5 + 2 * fprime_04008.subs(x, 2)) * sympy.Rational(-1, 10),
   "FRQ-AGT-04008-01:d1": lambda: 1 / fprime_04008.subs(x, 2),
   "FRQ-AGT-04008-01:d2": lambda: 2 + (4 - 5) / fprime_04008.subs(x, 2),
   "FRQ-AGT-05006-01:a3": lambda: max(f_05006.subs(x, point) for point in (0, 2, 4, 6)),
   "FRQ-AGT-05006-01:b2": lambda: min(f_05006.subs(x, point) for point in (0, 2, 4, 6)),
   "FRQ-AGT-05006-01:c2": lambda: sympy.Integer(5),
   "FRQ-AGT-05006-01:c4": lambda: min(g_05006.subs(x, point) for point in (0, 2, 5, 6)),
   "FRQ-AGT-05007-03:b1": lambda: sympy.expand(second_05007),
   "FRQ-AGT-05007-03:b2": lambda: second_05007.subs({x: 0, y: 2}),
   "FRQ-AGT-06005-01:a1": lambda: (0, 6),
   "FRQ-AGT-06005-01:a2": lambda: sympy.integrate(inflow_06005, t),
   "FRQ-AGT-06005-01:a3": lambda: sympy.integrate(inflow_06005, (t, 0, 6)),
   "FRQ-AGT-06005-01:b3": lambda: water_06005.subs(t, 6),
   "FRQ-AGT-06005-01:c2": lambda: water_06005,
   "FRQ-AGT-06005-01:c3": lambda: sympy.simplify(water_06005.subs(t, 12)),
   "FRQ-AGT-06006-01:a1": lambda: (0, 8),
   "FRQ-AGT-06006-01:a2": lambda: (0, 8),
   "FRQ-AGT-06006-01:b1": lambda: (0, 8),
   "FRQ-AGT-06006-01:c1": lambda: (0, 2),
   "FRQ-AGT-06006-01:d1": lambda: (8, 12),
   "FRQ-AGT-07003-02:a2": lambda: sympy.integrate(1 / sympy.sqrt(y), y),
   "FRQ-AGT-07003-02:a3": lambda: sympy.integrate(4 * t, t),
   "FRQ-AGT-07003-02:a5": lambda: f_07003_early,
   "FRQ-AGT-07003-02:b3": lambda: f_07003_late,
   "FRQ-AGT-07003-02:c1": lambda: 10 + sympy.integrate(f_07003_early, (t, 0, 2)) + sympy.integrate(f_07003_late, (t, 2, 4)),
   "FRQ-AGT-07004-02:a1": lambda: slope_07004 - 2,
   "FRQ-AGT-07004-02:a2": lambda: (slope_07004 - 2).subs({x: 0, y: 3}),
   "FRQ-AGT-07004-02:b2": lambda: euler(slope_07004, 0, 3, sympy.Rational(1, 2), 2),
   "FRQ-AGT-07004-02:c2": lambda: euler(slope_07004, 0, 3, sympy.Rational(-1, 2), 2),
   "FRQ-AGT-07004-02:d2": lambda: euler(slope_07004, 0, 3, sympy.Rational(1, 4), 2),
   "FRQ-AGT-08001-01:a1": lambda: (0, 24),
   "FRQ-AGT-08001-01:a2": lambda: average_08001,
   "FRQ-AGT-08001-01:b2": average_crossing_08001,
   "FRQ-AGT-08001-01:c3": running_average_crossing_08001,
   "FRQ-AGT-08001-01:d2": lambda: sympy.Integral(temperature_08001 - (62 + t / 4), (t, 0, 24)) / 24,
   "FRQ-AGT-08008-01:a2": lambda: (0, 4),
   "FRQ-AGT-08008-01:a3": lambda: sympy.integrate(f_08008 - g_08008, x),
   "FRQ-AGT-08008-01:a4": lambda: sympy.integrate(f_08008 - g_08008, (x, 0, 4)),
   "FRQ-AGT-08008-01:b3": lambda: sympy.Integer(2),
   "FRQ-AGT-08008-01:c2": lambda: sympy.integrate(g_08008 - f_08008, (x, 4, 5)),
   "FRQ-AGT-08012-01:a3": volume_about_line_08012,
   "FRQ-AGT-08012-01:b4": lambda: sympy.pi * sympy.integrate(f_08012**2, (x, 0, sympy.oo)),
   "FRQ-AGT-08012-01:c2": half_volume_radius_08012,
   "FRQ-AGT-09005-01:a1": lambda: (0, 2),
   "FRQ-AGT-09005-01:a3": lambda: 4 - sympy.Integral(velocity_x_09005, (t, 0, 2)),
   "FRQ-AGT-09005-01:b4": highest_y_09005,
   "FRQ-AGT-09005-01:c2": time_at_x_seven_09005,
   "FRQ-AGT-09012-01:a2": lambda: (0, sympy.pi / 2),
   "FRQ-AGT-09012-01:a3": lambda: sympy.integrate(r_09012**2 / 2, (theta, 0, sympy.pi / 2)),
   "FRQ-AGT-09012-01:b3": lambda: (7 * sympy.pi / 6, 11 * sympy.pi / 6),
   "FRQ-AGT-09012-01:b4": lambda: sympy.simplify(sympy.integrate(r_09012**2 / 2, (theta, 7 * sympy.pi / 6, 11 * sympy.pi / 6))),
   "FRQ-AGT-09012-01:c2": lambda: sympy.simplify(sympy.integrate(r_09012**2 / 2, (theta, -sympy.pi / 6, 7 * sympy.pi / 6)) - sympy.integrate(r_09012**2 / 2, (theta, 7 * sympy.pi / 6, 11 * sympy.pi / 6))),
   "FRQ-AGT-09013-01:a3": area_r_09013,
   "FRQ-AGT-09013-01:b3": area_s_09013,
   "FRQ-AGT-09013-01:c3": splitting_ray_09013,
   "FRQ-AGT-10010-02:a2": lambda: taylor_10010()[2],
   "FRQ-AGT-10010-02:b2": lambda: taylor_10010()[3],
   "FRQ-AGT-10010-02:c2": lambda: taylor_polynomial_10010(3),
   "FRQ-AGT-10010-02:c3": lambda: taylor_polynomial_10010(3).subs(x, sympy.Rational(6, 5)),
   "FRQ-AGT-10010-02:d2": lambda: taylor_10010()[4] / sympy.factorial(4),
   "FRQ-AGT-99008-01:a1": lambda: (0, 4),
   "FRQ-AGT-99008-01:a2": lambda: sympy.Integral(cars_99008, (t, 0, 4)),
   "FRQ-AGT-99008-01:b1": lambda: (7, 10),
   "FRQ-AGT-99008-01:b2": lambda: sympy.Integral(cars_99008, (t, 7, 10)),
   "FRQ-AGT-99008-01:c2": garage_fill_time_99008,
   "FRQ-AGT-99008-01:d2": lambda: (0, 10),
   "FRQ-AGT-99008-01:d3": lambda: sympy.Integral(cars_99008 * fee_99008, (t, 0, 10)),
}
