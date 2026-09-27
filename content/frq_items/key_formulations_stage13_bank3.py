"""Blind SymPy formulations of every checked point in the bank3 batch of stage 13 (content2),
written on 2026-09-27 by a separate Claude agent given only the stems and part prompts
(tools/frq_key_recheck.py stems), on the operator's delegation. Merged by key_formulations.py.
"""
import sympy

x, t, k, theta = sympy.symbols("x t k theta")

PRECISION = 50


def root(equation, variable, guess):
   return sympy.nsolve(equation, variable, guess, prec=PRECISION)


def numeric(expression):
   return sympy.N(expression, PRECISION)


position_04003 = 2 * t**3 - 15 * t**2 + 36 * t - 10
velocity_04003 = sympy.diff(position_04003, t)
acceleration_04003 = sympy.diff(velocity_04003, t)

radius_04006 = sympy.Integer(2)
radius_rate_04006 = sympy.Rational(-1, 10)

tea_rate_04008 = -16 / (t + 2) ** 2

wind_08001 = 14 + 8 * sympy.sin(t**2 / 50)
second_wind_08001 = 10 + 3 * t - t**2 / 4

gravel_rate_08002 = 30 - 12 * sympy.exp(-(t**2) / 20)
pond_rate_08002 = 25 * sympy.sin(t**2 / 18) - 6

f_08008_02 = 5 * sympy.exp(-(x**2) / 4)
g_08008_02 = x**2 - 2 * x

f_08008_03 = 3 * sympy.log(x + 1)
g_08008_03 = (x**2 - x) / 2

f_08011_01 = x * sympy.exp(-x / 2)
g_08011_01 = (x - sympy.Rational(3, 2)) ** 2 / 2

f_08011_02 = sympy.log(x)
g_08011_02 = (x - 1) ** 2 / 3

f_08012 = 2 * sympy.sqrt(x) * sympy.exp(-x / 4)

f_08013 = 4 - x**2
g_08013 = sympy.exp(x / 2)

f_08014 = x * sympy.cos(x / 2)
fprime_08014 = sympy.diff(f_08014, x)
arc_integrand_08014 = sympy.sqrt(1 + fprime_08014**2)

x_rate_09001_01 = 2 + sympy.sin(t**2)
y_09001_01 = 3 * sympy.sin(t / 2) + sympy.log(1 + t**2)

x_09001_02 = 3 * t + 2 * sympy.cos(t)
y_rate_09001_02 = sympy.exp(sympy.cos(t)) - sympy.Rational(5, 4)

x_rate_09005 = 2 * sympy.cos(t**2 / 5)
y_rate_09005 = sympy.log(1 + t**2) - 1

x_rate_09007_01 = sympy.cos(t) + t / 4
y_rate_09007_01 = sympy.log(1 + t**2) - 1
speed_09007_01 = sympy.sqrt(x_rate_09007_01**2 + y_rate_09007_01**2)

x_09007_02 = 4 * sympy.sin(t / 2) + t
y_09007_02 = t**2 * sympy.exp(-t / 2)
speed_09007_02 = sympy.sqrt(sympy.diff(x_09007_02, t) ** 2 + sympy.diff(y_09007_02, t) ** 2)

r_09012_02 = 3 - sympy.exp(sympy.sin(theta))
r_09012_03 = 1 + theta * sympy.cos(theta)

petal_09013 = 3 * sympy.sin(2 * theta)
limacon_09013 = 2 - sympy.cos(theta)


def average_acceleration_time_04003():
   average_acceleration = (velocity_04003.subs(t, 3) - velocity_04003.subs(t, 0)) / 3

   return sympy.solve(sympy.Eq(acceleration_04003, average_acceleration), t)[0]


def length_04006():
   return 72 / radius_04006**2


def length_rate_04006():
   length = 72 / x**2

   return sympy.diff(length, x).subs(x, radius_04006) * radius_rate_04006


def side_area_rate_04006():
   side_area = 2 * sympy.pi * x * (72 / x**2)

   return sympy.diff(side_area, x).subs(x, radius_04006) * radius_rate_04006


def tangent_04008(center, value, at):
   return value + tea_rate_04008.subs(t, center) * (at - center)


def tangent_time_at_87_04008():
   return sympy.solve(sympy.Eq(tangent_04008(0, 90, t), 87), t)[0]


average_wind_08001 = sympy.Integral(wind_08001, (t, 0, 12)) / 12


def running_average_wind_08001():
   running_integral = sympy.Integral(wind_08001, (t, 0, x))

   return root(running_integral - sympy.Rational(35, 2) * x, x, 10)


