"""Blind SymPy formulations of every checked point in content/frq_items, written on 2026-09-24 by a
separate Claude agent given only the stems and part prompts (tools/frq_key_recheck.py stems), on
the operator's delegation. One entry was corrected after triage: 06009-01:a2, where the agent
returned only the uv term; BC-PT-99057 names uv minus the integral of v du, so the key was right
and the formulation misread the point (BUILD-LEDGER.md, stage 4). Run with:
python3 tools/frq_key_recheck.py check content/frq_items content/frq_items/key_formulations.py
"""
import sympy

x, y, t, n = sympy.symbols("x y t n")

f_02007 = 2 * sympy.sin(x) - 3 * sympy.log(x) + sympy.exp(x)
k_02007 = f_02007.subs(x, 2 * x)
f_02008 = x**2 * sympy.exp(x)
g_02008 = (3 * x + 1) / (x**2 + 1)
f_02011 = sympy.sqrt(x) + 8 / x
f_03001 = x * sympy.sqrt(5 + 4 * x**2)
h_03001 = sympy.log(sympy.cos(2 * x))
g_03008 = x * sympy.exp(2 * x)
fprime_05007 = (2 - x) * sympy.sqrt(x**2 + 5)
r_06010 = (x + 7) / (x**2 - x - 6)


def euler(slope, start_x, start_y, step, steps):
   current_x = sympy.nsimplify(start_x)
   current_y = sympy.nsimplify(start_y)
   step = sympy.nsimplify(step)

   for _ in range(steps):
      current_y = current_y + step * slope.subs({x: current_x, y: current_y})
      current_x = current_x + step

   return current_y


def trapezoid(points):
   return sum((right_t - left_t) * (left_r + right_r) / sympy.Integer(2) for (left_t, left_r), (right_t, right_r) in zip(points, points[1:]))


table_06002 = [(0, 12), (2, 16), (5, 10), (9, 8), (10, 14)]

