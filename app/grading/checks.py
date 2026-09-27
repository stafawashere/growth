"""The four deterministic pre-checks of docs/plan/03-diagnosis-and-feedback.md, run against the
confirmed read-back of one part.

Each returns a CheckResult whose outcome is pass, fail or unsettled. Unsettled means the check
could not decide (a line SymPy could not read, or a comparison that did not settle in time), and
03 sends such a point to the model path rather than defaulting it either way.

Work the student crossed out is never read, because the booklet says crossed-out work is not
scored (05, "Free-response capture and grading").

The precision rule, 11 P3 scope item 4, first of the two separately stated rules: a decimal
answer must be accurate to three places after the decimal point, by rounding or by truncation,
and an unsimplified exact answer is accepted. A decimal that misses only because it was rounded
too early or to too few places fails with rounding_only set, which is what the per-question cap in
app/grading/point.py counts. The cap itself is the second rule and lives there, not here.

A check reads the part's work in the context of its question (QuestionContext): the functions the
question defines, so a line written with E(t) is read through E's definition; the numeric roots
the question names (p, q, alpha), so a limit written as the name, as a three-place decimal, or as a
symbol the student set to such a decimal elsewhere in the question is compared with the root's
value; and the whole question's work, where those assignments are found. A limit written to fewer
than three places is unsettled, never failed.

equation_setup, the fifth check, decides a setup equation whose unknown is a numeric root, such as
the integral of C from 0 to T set equal to 500. A written equation passes when its two sides, as a
function of the one symbol left in it, differ by a nonzero constant multiple of the reference
equation's difference at sampled points of the stated interval. It never fails a written line,
because a setup it cannot match may still be one the criterion accepts; it only passes or stays
unsettled.
"""
import math
import re
from dataclasses import dataclass, field

import sympy

from app.frq.items import root_names, sympy_of
from app.grading import latex
from app.items.verify import equivalence, run_bounded

PASS = "pass"
FAIL = "fail"
UNSETTLED = "unsettled"

EQUIVALENT = "equivalent"
NOT_EQUIVALENT = "not_equivalent"

REQUIRED_DECIMAL_PLACES = 3

EQUATION_SAMPLES = 5
EQUATION_TIMEOUT_S = 10
ROUNDED_CONSTANT_SLACK = 0.002
_DECIMAL = re.compile(r"-?\d*\.\d+")
_STATEMENT_BREAK = re.compile(r"\\implies|\\Rightarrow|\\Longrightarrow")


@dataclass(frozen=True)
class CheckResult:
   check: str
   outcome: str
   detail: str
   rounding_only: bool = False
   matched_line: str | None = None
   unreadable: tuple = field(default_factory=tuple)

   def as_record(self):
      return {
         "ran": True,
         "check": self.check,
         "outcome": self.outcome,
         "detail": self.detail,
         "rounding_only": self.rounding_only,
         "matched_line": self.matched_line,
         "unreadable": list(self.unreadable),
      }


@dataclass(frozen=True)
class QuestionContext:
   definitions: latex.Definitions | None = None
   roots: dict = field(default_factory=dict)
   question_work: dict = field(default_factory=dict)

   def expression(self, text):
      return sympy_of(text, names=[symbol.name for symbol in self.roots])


NO_CONTEXT = QuestionContext()


def question_context(record, work):
   """The context a check reads a part in: the question's defined functions and named roots, and
   the student's work on every part of the question."""
   functions = record.get("functions")
   definitions = None

   if functions is not None:
      definitions = latex.Definitions({
         name: (sympy.Symbol(spec["variable"]), sympy_of(spec["expression"]))
         for name, spec in functions.items()
      })

   roots = {
      sympy.Symbol(name): sympy_of(spec["value"], names=root_names(record))
      for name, spec in (record.get("roots") or {}).items()
   }

   return QuestionContext(definitions=definitions, roots=roots, question_work=work or {})


def live_lines(part_work):
   return [line for line in part_work.get("lines", []) if not line.get("crossed_out")]


def live_math_lines(part_work):
   return [line["content"] for line in live_lines(part_work) if line.get("kind") == "math"]