def wind_equals_average_08001():
   average_value = numeric(average_wind_08001.doit())

   return root(wind_08001 - average_value, t, 7)


average_gravel_08002 = sympy.Integral(gravel_rate_08002, (t, 0, 8)) / 8
late_average_gravel_08002 = sympy.Integral(gravel_rate_08002, (t, 4, 10)) / 6


def gravel_rate_equals_08002(average, guess):
   return root(gravel_rate_08002 - numeric(average.doit()), t, guess)


def gravel_running_average_08002():
   return root(sympy.Integral(gravel_rate_08002, (t, 0, x)) - 22 * x, x, 5)


average_pond_08002 = sympy.Integral(pond_rate_08002, (t, 0, 6)) / 6
late_average_pond_08002 = sympy.Integral(pond_rate_08002, (t, 6, 10)) / 4


def pond_rate_equals_08002(average, guess):
   return root(pond_rate_08002 - numeric(average.doit()), t, guess)


def pond_zero_average_08002():
   return root(sympy.Integral(pond_rate_08002, (t, 0, x)), x, 8)


def crossings_08008_02():
   p = root(f_08008_02 - g_08008_02, x, -1)
   q = root(f_08008_02 - g_08008_02, x, 3)

   return p, q


def area_08008_02():
   p, q = crossings_08008_02()

   return sympy.Integral(f_08008_02 - g_08008_02, (x, p, q))


def half_area_line_08008_02():
   p, _q = crossings_08008_02()
   half_area = numeric(area_08008_02().doit()) / 2

   return root(sympy.Integral(f_08008_02 - g_08008_02, (x, p, k)) - half_area, k, 1)


def crossing_08008_03():
   return root(f_08008_03 - g_08008_03, x, sympy.Rational(7, 2))


def area_region_left_08008_03():
   return root(sympy.Integral(f_08008_03 - g_08008_03, (x, 0, k)) - 2, k, 1)


def crossings_08011_01():
   p = root(f_08011_01 - g_08011_01, x, sympy.Rational(1, 2))
   q = root(f_08011_01 - g_08011_01, x, sympy.Rational(3))

   return p, q


def square_volume_08011_01():
   p, q = crossings_08011_01()

   return sympy.Integral((f_08011_01 - g_08011_01) ** 2, (x, p, q))


def semicircle_volume_08011_01():
   p, q = crossings_08011_01()

   return sympy.pi / 8 * sympy.Integral((f_08011_01 - g_08011_01) ** 2, (x, p, q))


def crossing_08011_02():
   return root(f_08011_02 - g_08011_02, x, 3)


def crossings_08012():
   p = root(f_08012 - 1, x, sympy.Rational(3, 10))
   q = root(f_08012 - 1, x, 6)

   return p, q


def volume_about_line_08012():
   p, q = crossings_08012()

   return sympy.pi * sympy.Integral((f_08012 - 1) ** 2, (x, p, q))


def volume_twenty_radius_08012():
   partial_volume = sympy.pi * sympy.integrate(f_08012**2, (x, 0, k))

   return root(partial_volume - 20, k, 3)


def crossings_08013():
   left = root(f_08013 - g_08013, x, -2)
   right = root(f_08013 - g_08013, x, sympy.Rational(3, 2))

   return left, right


def arc_length_five_08014():
   return root(sympy.Integral(arc_integrand_08014, (x, 0, k)) - 5, k, 4)


def extrema_08014():
   p = root(fprime_08014, x, sympy.Rational(17, 10))
   q = root(fprime_08014, x, 6)

   return p, q


def time_at_x_eight_09001_01():
   return root(1 + sympy.Integral(x_rate_09001_01, (t, 0, x)) - 8, x, 3)


def slope_at_time_09001_01():
   time = time_at_x_eight_09001_01()

   return (sympy.diff(y_09001_01, t) / x_rate_09001_01).subs(t, time)


def return_time_09001_02():
   return root(sympy.Integral(y_rate_09001_02, (t, 0, x)), x, 3)


def slope_at_return_09001_02():
   time = return_time_09001_02()

   return (y_rate_09001_02 / sympy.diff(x_09001_02, t)).subs(t, time)


turning_time_09005 = sympy.sqrt(sympy.E - 1)


def distance_five_time_09007_01():
   return root(sympy.Integral(speed_09007_01, (t, 0, x)) - 5, x, 3)


def x_at_distance_five_09007_01():
   time = distance_five_time_09007_01()

   return 1 + sympy.Integral(x_rate_09007_01, (t, 0, time))