FORMULATIONS = {
   "FRQ-AGT-02007-01:a1": lambda: sympy.diff(f_02007, x),
   "FRQ-AGT-02007-01:b1": lambda: sympy.diff(f_02007, x).subs(x, sympy.pi),
   "FRQ-AGT-02007-01:c1": lambda: sympy.diff(k_02007, x),
   "FRQ-AGT-02007-01:c2": lambda: sympy.diff(k_02007, x).subs(x, sympy.pi / 2),
   "FRQ-AGT-02008-01:a1": lambda: sympy.diff(f_02008, x),
   "FRQ-AGT-02008-01:b1": lambda: sympy.diff(g_02008, x),
   "FRQ-AGT-02008-01:b2": lambda: sympy.diff(g_02008, x).subs(x, 1),
   "FRQ-AGT-02008-01:c1": lambda: sympy.diff(f_02008 * g_02008, x).subs(x, 1),
   "FRQ-AGT-02011-01:a1": lambda: sympy.diff(f_02011, x).subs(x, 4),
   "FRQ-AGT-02011-01:c1": lambda: f_02011.subs(x, 4) + sympy.diff(f_02011, x).subs(x, 4) * sympy.Rational(2, 10),
   "FRQ-AGT-03001-01:a1": lambda: sympy.diff(f_03001, x),
   "FRQ-AGT-03001-01:b1": lambda: sympy.diff(f_03001, x).subs(x, 1),
   "FRQ-AGT-03001-01:c1": lambda: sympy.diff(h_03001, x),
   "FRQ-AGT-03001-01:c2": lambda: sympy.diff(h_03001, x).subs(x, sympy.pi / 8),
   "FRQ-AGT-03008-01:b1": lambda: (sympy.diff(x * y**2 + 1, x) + sympy.diff(x * y**2 + 1, y) * (x * y**2 + 1)).subs({x: 1, y: 2}),
   "FRQ-AGT-03008-01:c1": lambda: sympy.diff(g_03008, x),
   "FRQ-AGT-03008-01:c2": lambda: sympy.diff(g_03008, x, 2),
   "FRQ-AGT-03008-01:c3": lambda: sympy.diff(g_03008, x, 3).subs(x, 0),
   "FRQ-AGT-04009-01:a2": lambda: sympy.limit((sympy.exp(2 * x) - 1 - 2 * x) / x**2, x, 0),
   "FRQ-AGT-04009-01:b2": lambda: sympy.Integer(5) / sympy.diff(x**2 - 1, x).subs(x, 1),
   "FRQ-AGT-04009-01:c2": lambda: sympy.limit(sympy.log(x) / sympy.sqrt(x), x, sympy.oo),
   "FRQ-AGT-05007-01:a2": lambda: sympy.solve((x - 3) * sympy.exp(x), x)[0],
   "FRQ-AGT-05007-02:a2": lambda: sympy.solve(fprime_05007, x)[0],
   "FRQ-AGT-05007-02:b1": lambda: sympy.diff(fprime_05007, x).subs(x, 2),
   "FRQ-AGT-06002-01:a2": lambda: trapezoid(table_06002),
   "FRQ-AGT-06002-01:c2": lambda: trapezoid(table_06002[1:4]) / 7,
   "FRQ-AGT-06008-01:a1": lambda: sympy.integrate(x**2 * (x**3 + 2)**4, x),
   "FRQ-AGT-06008-01:b3": lambda: sympy.integrate(sympy.cos(x) * sympy.exp(sympy.sin(x)), (x, 0, sympy.pi / 2)),
   "FRQ-AGT-06008-01:c1": lambda: sympy.integrate(x / (x**2 + 1), (x, 0, 1)),
   "FRQ-AGT-06009-01:a2": lambda: x * sympy.exp(3 * x) / 3 - sympy.Integral(sympy.exp(3 * x) / 3, x),
   "FRQ-AGT-06009-01:a3": lambda: sympy.integrate(x * sympy.exp(3 * x), x),
   "FRQ-AGT-06009-01:b3": lambda: sympy.integrate(x**2 * sympy.log(x), (x, 1, sympy.E)),
   "FRQ-AGT-06010-01:b1": lambda: 2 * sympy.log(sympy.Abs(x - 3)) - sympy.log(sympy.Abs(x + 2)),
   "FRQ-AGT-06010-01:c1": lambda: sympy.integrate(r_06010, (x, 4, 5)),
   "FRQ-AGT-06012-01:a1": lambda: sympy.sqrt(x**2 + 16),
   "FRQ-AGT-06012-01:a2": lambda: sympy.sqrt(x**2 + 16).subs(x, 3),
   "FRQ-AGT-06012-01:b1": lambda: 2 * x * sympy.sqrt(x**4 + 16),
   "FRQ-AGT-06012-01:b2": lambda: (2 * x * sympy.sqrt(x**4 + 16)).subs(x, sympy.sqrt(3)),
   "FRQ-AGT-06012-01:c1": lambda: -sympy.exp(-x**2),
   "FRQ-AGT-06012-01:c2": lambda: -sympy.exp(-x**2).subs(x, 0),
   "FRQ-AGT-06013-01:a1": lambda: sympy.Integer(7) + (-3),
   "FRQ-AGT-06013-01:b1": lambda: -(2 * sympy.Integer(-3) - 3 * 6),
   "FRQ-AGT-06013-01:c1": lambda: sympy.Integer(-3) + 4 * (5 - 2),
   "FRQ-AGT-06013-01:d1": lambda: -sympy.Integer(7),
   "FRQ-AGT-07003-01:a2": lambda: -1 / y,
   "FRQ-AGT-07003-01:a3": lambda: x**2,
   "FRQ-AGT-07003-01:a5": lambda: -1 / (x**2 + 1),
   "FRQ-AGT-07004-01:a2": lambda: euler(x + 2 * y, 0, 1, sympy.Rational(1, 2), 2),
   "FRQ-AGT-07004-01:b2": lambda: euler(x + 2 * y, 0, 1, sympy.Rational(1, 4), 2),
   "FRQ-AGT-07005-01:a1": lambda: (2 * x - (x**2 - y)).subs({x: 1, y: 3}),
   "FRQ-AGT-07005-01:c1": lambda: (2 * x - (x**2 - y)).subs({x: 0, y: -1}),
   "FRQ-AGT-07007-01:b1": lambda: sympy.Integer(3) + 1,
   "FRQ-AGT-07007-01:c1": lambda: -2 * x - 1,
   "FRQ-AGT-10003-01:a1": lambda: sympy.summation(5 * sympy.Rational(-2, 3)**n, (n, 0, sympy.oo)),
   "FRQ-AGT-10003-01:b1": lambda: sympy.summation(3 * sympy.Rational(1, 4)**n, (n, 1, sympy.oo)),
   "FRQ-AGT-10003-01:c1": lambda: 2 / (3 - x),
   "FRQ-AGT-10003-01:d1": lambda: sympy.solve(2 / (3 - x) - 4, x)[0],
   "FRQ-AGT-10008-01:a1": lambda: sum((-1)**k * x**k / sympy.Integer(k + 1)**2 for k in range(4)),
   "FRQ-AGT-10008-01:b1": lambda: sympy.Rational(1, 2)**4 / 25,
   "FRQ-AGT-10008-01:c1": lambda: sympy.Rational(1, 5**3),
   "FRQ-AGT-10010-01:a2": lambda: sympy.Integer(2),
   "FRQ-AGT-10010-01:b1": lambda: sympy.Integer(2),
   "FRQ-AGT-10010-01:c2": lambda: 2 + x + x**2 + x**3 / 3,
   "FRQ-AGT-10018-01:a1": lambda: sympy.Rational(1, 3) + x / 9 + x**2 / 27,
   "FRQ-AGT-10018-01:c1": lambda: sympy.Integer(3),
   "FRQ-AGT-10018-01:d1": lambda: 1 / (3 - x),
}


def stage_six_formulations():
   """The 16 nine-point questions added in stage 6 (P5), formulated blind by another agent."""
   import importlib.util
   from pathlib import Path

   path = Path(__file__).with_name("key_formulations_p5.py")
   spec = importlib.util.spec_from_file_location("frq_formulations_p5", path)
   module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(module)

   return module.FORMULATIONS


FORMULATIONS.update(stage_six_formulations())