def answer_line(part_work):
   """The part's stated answer, or its last live math line when the student marked none."""
   stated = (part_work.get("answer") or "").strip()
   has_stated = stated != ""

   if has_stated:
      return stated

   math_lines = live_math_lines(part_work)
   has_math = len(math_lines) > 0

   return math_lines[-1] if has_math else ""


def candidate_lines(part_work, target):
   answer = answer_line(part_work)
   answer_only = target == "answer"

   if answer_only:
      return [answer] if answer else []

   lines = list(live_math_lines(part_work))
   answer_is_new = answer != "" and answer not in lines

   if answer_is_new:
      lines.append(answer)

   return lines


def _without_constant(expression, variable):
   constants = [symbol for symbol in expression.free_symbols if symbol.name == "C"]

   return expression.subs({symbol: 0 for symbol in constants})


def _matches(expected, candidate, up_to_constant, variable):
   if up_to_constant:
      difference = _without_constant(candidate, variable) - expected
      verdicts = [
         equivalence(sympy.diff(difference, symbol), sympy.Integer(0))
         for symbol in sorted(difference.free_symbols | {variable}, key=lambda symbol: symbol.name)
      ]
      every_derivative_vanishes = all(verdict == EQUIVALENT for verdict in verdicts)
      some_derivative_remains = any(verdict == NOT_EQUIVALENT for verdict in verdicts)

      if every_derivative_vanishes:
         return EQUIVALENT

      return NOT_EQUIVALENT if some_derivative_remains else UNSETTLED

   return equivalence(candidate, expected)


def _contains_unevaluated(expression):
   return bool(expression.atoms(sympy.Integral, sympy.Derivative, sympy.Limit, sympy.Sum))


def readings_of(line, each_side, definitions=None):
   """What a line offers the check: its right-hand side, or with each_side every side of it, so an
   antiderivative written on the left of -1/y = x^2/2 + C can be found too."""
   if not each_side:
      return [(line, lambda: latex.rhs_to_sympy(line, definitions))]

   try:
      sides, bindings = latex.split_sides(line, definitions)
   except latex.Unreadable:
      return [(line, lambda: latex.to_sympy(line, definitions))]

   return [(line, lambda side=side: latex.read_side(side, bindings)) for side in sides]


def sympy_equivalence(check, part_work, context=NO_CONTEXT):
   expected = sympy_of(check["expected"])
   variable = sympy.Symbol(check.get("variable") or "x")
   up_to_constant = bool(check.get("up_to_constant"))
   each_side = bool(check.get("each_side"))
   lines = candidate_lines(part_work, check["target"])
   readings = [reading for line in lines for reading in readings_of(line, each_side, context.definitions)]
   unreadable = []
   unsettled = False

   for line, read in readings:
      try:
         candidate = read()
      except latex.Unreadable:
         unreadable.append(line)
         continue
      except Exception:
         unreadable.append(line)
         continue

      is_unevaluated = _contains_unevaluated(candidate) and not _contains_unevaluated(expected)

      if is_unevaluated:
         continue

      try:
         verdict = _matches(expected, candidate, up_to_constant, variable)
      except (TypeError, ValueError, AttributeError, sympy.SympifyError):
         verdict = UNSETTLED

      if verdict == EQUIVALENT:
         return CheckResult("sympy_equivalence", PASS, f"{line} equals {check['expected']}", matched_line=line)

      if verdict != NOT_EQUIVALENT:
         unsettled = True

   has_no_lines = len(lines) == 0
   left_open = unsettled or len(unreadable) > 0

   if has_no_lines:
      return CheckResult("sympy_equivalence", FAIL, "no work was written for this part")

   if left_open:
      return CheckResult(
         "sympy_equivalence",
         UNSETTLED,
         f"no line settled against {check['expected']}",
         unreadable=tuple(unreadable),
      )

   return CheckResult("sympy_equivalence", FAIL, f"no line equals {check['expected']}")


def truncated(value, places):
   scale = 10 ** places

   return math.trunc(value * scale) / scale


def accurate_to_three_places(written, exact):
   rounded_matches = round(written, REQUIRED_DECIMAL_PLACES) == round(exact, REQUIRED_DECIMAL_PLACES)
   truncated_matches = truncated(written, REQUIRED_DECIMAL_PLACES) == truncated(exact, REQUIRED_DECIMAL_PLACES)

   return rounded_matches or truncated_matches


