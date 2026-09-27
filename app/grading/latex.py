r"""Reads one line of confirmed student work, written in LaTeX, into SymPy.

The read-back the student confirms is LaTeX, because that is what the transcriber writes and what
MathLive edits. SymPy's LaTeX parser (the lark backend) reads most of it once a few habits of
handwritten calculus are normalised: e is Euler's number, pi is a constant, ln|x| means ln(|x|),
and a line such as f'(x) = 3x^2 - 7 is a claim whose right-hand side is the object a point checks.

Anything the parser cannot read, or reads two ways that disagree, is Unreadable. A deterministic
check that meets an Unreadable line reports unsettled, and 03 sends an unsettled point to the
model path rather than deciding it either way.

A question that names its functions (E(t), L(t), H(t) in the stem) carries their definitions, and a
line written with those names is read by substituting each definition at its argument, so
\int_0^8 E(t)\,dt reads as the integral of E's expression. A prime on a defined name
differentiates it. When a question carries definitions, a capital letter called like a function
that the question does not define is Unreadable, because nothing says what it stands for.
"""
import re
import warnings
from dataclasses import dataclass, field

import sympy

with warnings.catch_warnings():
   warnings.simplefilter("ignore")
   from sympy.parsing.latex import parse_latex

EULER_SYMBOL = sympy.Symbol("e")
PI_STAND_IN = r"\zeta"
PI_SYMBOL = sympy.Symbol("zeta")
AMBIGUOUS_TREE_NAME = "_ambig"

_SPACING = re.compile(r"\\[,;:!]|\\quad|\\qquad|\\displaystyle|\\left|\\right|~")
_ROMAN_E = re.compile(r"\\mathrm\{e\}|\\text\{e\}")
_PI = re.compile(r"\\pi(?![a-zA-Z])")
_LOG_BARS = re.compile(r"\\ln\s*\|([^|]+)\|")
_TEXT_RUN = re.compile(r"\\text\{[^}]*\}|\\mathrm\{[^}]*\}")
_BOXED = re.compile(r"\\boxed\{(.*)\}")
_APPROX = re.compile(r"\\approx")
_PAREN_THEN_POWER = re.compile(r"\)\s*(?=[a-zA-Z]\^)")


FUNCTION_NAMES = (
   "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh",
   "sin", "cos", "tan", "sec", "csc", "cot", "ln", "log", "exp",
)
_FUNCTION_CALL = re.compile(r"\\(" + "|".join(FUNCTION_NAMES) + r")(\^\{[^}]*\}|\^-?\d)?\s*\(")
_FUNCTION_AFTER_TERM = re.compile(r"(?<=[}\)\]\w])\s*(\\(?:" + "|".join(FUNCTION_NAMES) + r")(?![a-zA-Z]))")


_SUPERSCRIPT_THEN_FACTOR = re.compile(r"\^(\{[^{}]*\}|\w)\s*(?=[a-zA-Z(\\])")
_BARE_ARGUMENT = re.compile(r"\\(" + "|".join(FUNCTION_NAMES) + r")(\^\{[^}]*\}|\^\d)?\s+([a-zA-Z0-9])(?![a-zA-Z0-9^_])")
_ENDS_WITH_FUNCTION = re.compile(r"\\(?:" + "|".join(FUNCTION_NAMES) + r")$")
_ENDS_WITH_BOUNDED_OPERATOR = re.compile(r"\\(?:int|sum|prod|lim)(?:_\{[^{}]*\}|_\w)?$")
_DIFFERENTIAL_NEXT = re.compile(r"d(?:[a-zA-Z](?![a-zA-Z])|\\theta(?![a-zA-Z]))")


class Unreadable(ValueError):
   pass


@dataclass(frozen=True)
class Definitions:
   """The functions a question defines, each name mapped to (variable, expression)."""
   functions: dict = field(default_factory=dict)


PLACEHOLDER_LETTER = "Q"
MAX_PLACEHOLDERS = 10
_PLACEHOLDER_IN_TEXT = re.compile(PLACEHOLDER_LETTER + r"_")
_NAMED_CALL = re.compile(r"(?<![\\A-Za-z^_])([A-Za-z])('*)\s*\(")


def without_spacing(text):
   return _SPACING.sub(" ", text)


def _placeholder(index):
   return f"{PLACEHOLDER_LETTER}_{{{index}}}"


