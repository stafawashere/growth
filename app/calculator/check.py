"""The two checks a drill answer gets (docs/calculator/architecture.md, The three-decimal check
and The setup check). Both are pure: they read the entry and the task and write nothing.
"""
import math as pymath
import re
from dataclasses import dataclass
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal

import sympy
from sympy.core.function import AppliedUndef

from app.calculator.kit import EQUATION, THREE_PLACES, rounded_and_truncated, setup_latex
from app.items import verify
from app.items.mathjson import UnsupportedMathJSON, to_sympy

DECIMAL_ENTRY = re.compile(r"-?(\d+(\.\d*)?|\.\d+)")
IGNORED_CHARACTERS = re.compile(r"[,\s]")
EMPTY_ENTRIES = ("", "Nothing")
SETTLE_TIMEOUT_S = verify.COMPARISON_TIMEOUT_S
SAMPLE_POINTS = (0.731, 1.379, 2.113, 0.417, 2.861, 1.618, 0.203)
NONZERO_FLOOR = 1e-9


@dataclass(frozen=True)
class ValueVerdict:
   correct: bool
   reason: str | None
   rounded: str
   truncated: str


@dataclass(frozen=True)
class SetupVerdict:
   shown: bool
   correct: bool | None
   reason: str | None
   key_latex: str


def check_value(entered, key):
   rounded, truncated = rounded_and_truncated(key)
   accepted = {Decimal(rounded), Decimal(truncated)}
   text = IGNORED_CHARACTERS.sub("", entered or "")

   def verdict(correct, reason=None):
      return ValueVerdict(correct=correct, reason=reason, rounded=rounded, truncated=truncated)

   if text == "":
      return verdict(False, "missing")

   is_decimal = DECIMAL_ENTRY.fullmatch(text) is not None

   if not is_decimal:
      return verdict(False, "not_a_number")

   value = Decimal(text)
   places = len(text.partition(".")[2])
   three_place_forms = {
      value.quantize(THREE_PLACES, rounding=ROUND_HALF_UP),
      value.quantize(THREE_PLACES, rounding=ROUND_DOWN),
   }

   if three_place_forms & accepted:
      return verdict(True)

   is_short = places < 3
   agrees_when_shortened = is_short and value in _shortened(accepted, places)

   if agrees_when_shortened:
      return verdict(False, "not_three_places")

   return verdict(False, "outside_tolerance")


def _shortened(accepted, places):
   step = Decimal(1).scaleb(-places)
   forms = set()

   for form in accepted:
      forms.add(form.quantize(step, rounding=ROUND_HALF_UP))
      forms.add(form.quantize(step, rounding=ROUND_DOWN))

   return forms


def check_setup(entered_mathjson, task):
   key = to_sympy(task.setup_key)
   key_latex = setup_latex(key)

   def verdict(correct, reason=None, shown=True):
      return SetupVerdict(shown=shown, correct=correct, reason=reason, key_latex=key_latex)

   is_missing = _is_empty(entered_mathjson)

   if is_missing:
      return verdict(None, "missing", shown=False)

   if _is_copied_answer(entered_mathjson):
      return verdict(False, "not_equivalent")

   functions = task.draw.get("functions") or {}

   try:
      entered = to_sympy(_applied(entered_mathjson, functions))
      entered = _with_functions(entered, functions)
   except (UnsupportedMathJSON, TypeError, sympy.SympifyError):
      return verdict(None, "unsupported")

   if task.setup_kind == EQUATION:
      outcome = _equation_outcome(entered, key)
   else:
      outcome = _expression_outcome(entered, key)

   if outcome == "equivalent":
      return verdict(True)

   if outcome == "not_equivalent":
      return verdict(False, "not_equivalent")

   return verdict(None, "unsettled")


def _is_empty(entered):
   if entered is None:
      return True

   is_empty_text = isinstance(entered, str) and entered.strip() in EMPTY_ENTRIES
   is_empty_list = isinstance(entered, list) and len(entered) == 0
   is_empty_sequence = isinstance(entered, list) and entered in (["Sequence"], ["Nothing"])

   return is_empty_text or is_empty_list or is_empty_sequence


