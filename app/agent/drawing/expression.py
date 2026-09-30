"""The expression grammar of the figure language, a Python twin of app/web/src/lessons/expression.ts
(docs/agent/drawing-design.md, The compiler).

The tokenizer and the recursive-descent parser read the same tokens with the same precedence and
the same implicit multiplication as the web grammar: ^ and ** are one operator, a number or a
closing bracket or a one-letter variable followed by a name or an opening bracket multiplies by
juxtaposition, and two names side by side do not. The differences are all refusals. A figure
names its variables per use (x for a curve, t for a parametric path, theta for a polar curve, n
for a sequence, x and y for a slope field), so any other name refuses instead of reading as NaN;
the function table is the design's (no Abs, sign or oo); only ASCII is read; and a string over 80
characters, 48 tokens or a bracket depth of 10 refuses as oversized.

parse builds a small tree of tuples, and evaluate walks it in floats through math and returns None
wherever the value is undefined or not finite. Nothing here reaches SymPy: a string written by the
model is never handed to a parser that can run code, and a tree written by the model is never built
into SymPy, which expands an integer power such as 9^9^9 in full.
"""
import math
import re

MAX_CHARACTERS = 80
MAX_TOKENS = 48
MAX_DEPTH = 10

MALFORMED = "malformed"
OVERSIZED = "oversized"

NUMBER = r"(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?"
NAME = r"[A-Za-z_][A-Za-z0-9_]*"
OPERATORS = "+-*/^()"
REAL_ROOT_DENOMINATORS = (3, 5, 7, 9)
RATIONAL_EXPONENT_TOLERANCE = 1e-9


def _secant(value):
   return 1 / math.cos(value)


def _cosecant(value):
   return 1 / math.sin(value)


def _cotangent(value):
   return 1 / math.tan(value)


FUNCTIONS = {
   "sqrt": math.sqrt,
   "exp": math.exp,
   "ln": math.log,
   "log": math.log,
   "sin": math.sin,
   "cos": math.cos,
   "tan": math.tan,
   "sec": _secant,
   "csc": _cosecant,
   "cot": _cotangent,
   "asin": math.asin,
   "acos": math.acos,
   "atan": math.atan,
   "sinh": math.sinh,
   "cosh": math.cosh,
   "tanh": math.tanh,
   "abs": math.fabs,
}

CONSTANTS = {
   "pi": math.pi,
   "e": math.e,
}


class ExpressionRefused(ValueError):
   """An expression the grammar will not read; reason is malformed or oversized."""

   def __init__(self, reason):
      super().__init__(reason)
      self.reason = reason


def _tokens(text):
   tokens = []
   rest = text.strip()

   while rest:
      number = re.match(NUMBER, rest)
      name = re.match(NAME, rest)

      if number is not None:
         tokens.append(("number", float(number.group(0))))
         rest = rest[number.end():]
      elif name is not None:
         tokens.append(("name", name.group(0)))
         rest = rest[name.end():]
      elif rest.startswith("**"):
         tokens.append(("op", "**"))
         rest = rest[2:]
      elif rest[0] in OPERATORS:
         operator = "**" if rest[0] == "^" else rest[0]
         tokens.append(("op", operator))
         rest = rest[1:]
      else:
         return None

      rest = rest.lstrip()

   return tokens


def _bracket_depth(tokens):
   depth = 0
   deepest = 0

   for kind, value in tokens:
      is_opener = kind == "op" and value == "("
      is_closer = kind == "op" and value == ")"

      if is_opener:
         depth += 1
         deepest = max(deepest, depth)
      elif is_closer:
         depth -= 1

   return deepest


