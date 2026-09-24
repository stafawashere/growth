"""BC-QA-01012, an instantaneous rate found as the value that average rates over shrinking intervals approach."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure, tex

ARCHETYPE_ID = "BC-QA-01012"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "quadratic", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1, "exclude": [0]}},
      {"name": "linear", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 20, "step": 1}},
      {"name": "point", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["particle", "tank", "population"]}},
      {"name": "source", "type": "label", "role": "difficulty", "domain": {"values": ["formula", "table"]}},
      {"name": "framing", "type": "label", "role": "difficulty", "domain": {"values": ["bare", "context"]}},
   ],
   "constraints": [
      "source == 'formula' or framing == 'context'",
      "2 * quadratic * point + linear != 0",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
      "is_integer(key)",
   ],
   "dial_bindings": [
      {"parameter": "source", "difficulty_factor_id": "BC-DF-03", "settings": {"formula": "off", "table": "low"}},
      {"parameter": "framing", "difficulty_factor_id": "BC-DF-16", "settings": {"bare": "off", "context": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["quadratic", "linear", "constant", "point"]},
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["quadratic", "linear", "constant", "point", "context"]},
      {"representation": "BC-REP-03", "figure_kind": "table", "requires": ["quadratic", "linear", "constant", "point", "context"]},
   ],
   "notes": "The quantity is quadratic in time, so the average rate over [point, point + h] is the instantaneous rate plus quadratic times h, and the averages for h = 0.1, 0.01, 0.001 visibly approach an integer. Tables are always given in context.",
}

CONTEXTS = {
   "particle": ("The position of a particle moving along a line is", "s", "meters", "seconds", "meters per second"),
   "tank": ("The volume of water in a tank is", "V", "liters", "minutes", "liters per minute"),
   "population": ("The mass of a bacteria culture is", "M", "milligrams", "hours", "milligrams per hour"),
}

STEPS = [sympy.Rational(1, 10), sympy.Rational(1, 100), sympy.Rational(1, 1000)]

t = sympy.Symbol("t")


def _decimal(value, places):
   return f"{float(value):.{places}f}"


def build(names):
   quadratic = names["quadratic"]
   linear = names["linear"]
   constant = names["constant"]
   point = names["point"]
   is_context = names["framing"] == "context"
   is_table = names["source"] == "table"

   quantity = quadratic * t**2 + linear * t + constant
   rate = 2 * quadratic * point + linear
   averages = [rate + quadratic * width for width in STEPS]
   first_difference = quantity.subs(t, point + STEPS[0]) - quantity.subs(t, point)

   if is_context:
      opening, letter, units, time_units, rate_units = CONTEXTS[names["context"]]
   else:
      opening, letter, units, time_units, rate_units = ("", "f", None, None, None)

   variable = "t" if is_context else "x"
   intervals = ", ".join(math(rf"[{point}, {_decimal(point + width, 3)}]") for width in STEPS)
   rate_request = "the instantaneous rate of change" if not is_context else f"the rate at which {letter} is changing"

   if is_table:
      rows = [[_decimal(point + width, 3), _decimal(quantity.subs(t, point + width), 6)] for width in [0] + STEPS]
      figure = table_figure(
         [f"t ({time_units})", f"{letter}(t) ({units})"],
         rows,
         alt=f"A table of t and {letter}(t): " + ", ".join(f"{letter}({row[0]}) = {row[1]}" for row in rows) + ".",
      )
      stem = (
         f"{opening} {letter}(t) {units} at time t {time_units}. Selected values of {letter}(t) are given in the table. "
         f"Compute the average rate of change of {letter} over each of the intervals {intervals}, and use them to "
         f"find {rate_request} at {math(f't = {point}')}. Indicate units of measure."
      )
      representation = "BC-REP-03"
   else:
      figure = None
      rule = tex(quantity.subs(t, sympy.Symbol(variable)))

      if is_context:
         stem = (
            f"{opening} {math(f'{letter}(t) = {rule}')} {units} at time t {time_units}. Compute the average rate of "
            f"change of {letter} over each of the intervals {intervals}, and use them to find {rate_request} at "
            f"{math(f't = {point}')}. Indicate units of measure."
         )
         representation = "BC-REP-05"
      else:
         stem = (
            f"Let {math(f'f(x) = {rule}')}. Compute the average rate of change of f over each of the intervals "
            f"{intervals}, and use them to find {rate_request} of f at {math(f'x = {point}')}."
         )
         representation = "BC-REP-01"

   unit_text = f" {rate_units}" if is_context else ""
   average_texts = ", ".join(_decimal(value, 3) for value in averages)
   steps = [
      Step(
         text=(
            f"The average rate over {math(rf'[{point}, {point} + h]')} is "
            f"{math(rf'\frac{{{letter}({point} + h) - {letter}({point})}}{{h}}')}, "
            f"which for h = 0.1, 0.01 and 0.001 gives {average_texts}."
         ),
         rule="average rate of change",
      ),
      Step(
         text=(
            f"As the intervals shrink the averages approach {rate}, so the instantaneous rate at "
            f"{math(f'{variable} = {point}')} is {rate}{unit_text}. Each average is only an approximation of it."
         ),
         value=sympy.Integer(rate),
         rule="instantaneous rate as the limit of average rates",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-01029",
         derivation="the change in the quantity over the first interval reported without dividing by its length 0.1",
         value=first_difference,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-01030",
         derivation="the average rate over the shortest interval, of length 0.001, reported as the exact instantaneous rate",
         value=averages[-1],
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01030",
         derivation="the average rate over the longest interval, of length 0.1, reported as the instantaneous rate",
         value=averages[0],
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=sympy.Integer(rate), units=rate_units),
      steps=steps,
      distractors=distractors,
      representation=representation,
      calculator_status="no_calculator",
      figure=figure,
      command_verb="estimate",
   )