def _is_bare_number(node):
   is_plain_number = isinstance(node, (int, float)) and not isinstance(node, bool)
   is_number_object = isinstance(node, dict) and "num" in node
   is_negated = isinstance(node, list) and len(node) == 2 and node[0] == "Negate"

   if is_negated:
      return _is_bare_number(node[1])

   return is_plain_number or is_number_object


def _is_copied_answer(node):
   """A number where a setup belongs: the whole entry, or an equation such as x = 1.681 whose
   sides carry no function or operator, which is the answer written in place of the work."""
   if _is_bare_number(node):
      return True

   is_equation = isinstance(node, list) and len(node) == 3 and node[0] == "Equal"

   if not is_equation:
      return False

   sides = node[1:]
   has_no_structure = all(_is_bare_number(side) or isinstance(side, str) for side in sides)
   has_number_side = any(_is_bare_number(side) for side in sides)

   return has_no_structure and has_number_side


def _applied(node, functions):
   """MathJSON with every function the task names written as Apply, since the math field writes
   f(x) as ["f", "x"], a head to_sympy does not know. Compute Engine does not know the task's
   names as functions either, so it reads f(0.31) as ["Multiply", "f", 0.31] and P'(4.5) as
   ["Multiply", ["Prime", "P"], 4.5], and wraps f'(x) = 0 as an Error for being no pure
   expression; each of those is read back as the call it was typed as."""
   if not isinstance(node, list) or len(node) == 0:
      return node

   head = node[0]
   prime = _prime_of_task_function(node, functions)

   if prime is not None:
      return _derivative_function(*prime, functions)

   if _is_impure_task_call(node, functions):
      return _applied(node[2], functions)

   arguments = [_applied(argument, functions) for argument in node[1:]]
   names_task_function = isinstance(head, str) and head in functions

   if names_task_function:
      return ["Apply", head, *arguments]

   applies_prime = head == "Apply" and len(node) == 3 and _prime_of_task_function(node[1], functions) is not None

   if applies_prime:
      return _derivative_at(*_prime_of_task_function(node[1], functions), arguments[1], functions)

   if head == "Multiply":
      return ["Multiply", *_calls_in_product(node[1:], arguments, functions)]

   return [head, *arguments]


def _prime_of_task_function(node, functions):
   """(name, order) for ["Prime", F], ["Prime", F, n] or ["Prime", ["Prime", F]] with F a
   function the task names, else None."""
   is_prime = isinstance(node, list) and len(node) in (2, 3) and node[0] == "Prime"

   if not is_prime:
      return None

   inner = node[1]
   has_order = len(node) == 3
   order = node[2] if has_order else 1
   is_whole_order = isinstance(order, int) and not isinstance(order, bool) and order >= 1

   if not is_whole_order:
      return None

   names_task_function = isinstance(inner, str) and inner in functions

   if names_task_function:
      return inner, order

   inner_prime = _prime_of_task_function(inner, functions)

   if inner_prime is None:
      return None

   name, inner_order = inner_prime

   return name, inner_order + order


def _derivative_function(name, order, functions):
   entry = functions[name]

   return ["D", entry["expression"], ["Tuple", entry["variable"], order]]


def _derivative_at(name, order, point, functions):
   """f'(x) is the derivative function itself, and not a Subs at x, because sympy leaves
   Subs(Derivative(g, x), x, x) as an unevaluated Derivative after doit."""
   variable = functions[name]["variable"]
   derivative = _derivative_function(name, order, functions)

   if point == variable:
      return derivative

   return ["Subs", derivative, ["Tuple", variable], ["Tuple", point]]


def _is_callable_factor(node, functions):
   names_task_function = isinstance(node, str) and node in functions

   return names_task_function or _prime_of_task_function(node, functions) is not None


