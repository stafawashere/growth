"""BC-QA-04005, a rate of change in a setting other than motion, computed with a calculator and interpreted."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, tex

ARCHETYPE_ID = "BC-QA-04005"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["liquid", "medicine", "tank", "pollutant", "crowd", "battery"]}},
      {"name": "base", "type": "integer", "role": "safe", "domain": {"min": 10, "max": 60, "step": 5}},
      {"name": "amount", "type": "integer", "role": "safe", "domain": {"min": 20, "max": 80, "step": 5}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"values": [4, 5, 6, 8, 10, 12]}},
      {"name": "instant", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "trend", "type": "label", "role": "safe", "domain": {"values": ["rising", "falling"]}},
      {"name": "supplied", "type": "label", "role": "difficulty", "domain": {"values": ["model", "rate"]}},
   ],
   "constraints": [
      "instant <= scale",
   ],
   "derived": [],
   "invariants": [
      "abs(rate) > 0.5",
      "abs(rate) < 20",
   ],
   "dial_bindings": [
      {"parameter": "supplied", "difficulty_factor_id": "BC-DF-07", "settings": {"rate": "off", "model": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["context", "base", "amount", "scale", "instant", "trend", "supplied"]},
   ],
   "notes": "The model is base plus or minus an exponential approach, so its rate keeps one sign and stays between 0.5 and 20 in size at the instant; the calculator is needed for the exponential, and the options share the number and differ in the interpretation.",
}

CONTEXTS = {
   "liquid": ("H", "The temperature of a liquid in a laboratory flask", "the temperature of the liquid", "degrees Celsius", "degree Celsius", "minutes", "minute"),
   "medicine": ("C", "The concentration of a medicine in a patient's blood", "the concentration of the medicine", "milligrams per liter", "milligram per liter", "hours", "hour"),
   "tank": ("W", "The amount of water in a storage tank", "the amount of water in the tank", "hundreds of gallons", "hundred gallons", "hours", "hour"),
   "pollutant": ("L", "The level of a pollutant in a lake", "the level of the pollutant", "parts per billion", "part per billion", "days", "day"),
   "crowd": ("N", "The number of people inside a museum", "the number of people inside the museum", "people", "person", "minutes", "minute"),
   "battery": ("B", "The charge stored in a battery", "the charge stored in the battery", "watt-hours", "watt-hour", "minutes", "minute"),
}

t = sympy.Symbol("t")


def _label(value_text, instant, time_plural, sentence):
   return f"{value_text}, so at time t = {instant} {time_plural} {sentence}."


def build(names):
   letter, subject, quantity, units, unit_single, time_plural, time_single = CONTEXTS[names["context"]]
   instant = int(names["instant"])
   scale = int(names["scale"])
   is_rising = names["trend"] == "rising"
   exponential = sympy.exp(-t / scale)

   if is_rising:
      model = names["base"] + names["amount"] * (1 - exponential)
   else:
      model = names["base"] + names["amount"] * exponential

   rate_function = sympy.diff(model, t)
   rate_value = rate_function.subs(t, instant).evalf(30)
   rate_text = decimal_text(rate_value)
   size_text = decimal_text(abs(rate_value))
   direction = "increasing" if rate_value > 0 else "decreasing"
   rate_units = f"{units} per {time_single}"
   window = rf"0 \le t \le {3 * scale}"
   value_name = f"{letter}'({instant})"
   rate_definition = f"{letter}'(t) = " + tex(rate_function)
   derivative_definition = rate_definition

   if names["supplied"] == "model":
      given = f"is modeled by {math(f'{letter}(t) = ' + tex(model))} {units}, for {math(window)}, where t is measured in {time_plural}"
      ask = f"find {math(value_name)}"
   else:
      given = (
         f"is modeled by a differentiable function {letter} of time t, measured in {time_plural}, whose rate of change is "
         f"{math(rate_definition)} {rate_units}, for {math(window)}"
      )
      ask = f"find {math(value_name)}"

   stem = (
      f"{subject} {given}. Using a calculator, {ask}, showing the setup, and interpret the value in the context of "
      "the problem with correct units. Give the value correct to three decimal places."
   )

   value_statement = f"{value_name} = {rate_text}"
   key_sentence = f"{quantity} is {direction} at a rate of {size_text} {rate_units}"

   steps = []

   if names["supplied"] == "model":
      steps.append(Step(
         text=f"Differentiate the model to get the rate, {math(derivative_definition)}.",
         point_type_id="BC-PT-99027",
         rule="derivative of the model",
      ))

   steps.extend([
      Step(
         text=f"With a calculator, {math(value_statement)} to three decimal places.",
         point_type_id="BC-PT-99027",
         rule="evaluate the derivative at the instant",
      ),
      Step(
         text=(
            f"The value is {'positive' if rate_value > 0 else 'negative'}, so at time t = {instant} {time_plural} "
            f"{key_sentence}."
         ),
         point_type_id="BC-PT-99014",
         rule="sign of the rate gives the direction of change",
      ),
   ])

   value_text = f"{math(value_statement)}"
   distractors = [
      Distractor(
         error_path="BC-ERR-04001",
         derivation="the units assembled the wrong way round, time units over the units of the quantity",
         label=_label(value_text, instant, time_plural, f"{quantity} is {direction} at a rate of {size_text} {time_plural} per {unit_single}"),
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-04013",
         derivation="the rate of change of a non-motion quantity called a velocity",
         label=_label(value_text, instant, time_plural, f"{quantity} is moving with a velocity of {rate_text} {rate_units}"),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-04012",
         derivation="the independent variable never named, so the input is read as a value of the quantity rather than a time",
         label=f"{value_text}, so when {quantity} is {instant} {units} it is {direction} at a rate of {size_text} {rate_units}.",
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=_label(value_text, instant, time_plural, key_sentence)),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="calculator",
      setup_required=True,
      command_verb="interpret",
      notes={"rate": rate_value},
   )