def leftward_times_09007_01():
   p = root(x_rate_09007_01, t, 2)
   q = root(x_rate_09007_01, t, 4)

   return p, q


def half_distance_time_09007_02():
   half_total = numeric(sympy.Integral(speed_09007_02, (t, 0, 6)).doit()) / 2

   return root(sympy.Integral(speed_09007_02, (t, 0, x)) - half_total, x, 3)


def speed_at_half_distance_09007_02():
   return speed_09007_02.subs(t, half_distance_time_09007_02())


area_quadrant_09012_02 = sympy.Integral(r_09012_02**2 / 2, (theta, 0, sympy.pi / 2))
alpha_09012_02 = sympy.pi + sympy.asin(sympy.log(2))
beta_09012_02 = 2 * sympy.pi - sympy.asin(sympy.log(2))


def half_area_ray_09012_02():
   half_area = numeric(area_quadrant_09012_02.doit()) / 2

   return root(sympy.Integral(r_09012_02**2 / 2, (theta, 0, x)) - half_area, x, sympy.Rational(1, 2))


def zero_angle_09012_03():
   return root(r_09012_03, theta, 2)


def unit_area_ray_09012_03():
   return root(sympy.Integral(r_09012_03**2 / 2, (theta, 0, x)) - 1, x, 1)


def intersections_09013():
   alpha = root(petal_09013 - limacon_09013, theta, sympy.Rational(4, 10))
   beta = root(petal_09013 - limacon_09013, theta, sympy.Rational(12, 10))

   return alpha, beta


def inside_petal_outside_limacon_09013():
   alpha, beta = intersections_09013()

   return sympy.Integral((petal_09013**2 - limacon_09013**2) / 2, (theta, alpha, beta))


def inside_both_09013():
   alpha, beta = intersections_09013()
   near_axis = sympy.Integral(petal_09013**2 / 2, (theta, 0, alpha))
   middle = sympy.Integral(limacon_09013**2 / 2, (theta, alpha, beta))
   near_top = sympy.Integral(petal_09013**2 / 2, (theta, beta, sympy.pi / 2))

   return near_axis + middle + near_top


def region_s_09013():
   alpha, _beta = intersections_09013()

   return sympy.Integral((limacon_09013**2 - petal_09013**2) / 2, (theta, 0, alpha))


