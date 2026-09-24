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
"""
import math
from dataclasses import dataclass, field

import sympy

from app.frq.items import sympy_of
from app.grading import latex
from app.items.verify import equivalence

PASS = "pass"
FAIL = "fail"
UNSETTLED = "unsettled"

EQUIVALENT = "equivalent"
NOT_EQUIVALENT = "not_equivalent"

REQUIRED_DECIMAL_PLACES = 3


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


def readings_of(line, each_side):
   """What a line offers the check: its right-hand side, or with each_side every side of it, so an
   antiderivative written on the left of -1/y = x^2/2 + C can be found too."""
   if not each_side:
      return [(line, lambda: latex.rhs_to_sympy(line))]

   sides = [side for side in latex.normalised(line).split("=") if side.strip() != ""]

   return [(line, lambda side=side: latex.to_sympy(side)) for side in sides]


def sympy_equivalence(check, part_work):
   expected = sympy_of(check["expected"])
   variable = sympy.Symbol(check.get("variable") or "x")
   up_to_constant = bool(check.get("up_to_constant"))
   each_side = bool(check.get("each_side"))
   lines = candidate_lines(part_work, check["target"])
   readings = [reading for line in lines for reading in readings_of(line, each_side)]
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


def numeric_three_decimals(check, part_work):
   expected = sympy_of(check["expected"])
   line = answer_line(part_work)
   has_line = line != ""

   if not has_line:
      return CheckResult("numeric_three_decimals", FAIL, "no answer was written for this part")

   try:
      candidate = latex.rhs_to_sympy(line)
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


def _integrals_in(line):
   sides = latex.normalised(line).split("=")
   found = []
   unreadable = []

   for side in sides:
      mentions_integral = "\\int" in side

      if not mentions_integral:
         continue

      try:
         expression = latex.to_sympy(side)
      except latex.Unreadable:
         unreadable.append(line)
         continue

      found.extend(expression.atoms(sympy.Integral))

   return found, unreadable


def _bounds_equal(integral, lower, upper):
   limits = integral.limits[0]
   has_bounds = len(limits) == 3

   if not has_bounds:
      return NOT_EQUIVALENT

   _variable, written_lower, written_upper = limits
   lower_verdict = equivalence(written_lower, lower)
   upper_verdict = equivalence(written_upper, upper)
   both_equal = lower_verdict == EQUIVALENT and upper_verdict == EQUIVALENT
   either_differs = lower_verdict == NOT_EQUIVALENT or upper_verdict == NOT_EQUIVALENT

   if both_equal:
      return EQUIVALENT

   if either_differs:
      return NOT_EQUIVALENT

   return UNSETTLED


def bounds_match(check, part_work):
   lower = sympy_of(check["lower"])
   upper = sympy_of(check["upper"])
   has_integrand = check.get("integrand") is not None
   integrand = sympy_of(check["integrand"]) if has_integrand else None
   variable = sympy.Symbol(check.get("variable") or "x")
   unreadable = []
   any_integral = False
   unsettled = False

   for line in live_math_lines(part_work):
      integrals, unread = _integrals_in(line)
      unreadable.extend(unread)

      for integral in integrals:
         any_integral = True
         bounds_verdict = _bounds_equal(integral, lower, upper)

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


def units_present(check, part_work):
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


CHECKS = {
   "sympy_equivalence": sympy_equivalence,
   "numeric_three_decimals": numeric_three_decimals,
   "bounds_match": bounds_match,
   "units_present": units_present,
}


def run_check(check, part_work):
   """A check that raises has not decided anything, so it reports unsettled and the point goes to
   the model, as 03 sends every unsettled check."""
   try:
      return CHECKS[check["kind"]](check, part_work)
   except Exception as raised:
      return CheckResult(check["kind"], UNSETTLED, f"the check could not run: {type(raised).__name__}")
