"""BC-QA-99007, the average rate of change of a modelling function over an interval, with units, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_integral, tex

ARCHETYPE_ID = "BC-QA-99007"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "level", "type": "integer", "role": "safe", "domain": {"min": 20, "max": 80, "step": 5}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "spread", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "length", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["tank", "temperature", "snow"]}},
      {"name": "direction", "type": "label", "role": "difficulty", "domain": {"values": ["increasing", "decreasing"]}},
   ],
   "constraints": [
      "direction == 'increasing' or level > 5 * scale",
      "not (spread == 2 and start == 2 and length == 2)",
   ],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
      "key * (1 if direction == 'increasing' else -1) > 0",
   ],
   "dial_bindings": [
      {"parameter": "direction", "difficulty_factor_id": "BC-DF-12", "settings": {"increasing": "off", "decreasing": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {
         "representation": "BC-REP-05",
         "figure_kind": None,
         "requires": ["level", "scale", "spread", "start", "length", "context"],
      },
   ],
   "notes": "The model is level plus or minus scale times ln(1 + t^2 / spread), monotone for t > 0, so the sign of the average rate of change follows the direction; the interval starts after 0 so the interval from 0 is a different one. On the decreasing model the level exceeds 5 times the scale, and ln(1 + t^2 / spread) stays below 4.5 for t up to 9, so A stays positive. With spread 2 on [2, 4] the rate over [0, 4] equals the rate over [2, 4] (both ln 3 / 2), so that draw is excluded.",
}

CONTEXTS = {
   "tank": ("The amount of water in a storage tank", "gallons", "hour"),
   "temperature": ("The temperature of a liquid in a lab vessel", "degrees Celsius", "minute"),
   "snow": ("The depth of snow at a weather station", "centimeters", "hour"),
}

t = sympy.Symbol("t")


def build(names):
   level = names["level"]
   scale = names["scale"]
   spread = names["spread"]
   start = names["start"]
   end = start + names["length"]
   sign = 1 if names["direction"] == "increasing" else -1
   subject, units, time_unit = CONTEXTS[names["context"]]

   model = level + sign * scale * sympy.log(1 + t**2 / spread)
   start_value = sympy.N(model.subs(t, start), 30)
   end_value = sympy.N(model.subs(t, end), 30)
   zero_value = sympy.N(model.subs(t, 0), 30)
   length = end - start

   key_value = (end_value - start_value) / length
   no_division = end_value - start_value
   average_value = numeric_integral(model, t, start, end) / length
   from_zero = (end_value - zero_value) / end

   rate_units = f"{units} per {time_unit}"
   stem = (
      f"{subject} is modeled by {math('A(t) = ' + tex(model))} {units}, where t is measured in {time_unit}s for "
      f"{math(r'0 \le t \le ' + str(end + 1))}. Using a calculator, find the average rate of change of A over the interval "
      f"{math(rf'{start} \le t \le {end}')}. Show the setup, give the value correct to three decimal places, and "
      "indicate units of measure."
   )

   steps = [
      Step(
         text=(
            f"The average rate of change is {math(rf'\frac{{A({end}) - A({start})}}{{{end} - {start}}}')}, with "
            f"{math(rf'A({end}) \approx ' + decimal_text(end_value))} and {math(rf'A({start}) \approx ' + decimal_text(start_value))} "
            "from a calculator."
         ),
         point_type_id="BC-PT-99021",
         rule="average rate of change",
      ),
      Step(
         text=f"Dividing the change by {length} gives about {decimal_text(key_value)} {rate_units}.",
         value=key_value,
         point_type_id="BC-PT-99006",
         rule="units of a rate",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-99015",
         derivation="the average value of A over the interval, the integral divided by the length, reported as the average rate of change",
         value=average_value,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-08001",
         derivation="the change A(b) - A(a) reported without dividing by the length of the interval",
         value=no_division,
         mechanism="forgot_constant",
      ),
      Distractor(
         error_path="BC-ERR-08002",
         derivation=f"the rate taken over 0 <= t <= {end}, an interval the question did not name",
         value=from_zero,
         mechanism="wrong_limits",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=key_value, decimals=3, units=rate_units),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
