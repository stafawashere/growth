"""Evaluate the predicate and expression strings a parameter spec carries.

A spec is registry data, so its strings are read by walking the Python syntax tree against an
allow-list rather than handed to eval or sympify. Numbers become SymPy numbers, so arithmetic on
a draw stays exact.
"""
import ast
import math
import re

import sympy


class SpecExpressionError(ValueError):
   pass


FORM_ALLOWED = re.compile(r"^[A-Za-z0-9_+\-*/^(),.\s]+$")
IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

FORM_FUNCTIONS = {
   "sin": sympy.sin,
   "cos": sympy.cos,
   "tan": sympy.tan,
   "sec": sympy.sec,
   "csc": sympy.csc,
   "cot": sympy.cot,
   "asin": sympy.asin,
   "acos": sympy.acos,
   "atan": sympy.atan,
   "exp": sympy.exp,
   "log": sympy.log,
   "ln": sympy.log,
   "sqrt": sympy.sqrt,
   "Abs": sympy.Abs,
   "pi": sympy.pi,
   "E": sympy.E,
   "Rational": sympy.Rational,
}

FORM_SYMBOLS = {name: sympy.Symbol(name) for name in ("x", "t", "y", "n", "k", "theta")}


def _is_exact(value):
   is_sympy = isinstance(value, sympy.Basic)

   if not is_sympy:
      return isinstance(value, (int, bool))

   has_float = value.has(sympy.Float)
   has_unevaluated = value.has(sympy.Integral, sympy.Limit, sympy.Sum, sympy.RootOf, sympy.Derivative)

   return not has_float and not has_unevaluated


def _is_finite(value):
   try:
      number = complex(sympy.N(value))
   except (TypeError, ValueError):
      return False

   is_real = abs(number.imag) < 1e-12

   return is_real and math.isfinite(number.real)


def _strictly_increasing(values):
   return all(values[index] < values[index + 1] for index in range(len(values) - 1))


def _distinct(values):
   return len(set(values)) == len(values)


def _differences(values):
   return [values[index + 1] - values[index] for index in range(len(values) - 1)]


def _decimal_places_nondegenerate(value):
   """A three-decimal answer is degenerate when it rounds to a whole number or to zero."""
   number = float(sympy.N(value))
   rounded = round(number, 3)
   is_zero = rounded == 0
   is_whole = rounded == round(rounded)

   return not is_zero and not is_whole


FUNCTIONS = {
   "abs": lambda value: abs(value),
   "min": min,
   "max": max,
   "len": len,
   "all": all,
   "any": any,
   "sum": lambda values: sum(values, sympy.Integer(0)),
   "gcd": lambda left, right: sympy.gcd(left, right),
   "is_integer": lambda value: sympy.sympify(value).is_integer is True,
   "is_square": lambda value: sympy.sqrt(sympy.sympify(value)).is_integer is True,
   "numerator": lambda value: sympy.fraction(sympy.nsimplify(value))[0],
   "denominator": lambda value: sympy.fraction(sympy.nsimplify(value))[1],
   "strictly_increasing": _strictly_increasing,
   "distinct": _distinct,
   "differences": _differences,
   "exact": _is_exact,
   "finite": _is_finite,
   "nondegenerate_three_decimals": _decimal_places_nondegenerate,
   "sqrt": sympy.sqrt,
   "Rational": sympy.Rational,
}

ALLOWED_NODES = (
   ast.Expression, ast.BoolOp, ast.And, ast.Or, ast.UnaryOp, ast.Not, ast.USub, ast.UAdd,
   ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv,
   ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.In, ast.NotIn,
   ast.IfExp, ast.Call, ast.Name, ast.Load, ast.Constant, ast.List, ast.Tuple, ast.Subscript,
   ast.Slice,
)


def _number(value):
   is_bool = isinstance(value, bool)

   if is_bool:
      return value

   if isinstance(value, int):
      return sympy.Integer(value)

   if isinstance(value, float):
      return sympy.Rational(str(value))

   return value


def _check_tree(tree, text):
   for node in ast.walk(tree):
      is_allowed = isinstance(node, ALLOWED_NODES)

      if not is_allowed:
         raise SpecExpressionError(f"{type(node).__name__} is not allowed in {text!r}")

      is_call = isinstance(node, ast.Call)
      calls_by_name = is_call and isinstance(node.func, ast.Name)

      if is_call and not calls_by_name:
         raise SpecExpressionError(f"only named functions may be called in {text!r}")