def numeric_three_decimals(check, part_work, context=NO_CONTEXT):
   expected = sympy_of(check["expected"])
   line = answer_line(part_work)
   has_line = line != ""

   if not has_line:
      return CheckResult("numeric_three_decimals", FAIL, "no answer was written for this part")

   try:
      candidate = latex.rhs_to_sympy(line, context.definitions)
   except latex.Unreadable:
      return CheckResult("numeric_three_decimals", UNSETTLED, "the answer could not be read", unreadable=(line,))

   places = latex.decimal_places(line)
   is_decimal = places is not None

   if not is_decimal:
      verdict = equivalence(candidate, expected)

      if verdict == EQUIVALENT:
         return CheckResult("numeric_three_decimals", PASS, f"exact answer {line}", matched_line=line)

      if verdict == NOT_EQUIVALENT:
         return CheckResult("numeric_three_decimals", FAIL, f"{line} is not {check['expected']}")

      return CheckResult("numeric_three_decimals", UNSETTLED, f"{line} did not settle")

   written = float(candidate)
   exact = float(expected)
   is_the_exact_value = math.isclose(written, exact, rel_tol=0, abs_tol=1e-12)
   has_enough_places = places >= REQUIRED_DECIMAL_PLACES
   is_accurate = is_the_exact_value or (has_enough_places and accurate_to_three_places(written, exact))

   if is_accurate:
      return CheckResult("numeric_three_decimals", PASS, f"{line} is accurate to three places", matched_line=line)

   last_place = 10 ** (-places)
   near_the_value = abs(written - exact) <= max(last_place, 0.005)
   detail = f"{line} against {exact:.6f}"

   return CheckResult("numeric_three_decimals", FAIL, detail, rounding_only=near_the_value, matched_line=line)


def _integrals_in(line, definitions=None):
   try:
      sides, bindings = latex.split_sides(line, definitions)
   except latex.Unreadable:
      return [], [line]

   found = []
   unreadable = []

   for side in sides:
      mentions_integral = "\\int" in side

      if not mentions_integral:
         continue

      try:
         expression = latex.read_side(side, bindings)
      except latex.Unreadable:
         unreadable.append(line)
         continue

      found.extend(expression.atoms(sympy.Integral))

   return found, unreadable


def written_decimal_places(value, line):
   """The places after the point of the decimal numeral in line that reads as value, or None when
   no numeral in the line does."""
   for numeral in _DECIMAL.findall(line):
      is_this_value = math.isclose(float(numeral), float(value), rel_tol=0, abs_tol=1e-12)

      if is_this_value:
         return len(numeral.split(".")[1])

   return None


def assigned_decimals(symbol, question_work):
   """The decimals the student set symbol to anywhere in the question, as in p \\approx 0.357."""
   name = sympy.latex(symbol)
   assignment = re.compile(r"(?<![A-Za-z\\])" + re.escape(name) + r"(?![A-Za-z])\s*(?:=|\\approx)\s*(-?\d*\.\d+)")
   found = []

   for part_work in question_work.get("parts", []):
      for line in live_math_lines(part_work):
         found.extend(assignment.findall(latex.without_spacing(line)))

   return found


def decimal_verdict(value_text_or_number, places, exact):
   has_enough_places = places is not None and places >= REQUIRED_DECIMAL_PLACES

   if not has_enough_places:
      return UNSETTLED

   is_accurate = accurate_to_three_places(float(value_text_or_number), float(exact))

   return EQUIVALENT if is_accurate else NOT_EQUIVALENT


