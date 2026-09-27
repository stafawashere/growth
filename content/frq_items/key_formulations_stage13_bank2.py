"""Blind SymPy formulations of every checked point in the bank2 batch of stage 13 (content2),
written on 2026-09-27 by a separate Claude agent given only the stems and part prompts
(tools/frq_key_recheck.py stems), on the operator's delegation. Merged by key_formulations.py.
"""
import sympy

x, y, t, a = sympy.symbols("x y t a")

PRECISION = 50

f_06003 = sympy.Piecewise(
   (x + 2, x <= 0),
   (2 - x, x <= 2),
   (-sympy.sqrt(4 - (x - 4) ** 2), True),
)

v_06004 = sympy.Piecewise(
   (2 * t, t <= 2),
   (4, t <= 4),
   (12 - 2 * t, t <= 6),
   (-sympy.sqrt(4 - (t - 8) ** 2), t <= 10),
   (t - 10, True),
)

r_06010 = (x + 9) / (2 * x**2 + x - 3)
q_06010 = (x**2 + 3 * x) / (x**2 - 1)
p_06010 = 6 / (x**2 + 5 * x + 6)

slope_07004 = y * (6 - y) / 8

slope_07005 = (x + 1) * (4 - y)

w_symbol = sympy.Symbol("W")
slope_07010 = (w_symbol - 40) * (t - 3) / 10

f_10012 = sympy.exp(-2 * x)

f_10019 = 4 / (4 - x)


def g_06003(upper):
   return sympy.integrate(f_06003, (x, 0, upper))


def v_integral_06004(lower, upper):
   return sympy.integrate(v_06004, (t, lower, upper))


def euler_07004(step, steps):
   current = sympy.Integer(2)

   for _ in range(steps):
      current = current + step * slope_07004.subs(y, current)

   return current


def second_derivative_07004():
   return sympy.diff(slope_07004, y) * slope_07004


def second_derivative_07005():
   return sympy.diff(slope_07005, x) + sympy.diff(slope_07005, y) * slope_07005


def second_derivative_07010():
   return sympy.diff(slope_07010, t) + sympy.diff(slope_07010, w_symbol) * slope_07010


def maclaurin(expression, order):
   return sympy.series(expression, x, 0, order).removeO()


def average_value_06004():
   area = v_integral_06004(0, 10)

   return sympy.simplify(area / 10)


def a_value_07007():
   candidate = a * x**3
   residual = sympy.diff(candidate, x) - (candidate / x + x**2)

   return sympy.solve(sympy.expand(residual / x**2), a)[0]


