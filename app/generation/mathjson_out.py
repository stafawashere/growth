"""SymPy to MathJSON, the inverse of app/items/mathjson.py for the heads that module reads.

An expression outside those heads raises, because a key the grader cannot read back is a key no
student answer can be compared with.
"""
import sympy

from app.items.mathjson import UnsupportedMathJSON

_FUNCTION_HEADS = {
   sympy.sin: "Sin",
   sympy.cos: "Cos",
   sympy.tan: "Tan",
   sympy.sec: "Sec",
   sympy.csc: "Csc",
   sympy.cot: "Cot",
   sympy.asin: "Arcsin",
   sympy.acos: "Arccos",
   sympy.atan: "Arctan",
   sympy.exp: "Exp",
   sympy.Abs: "Abs",
}


def from_sympy(expression):
   expression = sympy.sympify(expression)

   if expression is sympy.pi:
      return "Pi"

   if expression is sympy.E:
      return "ExponentialE"

   if expression.is_Integer:
      return int(expression)

   if expression.is_Rational:
      return ["Rational", int(expression.p), int(expression.q)]

   if expression.is_Float:
      return float(expression)

   if expression.is_Symbol:
      return expression.name

   if expression.is_Add:
      return ["Add", *[from_sympy(term) for term in expression.as_ordered_terms()]]

   if expression.is_Mul:
      return _product(expression)

   if expression.is_Pow:
      return _power(expression)

   if isinstance(expression, sympy.log):
      return ["Ln", from_sympy(expression.args[0])]

   head = _FUNCTION_HEADS.get(expression.func)
   has_head = head is not None

   if has_head:
      return [head, from_sympy(expression.args[0])]

   raise UnsupportedMathJSON(f"no MathJSON head for {expression.func.__name__}")


def _product(expression):
   coefficient, rest = expression.as_coeff_Mul()
   is_negated = coefficient == -1

   if is_negated:
      return ["Negate", from_sympy(rest)]

   return ["Multiply", *[from_sympy(factor) for factor in expression.as_ordered_factors()]]


def _power(expression):
   base, exponent = expression.args
   is_square_root = exponent == sympy.Rational(1, 2)

   if is_square_root:
      return ["Sqrt", from_sympy(base)]

   is_exponential = base is sympy.E

   if is_exponential:
      return ["Exp", from_sympy(exponent)]

   return ["Power", from_sympy(base), from_sympy(exponent)]