def _calls_in_product(factors, rewritten, functions):
   """A product with each task function, or a prime of one, applied to the factor after it."""
   calls = []
   index = 0

   while index < len(factors):
      factor = factors[index]
      has_argument = index + 1 < len(factors)
      is_call = has_argument and _is_callable_factor(factor, functions)

      if not is_call:
         calls.append(rewritten[index])
         index += 1
         continue

      argument = rewritten[index + 1]
      prime = _prime_of_task_function(factor, functions)

      if prime is None:
         calls.append(["Apply", factor, argument])
      else:
         calls.append(_derivative_at(*prime, argument, functions))

      index += 2

   return calls


def _mentions_task_function(node, functions):
   if isinstance(node, str):
      return node in functions

   if not isinstance(node, list):
      return False

   return any(_mentions_task_function(part, functions) for part in node)


def _is_impure_task_call(node, functions):
   is_impure_error = len(node) == 3 and node[0] == "Error" and node[1] == "'expected-pure-expression'"

   return is_impure_error and _mentions_task_function(node[2], functions)


def _with_functions(expression, functions):
   for name, entry in functions.items():
      body = to_sympy(entry["expression"])
      variable = sympy.Symbol(entry["variable"])

      def is_call(node, name=name):
         is_named_call = isinstance(node, AppliedUndef) and node.func.__name__ == name

         return is_named_call and len(node.args) == 1

      def expanded(node, body=body, variable=variable):
         return body.subs(variable, node.args[0])

      expression = expression.replace(is_call, expanded)

   return expression


def _settled(expression):
   """Definite integrals by quadrature, then doit for derivatives and substitutions, so a typed
   integral compares as the number the calculator gives."""
   def is_definite_integral(node):
      return isinstance(node, sympy.Integral) and not node.free_symbols

   expression = expression.replace(is_definite_integral, lambda node: node.evalf(30))

   if hasattr(expression, "doit"):
      expression = expression.doit()

   return expression


def _settled_pair(left, right):
   return _settled(left), _settled(right)


def _bounded_settle(left, right):
   return verify.run_bounded(_settled_pair, (left, right), SETTLE_TIMEOUT_S, None)


def _expression_outcome(entered, key):
   settled = _bounded_settle(entered, key)

   if settled is None:
      return "unsettled"

   return verify.equivalence(*settled)


def _is_relation(expression):
   return isinstance(expression, sympy.Eq)


def _equation_outcome(entered, key):
   if not _is_relation(entered):
      return "not_equivalent"

   settled = _bounded_settle(entered.lhs - entered.rhs, key.lhs - key.rhs)

   if settled is None:
      return "unsettled"

   entered_difference, key_difference = settled
   scale = _scale(entered_difference, key_difference)

   if scale is None:
      return "unsettled"

   if scale == 0:
      return "not_equivalent"

   return verify.equivalence(entered_difference, scale * key_difference)


def _numeric(expression, substitution):
   try:
      value = complex(expression.subs(substitution).evalf())
   except (TypeError, ValueError, sympy.SympifyError):
      return None

   is_finite = pymath.isfinite(value.real) and pymath.isfinite(value.imag)

   return value if is_finite else None


def _scale(entered_difference, key_difference):
   """The constant k with entered = k * key at the first sample point where the key's
   difference is nonzero, or None when no sample point settles it."""
   symbols = entered_difference.free_symbols | key_difference.free_symbols

   for point in SAMPLE_POINTS:
      substitution = {symbol: point for symbol in symbols}
      key_value = _numeric(key_difference, substitution)
      entered_value = _numeric(entered_difference, substitution)
      is_usable = key_value is not None and entered_value is not None and abs(key_value) > NONZERO_FLOOR

      if not is_usable:
         continue

      ratio = entered_value / key_value
      is_real = abs(ratio.imag) <= NONZERO_FLOOR * max(1.0, abs(ratio.real))

      if not is_real:
         return 0

      return sympy.Float(ratio.real, 17)

   return None