def _evaluate(node, names):
   if isinstance(node, ast.Expression):
      return _evaluate(node.body, names)

   if isinstance(node, ast.Constant):
      return _number(node.value)

   if isinstance(node, ast.Name):
      if node.id in names:
         return names[node.id]

      if node.id in ("True", "False"):
         return node.id == "True"

      raise SpecExpressionError(f"unknown name {node.id!r}")

   if isinstance(node, (ast.List, ast.Tuple)):
      return [_evaluate(element, names) for element in node.elts]

   if isinstance(node, ast.Subscript):
      container = _evaluate(node.value, names)

      if isinstance(node.slice, ast.Slice):
         lower = None if node.slice.lower is None else int(_evaluate(node.slice.lower, names))
         upper = None if node.slice.upper is None else int(_evaluate(node.slice.upper, names))

         return container[lower:upper]

      return container[int(_evaluate(node.slice, names))]

   if isinstance(node, ast.UnaryOp):
      operand = _evaluate(node.operand, names)

      if isinstance(node.op, ast.Not):
         return not operand

      if isinstance(node.op, ast.USub):
         return -operand

      return operand

   if isinstance(node, ast.BinOp):
      return _binary(node, names)

   if isinstance(node, ast.BoolOp):
      return _boolean(node, names)

   if isinstance(node, ast.Compare):
      return _compare(node, names)

   if isinstance(node, ast.IfExp):
      chosen = node.body if _evaluate(node.test, names) else node.orelse
      return _evaluate(chosen, names)

   if isinstance(node, ast.Call):
      return _call(node, names)

   raise SpecExpressionError(f"cannot evaluate {type(node).__name__}")


def _binary(node, names):
   left = _evaluate(node.left, names)
   right = _evaluate(node.right, names)
   operator = node.op

   if isinstance(operator, ast.Add):
      return left + right

   if isinstance(operator, ast.Sub):
      return left - right

   if isinstance(operator, ast.Mult):
      return left * right

   if isinstance(operator, ast.Div):
      return sympy.Rational(left, right) if _both_integers(left, right) else left / right

   if isinstance(operator, ast.Pow):
      return left ** right

   if isinstance(operator, ast.Mod):
      return left % right

   return left // right


def _both_integers(left, right):
   left_is_integer = isinstance(left, (int, sympy.Integer))
   right_is_integer = isinstance(right, (int, sympy.Integer))

   return left_is_integer and right_is_integer


def _boolean(node, names):
   is_and = isinstance(node.op, ast.And)

   if is_and:
      return all(bool(_evaluate(value, names)) for value in node.values)

   return any(bool(_evaluate(value, names)) for value in node.values)


def _compare(node, names):
   left = _evaluate(node.left, names)

   for operator, right_node in zip(node.ops, node.comparators):
      right = _evaluate(right_node, names)
      holds = _compare_pair(operator, left, right)

      if not holds:
         return False

      left = right

   return True


def _compare_pair(operator, left, right):
   if isinstance(operator, ast.Eq):
      return bool(sympy.simplify(sympy.sympify(left) - sympy.sympify(right)) == 0) if _is_symbolic(left, right) else left == right

   if isinstance(operator, ast.NotEq):
      return not _compare_pair(ast.Eq(), left, right)

   if isinstance(operator, ast.In):
      return left in right

   if isinstance(operator, ast.NotIn):
      return left not in right

   if isinstance(operator, ast.Lt):
      return bool(left < right)

   if isinstance(operator, ast.LtE):
      return bool(left <= right)

   if isinstance(operator, ast.Gt):
      return bool(left > right)

   return bool(left >= right)


def _is_symbolic(left, right):
   left_is_expression = isinstance(left, sympy.Basic)
   right_is_expression = isinstance(right, sympy.Basic)
   neither_is_text = not isinstance(left, str) and not isinstance(right, str)

   return (left_is_expression or right_is_expression) and neither_is_text


def _call(node, names):
   function_name = node.func.id
   is_known = function_name in FUNCTIONS or function_name == "form"

   if not is_known:
      raise SpecExpressionError(f"function {function_name!r} is not allowed")

   arguments = [_evaluate(argument, names) for argument in node.args]

   if function_name == "form":
      return parse_form(arguments[0], names)

   return FUNCTIONS[function_name](*arguments)


def evaluate(text, names):
   """Evaluate one spec string against a mapping of names to values."""
   try:
      tree = ast.parse(text, mode="eval")
   except SyntaxError as unreadable:
      raise SpecExpressionError(f"cannot parse {text!r}") from unreadable

   _check_tree(tree, text)

   return _evaluate(tree, names)


def parse_form(text, names):
   """A function_form string such as "a*x**2 + b", with its parameters substituted from names."""
   is_allowed = isinstance(text, str) and FORM_ALLOWED.match(text) is not None

   if not is_allowed:
      raise SpecExpressionError(f"function form {text!r} has characters outside the allow-list")

   local = dict(FORM_FUNCTIONS)
   local.update(FORM_SYMBOLS)

   for name, value in names.items():
      is_substitutable = isinstance(value, (sympy.Basic, int)) and not isinstance(value, bool)

      if is_substitutable:
         local[name] = sympy.sympify(value)

   unknown_identifiers = [
      identifier for identifier in IDENTIFIER.findall(text) if identifier not in local
   ]

   if unknown_identifiers:
      raise SpecExpressionError(f"function form {text!r} names {unknown_identifiers}")

   try:
      parsed = sympy.parse_expr(text.replace("^", "**"), local_dict=local, evaluate=True)
   except Exception as unreadable:
      raise SpecExpressionError(f"cannot parse function form {text!r}") from unreadable

   return parsed
