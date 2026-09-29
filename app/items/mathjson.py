"""MathLive MathJSON to SymPy conversion (https://cortexjs.io/math-json/).

Covers the forms P1 items need: numbers, symbols, the arithmetic and
transcendental function heads, Factorial, and the two constant symbols Pi and
ExponentialE. Lesson records add sets (Set, Interval with Open endpoints, Union,
SetMinus), List and Tuple, the relations, the infinities and NaN, and the calculus
operators Integrate, D, Limit, Sum and Subs with Apply for a named function, because the
lesson designs state keys and steps in them (docs/lessons/BUILD-PLAN.md, The design to
record path). The web client's MathLive field adds what the Compute Engine 0.24 canonical form
emits for typed answers: Square, Half, Delimiter around a group or a parenthesised pair, the
{"num": ...} object for infinities and NaN, one-argument Log as base 10, the hyperbolic and
remaining inverse trig heads, Floor, Ceil, Sign, Min, Max and an InverseFunction applied to a
trig head. Anything else raises UnsupportedMathJSON rather than guessing.

from_sympy is the inverse over the same heads, which tools/lesson_transcribe.py uses.
"""
import re

import sympy


class UnsupportedMathJSON(ValueError):
   pass


_UNARY_FUNCTIONS = {
   "Negate": lambda a: -a,
   "Square": lambda a: a ** 2,
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
   "Arcsec": sympy.asec,
   "Arccsc": sympy.acsc,
   "Arccot": sympy.acot,
   "Sinh": sympy.sinh,
   "Cosh": sympy.cosh,
   "Tanh": sympy.tanh,
   "Coth": sympy.coth,
   "Sech": sympy.sech,
   "Csch": sympy.csch,
   "Arsinh": sympy.asinh,
   "Arcosh": sympy.acosh,
   "Artanh": sympy.atanh,
   "Arcoth": sympy.acoth,
   "Arsech": sympy.asech,
   "Arcsech": sympy.asech,
   "Arcsch": sympy.acsch,
   "Abs": sympy.Abs,
   "Factorial": sympy.factorial,
   "Floor": sympy.floor,
   "Ceil": sympy.ceiling,
   "Sign": sympy.sign,
}

# The Compute Engine parses \sin^{-1} straight to Arcsin but leaves \cot^{-1} as
# ["Apply", ["InverseFunction", "Cot"], x].
_INVERSE_FUNCTIONS = {
   "Sin": sympy.asin,
   "Cos": sympy.acos,
   "Tan": sympy.atan,
   "Sec": sympy.asec,
   "Csc": sympy.acsc,
   "Cot": sympy.acot,
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
   "ImaginaryUnit": sympy.I,
}

# Read but never written, so from_sympy keeps Rational(1, 2) and the empty Set.
_READ_ONLY_SYMBOLS = {
   "Half": sympy.Rational(1, 2),
   "EmptySet": sympy.S.EmptySet,
}

_NUMBER_OBJECT_VALUES = {
   "+Infinity": sympy.oo,
   "-Infinity": -sympy.oo,
   "NaN": sympy.nan,
}

_PLAIN_DECIMAL = re.compile(r"-?\d+(\.\d+)?([eE][-+]?\d+)?")

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

   if isinstance(expr, dict):
      return _number_object(expr)

   raise UnsupportedMathJSON(f"unsupported MathJSON node: {expr!r}")


def _symbol_or_constant(name):
   is_constant = name in _CONSTANTS

   if is_constant:
      return _CONSTANTS[name]

   is_read_only = name in _READ_ONLY_SYMBOLS

   if is_read_only:
      return _READ_ONLY_SYMBOLS[name]

   return sympy.Symbol(name)


