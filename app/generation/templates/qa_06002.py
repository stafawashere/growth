"""BC-QA-06002, a trapezoidal sum from a table of rates over unevenly spaced inputs."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure

ARCHETYPE_ID = "BC-QA-06002"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

GAP_COUNT = 3

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "gaps", "type": "integer", "role": "safe", "count": 3, "domain": {"values": [2, 4, 6]}},
      {"name": "rates", "type": "integer", "role": "safe", "count": 4, "domain": {"min": 2, "max": 20, "step": 1}},
      {"name": "initial", "type": "integer", "role": "safe", "domain": {"min": 20, "max": 90, "step": 5}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["tank", "traffic", "rain", "download"]}},
      {"name": "ask", "type": "label", "role": "difficulty", "domain": {"values": ["integral", "amount"]}},
   ],
   "constraints": [
      "not (gaps[0] == gaps[1] and gaps[1] == gaps[2])",
      "total_time % 6 == 0",
      "distinct(options)",
   ],
   "derived": [
      {"name": "total_time", "expression": "gaps[0] + gaps[1] + gaps[2]"},
      {"name": "pair_0", "expression": "rates[0] + rates[1]"},
      {"name": "pair_1", "expression": "rates[1] + rates[2]"},
      {"name": "pair_2", "expression": "rates[2] + rates[3]"},
      {"name": "trapezoid", "expression": "(gaps[0] * pair_0 + gaps[1] * pair_1 + gaps[2] * pair_2) / 2"},
      {"name": "half_once", "expression": "gaps[0] * pair_0 / 2 + gaps[1] * pair_1 + gaps[2] * pair_2"},
      {"name": "common_width", "expression": "total_time / 3 * (pair_0 + pair_1 + pair_2) / 2"},
      {"name": "left_plus_right", "expression": "2 * trapezoid"},
      {"name": "options", "expression": "[trapezoid, half_once, common_width, left_plus_right] if ask == 'integral' else [initial + trapezoid, initial + half_once, initial + common_width, trapezoid]"},
   ],
   "invariants": [
      "exact(key)",
      "is_integer(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "ask", "difficulty_factor_id": "BC-DF-06", "settings": {"integral": "off", "amount": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-05", "figure_kind": "table", "requires": ["gaps", "rates", "context", "ask"]},
   ],
   "notes": (
      "Four rows give three unevenly spaced subintervals with even widths whose total is a multiple of 6, so the "
      "trapezoidal sum and the one-width distractor are whole numbers. The amount ask adds a known starting amount."
   ),
}

CONTEXTS = {
   "tank": ("Water is pumped into a tank at a rate of R(t) liters per minute", "minutes", "liters per minute", "liters", "the tank holds"),
   "traffic": ("Cars enter a parking garage at a rate of R(t) cars per hour", "hours", "cars per hour", "cars", "the garage holds"),
   "rain": ("Rain collects in a gauge at a rate of R(t) millimeters per hour", "hours", "millimeters per hour", "millimeters", "the gauge holds"),
   "download": ("Data is written to a drive at a rate of R(t) megabytes per second", "seconds", "megabytes per second", "megabytes", "the drive holds"),
}


def build(names):
   widths = [int(width) for width in names["gaps"]]
   rates = [int(rate) for rate in names["rates"]]
   times = [0]

   for width in widths:
      times.append(times[-1] + width)

   total_time = times[-1]
   initial = names["initial"]
   is_amount = names["ask"] == "amount"
   opening, time_unit, rate_unit, amount_unit, holds = CONTEXTS[names["context"]]
   pairs = [rates[index] + rates[index + 1] for index in range(GAP_COUNT)]
   trapezoid = sympy.Rational(sum(width * pair for width, pair in zip(widths, pairs)), 2)
   window_text = math(r"0 \le t \le " + str(total_time))
   integral_text = math(rf"\int_{{0}}^{{{total_time}}} R(t)\,dt")

   stem = (
      f"{opening}, where t is measured in {time_unit} for {window_text}. Selected values of R(t) are shown in the "
      "table."
   )

   if is_amount:
      stem += (
         f" At time t = 0, {holds} {initial} {amount_unit}. Use a trapezoidal sum with the three subintervals indicated "
         f"by the table to approximate the amount at time t = {total_time}, in {amount_unit}. Show the setup."
      )
      key_value = initial + trapezoid
   else:
      stem += (
         f" Use a trapezoidal sum with the three subintervals indicated by the table to approximate {integral_text}, "
         f"in {amount_unit}. Show the setup."
      )
      key_value = trapezoid

   rows = [[time, rate] for time, rate in zip(times, rates)]
   table = table_figure(
      [f"t ({time_unit})", f"R(t) ({rate_unit})"],
      rows,
      alt="A table of R(t): " + "; ".join(f"at t = {time}, R(t) = {rate}" for time, rate in rows) + ".",
   )

   terms = " + ".join(
      rf"\tfrac{{1}}{{2}}({widths[index]})({rates[index]} + {rates[index + 1]})" for index in range(GAP_COUNT)
   )
   steps = [
      Step(
         text=f"The widths of the subintervals are {', '.join(str(width) for width in widths)}, read from the table inputs.",
         rule="subinterval widths from the table",
      ),
      Step(
         text=f"Each trapezoid is half the width times the sum of its two end values: {math(terms)}.",
         point_type_id="BC-PT-99018",
         rule="trapezoidal sum",
      ),
      Step(
         text=f"The trapezoidal sum is {math(str(trapezoid))} {amount_unit}.",
         value=trapezoid,
         point_type_id="BC-PT-99019",
         rule="arithmetic",
      ),
   ]

   if is_amount:
      steps.append(Step(
         text=f"Adding the starting amount, the amount at t = {total_time} is about {math(f'{initial} + {trapezoid} = {key_value}')} {amount_unit}.",
         value=key_value,
         point_type_id="BC-PT-99033",
         rule="initial amount plus accumulated change",
      ))

   level = initial if is_amount else 0
   half_once = sympy.Rational(widths[0] * pairs[0], 2) + widths[1] * pairs[1] + widths[2] * pairs[2]
   common_width = sympy.Rational(total_time, GAP_COUNT) * sympy.Rational(sum(pairs), 2)

   distractors = [
      Distractor(
         error_path="BC-ERR-06004",
         derivation="the factor of one half applied to the first trapezoid only",
         value=level + half_once,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-06001",
         derivation=f"one common width, {total_time}/3, used for every subinterval although the table inputs are unevenly spaced",
         value=level + common_width,
         mechanism="conceptual_confusion",
      ),
   ]

   if is_amount:
      distractors.append(Distractor(
         error_path="BC-ERR-06015",
         derivation=f"the trapezoidal sum reported as the amount, with the starting {initial} {amount_unit} left out",
         value=trapezoid,
         mechanism="forgot_constant",
      ))
   else:
      distractors.append(Distractor(
         error_path="BC-ERR-99028",
         derivation="the left and right Riemann sums added without dividing by two",
         value=2 * trapezoid,
         mechanism="algebra_slip",
      ))

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value, units=amount_unit),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="no_calculator",
      figure=table,
      command_verb="approximate",
   )