class _Parser:
   def __init__(self, tokens, variables):
      self.tokens = tokens
      self.variables = variables
      self.position = 0

   def parse(self):
      tree = self._sum()
      is_finished = self.position == len(self.tokens)
      is_complete = tree is not None and is_finished

      return tree if is_complete else None

   def _peek(self):
      has_token = self.position < len(self.tokens)

      return self.tokens[self.position] if has_token else None

   def _is_op(self, value):
      return self._peek() == ("op", value)

   def _sum(self):
      left = self._product()

      while left is not None:
         is_plus = self._is_op("+")
         continues_sum = is_plus or self._is_op("-")

         if not continues_sum:
            break

         operation = "add" if is_plus else "subtract"
         self.position += 1
         right = self._product()

         if right is None:
            return None

         left = (operation, left, right)

      return left

   def _starts_implicit_factor(self, previous):
      following = self._peek()
      is_at_an_end = previous is None or following is None

      if is_at_an_end:
         return False

      previous_kind, previous_value = previous
      following_kind, following_value = following
      previous_ends_value = previous_kind in ("number", "name") or previous == ("op", ")")
      following_starts_value = following_kind == "name" or following == ("op", "(")
      is_name_after_name = previous_kind == "name" and following_kind == "name"
      is_call_after_name = previous_kind == "name" and following == ("op", "(") and len(previous_value) > 1

      return previous_ends_value and following_starts_value and not is_name_after_name and not is_call_after_name

   def _product(self):
      left = self._unary()

      while left is not None:
         previous = self.tokens[self.position - 1] if self.position > 0 else None
         is_explicit = self._is_op("*") or self._is_op("/")

         if is_explicit:
            operation = "multiply" if self._is_op("*") else "divide"
            self.position += 1
            right = self._unary()

            if right is None:
               return None

            left = (operation, left, right)
         elif self._starts_implicit_factor(previous):
            right = self._power()

            if right is None:
               return None

            left = ("multiply", left, right)
         else:
            break

      return left

   def _unary(self):
      if self._is_op("-"):
         self.position += 1
         operand = self._unary()

         return None if operand is None else ("negate", operand)

      if self._is_op("+"):
         self.position += 1

         return self._unary()

      return self._power()

   def _power(self):
      base = self._atom()

      if base is None:
         return None

      if self._is_op("**"):
         self.position += 1
         exponent = self._unary()

         return None if exponent is None else ("power", base, exponent)

      return base

   def _atom(self):
      token = self._peek()

      if token is None:
         return None

      self.position += 1
      kind, value = token

      if kind == "number":
         return ("number", value)

      if token == ("op", "("):
         inner = self._sum()
         is_closed = inner is not None and self._is_op(")")

         if not is_closed:
            return None

         self.position += 1

         return inner

      if kind != "name":
         return None

      is_call = self._is_op("(") and len(value) > 1

      if is_call:
         if value not in FUNCTIONS:
            return None

         self.position += 1
         argument = self._sum()
         is_closed = argument is not None and self._is_op(")")

         if not is_closed:
            return None

         self.position += 1

         return ("call", value, argument)

      if value in FUNCTIONS:
         return None

      if value in self.variables:
         return ("variable", value)

      if value in CONSTANTS:
         return ("constant", value)

      return None


def parse(text, variables=("x",)):
   """The tree of an expression in the named variables, or ExpressionRefused."""
   is_text = isinstance(text, str)

   if not is_text:
      raise ExpressionRefused(MALFORMED)

   if len(text) > MAX_CHARACTERS:
      raise ExpressionRefused(OVERSIZED)

   if not text.isascii():
      raise ExpressionRefused(MALFORMED)

   tokens = _tokens(text)

   if not tokens:
      raise ExpressionRefused(MALFORMED)

   is_too_long = len(tokens) > MAX_TOKENS
   is_too_deep = _bracket_depth(tokens) > MAX_DEPTH

   if is_too_long or is_too_deep:
      raise ExpressionRefused(OVERSIZED)

   has_infinite_literal = any(kind == "number" and not math.isfinite(value) for kind, value in tokens)

   if has_infinite_literal:
      raise ExpressionRefused(MALFORMED)

   tree = _Parser(tokens, frozenset(variables)).parse()

   if tree is None:
      raise ExpressionRefused(MALFORMED)

   return tree


def variables_of(tree):
   kind = tree[0]

   if kind == "variable":
      return {tree[1]}

   if kind in ("number", "constant"):
      return set()

   if kind == "call":
      return variables_of(tree[2])

   if kind == "negate":
      return variables_of(tree[1])

   return variables_of(tree[1]) | variables_of(tree[2])


def _real_power(base, exponent):
   """SymPy's real root, as the web grammar takes it: a negative base under a rational power with
   an odd denominator, such as (-8)^(1/3), has a real value where math.pow refuses."""
   try:
      return math.pow(base, exponent)
   except ValueError:
      if base >= 0:
         raise

   for denominator in REAL_ROOT_DENOMINATORS:
      numerator = exponent * denominator
      is_rational = abs(numerator - round(numerator)) < RATIONAL_EXPONENT_TOLERANCE

      if is_rational:
         magnitude = math.pow(-base, exponent)
         is_odd_numerator = abs(round(numerator)) % 2 == 1

         return -magnitude if is_odd_numerator else magnitude

   raise ValueError("no real power")


def _value(tree, scope):
   kind = tree[0]

   if kind == "number":
      return tree[1]

   if kind == "variable":
      return float(scope[tree[1]])

   if kind == "constant":
      return CONSTANTS[tree[1]]

   if kind == "negate":
      return -_value(tree[1], scope)

   if kind == "call":
      return FUNCTIONS[tree[1]](_value(tree[2], scope))

   left = _value(tree[1], scope)
   right = _value(tree[2], scope)

   if kind == "add":
      return left + right

   if kind == "subtract":
      return left - right

   if kind == "multiply":
      return left * right

   if kind == "divide":
      return left / right

   return _real_power(left, right)


def evaluate(tree, scope):
   """The float value of the tree with the variables in scope, or None where it is undefined."""
   try:
      value = _value(tree, scope)
   except (ArithmeticError, ValueError, KeyError):
      return None

   is_finite = isinstance(value, float) and math.isfinite(value)

   return value if is_finite else None