FORMULATIONS = {
   "FRQ-AGT-04003-01:a1": lambda: (position_04003.subs(t, 4) - position_04003.subs(t, 0)) / 4,
   "FRQ-AGT-04003-01:c2": average_acceleration_time_04003,
   "FRQ-AGT-04006-01:a1": length_04006,
   "FRQ-AGT-04006-01:b3": length_rate_04006,
   "FRQ-AGT-04006-01:c2": side_area_rate_04006,
   "FRQ-AGT-04008-02:a3": lambda: tangent_04008(0, 90, sympy.Rational(1, 2)),
   "FRQ-AGT-04008-02:b1": lambda: sympy.diff(tea_rate_04008, t),
   "FRQ-AGT-04008-02:c1": tangent_time_at_87_04008,
   "FRQ-AGT-04008-02:d2": lambda: tangent_04008(2, 86, sympy.Rational(12, 5)),
   "FRQ-AGT-05001-02:a1": lambda: sympy.Rational(62 - 20, 12),
   "FRQ-AGT-05006-03:a1": lambda: sympy.diff((x**2 - 3) * sympy.exp(-x), x),
   "FRQ-AGT-05006-03:d2": lambda: sympy.Integer(3),
   "FRQ-AGT-08001-02:a2": lambda: average_wind_08001,
   "FRQ-AGT-08001-02:b1": running_average_wind_08001,
   "FRQ-AGT-08001-02:b2": running_average_wind_08001,
   "FRQ-AGT-08001-02:c3": lambda: sympy.integrate(second_wind_08001, (t, 0, 12)) / 12,
   "FRQ-AGT-08001-02:d1": wind_equals_average_08001,
   "FRQ-AGT-08001-02:d2": wind_equals_average_08001,
   "FRQ-AGT-08002-01:a2": lambda: average_gravel_08002,
   "FRQ-AGT-08002-01:b1": lambda: gravel_rate_equals_08002(average_gravel_08002, 4),
   "FRQ-AGT-08002-01:b2": lambda: gravel_rate_equals_08002(average_gravel_08002, 4),
   "FRQ-AGT-08002-01:c1": gravel_running_average_08002,
   "FRQ-AGT-08002-01:c2": gravel_running_average_08002,
   "FRQ-AGT-08002-01:d3": lambda: gravel_rate_equals_08002(late_average_gravel_08002, 6),
   "FRQ-AGT-08002-02:a2": lambda: average_pond_08002,
   "FRQ-AGT-08002-02:b1": lambda: pond_rate_equals_08002(average_pond_08002, 4),
   "FRQ-AGT-08002-02:b2": lambda: pond_rate_equals_08002(average_pond_08002, 4),
   "FRQ-AGT-08002-02:c1": pond_zero_average_08002,
   "FRQ-AGT-08002-02:c2": pond_zero_average_08002,
   "FRQ-AGT-08002-02:d3": lambda: pond_rate_equals_08002(late_average_pond_08002, 8),
   "FRQ-AGT-08008-02:a2": crossings_08008_02,
   "FRQ-AGT-08008-02:a3": area_08008_02,
   "FRQ-AGT-08008-02:b1": half_area_line_08008_02,
   "FRQ-AGT-08008-02:b2": half_area_line_08008_02,
   "FRQ-AGT-08008-02:c2": lambda: (0, 2),
   "FRQ-AGT-08008-02:c4": lambda: sympy.integrate(-g_08008_02, (x, 0, 2)),
   "FRQ-AGT-08008-03:a2": lambda: (0, crossing_08008_03()),
   "FRQ-AGT-08008-03:a3": lambda: sympy.Integral(f_08008_03 - g_08008_03, (x, 0, crossing_08008_03())),
   "FRQ-AGT-08008-03:b2": lambda: sympy.Integral(g_08008_03 - f_08008_03, (x, crossing_08008_03(), 5)),
   "FRQ-AGT-08008-03:c1": area_region_left_08008_03,
   "FRQ-AGT-08008-03:c2": area_region_left_08008_03,
   "FRQ-AGT-08008-03:d2": lambda: sympy.integrate(-g_08008_03, (x, 0, 1)),
   "FRQ-AGT-08011-01:a1": crossings_08011_01,
   "FRQ-AGT-08011-01:a2": square_volume_08011_01,
   "FRQ-AGT-08011-01:b2": semicircle_volume_08011_01,
   "FRQ-AGT-08011-01:c1": lambda: (0, 2),
   "FRQ-AGT-08011-01:c5": lambda: sympy.integrate(f_08011_01**2, (x, 0, 2)),
   "FRQ-AGT-08011-02:a2": lambda: sympy.sqrt(3) / 4 * sympy.Integral((f_08011_02 - g_08011_02) ** 2, (x, 1, crossing_08011_02())),
   "FRQ-AGT-08011-02:b1": lambda: (1, crossing_08011_02()),
   "FRQ-AGT-08011-02:b2": lambda: sympy.Integral((f_08011_02 - g_08011_02) ** 2, (x, 1, crossing_08011_02())),
   "FRQ-AGT-08011-02:c1": lambda: (1, sympy.E),
   "FRQ-AGT-08011-02:c5": lambda: sympy.integrate(f_08011_02**2, (x, 1, sympy.E)),
   "FRQ-AGT-08012-02:a2": crossings_08012,
   "FRQ-AGT-08012-02:a3": volume_about_line_08012,
   "FRQ-AGT-08012-02:b4": lambda: sympy.pi * sympy.integrate(f_08012**2, (x, 0, sympy.oo)),
   "FRQ-AGT-08012-02:c1": volume_twenty_radius_08012,
   "FRQ-AGT-08012-02:c2": volume_twenty_radius_08012,
   "FRQ-AGT-08013-01:a3": crossings_08013,
   "FRQ-AGT-08013-01:b3": crossings_08013,
   "FRQ-AGT-08013-01:c3": crossings_08013,
   "FRQ-AGT-08014-01:a2": lambda: fprime_08014,
   "FRQ-AGT-08014-01:a3": lambda: (0, 3),
   "FRQ-AGT-08014-01:a4": lambda: sympy.Integral(arc_integrand_08014, (x, 0, 3)),
   "FRQ-AGT-08014-01:b1": arc_length_five_08014,
   "FRQ-AGT-08014-01:b2": arc_length_five_08014,
   "FRQ-AGT-08014-01:c2": extrema_08014,
   "FRQ-AGT-08014-01:c3": lambda: sympy.Integral(arc_integrand_08014, (x, *extrema_08014())),
   "FRQ-AGT-09001-01:a1": lambda: (0, 2),
   "FRQ-AGT-09001-01:a2": lambda: 1 + sympy.Integral(x_rate_09001_01, (t, 0, 2)),
   "FRQ-AGT-09001-01:b1": time_at_x_eight_09001_01,
   "FRQ-AGT-09001-01:b4": slope_at_time_09001_01,
   "FRQ-AGT-09001-01:c1": lambda: (0, sympy.Rational(3, 2)),
   "FRQ-AGT-09001-02:a1": lambda: (0, 1),
   "FRQ-AGT-09001-02:a2": lambda: 1 + sympy.Integral(y_rate_09001_02, (t, 0, 1)),
   "FRQ-AGT-09001-02:b1": lambda: (0, sympy.Rational(5, 2)),
   "FRQ-AGT-09001-02:c1": return_time_09001_02,
   "FRQ-AGT-09001-02:c4": slope_at_return_09001_02,
   "FRQ-AGT-09005-02:a1": lambda: (1, 5),
   "FRQ-AGT-09005-02:a3": lambda: 4 + sympy.Integral(x_rate_09005, (t, 1, 5)),
   "FRQ-AGT-09005-02:b1": lambda: (1, turning_time_09005),
   "FRQ-AGT-09005-02:b4": lambda: 2 + sympy.Integral(y_rate_09005, (t, 1, turning_time_09005)),
   "FRQ-AGT-09005-02:c2": lambda: 4 - sympy.Integral(x_rate_09005, (t, 0, 1)),
   "FRQ-AGT-09007-01:a1": lambda: (0, 2),
   "FRQ-AGT-09007-01:a2": lambda: sympy.Integral(speed_09007_01, (t, 0, 2)),
   "FRQ-AGT-09007-01:b1": distance_five_time_09007_01,
   "FRQ-AGT-09007-01:b3": x_at_distance_five_09007_01,
   "FRQ-AGT-09007-01:c1": lambda: (0, 5),
   "FRQ-AGT-09007-01:c2": lambda: sympy.Integral(speed_09007_01, (t, 0, 5)) / 5,
   "FRQ-AGT-09007-01:d1": leftward_times_09007_01,
   "FRQ-AGT-09007-01:d2": lambda: sympy.Integral(speed_09007_01, (t, *leftward_times_09007_01())),
   "FRQ-AGT-09007-02:a1": lambda: (0, 3),
   "FRQ-AGT-09007-02:a2": lambda: sympy.Integral(speed_09007_02, (t, 0, 3)),
   "FRQ-AGT-09007-02:b1": half_distance_time_09007_02,
   "FRQ-AGT-09007-02:b3": speed_at_half_distance_09007_02,
   "FRQ-AGT-09007-02:c1": lambda: (4 * sympy.pi / 3, 6),
   "FRQ-AGT-09007-02:c2": lambda: sympy.Integral(speed_09007_02, (t, 4 * sympy.pi / 3, 6)),
   "FRQ-AGT-09007-02:d1": lambda: (0, 6),
   "FRQ-AGT-09007-02:d2": lambda: sympy.Integral(speed_09007_02, (t, 0, 6)) / 6,
   "FRQ-AGT-09012-02:a2": lambda: (0, sympy.pi / 2),
   "FRQ-AGT-09012-02:a3": lambda: area_quadrant_09012_02,
   "FRQ-AGT-09012-02:b2": lambda: (alpha_09012_02, beta_09012_02),
   "FRQ-AGT-09012-02:b3": lambda: sympy.Integral((r_09012_02**2 - sympy.Rational(25, 4)) / 2, (theta, alpha_09012_02, beta_09012_02)),
   "FRQ-AGT-09012-02:c2": half_area_ray_09012_02,
   "FRQ-AGT-09012-02:c3": half_area_ray_09012_02,
   "FRQ-AGT-09012-03:a2": lambda: (0, zero_angle_09012_03()),
   "FRQ-AGT-09012-03:a3": lambda: sympy.Integral(r_09012_03**2 / 2, (theta, 0, zero_angle_09012_03())),
   "FRQ-AGT-09012-03:b2": lambda: (zero_angle_09012_03(), sympy.pi),
   "FRQ-AGT-09012-03:b3": lambda: sympy.Integral(r_09012_03**2 / 2, (theta, zero_angle_09012_03(), sympy.pi)),
   "FRQ-AGT-09012-03:c2": unit_area_ray_09012_03,
   "FRQ-AGT-09012-03:c3": unit_area_ray_09012_03,
   "FRQ-AGT-09013-02:a2": intersections_09013,
   "FRQ-AGT-09013-02:a3": inside_petal_outside_limacon_09013,
   "FRQ-AGT-09013-02:b3": inside_both_09013,
   "FRQ-AGT-09013-02:c2": lambda: (0, intersections_09013()[0]),
   "FRQ-AGT-09013-02:c3": region_s_09013,
}
