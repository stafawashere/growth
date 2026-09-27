"""Blind SymPy formulations of every checked point in the bank1 batch of stage 13 (content2),
written on 2026-09-27 by a separate Claude agent given only the stems and part prompts
(tools/frq_key_recheck.py stems), on the operator's delegation. Merged by key_formulations.py.
"""
import sympy

x, y, t = sympy.symbols("x y t")

PRECISION = 50

R = sympy.Rational


def root(equation, variable, guess):
   return sympy.nsolve(equation, variable, guess, prec=PRECISION)


concentration_01010 = 3 * t / (50 + 4 * t)
second_tank_01010 = 3 * t - 20 + 20 * sympy.exp(-t / 10)
position_p_01010 = sympy.sqrt(t**2 + 8 * t + 1)

f_02007 = 3 * sympy.exp(x) + 4 * sympy.cos(x)
h_02007 = sympy.log(x) - 2 * sympy.sin(x)

f_02008 = (2 * x + 1) * sympy.log(x)
g_02008 = sympy.cos(x) / (1 + sympy.sin(x))

table_02009_f = {0: 2, 1: -1, 2: 3, 3: 4}
table_02009_fp = {0: 5, 1: 2, 2: -4, 3: 1}
table_02009_g = {0: 1, 1: 4, 2: -3, 3: 2}
table_02009_gp = {0: -3, 1: 3, 2: 5, 3: 6}

length_02009 = {0: 10, 1: 12, 2: 15, 3: 16}
length_rate_02009 = {0: 3, 1: 2, 2: 4, 3: 1}
width_02009 = {0: 6, 1: 5, 2: 4, 3: 3}
width_rate_02009 = {0: -1, 1: -1, 2: -2, 3: -1}

f_02011 = sympy.log(3 * x - 2) + x**2

f_03001 = (x**3 - 3 * x + 1) ** 4
g_03001 = sympy.exp(sympy.sin(sympy.pi * x))
h_03001 = sympy.cos(3 * x) ** 2

F_03001 = sympy.log(x**2 + 4 * x + 5)
G_03001 = sympy.atan(sympy.exp(x))
H_03001 = x**2 * sympy.sqrt(9 - x**2)

p_03001 = 1 / (1 + sympy.exp(-2 * x))
r_03001 = 3 ** sympy.cos(x)
s_03001 = sympy.log(sympy.sec(x) + sympy.tan(x))

g_03008 = sympy.cos(x**2)
slope_03008_curve = -y / (x + 2 * y)
slope_03008_ode = sympy.exp(y) * sympy.cos(x)
second_03008_ode = sympy.diff(slope_03008_ode, x) + sympy.diff(slope_03008_ode, y) * slope_03008_ode
third_03008_ode = sympy.diff(second_03008_ode, x) + sympy.diff(second_03008_ode, y) * slope_03008_ode

f_05006 = sympy.sin(x) ** 2 + sympy.cos(x)

f_05008 = x**2 / (x - 1)

rate_06005_river = 2 * sympy.sin(t / 3) / (t + 1)
rate_06005_battery = R(22, 10) * sympy.exp(-t**2 / 1600)
drain_06005_battery = R(6, 10) + R(25, 100) * sympy.sin(t / 8)

enter_06006 = 90 + 70 * sympy.exp(-(t - 3) ** 2 / 4)
leave_06006 = 150 * t**2 / (t**2 + 9)

arrivals_99008 = 400 * sympy.sqrt(t) * sympy.exp(-t / 3)
solar_99008 = 45 * sympy.exp(-(t - 6) ** 2 / 10)
price_99008 = R(12, 100) + R(1, 100) * t


def curve_second_derivative_03008():
   slope = slope_03008_curve
   second = sympy.diff(slope, x) + sympy.diff(slope, y) * slope

   return sympy.simplify(second.subs({x: 1, y: 2}))


def river_depth_time_06005():
   depth = R(72, 10) + sympy.Integral(rate_06005_river, (t, 4, x))

   return root(depth - 8, x, R(63, 10))


def battery_time_06005():
   level = 18 + sympy.Integral(rate_06005_battery, (t, 0, x))

   return root(level - 80, x, 34)


def battery_at_120_06005():
   level_at_60 = 18 + sympy.Integral(rate_06005_battery, (t, 0, 60))

   return level_at_60 - sympy.Integral(drain_06005_battery, (t, 60, 120))


