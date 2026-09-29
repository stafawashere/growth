"""Blind answers for the unit 7 items in stems_s15.json, worked from each stem alone."""
import sympy
from sympy import cos, exp, sin

from tools.key_recheck import x, y

CHOICES = {
   "ITM-GEN-07012-00": [
      "\\( \\frac{dy}{y - 5} = 4 \\cos{\\left(x \\right)}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 20 \\cos{\\left(x \\right)} + 4 \\cos{\\left(x \\right)}\\right)dx \\)",
      "\\( \\left(y - 5\\right)dy = 4 \\cos{\\left(x \\right)}\\,dx \\)",
      "\\( dy = 4 \\cos{\\left(x \\right)}\\left(y - 5\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-01": [
      "\\( \\frac{dy}{y - 6} = - 6 x\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 6 x + 36 x\\right)dx \\)",
      "\\( \\left(y - 6\\right)dy = - 6 x\\,dx \\)",
      "\\( dy = - 6 x\\left(y - 6\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-02": [
      "The equation cannot be separated.",
      "\\( \\frac{dy}{y - 3} = 2 x\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(2 x - 3\\right)dx \\)",
      "\\( dy = \\left(2 x y - 3\\right)dx \\)"
   ],
   "ITM-GEN-07012-03": [
      "\\( \\frac{dy}{y + 2} = - 2 x\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 4 x - 2 x\\right)dx \\)",
      "\\( \\left(y + 2\\right)dy = - 2 x\\,dx \\)",
      "\\( dy = - 2 x\\left(y + 2\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-04": [
      "The equation cannot be separated.",
      "\\( \\frac{dy}{y - 5} = 4 \\sin{\\left(x \\right)}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(4 \\sin{\\left(x \\right)} - 5\\right)dx \\)",
      "\\( dy = \\left(4 y \\sin{\\left(x \\right)} - 5\\right)dx \\)"
   ],
   "ITM-GEN-07012-05": [
      "\\( \\frac{dy}{y - 8} = x\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 8 x + x\\right)dx \\)",
      "\\( \\left(y - 8\\right)dy = x\\,dx \\)",
      "\\( dy = x\\left(y - 8\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-06": [
      "\\( \\frac{dy}{y - 8} = - x^{3}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- x^{3} + 8 x^{3}\\right)dx \\)",
      "\\( \\left(y - 8\\right)dy = - x^{3}\\,dx \\)",
      "\\( dy = - x^{3}\\left(y - 8\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-07": [
      "The equation cannot be separated.",
      "\\( \\frac{dy}{y + 2} = 4 \\cos{\\left(x \\right)}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(4 \\cos{\\left(x \\right)} + 2\\right)dx \\)",
      "\\( dy = \\left(4 y \\cos{\\left(x \\right)} + 2\\right)dx \\)"
   ],
   "ITM-GEN-07012-08": [
      "\\( \\frac{dy}{y - 8} = 4 x^{2}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 32 x^{2} + 4 x^{2}\\right)dx \\)",
      "\\( \\left(y - 8\\right)dy = 4 x^{2}\\,dx \\)",
      "\\( dy = 4 x^{2}\\left(y - 8\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-09": [
      "\\( \\frac{dy}{y - 7} = - 2 e^{x}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 2 e^{x} + 14 e^{x}\\right)dx \\)",
      "\\( \\left(y - 7\\right)dy = - 2 e^{x}\\,dx \\)",
      "\\( dy = - 2 e^{x}\\left(y - 7\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-10": [
      "The equation cannot be separated.",
      "\\( \\frac{dy}{y - 2} = - 5 \\sin{\\left(x \\right)}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 5 \\sin{\\left(x \\right)} - 2\\right)dx \\)",
      "\\( dy = \\left(- 5 y \\sin{\\left(x \\right)} - 2\\right)dx \\)"
   ],
   "ITM-GEN-07012-11": [
      "\\( \\frac{dy}{y - 6} = e^{x}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 6 e^{x} + e^{x}\\right)dx \\)",
      "\\( \\left(y - 6\\right)dy = e^{x}\\,dx \\)",
      "\\( dy = e^{x}\\left(y - 6\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-12": [
      "The equation cannot be separated.",
      "\\( \\frac{dy}{y - 4} = - 3 \\sin{\\left(x \\right)}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 3 \\sin{\\left(x \\right)} - 4\\right)dx \\)",
      "\\( dy = \\left(- 3 y \\sin{\\left(x \\right)} - 4\\right)dx \\)"
   ],
   "ITM-GEN-07012-13": [
      "The equation cannot be separated.",
      "\\( \\frac{dy}{y + 4} = 6 x\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(6 x + 4\\right)dx \\)",
      "\\( dy = \\left(6 x y + 4\\right)dx \\)"
   ],
   "ITM-GEN-07012-14": [
      "\\( \\frac{dy}{y + 7} = 6 e^{x}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(6 e^{x} + 42 e^{x}\\right)dx \\)",
      "\\( \\left(y + 7\\right)dy = 6 e^{x}\\,dx \\)",
      "\\( dy = 6 e^{x}\\left(y + 7\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-15": [
      "\\( \\frac{dy}{y + 7} = - 6 \\sin{\\left(x \\right)}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 42 \\sin{\\left(x \\right)} - 6 \\sin{\\left(x \\right)}\\right)dx \\)",
      "\\( \\left(y + 7\\right)dy = - 6 \\sin{\\left(x \\right)}\\,dx \\)",
      "\\( dy = - 6 \\sin{\\left(x \\right)}\\left(y + 7\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-16": [
      "\\( \\frac{dy}{y - 4} = 6 x\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 24 x + 6 x\\right)dx \\)",
      "\\( \\left(y - 4\\right)dy = 6 x\\,dx \\)",
      "\\( dy = 6 x\\left(y - 4\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-17": [
      "The equation cannot be separated.",
      "\\( \\frac{dy}{y - 5} = - 6 x^{3}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 6 x^{3} - 5\\right)dx \\)",
      "\\( dy = \\left(- 6 x^{3} y - 5\\right)dx \\)"
   ],
   "ITM-GEN-07012-18": [
      "\\( \\frac{dy}{y + 8} = - 5 x^{2}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 40 x^{2} - 5 x^{2}\\right)dx \\)",
      "\\( \\left(y + 8\\right)dy = - 5 x^{2}\\,dx \\)",
      "\\( dy = - 5 x^{2}\\left(y + 8\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-19": [
      "\\( \\frac{dy}{y - 6} = - 4 x^{3}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 4 x^{3} + 24 x^{3}\\right)dx \\)",
      "\\( \\left(y - 6\\right)dy = - 4 x^{3}\\,dx \\)",
      "\\( dy = - 4 x^{3}\\left(y - 6\\right)\\,dx \\)"
   ],
   "ITM-GEN-07012-20": [
      "The equation cannot be separated.",
      "\\( \\frac{dy}{y - 2} = - 4 \\sin{\\left(x \\right)}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(- 4 \\sin{\\left(x \\right)} - 2\\right)dx \\)",
      "\\( dy = \\left(- 4 y \\sin{\\left(x \\right)} - 2\\right)dx \\)"
   ],
   "ITM-GEN-07012-21": [
      "\\( \\frac{dy}{y + 4} = 5 x^{3}\\,dx \\)",
      "\\( \\frac{dy}{y} = \\left(5 x^{3} + 20 x^{3}\\right)dx \\)",
      "\\( \\left(y + 4\\right)dy = 5 x^{3}\\,dx \\)",
      "\\( dy = 5 x^{3}\\left(y + 4\\right)\\,dx \\)"
   ]
}

CANNOT_SEPARATE = "The equation cannot be separated."


def choice_matching(item_id, statement):
   choices = CHOICES[item_id]

   if statement not in choices:
      raise ValueError(f"{item_id}: no choice states {statement!r}")

   return statement


def separated_parts(slope):
   """The right side as g(x) * h(y) with h monic in y, or None when it does not factor that way."""
   parts = sympy.separatevars(sympy.expand(slope), symbols=[x, y], dict=True)

   if parts is None:
      return None

   x_factor = parts["coeff"] * parts[x]
   y_factor = parts[y]
   leading = sympy.Poly(y_factor, y).LC()
   x_factor = sympy.expand(x_factor * leading)
   y_factor = sympy.expand(y_factor / leading)
   reassembled = sympy.expand(x_factor * y_factor - slope)

   if reassembled != 0:
      raise ValueError(f"separation of {slope} does not multiply back")

   return x_factor, y_factor


def separation_statement(item_id, slope):
   parts = separated_parts(slope)

   if parts is None:
      return choice_matching(item_id, CANNOT_SEPARATE)

   x_factor, y_factor = parts
   statement = rf"\( \frac{{dy}}{{{sympy.latex(y_factor)}}} = {sympy.latex(x_factor)}\,dx \)"

   return choice_matching(item_id, statement)


def separation(suffix, slope):
   return lambda: separation_statement(f"ITM-GEN-{suffix}", slope)


BY_SUFFIX = {
   "07012-00": separation("07012-00", 4 * y * cos(x) - 20 * cos(x)),
   "07012-01": separation("07012-01", -6 * x * y + 36 * x),
   "07012-02": separation("07012-02", 2 * x * y - 3),
   "07012-03": separation("07012-03", -2 * x * y - 4 * x),
   "07012-04": separation("07012-04", 4 * y * sin(x) - 5),
   "07012-05": separation("07012-05", x * y - 8 * x),
   "07012-06": separation("07012-06", -x**3 * y + 8 * x**3),
   "07012-07": separation("07012-07", 4 * y * cos(x) + 2),
   "07012-08": separation("07012-08", 4 * x**2 * y - 32 * x**2),
   "07012-09": separation("07012-09", -2 * y * exp(x) + 14 * exp(x)),
   "07012-10": separation("07012-10", -5 * y * sin(x) - 2),
   "07012-11": separation("07012-11", y * exp(x) - 6 * exp(x)),
   "07012-12": separation("07012-12", -3 * y * sin(x) - 4),
   "07012-13": separation("07012-13", 6 * x * y + 4),
   "07012-14": separation("07012-14", 6 * y * exp(x) + 42 * exp(x)),
   "07012-15": separation("07012-15", -6 * y * sin(x) - 42 * sin(x)),
   "07012-16": separation("07012-16", 6 * x * y - 24 * x),
   "07012-17": separation("07012-17", -6 * x**3 * y - 5),
   "07012-18": separation("07012-18", -5 * x**2 * y - 40 * x**2),
   "07012-19": separation("07012-19", -4 * x**3 * y + 24 * x**3),
   "07012-20": separation("07012-20", -4 * y * sin(x) - 2),
   "07012-21": separation("07012-21", 5 * x**3 * y + 20 * x**3),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
