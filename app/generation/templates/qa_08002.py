"""BC-QA-08002, the time at which the instantaneous rate equals the average rate of change, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_roots
from app.generation.templates._helpers_f import first_distinct, rounded, tex_f, tidy, truncated

ARCHETYPE_ID = "BC-QA-08002"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "model", "type": "label", "role": "safe", "domain": {"values": ["exponential", "arctangent", "radical"]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "linear_rate", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"values": [2, 3, 4, 5]}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"values": [1, 2, 3]}},
      {"name": "length", "type": "rational", "role": "safe", "domain": {"values": ["2", "5/2", "3", "4"]}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["water", "bacteria", "sand"]}},
      {"name": "framing", "type": "label", "role": "safe", "domain": {"values": ["bare", "context"]}},
      {"name": "presentation", "type": "label", "role": "difficulty", "domain": {"values": ["formula", "accumulation"]}},
   ],
   "constraints": [
      "start + length <= 7",
   ],
   "derived": [
      {"name": "end", "expression": "start + length"},
   ],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
      "start < key",
      "key < end",
   ],
   "dial_bindings": [
      {"parameter": "presentation", "difficulty_factor_id": "BC-DF-03", "settings": {"formula": "off", "accumulation": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["model", "coefficient", "linear_rate", "scale", "start", "length"]},
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["model", "coefficient", "linear_rate", "scale", "start", "length", "context"]},
   ],
   "notes": "Each model has a derivative that is strictly monotonic for t at least 1, so the time given by the Mean Value Theorem is unique on the interval and on the wider interval from 0. The accumulation presentation defines the amount as the integral from 0 of its rate, so the amount is 0 at t = 0.",
}

CONTEXTS = {
   "water": ("The amount of water in a tank", "gallons", "hours"),
   "bacteria": ("The mass of a bacteria culture", "milligrams", "days"),
   "sand": ("The amount of sand in a pile", "tons", "hours"),
}

t = sympy.Symbol("t")
s = sympy.Symbol("s")


def _model(names):
   coefficient = names["coefficient"]
   linear_rate = names["linear_rate"]
   scale = names["scale"]

   if names["model"] == "exponential":
      return coefficient * sympy.exp(t / scale) + linear_rate * t

   if names["model"] == "arctangent":
      return coefficient * sympy.atan(2 * t / scale) + linear_rate * t

   return coefficient * sympy.sqrt(t**2 + scale) + linear_rate * t


def _unique_root(rate, target, low, high):
   roots = numeric_roots(rate - target, t, low, high, pieces=397)

   return roots[0] if len(roots) == 1 else None


def build(names):
   start = names["start"]
   end = names["end"]
   length = names["length"]
   is_accumulation = names["presentation"] == "accumulation"
   is_context = names["framing"] == "context"

   antiderivative = _model(names)
   rate = sympy.diff(antiderivative, t)

   if is_accumulation:
      amount = antiderivative - antiderivative.subs(t, 0)
   else:
      amount = antiderivative

   change = (amount.subs(t, end) - amount.subs(t, start)).evalf(30)
   average_rate = change / length
   key_value = _unique_root(rate, average_rate, start, end)

   whole_change = (amount.subs(t, end) - amount.subs(t, 0)).evalf(30)
   wrong_interval_rate = whole_change / end
   wrong_interval_time = _unique_root(rate, wrong_interval_rate, 0, end)

   window = rf"{tex_f(start)} \le t \le {tex_f(end)}"
   open_window = rf"{tex_f(start)} < t < {tex_f(end)}"
   rate_tex = tex_f(tidy(rate).subs(t, s))

   if is_accumulation:
      definition = rf"W(t) = \int_{{0}}^{{t}} \left({rate_tex}\right)\,ds"
   else:
      definition = f"W(t) = {tex_f(amount)}"

   if is_context:
      subject, units, time_units = CONTEXTS[names["context"]]
      stem = (
         f"{subject} is modeled by {math(definition)} {units}, where t is measured in {time_units} for "
         f"{math(r'0 \le t \le 7')}. Using a calculator, find the time t in the interval {math(open_window)} at which "
         f"the instantaneous rate of change of W equals the average rate of change of W over {math(window)}. "
         "Show the setup for the calculation, and give the value correct to three decimal places."
      )
      representation = "BC-REP-05"
      key_units = time_units
   else:
      stem = (
         f"Let {math(definition)} for {math(r'0 \le t \le 7')}. Using a calculator, find the value of t in the "
         f"interval {math(open_window)} at which the instantaneous rate of change of W equals the average rate "
         f"of change of W over {math(window)}. Show the setup for the calculation, and give the value correct "
         "to three decimal places."
      )
      representation = "BC-REP-01"
      key_units = None

   quotient = rf"\frac{{W({tex_f(end)}) - W({tex_f(start)})}}{{{tex_f(end)} - {tex_f(start)}}}"

   if is_accumulation:
      average_text = (
         f"The average rate of change of W over the interval is {math(quotient + ' = ' + rf'\frac{{1}}{{{tex_f(length)}}}\int_{{{tex_f(start)}}}^{{{tex_f(end)}}} \left({rate_tex}\right)\,ds')}, "
         f"which a calculator gives as about {decimal_text(average_rate)} (more places are kept)."
      )
      derivative_text = f"By the Fundamental Theorem of Calculus, {math(r"W'(t) = " + tex_f(tidy(rate)))}."
   else:
      average_text = (
         f"The average rate of change of W over the interval is {math(quotient)}, which is about "
         f"{decimal_text(average_rate)} (more places are kept)."
      )
      derivative_text = f"Differentiate: {math(r"W'(t) = " + tex_f(tidy(rate)))}."

   steps = [
      Step(text=average_text, value=average_rate, point_type_id="BC-PT-99021", rule="average rate of change"),
      Step(
         text=f"{derivative_text} Set {math(r"W'(t)")} equal to the average rate of change and solve on {math(open_window)}.",
         point_type_id="BC-PT-99005",
         rule="instantaneous rate set equal to the average rate",
      ),
      Step(
         text=f"The calculator's solver gives one solution in the interval, {math('t = ' + decimal_text(key_value))}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="numerical solve",
      ),
   ]

   endpoint_start = amount.subs(t, start).evalf(30)
   endpoint_end = amount.subs(t, end).evalf(30)
   rounding_candidates = [
      (_unique_root(rate, rounded(average_rate, 1), start, end), "the average rate of change rounded to one decimal place before solving"),
      (_unique_root(rate, (rounded(endpoint_end, 0) - rounded(endpoint_start, 0)) / length, start, end), "W at both endpoints rounded to whole numbers before forming the average rate of change"),
      (_unique_root(rate, rounded(average_rate, 2), start, end), "the average rate of change rounded to two decimal places before solving"),
      (_unique_root(rate, (rounded(endpoint_end, 1) - rounded(endpoint_start, 1)) / length, start, end), "W at both endpoints rounded to one decimal place before forming the average rate of change"),
      (_unique_root(rate, rounded(average_rate, 0), start, end), "the average rate of change rounded to a whole number before solving"),
      (_unique_root(rate, truncated(average_rate, 1), start, end), "the average rate of change cut off after one decimal place before solving"),
      (_unique_root(rate, truncated(average_rate, 2), start, end), "the average rate of change cut off after two decimal places before solving"),
      (_unique_root(rate, (truncated(endpoint_end, 0) - truncated(endpoint_start, 0)) / length, start, end), "W at both endpoints cut off to whole numbers before forming the average rate of change"),
      (_unique_root(rate, (truncated(endpoint_end, 1) - truncated(endpoint_start, 1)) / length, start, end), "W at both endpoints cut off after one decimal place before forming the average rate of change"),
      (_unique_root(rate, truncated(average_rate, 0), start, end), "the average rate of change cut off to a whole number before solving"),
   ]
   rounding_choices = first_distinct(rounding_candidates, [key_value, wrong_interval_time], wanted=2)

   distractors = [
      Distractor(
         error_path="BC-ERR-08002",
         derivation=f"the average rate of change taken over 0 to {tex_f(end)} instead of the stated interval, then solved on that wider interval",
         value=wrong_interval_time,
         mechanism="wrong_limits",
      ),
   ]

   for value, description in rounding_choices:
      distractors.append(Distractor(error_path="BC-ERR-99019", derivation=description, value=value, mechanism="algebra_slip"))

   rounding_collapsed = len(rounding_choices) < 2

   if rounding_collapsed:
      early_change = (amount.subs(t, start) - amount.subs(t, 0)).evalf(30)
      early_time = _unique_root(rate, early_change / start, 0, start)
      taken = [key_value, wrong_interval_time] + [value for value, _ in rounding_choices]
      fallback = first_distinct([(early_time, "")], taken)

      for value, _ in fallback:
         distractors.append(Distractor(
            error_path="BC-ERR-08002",
            derivation=f"the average rate of change taken over 0 to {tex_f(start)}, the stretch before the stated interval, then solved there",
            value=value,
            mechanism="wrong_limits",
         ))

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=key_value, decimals=3, units=key_units),
      steps=steps,
      distractors=distractors,
      representation=representation,
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
