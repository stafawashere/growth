"""MathLive MathJSON to SymPy conversion (https://cortexjs.io/math-json/).

Covers the forms P1 items need: numbers, symbols, the arithmetic and
transcendental function heads, Factorial, and the two constant symbols Pi and
ExponentialE. Lesson records add sets (Set, Interval with Open endpoints, Union,
SetMinus), List and Tuple, the relations, the infinities and NaN, and the calculus
operators Integrate, D, Limit, Sum and Subs with Apply for a named function, because the
lesson designs state keys and steps in them (docs/lessons/BUILD-PLAN.md, The design to
record path). Anything else raises UnsupportedMathJSON rather than guessing.

from_sympy is the inverse over the same heads, which tools/lesson_transcribe.py uses.
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
   "Factorial": sympy.factorial,
}

_CONSTANTS = {
   "Pi": sympy.pi,
   "ExponentialE": sympy.E,
   "PositiveInfinity": sympy.oo,
   "NegativeInfinity": -sympy.oo,
   "ComplexInfinity": sympy.zoo,
   "NaN": sympy.nan,
   "True": sympy.true,
   "False": sympy.false,
}

_RELATIONS = {
   "Equal": sympy.Eq,
   "NotEqual": sympy.Ne,
   "Greater": sympy.Gt,
   "GreaterEqual": sympy.Ge,
   "Less": sympy.Lt,
   "LessEqual": sympy.Le,
}

_SEQUENCE_HEADS = ("Tuple", "List")


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

   extended = _from_extended_head(head, args)

   if extended is not None:
      return extended

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


def _from_extended_head(head, args):
   """The heads lesson records add, or None when head is not one of them."""
   is_relation = head in _RELATIONS

   if is_relation:
      return _relation(head, args)

   is_sequence = head in _SEQUENCE_HEADS

   if is_sequence:
      return sympy.Tuple(*[to_sympy(arg) for arg in args])

   if head == "Set":
      return sympy.FiniteSet(*[to_sympy(arg) for arg in args])

   if head == "Interval":
      return _interval(args)

   if head == "Union":
      return sympy.Union(*[to_sympy(arg) for arg in args])

   if head == "SetMinus":
      return _set_minus(args)

   if head == "Integrate":
      return sympy.Integral(_body(head, args), *_limits(args[1:]))

   if head == "Sum":
      return sympy.Sum(_body(head, args), *_limits(args[1:]))

   if head == "D":
      return sympy.Derivative(_body(head, args), *_limits(args[1:]))

   if head == "Limit":
      return _limit(args)

   if head == "Subs":
      return _subs(args)

   if head == "Apply":
      return _apply(args)

   return None


def _relation(head, args):
   has_two_terms = len(args) == 2

   if not has_two_terms:
      raise UnsupportedMathJSON(f"{head} expects exactly two arguments")

   left, right = args

   return _RELATIONS[head](to_sympy(left), to_sympy(right))


def _endpoint(node):
   is_open = isinstance(node, list) and len(node) == 2 and node[0] == "Open"

   if is_open:
      return to_sympy(node[1]), True

   return to_sympy(node), False


def _interval(args):
   has_two_terms = len(args) == 2

   if not has_two_terms:
      raise UnsupportedMathJSON("Interval expects exactly two endpoints")

   low, low_open = _endpoint(args[0])
   high, high_open = _endpoint(args[1])

   return sympy.Interval(low, high, low_open, high_open)


def _set_minus(args):
   has_two_terms = len(args) == 2

   if not has_two_terms:
      raise UnsupportedMathJSON("SetMinus expects exactly two arguments")

   left, right = args

   return sympy.Complement(to_sympy(left), to_sympy(right))


def _body(head, args):
   has_body_and_limits = len(args) >= 2

   if not has_body_and_limits:
      raise UnsupportedMathJSON(f"{head} expects a body and at least one limit")

   return to_sympy(args[0])


def _limits(nodes):
   limits = []

   for node in nodes:
      is_tuple = isinstance(node, list) and len(node) >= 2 and node[0] in _SEQUENCE_HEADS

      if is_tuple:
         limits.append(tuple(to_sympy(part) for part in node[1:]))
      else:
         limits.append(to_sympy(node))

   return limits


def _limit(args):
   has_direction = len(args) == 4
   has_no_direction = len(args) == 3

   if not has_direction and not has_no_direction:
      raise UnsupportedMathJSON("Limit expects a body, a variable, a point and an optional direction")

   direction = args[3] if has_direction else "+"
   is_direction = direction in ("+", "-", "+-")

   if not is_direction:
      raise UnsupportedMathJSON(f"Limit direction {direction!r} is not +, - or +-")

   return sympy.Limit(to_sympy(args[0]), to_sympy(args[1]), to_sympy(args[2]), dir=direction)


def _subs(args):
   has_three_terms = len(args) == 3

   if not has_three_terms:
      raise UnsupportedMathJSON("Subs expects a body, the variables and the points")

   body, variables, points = args

   return sympy.Subs(to_sympy(body), tuple(_limits([variables])[0]), tuple(_limits([points])[0]))


def _apply(args):
   has_name = len(args) >= 1 and isinstance(args[0], str)

   if not has_name:
      raise UnsupportedMathJSON("Apply expects a function name and its arguments")

   return sympy.Function(args[0])(*[to_sympy(arg) for arg in args[1:]])


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
   sympy.log: "Ln",
   sympy.Abs: "Abs",
   sympy.factorial: "Factorial",
}

_RELATION_HEADS = {
   sympy.Equality: "Equal",
   sympy.Unequality: "NotEqual",
   sympy.StrictGreaterThan: "Greater",
   sympy.GreaterThan: "GreaterEqual",
   sympy.StrictLessThan: "Less",
   sympy.LessThan: "LessEqual",
}


def _constant_name(expression):
   for name, value in _CONSTANTS.items():
      if expression is value:
         return name

   return None


def from_sympy(expression):
   """MathJSON for a SymPy expression over the heads to_sympy reads, structure kept as SymPy
   holds it, so to_sympy(from_sympy(e)) == e. A class outside those heads raises."""
   if isinstance(expression, bool):
      return "True" if expression else "False"

   expression = sympy.sympify(expression)
   constant = _constant_name(expression)

   if constant is not None:
      return constant

   if expression.is_Integer:
      return int(expression)

   if expression.is_Rational:
      return ["Rational", int(expression.p), int(expression.q)]

   if expression.is_Float:
      return float(expression)

   if expression.is_Symbol:
      return expression.name

   if expression.is_Add:
      return ["Add", *[from_sympy(term) for term in expression.args]]

   if expression.is_Mul:
      return ["Multiply", *[from_sympy(factor) for factor in expression.args]]

   if expression.is_Pow:
      return ["Power", from_sympy(expression.base), from_sympy(expression.exp)]

   return _from_structured(expression)


def _from_structured(expression):
   relation = _RELATION_HEADS.get(type(expression))

   if relation is not None:
      return [relation, from_sympy(expression.lhs), from_sympy(expression.rhs)]

   if isinstance(expression, sympy.Tuple):
      return ["Tuple", *[from_sympy(part) for part in expression.args]]

   is_empty_set = expression is sympy.S.EmptySet

   if is_empty_set or isinstance(expression, sympy.FiniteSet):
      return ["Set", *[from_sympy(part) for part in expression.args]]

   if isinstance(expression, sympy.Interval):
      return _from_interval(expression)

   if isinstance(expression, sympy.Union):
      return ["Union", *[from_sympy(part) for part in expression.args]]

   if isinstance(expression, sympy.Complement):
      return ["SetMinus", from_sympy(expression.args[0]), from_sympy(expression.args[1])]

   return _from_operator(expression)


def _from_interval(expression):
   low = from_sympy(expression.start)
   high = from_sympy(expression.end)

   if expression.left_open:
      low = ["Open", low]

   if expression.right_open:
      high = ["Open", high]

   return ["Interval", low, high]


def _from_limits(limits):
   return [["Tuple", *[from_sympy(part) for part in limit]] for limit in limits]


def _from_operator(expression):
   if isinstance(expression, sympy.Integral):
      return ["Integrate", from_sympy(expression.function), *_from_limits(expression.limits)]

   if isinstance(expression, sympy.Sum):
      return ["Sum", from_sympy(expression.function), *_from_limits(expression.limits)]

   if isinstance(expression, sympy.Derivative):
      return ["D", from_sympy(expression.expr), *_from_limits(expression.variable_count)]

   if isinstance(expression, sympy.Limit):
      body, variable, point, direction = expression.args

      return ["Limit", from_sympy(body), from_sympy(variable), from_sympy(point), str(direction)]

   if isinstance(expression, sympy.Subs):
      body, variables, points = expression.args

      return ["Subs", from_sympy(body), from_sympy(variables), from_sympy(points)]

   is_named_function = isinstance(expression, sympy.core.function.AppliedUndef)

   if is_named_function:
      return ["Apply", expression.func.__name__, *[from_sympy(arg) for arg in expression.args]]

   head = _FUNCTION_HEADS.get(expression.func)
   has_one_argument = head is not None and len(expression.args) == 1

   if has_one_argument:
      return [head, from_sympy(expression.args[0])]

   raise UnsupportedMathJSON(f"no MathJSON head for {type(expression).__name__}")