def _placeholder_symbol(index):
   return sympy.Symbol(f"{PLACEHOLDER_LETTER}_{{{index}}}")


def with_definitions(latex, definitions):
   """The line with every call of a defined function replaced by a placeholder symbol, and the
   expression each placeholder stands for. Without definitions the line is returned unchanged."""
   if definitions is None:
      return latex, {}

   text = without_spacing(latex)

   if _PLACEHOLDER_IN_TEXT.search(text):
      raise Unreadable(f"{latex!r} already uses the placeholder name")

   pieces = []
   bindings = {}
   cursor = 0

   while True:
      match = _NAMED_CALL.search(text, cursor)

      if match is None:
         break

      name, primes = match.group(1), match.group(2)
      is_defined = name in definitions.functions
      is_capital = name.isupper()

      if not is_defined and is_capital:
         raise Unreadable(f"{latex!r} calls {name}, which the question does not define")

      if not is_defined:
         pieces.append(text[cursor:match.end()])
         cursor = match.end()
         continue

      opening = match.end() - 1
      closing = _closing_paren(text, opening)

      if closing is None:
         raise Unreadable(f"{latex!r} leaves a call of {name} open")

      has_room = len(bindings) < MAX_PLACEHOLDERS

      if not has_room:
         raise Unreadable(f"{latex!r} calls defined functions too many times to read")

      argument = _read_normalised(normalised(text[opening + 1:closing]))
      variable, expression = definitions.functions[name]

      for _prime in primes:
         expression = sympy.diff(expression, variable)

      index = len(bindings)
      bindings[_placeholder_symbol(index)] = expression.subs(variable, argument)
      pieces.append(text[cursor:match.start()])
      pieces.append("(" + _placeholder(index) + ")")
      cursor = closing + 1

   pieces.append(text[cursor:])

   return "".join(pieces), bindings


def _parenthesised_argument(match):
   name, power, argument = match.group(1), match.group(2) or "", match.group(3)

   return "\\" + name + power + "(" + argument + ")"


def multiplied_after_superscripts(text):
   """x^2 e^{x} is a product the lark grammar will not read without an explicit operator. A
   superscript on a function name, as in sin^{2}(x), the upper bound of an integral or a sum, and
   a power followed by the differential dx are left alone."""

   def replacement(match):
      before = text[:match.start()]
      after = text[match.end():]
      belongs_to_a_function = _ENDS_WITH_FUNCTION.search(before) is not None
      is_a_bound = _ENDS_WITH_BOUNDED_OPERATOR.search(before) is not None
      starts_an_operator = after.startswith(("\\cdot", "\\times"))
      is_the_differential = _DIFFERENTIAL_NEXT.match(after) is not None
      leaves_it_alone = belongs_to_a_function or is_a_bound or starts_an_operator or is_the_differential

      if leaves_it_alone:
         return match.group(0)

      return "^" + match.group(1) + r" \cdot "

   return _SUPERSCRIPT_THEN_FACTOR.sub(replacement, text)


def _closing_paren(text, opening):
   depth = 0

   for position in range(opening, len(text)):
      character = text[position]

      if character == "(":
         depth += 1
      elif character == ")":
         depth -= 1

         if depth == 0:
            return position

   return None


def wrapped_function_calls(text):
   """The lark grammar reads \\ln(x)+C two ways, as ln(x + C) and as ln(x) + C. Wrapping every
   parenthesised call in its own parentheses leaves one reading."""
   pieces = []
   cursor = 0

   while True:
      match = _FUNCTION_CALL.search(text, cursor)

      if match is None:
         break

      opening = match.end() - 1
      closing = _closing_paren(text, opening)

      if closing is None:
         break

      inner = wrapped_function_calls(text[opening + 1:closing])
      pieces.append(text[cursor:match.start()])
      pieces.append("(" + text[match.start():opening] + "(" + inner + "))")
      cursor = closing + 1

   pieces.append(text[cursor:])

   return "".join(pieces)