def _number_object(expr):
   value = expr.get("num")
   has_only_num = set(expr) == {"num"} and isinstance(value, str)

   if not has_only_num:
      raise UnsupportedMathJSON(f"unsupported MathJSON number object: {expr!r}")

   is_named_value = value in _NUMBER_OBJECT_VALUES

   if is_named_value:
      return _NUMBER_OBJECT_VALUES[value]

   is_plain_decimal = _PLAIN_DECIMAL.fullmatch(value) is not None

   if is_plain_decimal:
      return sympy.Rational(value)

   raise UnsupportedMathJSON(f"unsupported MathJSON number object: {expr!r}")


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

   # The Compute Engine reads ["Log", x] as base 10 and writes \log_{10} x that way too.
   if has_one_argument:
      return sympy.log(to_sympy(args[0]), 10)

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

   if head == "Min":
      return sympy.Min(*_at_least_one(head, args))

   if head == "Max":
      return sympy.Max(*_at_least_one(head, args))

   if head == "Delimiter":
      return _delimiter(args)

   return None


def _at_least_one(head, args):
   has_arguments = len(args) >= 1

   if not has_arguments:
      raise UnsupportedMathJSON(f"{head} expects at least one argument")

   return [to_sympy(arg) for arg in args]


def _delimiter(args):
   has_body = len(args) in (1, 2)

   if not has_body:
      raise UnsupportedMathJSON("Delimiter expects a body and an optional delimiter string")

   body = args[0]
   delimiters = args[1] if len(args) == 2 else "'(,)'"
   is_parentheses = delimiters == "'(,)'"

   if not is_parentheses:
      raise UnsupportedMathJSON(f"Delimiter {delimiters!r} is not parentheses")

   is_sequence = isinstance(body, list) and len(body) >= 1 and body[0] == "Sequence"

   if not is_sequence:
      return to_sympy(body)

   members = body[1:]

   if len(members) == 0:
      raise UnsupportedMathJSON("Delimiter around an empty Sequence")

   if len(members) == 1:
      return to_sympy(members[0])

   return sympy.Tuple(*[to_sympy(member) for member in members])


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
   has_function = len(args) >= 1
   inverse = _inverse_function(args[0]) if has_function else None

   if inverse is not None:
      return _unary_inverse(inverse, args[1:])

   has_name = has_function and isinstance(args[0], str)

   if not has_name:
      raise UnsupportedMathJSON("Apply expects a function name and its arguments")

   return sympy.Function(args[0])(*[to_sympy(arg) for arg in args[1:]])


def _inverse_function(node):
   is_inverse_node = isinstance(node, list) and len(node) == 2 and node[0] == "InverseFunction"

   if not is_inverse_node:
      return None

   inverse = _INVERSE_FUNCTIONS.get(node[1]) if isinstance(node[1], str) else None

   if inverse is None:
      raise UnsupportedMathJSON(f"no inverse known for {node[1]!r}")

   return inverse


def _unary_inverse(inverse, args):
   has_one_argument = len(args) == 1

   if not has_one_argument:
      raise UnsupportedMathJSON("an inverse function expects exactly one argument")

   return inverse(to_sympy(args[0]))


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
   sympy.asec: "Arcsec",
   sympy.acsc: "Arccsc",
   sympy.acot: "Arccot",
   sympy.sinh: "Sinh",
   sympy.cosh: "Cosh",
   sympy.tanh: "Tanh",
   sympy.coth: "Coth",
   sympy.sech: "Sech",
   sympy.csch: "Csch",
   sympy.asinh: "Arsinh",
   sympy.acosh: "Arcosh",
   sympy.atanh: "Artanh",
   sympy.acoth: "Arcoth",
   sympy.asech: "Arsech",
   sympy.acsch: "Arcsch",
   sympy.floor: "Floor",
   sympy.ceiling: "Ceil",
   sympy.sign: "Sign",
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

   if isinstance(expression, sympy.Min):
      return ["Min", *[from_sympy(arg) for arg in expression.args]]

   if isinstance(expression, sympy.Max):
      return ["Max", *[from_sympy(arg) for arg in expression.args]]

   is_named_function = isinstance(expression, sympy.core.function.AppliedUndef)

   if is_named_function:
      return ["Apply", expression.func.__name__, *[from_sympy(arg) for arg in expression.args]]

   head = _FUNCTION_HEADS.get(expression.func)
   has_one_argument = head is not None and len(expression.args) == 1

   if has_one_argument:
      return [head, from_sympy(expression.args[0])]

   raise UnsupportedMathJSON(f"no MathJSON head for {type(expression).__name__}")
