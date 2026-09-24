"""BC-QA-08001, average value of a function over an interval, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_integral, numeric_roots, tex

ARCHETYPE_ID = "BC-QA-08001"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "length", "type": "real", "role": "safe", "domain": {"values": [2, 2.5, 3, 3.5, 4]}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["temperature", "depth", "flow"]}},
      {"name": "framing", "type": "label", "role": "difficulty", "domain": {"values": ["bare", "context"]}},
   ],
   "constraints": [
      "amplitude > abs(shift)",
      "length**2 >= 4*scale",
   ],
   "derived": [
      {"name": "interval_length", "expression": "length"},
   ],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
      "abs(key) < amplitude + abs(shift)",
   ],
   "dial_bindings": [
      {"parameter": "framing", "difficulty_factor_id": "BC-DF-05", "settings": {"bare": "off", "context": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["amplitude", "shift", "scale", "length"]},
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["amplitude", "shift", "scale", "length", "context"]},
   ],
   "notes": "The cosine argument reaches pi inside the interval (length squared at least 4 times the scale) and the amplitude exceeds the shift, so the function changes sign and the average of its absolute value is a distinct distractor.",
}

CONTEXTS = {
   "temperature": ("The temperature of a chemical mixture", "degrees Celsius", "minutes"),
   "depth": ("The depth of water at a tide marker, measured from a reference line,", "feet", "hours"),
   "flow": ("The net flow rate of air into a chamber", "liters per second", "seconds"),
}

t = sympy.Symbol("t")


def _rounded_early(integral_value, length):
   """The integral rounded before dividing, to one place or, when that coincides with the key at
   three places, to a whole number."""
   key = integral_value / length

   for places in (1, 0):
      early = sympy.Float(round(float(integral_value), places), 15) / length
      coincides = round(float(early), 3) == round(float(key), 3)

      if not coincides:
         return early, places

   return sympy.Float(round(float(integral_value)) + 1, 15) / length, -1


def build(names):
   amplitude = names["amplitude"]
   shift = names["shift"]
   scale = names["scale"]
   length = sympy.nsimplify(names["length"])
   function = amplitude * sympy.cos(t**2 / scale) + shift
   integral_value = numeric_integral(function, t, 0, length)
   key_value = integral_value / length
   sign_changes = numeric_roots(function, t, 0, length)
   absolute_value = numeric_integral(sympy.Abs(function), t, 0, length, sign_changes) / length
   endpoint_rate = (function.subs(t, length) - function.subs(t, 0)).evalf(30) / length
   early_value, places = _rounded_early(integral_value, length)

   function_tex = tex(function)
   window = rf"0 \le t \le {tex(length)}"

   if names["framing"] == "context":
      subject, units, time_units = CONTEXTS[names["context"]]
      stem = (
         f"{subject} is modeled by {math('W(t) = ' + function_tex)} {units}, where t is measured in "
         f"{time_units} for {math(window)}. Using a calculator, find the average value of W(t) over "
         f"{math(window)}. Show the setup for the calculation, and give the value correct to three "
         "decimal places."
      )
      representation = "BC-REP-05"
   else:
      stem = (
         f"Let {math('W(t) = ' + function_tex)}. Using a calculator, find the average value of W on the "
         f"interval {math(window)}. Show the setup for the calculation, and give the value correct to "
         "three decimal places."
      )
      representation = "BC-REP-01"

   setup = rf"\frac{{1}}{{{tex(length)}}}\int_{{0}}^{{{tex(length)}}} \left({function_tex}\right)\,dt"
   steps = [
      Step(
         text=f"The average value of W over the interval is {math(setup)}.",
         point_type_id="BC-PT-99020",
         rule="average value formula",
      ),
      Step(
         text=(
            rf"With a calculator, {math(rf'\int_{{0}}^{{{tex(length)}}} \left({function_tex}\right)\,dt')} "
            f"is approximately {decimal_text(integral_value)} (more places are kept for the next step)."
         ),
         value=integral_value,
         point_type_id="BC-PT-99001",
         rule="numerical integration",
      ),
      Step(
         text=f"Divide by the length of the interval, {math(tex(length))}: the average value is about {decimal_text(key_value)}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="division",
      ),
   ]

   if places == 1:
      rounding = "the integral rounded to one decimal place before dividing"
   elif places == 0:
      rounding = "the integral rounded to a whole number before dividing"
   else:
      rounding = "the integral rounded up to the next whole number before dividing"

   distractors = [
      Distractor(
         error_path="BC-ERR-99015",
         derivation="the average rate of change of W over the interval, (W(b) - W(a)) / (b - a)",
         value=endpoint_rate,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-06014",
         derivation="the part of the interval where W is negative counted as positive, the integral of |W| divided by the length",
         value=absolute_value,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99019",
         derivation=rounding,
         value=early_value,
         mechanism="algebra_slip",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=key_value, decimals=3),
      steps=steps,
      distractors=distractors,
      representation=representation,
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