def normalised(latex):
   text = latex.strip()
   boxed = _BOXED.fullmatch(text)

   if boxed:
      text = boxed.group(1)

   text = _SPACING.sub(" ", text)
   text = _ROMAN_E.sub("e", text)
   text = _TEXT_RUN.sub(" ", text)
   text = _PI.sub(lambda _match: PI_STAND_IN + " ", text)
   text = _LOG_BARS.sub(r"\\ln(|\1|)", text)
   text = _APPROX.sub("=", text)
   text = _PAREN_THEN_POWER.sub(lambda _match: ") \\cdot ", text)
   text = _FUNCTION_AFTER_TERM.sub(lambda match: r" \cdot " + match.group(1), text)
   text = _BARE_ARGUMENT.sub(_parenthesised_argument, text)
   text = multiplied_after_superscripts(text)
   text = wrapped_function_calls(text)

   return text.strip().rstrip(".").strip()


def _right_side_of(text):
   has_equals = "=" in text

   if not has_equals:
      return text

   return text.rsplit("=", 1)[1].strip()


def right_hand_side(latex):
   """The object a line claims, normalised: what follows the last = sign, or the whole line."""
   return _right_side_of(normalised(latex))


def _constants_restored(expression):
   return expression.subs({EULER_SYMBOL: sympy.E, PI_SYMBOL: sympy.pi})


def _parsed(text):
   try:
      with warnings.catch_warnings():
         warnings.simplefilter("ignore")
         parsed = parse_latex(text, backend="lark")
   except Exception as failure:
      raise Unreadable(f"could not read {text!r}: {type(failure).__name__}") from None

   return parsed


def _disambiguated(parsed, text):
   is_tree = type(parsed).__name__ == "Tree"

   if not is_tree:
      return parsed

   is_ambiguous = getattr(parsed, "data", None) == AMBIGUOUS_TREE_NAME

   if not is_ambiguous:
      raise Unreadable(f"could not read {text!r}")

   readings = [child for child in parsed.children if isinstance(child, sympy.Basic)]
   has_readings = len(readings) > 0

   if not has_readings:
      raise Unreadable(f"could not read {text!r}")

   first = readings[0]
   every_reading_is_an_expression = all(isinstance(reading, sympy.Expr) for reading in readings)

   if not every_reading_is_an_expression:
      raise Unreadable(f"{text!r} reads more than one way")

   all_agree = all(sympy.simplify(reading - first) == 0 for reading in readings[1:])

   if not all_agree:
      raise Unreadable(f"{text!r} reads more than one way")

   return first


def to_sympy(latex, definitions=None):
   text, bindings = with_definitions(latex, definitions)

   return _read_normalised(normalised(text)).subs(bindings)


def _read_normalised(text):
   is_empty = text == ""

   if is_empty:
      raise Unreadable("empty line")

   parsed = _disambiguated(_parsed(text), text)
   is_expression = isinstance(parsed, sympy.Expr)
   holds_a_stray_tuple = is_expression and bool(parsed.atoms(sympy.Tuple) - _limit_tuples(parsed))

   if not is_expression or holds_a_stray_tuple:
      raise Unreadable(f"{text!r} is not an expression")

   return _constants_restored(parsed)


def _limit_tuples(expression):
   """The (variable, lower, upper) tuples an integral or a sum legitimately holds."""
   held = set()

   for bounded in expression.atoms(sympy.Integral, sympy.Sum):
      held.update(sympy.Tuple(*limits) for limits in bounded.limits)

   return held


def rhs_to_sympy(latex, definitions=None):
   text, bindings = with_definitions(latex, definitions)

   return _read_normalised(right_hand_side(text)).subs(bindings)


def split_sides(latex, definitions=None):
   """The sides of a line written as a chain of = (or \\approx), normalised and unread, with the
   placeholder bindings read_side needs. A side is read on its own, so one unreadable side does
   not hide the others."""
   text, bindings = with_definitions(latex, definitions)
   sides = [side.strip() for side in normalised(text).split("=") if side.strip() != ""]

   return sides, bindings


def read_side(side, bindings):
   return _read_normalised(side).subs(bindings)


def sides_to_sympy(latex, definitions=None):
   sides, bindings = split_sides(latex, definitions)

   return [read_side(side, bindings) for side in sides]


def decimal_places(latex):
   """The number of digits written after the decimal point in the right-hand side, or None when
   the right-hand side is not a plain decimal numeral."""
   text = right_hand_side(latex).replace(" ", "")
   match = re.fullmatch(r"[-+]?\d*\.(\d+)", text)

   if match is None:
      return None

   return len(match.group(1))