FORMULATIONS = {
   "FRQ-AGT-06003-01:a2": lambda: sympy.simplify(g_06003(6)),
   "FRQ-AGT-06003-01:d3": lambda: max(g_06003(-5), g_06003(2), g_06003(6), key=lambda value: float(value)),
   "FRQ-AGT-06004-01:a2": lambda: sympy.simplify(v_integral_06004(6, 12)),
   "FRQ-AGT-06004-01:b2": lambda: sympy.simplify(v_integral_06004(0, 6) - v_integral_06004(6, 10) + v_integral_06004(10, 12)),
   "FRQ-AGT-06004-01:c2": lambda: sympy.simplify(3 * v_integral_06004(2, 10) - 8),
   "FRQ-AGT-06004-01:d3": average_value_06004,
   "FRQ-AGT-06008-02:a2": lambda: sympy.integrate(sympy.sin(x) / sympy.cos(x) ** 3, x),
   "FRQ-AGT-06008-02:b3": lambda: sympy.integrate(x * sympy.sqrt(x**2 + 4), (x, 0, sympy.sqrt(5))),
   "FRQ-AGT-06008-02:c3": lambda: sympy.integrate(sympy.exp(x) / (1 + sympy.exp(x)) ** 2, (x, 0, 1)),
   "FRQ-AGT-06008-02:d1": lambda: 2 * sympy.sin(sympy.sqrt(x)),
   # Triage 2026-09-27: the point checks the whole integration-by-parts line, uv minus the integral
   # of v du, not the uv term alone; settled against the part's own prompt and the matching answer a3.
   "FRQ-AGT-06009-02:a2": lambda: x * sympy.sin(2 * x) / 2 - sympy.Integral(sympy.sin(2 * x) / 2, x),
   "FRQ-AGT-06009-02:a3": lambda: sympy.integrate(x * sympy.cos(2 * x), x),
   "FRQ-AGT-06009-02:b3": lambda: sympy.integrate(sympy.atan(x), (x, 0, 1)),
   "FRQ-AGT-06009-02:c3": lambda: sympy.Integer(4 * -2 - 1 * 3 - 5),
   "FRQ-AGT-06010-02:a3": lambda: sympy.integrate(sympy.apart(r_06010, x), (x, 2, 4)),
   # Triage 2026-09-27: the antiderivative needs absolute values, since q is defined on both sides of
   # x = 1 and x = -1; differentiating the Abs form gives q on every interval.
   "FRQ-AGT-06010-02:b2": lambda: x + 2 * sympy.log(sympy.Abs(x - 1)) + sympy.log(sympy.Abs(x + 1)),
   "FRQ-AGT-06010-02:b3": lambda: sympy.integrate(sympy.apart(q_06010, x), (x, 2, 3)),
   "FRQ-AGT-06010-02:c3": lambda: sympy.integrate(sympy.apart(p_06010, x), (x, 0, 1)),
   "FRQ-AGT-06011-01:a3": lambda: sympy.integrate(x * sympy.exp(-(x**2)), (x, 0, sympy.oo)),
   "FRQ-AGT-06011-01:b3": lambda: sympy.integrate(1 / sympy.sqrt(3 - x), (x, 0, 3)),
   "FRQ-AGT-06011-01:c2": lambda: -1 / x,
   "FRQ-AGT-06012-02:a2": lambda: sympy.Integer(3),
   "FRQ-AGT-06012-02:b2": lambda: sympy.Integer(6 * 2 * 2),
   "FRQ-AGT-06012-02:c2": lambda: sympy.Integer(-2 * -1),
   "FRQ-AGT-06012-02:d3": lambda: sympy.Integer(4 * 2),
   "FRQ-AGT-06013-02:a2": lambda: sympy.Integer(2 * 8 - 3 * (-4 + 6) + 5),
   "FRQ-AGT-06013-02:c2": lambda: sympy.Integer(5 + 6),
   "FRQ-AGT-06013-02:d2": lambda: sympy.Rational(-(-4 + 2 * 5 - 2), 5),
   "FRQ-AGT-07003-03:a5": lambda: sympy.log(x**2 + x + 1),
   "FRQ-AGT-07003-03:b3": lambda: 3 * sympy.exp(x**2 + x),
   "FRQ-AGT-07003-03:c1": lambda: 2 + sympy.integrate(x**2 + x + 1, (x, 0, 3)),
   "FRQ-AGT-07004-03:a2": lambda: euler_07004(1, 2),
   "FRQ-AGT-07004-03:b1": lambda: sympy.factor(second_derivative_07004()),
   "FRQ-AGT-07004-03:b2": lambda: second_derivative_07004().subs(y, 2),
   "FRQ-AGT-07004-03:c2": lambda: euler_07004(sympy.Rational(1, 4), 2),
   "FRQ-AGT-07005-02:a1": lambda: sympy.factor(second_derivative_07005()),
   "FRQ-AGT-07005-02:a2": lambda: second_derivative_07005().subs({x: 0, y: 2}),
   "FRQ-AGT-07007-02:d2": a_value_07007,
   "FRQ-AGT-07010-01:b2": lambda: sympy.factor(second_derivative_07010()),
   "FRQ-AGT-07010-01:b3": lambda: second_derivative_07010().subs({t: 3, w_symbol: 45}),
   "FRQ-AGT-07010-01:d2": lambda: sympy.Integer(45),
   "FRQ-AGT-10003-02:a1": lambda: (x + 2) / 3,
   "FRQ-AGT-10003-02:c4": lambda: ((x + 2) / (3 * (1 - x))).subs(x, -3),
   "FRQ-AGT-10003-02:d1": lambda: sympy.solve((x + 2) / (3 * (1 - x)) - 2, x)[0],
   "FRQ-AGT-10005-01:a1": lambda: sympy.factor(sympy.diff(x / (x**2 + 3) ** 2, x)),
   "FRQ-AGT-10005-01:b3": lambda: sympy.integrate(x / (x**2 + 3) ** 2, (x, 1, sympy.oo)),
   "FRQ-AGT-10008-02:a1": lambda: sum((-1) ** n * x**n / ((n + 2) * 2**n) for n in range(4)),
   "FRQ-AGT-10011-01:d2": lambda: 3 - 4 * x**2 + sympy.Rational(6, 2) * x**4 - sympy.Rational(18, 6) * x**6,
   "FRQ-AGT-10012-01:a2": lambda: maclaurin(f_10012, 4),
   "FRQ-AGT-10012-01:a3": lambda: maclaurin(sympy.diff(f_10012, x), 3),
   "FRQ-AGT-10012-01:b2": lambda: sympy.diff(x * f_10012, x, 3).subs(x, 0),
   "FRQ-AGT-10012-01:c2": lambda: maclaurin(x * f_10012, 4),
   "FRQ-AGT-10012-01:d1": lambda: sympy.integrate(maclaurin(f_10012, 4), x),
   "FRQ-AGT-10014-01:a3": lambda: sympy.Integer(4),
   "FRQ-AGT-10014-01:b3": lambda: sympy.Integer(3),
   "FRQ-AGT-10014-01:c3": lambda: sympy.Rational(5, 2),
   "FRQ-AGT-10017-01:a2": lambda: maclaurin(sympy.cos(3 * x), 7),
   "FRQ-AGT-10017-01:a3": lambda: sympy.expand((1 - maclaurin(sympy.cos(3 * x), 7)) / x**2),
   "FRQ-AGT-10017-01:b2": lambda: maclaurin(sympy.exp(-(x**3)), 10),
   "FRQ-AGT-10017-01:c2": lambda: maclaurin(6 / (3 + x**2), 7),
   "FRQ-AGT-10017-01:c3": lambda: sympy.expand(x * maclaurin(6 / (3 + x**2), 5)),
   "FRQ-AGT-10017-01:d1": lambda: maclaurin(sympy.cos(3 * x) * sympy.exp(-(x**3)), 4),
   "FRQ-AGT-10019-01:a1": lambda: f_10019,
   "FRQ-AGT-10019-01:b2": lambda: 2 + sum(x ** (n + 1) / ((n + 1) * 4**n) for n in range(3)),
   "FRQ-AGT-10019-01:c2": lambda: 2 + 4 * sympy.log(4) - 4 * sympy.log(4 - x),
   "FRQ-AGT-10019-01:d2": lambda: sympy.summation(1 / ((sympy.Symbol("n") + 1) * 2 ** sympy.Symbol("n")), (sympy.Symbol("n"), 0, sympy.oo)),
}