def crowd_peak_06006():
   return root(enter_06006 - leave_06006, t, R(52, 10))


def rush_window_99008():
   start = root(arrivals_99008 - 200, t, R(3, 10))
   end = root(arrivals_99008 - 200, t, R(42, 10))

   return start, end


def rush_arrivals_99008():
   start, end = rush_window_99008()

   return sympy.Integral(arrivals_99008, (t, start, end))


def arrival_time_99008():
   arrived = sympy.Integral(arrivals_99008, (t, 0, x))

   return root(arrived - 1200, x, 5)


def solar_time_99008():
   produced = sympy.Integral(solar_99008, (t, 0, x))

   return root(produced - 200, x, 8)


FORMULATIONS = {
   "FRQ-AGT-01003-02:b3": lambda: sympy.Integer(6),
   "FRQ-AGT-01003-02:d1": lambda: sympy.Integer(2),
   "FRQ-AGT-01010-01:a2": lambda: sympy.limit(concentration_01010, t, sympy.oo),
   "FRQ-AGT-01010-01:b1": lambda: sympy.diff(concentration_01010, t),
   "FRQ-AGT-01010-01:c2": lambda: sympy.limit(3 * t - second_tank_01010, t, sympy.oo),
   "FRQ-AGT-01010-01:d2": lambda: sympy.limit(sympy.diff(second_tank_01010, t), t, sympy.oo),
   "FRQ-AGT-01010-02:a2": lambda: sympy.limit(position_p_01010 - (t + 1), t, sympy.oo),
   "FRQ-AGT-01010-02:b1": lambda: sympy.diff(position_p_01010, t),
   "FRQ-AGT-01010-02:c2": lambda: sympy.limit((8 * t + 3 * sympy.exp(-t)) / (2 * t + 1), t, sympy.oo),
   "FRQ-AGT-01010-02:d2": lambda: sympy.limit((8 - 6 * t * sympy.exp(-t) - 9 * sympy.exp(-t)) / (2 * t + 1) ** 2, t, sympy.oo),
   "FRQ-AGT-02007-02:a1": lambda: sympy.diff(f_02007, x),
   "FRQ-AGT-02007-02:b1": lambda: sympy.diff(h_02007, x, 2),
   "FRQ-AGT-02007-02:c1": lambda: sympy.diff(f_02007.subs(x, x**2), x),
   "FRQ-AGT-02007-02:d1": lambda: sympy.diff(h_02007.subs(x, sympy.exp(x)), x),
   "FRQ-AGT-02008-02:a1": lambda: sympy.diff(f_02008, x),
   "FRQ-AGT-02008-02:b1": lambda: -1 / (1 + sympy.sin(x)),
   "FRQ-AGT-02008-02:c1": lambda: sympy.diff(x**2 * g_02008, x),
   "FRQ-AGT-02008-02:d1": lambda: sympy.diff(f_02008 / (x + 1), x),
   "FRQ-AGT-02009-01:a2": lambda: sympy.Integer(table_02009_fp[1] * table_02009_g[1] + table_02009_f[1] * table_02009_gp[1]),
   "FRQ-AGT-02009-01:b2": lambda: R(table_02009_gp[2] * table_02009_f[2] - table_02009_g[2] * table_02009_fp[2], table_02009_f[2] ** 2),
   "FRQ-AGT-02009-01:c2": lambda: sympy.Integer(3 * 2**2 * table_02009_f[2] + 2**3 * table_02009_fp[2]),
   "FRQ-AGT-02009-02:a2": lambda: sympy.Integer(length_rate_02009[2] * width_02009[2] + length_02009[2] * width_rate_02009[2]),
   "FRQ-AGT-02009-02:b2": lambda: R(width_rate_02009[1] * length_02009[1] - width_02009[1] * length_rate_02009[1], length_02009[1] ** 2),
   "FRQ-AGT-02009-02:c2": lambda: sympy.Integer(
      length_rate_02009[3] * width_02009[3] * 7
      + length_02009[3] * width_rate_02009[3] * 7
      + length_02009[3] * width_02009[3] * 2
   ),
   "FRQ-AGT-02009-02:d3": lambda: R(
      (length_rate_02009[2] * width_02009[2] + length_02009[2] * width_rate_02009[2]) * (2 * length_02009[2] + 2 * width_02009[2])
      - length_02009[2] * width_02009[2] * (2 * length_rate_02009[2] + 2 * width_rate_02009[2]),
      (2 * length_02009[2] + 2 * width_02009[2]) ** 2,
   ),
   "FRQ-AGT-02011-02:a1": lambda: sympy.diff(f_02011, x),
   "FRQ-AGT-02011-02:b2": lambda: 1 + sympy.diff(f_02011, x).subs(x, 1) * R(1, 10),
   "FRQ-AGT-03001-02:a1": lambda: sympy.diff(f_03001, x),
   "FRQ-AGT-03001-02:a2": lambda: sympy.diff(f_03001, x).subs(x, 2),
   "FRQ-AGT-03001-02:b1": lambda: sympy.diff(g_03001, x),
   "FRQ-AGT-03001-02:b2": lambda: sympy.diff(g_03001, x).subs(x, 1),
   "FRQ-AGT-03001-02:c1": lambda: sympy.diff(h_03001, x),
   "FRQ-AGT-03001-02:c2": lambda: sympy.simplify(sympy.diff(h_03001, x).subs(x, sympy.pi / 18)),
   "FRQ-AGT-03001-02:d2": lambda: sympy.diff(f_03001.subs(x, x**2 - 1), x),
   "FRQ-AGT-03001-02:d3": lambda: sympy.simplify(sympy.diff(f_03001.subs(x, x**2 - 1), x).subs(x, sympy.sqrt(3))),
   "FRQ-AGT-03001-03:a1": lambda: sympy.diff(F_03001, x),
   "FRQ-AGT-03001-03:a2": lambda: sympy.diff(F_03001, x).subs(x, 0),
   "FRQ-AGT-03001-03:b1": lambda: sympy.diff(G_03001, x),
   "FRQ-AGT-03001-03:b2": lambda: sympy.diff(G_03001, x).subs(x, 0),
   "FRQ-AGT-03001-03:c1": lambda: sympy.diff(H_03001, x),
   "FRQ-AGT-03001-03:c2": lambda: sympy.simplify(sympy.diff(H_03001, x).subs(x, sympy.sqrt(5))),
   "FRQ-AGT-03001-03:d2": lambda: sympy.diff(G_03001**3, x),
   "FRQ-AGT-03001-03:d3": lambda: sympy.simplify(sympy.diff(G_03001**3, x).subs(x, 0)),
   "FRQ-AGT-03001-04:a1": lambda: sympy.diff(p_03001, x),
   "FRQ-AGT-03001-04:a3": lambda: sympy.simplify(sympy.diff(p_03001, x).subs(x, sympy.log(2))),
   "FRQ-AGT-03001-04:b1": lambda: sympy.diff(r_03001, x),
   "FRQ-AGT-03001-04:b3": lambda: sympy.pi,
   "FRQ-AGT-03001-04:c1": lambda: sympy.sec(x),
   "FRQ-AGT-03001-04:c2": lambda: 2 * sympy.sec(2 * x),
   "FRQ-AGT-03001-04:c3": lambda: sympy.Integer(4),
   "FRQ-AGT-03008-02:a1": lambda: sympy.diff(g_03008, x),
   "FRQ-AGT-03008-02:a3": lambda: sympy.diff(g_03008, x, 2),
   "FRQ-AGT-03008-02:a4": lambda: sympy.simplify(sympy.diff(g_03008, x, 2).subs(x, sympy.sqrt(sympy.pi))),
   "FRQ-AGT-03008-02:b2": lambda: slope_03008_curve,
   "FRQ-AGT-03008-02:c3": curve_second_derivative_03008,
   "FRQ-AGT-03008-03:a2": lambda: second_03008_ode,
   "FRQ-AGT-03008-03:b1": lambda: second_03008_ode.subs({x: 0, y: 0}),
   "FRQ-AGT-03008-03:c3": lambda: third_03008_ode.subs({x: 0, y: 0}),
   "FRQ-AGT-03008-03:d3": lambda: 4 * slope_03008_ode.subs({x: 0, y: 0}),
   "FRQ-AGT-04002-01:a1": lambda: R(330 - 180, 10 - 4),
   "FRQ-AGT-04002-01:b1": lambda: R(450 - 460, 24 - 20),
   "FRQ-AGT-04002-01:c1": lambda: (R(315, 10) - 34) / (15 - 10),
   "FRQ-AGT-04002-01:d1": lambda: (420 - 330) / (R(315, 10) - 34),
   "FRQ-AGT-04009-02:a3": lambda: (sympy.Integer(-4) + 0) / 2,
   "FRQ-AGT-04009-02:b3": lambda: sympy.limit((1 + 2 / x) ** x, x, sympy.oo),
   "FRQ-AGT-04009-02:c3": lambda: sympy.Integer(-4),
   "FRQ-AGT-05001-01:a1": lambda: R(1 - 4, 8),
   "FRQ-AGT-05005-01:d1": lambda: R(1, 2),
   "FRQ-AGT-05006-02:b2": lambda: f_05006.subs(x, sympy.pi / 3),
   "FRQ-AGT-05006-02:c2": lambda: f_05006.subs(x, sympy.pi),
   "FRQ-AGT-05006-02:d2": lambda: 5 * sympy.pi / 3,
   "FRQ-AGT-05007-04:a1": lambda: (x - 3) * sympy.log(x),
   "FRQ-AGT-05007-04:b1": lambda: sympy.diff((x - 3) * sympy.log(x), x),
   "FRQ-AGT-05007-04:b2": lambda: sympy.diff((x - 3) * sympy.log(x), x).subs(x, 3),
   "FRQ-AGT-05008-02:a1": lambda: sympy.diff(f_05008, x),
   "FRQ-AGT-05008-02:d2": lambda: f_05008.subs(x, 2),
   "FRQ-AGT-06005-02:a1": lambda: (4, 12),
   "FRQ-AGT-06005-02:a3": lambda: R(72, 10) + sympy.Integral(rate_06005_river, (t, 4, 12)),
   "FRQ-AGT-06005-02:b3": lambda: R(72, 10) - sympy.Integral(rate_06005_river, (t, 0, 4)),
   "FRQ-AGT-06005-02:c1": river_depth_time_06005,
   "FRQ-AGT-06005-02:c3": river_depth_time_06005,
   "FRQ-AGT-06005-03:a1": lambda: (0, 20),
   "FRQ-AGT-06005-03:a3": lambda: 18 + sympy.Integral(rate_06005_battery, (t, 0, 20)),
   "FRQ-AGT-06005-03:b1": battery_time_06005,
   "FRQ-AGT-06005-03:b3": battery_time_06005,
   "FRQ-AGT-06005-03:c1": lambda: (60, 120),
   "FRQ-AGT-06005-03:c3": battery_at_120_06005,
   "FRQ-AGT-06006-02:a1": lambda: (0, 9),
   "FRQ-AGT-06006-02:b1": lambda: (0, 9),
   "FRQ-AGT-06006-02:c1": lambda: (0, 4),
   "FRQ-AGT-06006-02:d1": lambda: (9, 12),
   "FRQ-AGT-06006-03:a1": lambda: (0, 8),
   "FRQ-AGT-06006-03:b1": lambda: (0, 4),
   "FRQ-AGT-06006-03:c1": lambda: (0, crowd_peak_06006()),
   "FRQ-AGT-06006-03:d1": lambda: (4, 8),
   "FRQ-AGT-99008-02:a1": lambda: (0, 3),
   "FRQ-AGT-99008-02:a2": lambda: sympy.Integral(arrivals_99008, (t, 0, 3)),
   "FRQ-AGT-99008-02:b1": rush_window_99008,
   "FRQ-AGT-99008-02:b2": rush_arrivals_99008,
   "FRQ-AGT-99008-02:c1": arrival_time_99008,
   "FRQ-AGT-99008-02:c2": arrival_time_99008,
   "FRQ-AGT-99008-02:d2": lambda: (0, 10),
   "FRQ-AGT-99008-02:d3": lambda: sympy.Integral((10 - t) * arrivals_99008, (t, 0, 10)),
   "FRQ-AGT-99008-03:a1": lambda: (0, 4),
   "FRQ-AGT-99008-03:a2": lambda: sympy.Integral(solar_99008, (t, 0, 4)),
   "FRQ-AGT-99008-03:b1": lambda: (0, 12),
   "FRQ-AGT-99008-03:b2": lambda: sympy.Integral(solar_99008, (t, 0, 12)) / 12,
   "FRQ-AGT-99008-03:c1": solar_time_99008,
   "FRQ-AGT-99008-03:c2": solar_time_99008,
   "FRQ-AGT-99008-03:d2": lambda: (0, 12),
   "FRQ-AGT-99008-03:d3": lambda: sympy.Integral(price_99008 * solar_99008, (t, 0, 12)),
}