def bound_verdict(written, expected, line, context):
   """A written limit against the expected one. Beyond symbolic equivalence, an expected limit
   that is a named root (or evaluates to a number once the roots are known) accepts the root's
   name, a decimal accurate to three places, or a symbol the student set to such a decimal."""
   verdict = equivalence(written, expected)

   if verdict == EQUIVALENT:
      return EQUIVALENT

   expected_value = expected.subs(context.roots)
   is_irrational_limit = expected_value.is_number and not expected_value.is_rational

   if not is_irrational_limit:
      return verdict

   is_named_root = written in context.roots

   if is_named_root:
      return equivalence(context.roots[written], expected_value)

   is_decimal = isinstance(written, sympy.Float)

   if is_decimal:
      return decimal_verdict(written, written_decimal_places(written, line), expected_value)

   is_student_symbol = isinstance(written, sympy.Symbol)

   if is_student_symbol:
      assigned = set(assigned_decimals(written, context.question_work))
      has_one_value = len(assigned) == 1

      if not has_one_value:
         return UNSETTLED

      numeral = assigned.pop()

      return decimal_verdict(numeral, len(numeral.split(".")[1]), expected_value)

   return verdict


def _bounds_equal(integral, lower, upper, line="", context=NO_CONTEXT):
   limits = integral.limits[0]
   has_bounds = len(limits) == 3

   if not has_bounds:
      return NOT_EQUIVALENT

   _variable, written_lower, written_upper = limits
   lower_verdict = bound_verdict(written_lower, lower, line, context)
   upper_verdict = bound_verdict(written_upper, upper, line, context)
   both_equal = lower_verdict == EQUIVALENT and upper_verdict == EQUIVALENT
   either_differs = lower_verdict == NOT_EQUIVALENT or upper_verdict == NOT_EQUIVALENT

   if both_equal:
      return EQUIVALENT

   if either_differs:
      return NOT_EQUIVALENT

   return UNSETTLED


def bounds_match(check, part_work, context=NO_CONTEXT):
   lower = context.expression(check["lower"])
   upper = context.expression(check["upper"])
   has_integrand = check.get("integrand") is not None
   integrand = context.expression(check["integrand"]) if has_integrand else None
   variable = sympy.Symbol(check.get("variable") or "x")
   unreadable = []
   any_integral = False
   unsettled = False

   for line in live_math_lines(part_work):
      integrals, unread = _integrals_in(line, context.definitions)
      unreadable.extend(unread)

      for integral in integrals:
         any_integral = True
         bounds_verdict = _bounds_equal(integral, lower, upper, line, context)

         if bounds_verdict == UNSETTLED:
            unsettled = True
            continue

         if bounds_verdict == NOT_EQUIVALENT:
            continue

         if not has_integrand:
            return CheckResult("bounds_match", PASS, f"{line} has the limits {check['lower']} to {check['upper']}", matched_line=line)

         written_variable = integral.limits[0][0]
         written_integrand = integral.function.subs(written_variable, variable)
         integrand_verdict = equivalence(written_integrand, integrand)

         if integrand_verdict == EQUIVALENT:
            return CheckResult("bounds_match", PASS, f"{line} has the limits and the integrand", matched_line=line)

         if integrand_verdict != NOT_EQUIVALENT:
            unsettled = True

   left_open = unsettled or len(unreadable) > 0

   if left_open:
      return CheckResult("bounds_match", UNSETTLED, "an integral could not be settled", unreadable=tuple(unreadable))

   if not any_integral:
      return CheckResult("bounds_match", FAIL, "no definite integral was written")

   return CheckResult("bounds_match", FAIL, f"no integral runs from {check['lower']} to {check['upper']} with the expected integrand")


def _plain_text(line):
   text = line.replace("\\text{", " ").replace("\\mathrm{", " ").replace("}", " ").replace("{", " ")
   text = text.replace("\\,", " ").replace("\\", " ")

   return " ".join(text.lower().split())


def units_present(check, part_work, context=NO_CONTEXT):
   texts = [_plain_text(line["content"]) for line in live_lines(part_work)]
   texts.append(_plain_text(part_work.get("answer") or ""))
   accepted = [" ".join(unit.lower().split()) for unit in check["units"]]

   for text in texts:
      for unit in accepted:
         padded_text = f" {text} "
         padded_unit = f" {unit} "
         is_present = padded_unit in padded_text or (unit in text and not unit.isalpha())

         if is_present:
            return CheckResult("units_present", PASS, f"units {unit!r} written", matched_line=text)

   return CheckResult("units_present", FAIL, f"none of {check['units']} written")


