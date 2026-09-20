"""MathLive MathJSON to SymPy conversion (https://cortexjs.io/math-json/).

Covers the forms P1 items need: numbers, symbols, the arithmetic and
transcendental function heads, and the two constant symbols Pi and
ExponentialE. Anything else raises UnsupportedMathJSON rather than guessing.
"""
import sympy


class UnsupportedMathJSON(ValueError):
   pass


_UNARY_FUNCTIONS = {
   "Negate": lambda a: -a,
   "Sqrt": sympy.sqrt,
   "Exp": sympy.exp,
   "Ln": sympy.log,
   "Sin": sympy.sin,
   "Cos": sympy.cos,
   "Tan": sympy.tan,
   "Sec": sympy.sec,
   "Csc": sympy.csc,
   "Cot": sympy.cot,
   "Arcsin": sympy.asin,
   "Arccos": sympy.acos,
   "Arctan": sympy.atan,
   "Abs": sympy.Abs,
}

_CONSTANTS = {
   "Pi": sympy.pi,
   "ExponentialE": sympy.E,
}


def to_sympy(expr):
   if isinstance(expr, bool):
      raise UnsupportedMathJSON(f"unsupported MathJSON node: {expr!r}")

   if isinstance(expr, (int, float)):
      return sympy.sympify(expr)

   if isinstance(expr, str):
      return _symbol_or_constant(expr)

   if isinstance(expr, list):
      return _from_list(expr)

   raise UnsupportedMathJSON(f"unsupported MathJSON node: {expr!r}")


def _symbol_or_constant(name):
   is_constant = name in _CONSTANTS

   if is_constant:
      return _CONSTANTS[name]

   return sympy.Symbol(name)


def _from_list(expr):
   has_head = len(expr) > 0

   if not has_head:
      raise UnsupportedMathJSON("empty MathJSON expression")

   head = expr[0]
   args = expr[1:]

   if head == "Add":
      return sympy.Add(*[to_sympy(arg) for arg in args])

   if head == "Subtract":
      return _subtract(args)

   if head == "Multiply":
      return sympy.Mul(*[to_sympy(arg) for arg in args])

   if head == "Divide":
      return _divide(args)

   if head == "Power":
      return _power(args)

   if head == "Root":
      return _root(args)

   if head == "Log":
      return _log(args)

   if head == "Rational":
      return _rational(args)

   if head == "Equal":
      return _equal(args)

   is_unary_function = head in _UNARY_FUNCTIONS

   if is_unary_function:
      return _unary(head, args)

   raise UnsupportedMathJSON(f"unsupported MathJSON head: {head!r}")


def _unary(head, args):
   has_one_argument = len(args) == 1

   if not has_one_argument:
      raise UnsupportedMathJSON(f"{head} expects exactly one argument")

   return _UNARY_FUNCTIONS[head](to_sympy(args[0]))


def _subtract(args):
   has_two_terms = len(args) == 2

   if not has_two_terms:
      raise UnsupportedMathJSON("Subtract expects exactly two arguments")

   left, right = args

   return to_sympy(left) - to_sympy(right)


def _divide(args):
   has_two_terms = len(args) == 2

   if not has_two_terms:
      raise UnsupportedMathJSON("Divide expects exactly two arguments")

   numerator, denominator = args

   return to_sympy(numerator) / to_sympy(denominator)


def _power(args):
   has_two_terms = len(args) == 2

   if not has_two_terms:
      raise UnsupportedMathJSON("Power expects exactly two arguments")

   base, exponent = args

   return to_sympy(base) ** to_sympy(exponent)


def _root(args):
   has_two_terms = len(args) == 2

   if not has_two_terms:
      raise UnsupportedMathJSON("Root expects exactly two arguments")

   radicand, degree = args

   return to_sympy(radicand) ** (sympy.Integer(1) / to_sympy(degree))


def _log(args):
   has_one_argument = len(args) == 1
   has_two_arguments = len(args) == 2

   if has_one_argument:
      return sympy.log(to_sympy(args[0]))

   if has_two_arguments:
      value, base = args
      return sympy.log(to_sympy(value), to_sympy(base))

   raise UnsupportedMathJSON("Log expects one or two arguments")


def _rational(args):
   has_two_terms = len(args) == 2

   if not has_two_terms:
      raise UnsupportedMathJSON("Rational expects exactly two arguments")

   numerator, denominator = args

   return sympy.Rational(numerator, denominator)


def _equal(args):
   has_two_terms = len(args) == 2

   if not has_two_terms:
      raise UnsupportedMathJSON("Equal expects exactly two arguments")

   left, right = args

   return sympy.Eq(to_sympy(left), to_sympy(right))