def sample_points(interval, count=EQUATION_SAMPLES):
   low, high = (float(sympy_of(end)) for end in interval)
   step = (high - low) / (count + 1)

   return [low + step * index for index in range(1, count + 1)]


def residuals(difference, symbol, points):
   """difference evaluated at each point, as floats, or None when any value is not a real number.
   Module level, so run_bounded can run it in a child process."""
   values = []

   for point in points:
      value = sympy.N(difference.subs(symbol, point), 15)
      is_real_number = value.is_number and value.is_real and value.is_finite

      if not is_real_number:
         return None

      values.append(float(value))

   return values


def proportional_to(candidate, reference):
   """Whether candidate is a nonzero constant multiple of reference at every sample, allowing the
   slack of constants written to three decimal places."""
   anchor = max(range(len(reference)), key=lambda index: abs(reference[index]))
   is_flat_reference = abs(reference[anchor]) < 1e-9

   if is_flat_reference:
      return False

   factor = candidate[anchor] / reference[anchor]
   is_zero_factor = abs(factor) < 1e-9

   if is_zero_factor:
      return False

   slack = ROUNDED_CONSTANT_SLACK * max(1.0, abs(factor))

   return all(abs(written - factor * expected) <= slack for written, expected in zip(candidate, reference))


def equation_pairs(line, definitions):
   """Each pair of adjacent sides that both read, within each statement of the line, where a
   statement ends at \\implies or \\Rightarrow."""
   pairs = []

   for statement in _STATEMENT_BREAK.split(line):
      sides, bindings = latex.split_sides(statement, definitions)
      readings = []

      for side in sides:
         try:
            readings.append(latex.read_side(side, bindings))
         except latex.Unreadable:
            readings.append(None)

      pairs.extend((left, right) for left, right in zip(readings, readings[1:]) if left is not None and right is not None)

   return pairs


def equation_setup(check, part_work, context=NO_CONTEXT):
   unknown = sympy.Symbol(check["unknown"])
   reference_difference = (context.expression(check["left"]) - context.expression(check["right"])).subs(context.roots)
   points = sample_points(check["interval"])
   reference = run_bounded(residuals, (reference_difference, unknown, points), EQUATION_TIMEOUT_S, None)
   needs_integral = bool(reference_difference.atoms(sympy.Integral))
   lines = candidate_lines(part_work, "any_line")
   unreadable = []

   if reference is None:
      return CheckResult("equation_setup", UNSETTLED, "the reference equation did not evaluate")

   if not lines:
      return CheckResult("equation_setup", FAIL, "no work was written for this part")

   for line in lines:
      try:
         pairs = equation_pairs(line, context.definitions)
      except latex.Unreadable:
         unreadable.append(line)
         continue

      for left, right in pairs:
         difference = (left - right).subs(context.roots)
         symbols = difference.free_symbols
         has_one_unknown = len(symbols) == 1
         has_integral = bool(difference.atoms(sympy.Integral))
         is_candidate = has_one_unknown and (has_integral or not needs_integral)

         if not is_candidate:
            continue

         written_unknown = next(iter(symbols))
         written = run_bounded(residuals, (difference, written_unknown, points), EQUATION_TIMEOUT_S, None)
         matches = written is not None and proportional_to(written, reference)

         if matches:
            return CheckResult("equation_setup", PASS, f"{line} is the setup equation in {written_unknown}", matched_line=line)

   return CheckResult(
      "equation_setup",
      UNSETTLED,
      f"no line matched the setup equation in {check['unknown']}",
      unreadable=tuple(unreadable),
   )


CHECKS = {
   "sympy_equivalence": sympy_equivalence,
   "numeric_three_decimals": numeric_three_decimals,
   "bounds_match": bounds_match,
   "units_present": units_present,
   "equation_setup": equation_setup,
}


def run_check(check, part_work, context=NO_CONTEXT):
   """A check that raises has not decided anything, so it reports unsettled and the point goes to
   the model, as 03 sends every unsettled check."""
   try:
      return CHECKS[check["kind"]](check, part_work, context)
   except Exception as raised:
      return CheckResult(check["kind"], UNSETTLED, f"the check could not run: {type(raised).__name__}")
