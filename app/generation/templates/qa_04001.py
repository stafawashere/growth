"""BC-QA-04001, the meaning of a derivative value in context, with units."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math

ARCHETYPE_ID = "BC-QA-04001"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["tank", "tea", "bacteria", "sand", "line", "snow", "ice", "balloon"]}},
      {"name": "instant", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 12, "step": 1}},
      {"name": "magnitude", "type": "rational", "role": "safe", "domain": {"min": 0.5, "max": 9.5, "step": 0.5, "exclude": [1]}},
      {"name": "sign", "type": "label", "role": "difficulty", "domain": {"values": ["positive", "negative"]}},
      {"name": "order", "type": "label", "role": "difficulty", "domain": {"values": ["first", "second"]}},
   ],
   "constraints": [
      "magnitude > 0",
   ],
   "derived": [
      {"name": "stated_value", "expression": "magnitude if sign == 'positive' else -magnitude"},
   ],
   "invariants": [
      "stated_value != 0",
      "abs(stated_value) == magnitude",
   ],
   "dial_bindings": [
      {"parameter": "sign", "difficulty_factor_id": "BC-DF-12", "settings": {"positive": "off", "negative": "low"}},
      {"parameter": "order", "difficulty_factor_id": "BC-DF-16", "settings": {"first": "off", "second": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["context", "instant", "magnitude", "sign", "order"]},
   ],
   "notes": "The stem gives one value of the first or second derivative of a modelled quantity; the key is the full interpretation with the instant, the direction and the units, and each distractor drops or garbles exactly one of those.",
}

CONTEXTS = {
   "tank": ("V", "the volume of water in a tank", "the volume of water in the tank", "liters", "hours", "hour", "liter"),
   "tea": ("H", "the temperature of a cup of tea", "the temperature of the tea", "degrees Celsius", "minutes", "minute", "degree Celsius"),
   "bacteria": ("P", "the number of bacteria in a dish", "the number of bacteria in the dish", "bacteria", "hours", "hour", "bacterium"),
   "sand": ("S", "the amount of sand in a pile", "the amount of sand in the pile", "cubic feet", "hours", "hour", "cubic foot"),
   "line": ("N", "the number of people waiting in a line", "the number of people in the line", "people", "minutes", "minute", "person"),
   "snow": ("D", "the depth of snow on a field", "the depth of snow on the field", "inches", "hours", "hour", "inch"),
   "ice": ("M", "the mass of a block of melting ice", "the mass of the block of ice", "kilograms", "minutes", "minute", "kilogram"),
   "balloon": ("A", "the height of a weather balloon above the ground", "the height of the balloon", "meters", "seconds", "second", "meter"),
}


def _number_text(value):
   value = sympy.Rational(value)

   if value.q == 1:
      return str(value.p)

   whole, remainder = divmod(abs(value.p), value.q)
   sign = "-" if value < 0 else ""
   tenths = remainder * 10 // value.q

   return f"{sign}{whole}.{tenths}"


def _first_order(names, context):
   letter, subject, quantity, units, time_plural, time_single, unit_single = context
   instant = names["instant"]
   magnitude_text = _number_text(names["magnitude"])
   is_negative = names["sign"] == "negative"
   direction = "decreasing" if is_negative else "increasing"
   opposite = "increasing" if is_negative else "decreasing"
   when = f"At time t = {instant} {time_plural}"
   rate_units = f"{units} per {time_single}"

   first_value = f"{letter}'({instant})"
   key = f"{when}, {quantity} is {direction} at a rate of {magnitude_text} {rate_units}."
   steps = [
      Step(
         text=(
            f"{math(first_value)} is the rate of change of {quantity} at the instant t = {instant}, "
            f"so it is measured in {rate_units}."
         ),
         point_type_id="BC-PT-99008",
         rule="derivative as a rate of change",
      ),
      Step(
         text=(
            f"The value is {'negative' if is_negative else 'positive'}, so {quantity} is {direction} at that instant, "
            f"by {magnitude_text} {units} for each {time_single}."
         ),
         point_type_id="BC-PT-99004",
         rule="sign of the derivative gives the direction",
      ),
   ]

   inverted = Distractor(
      error_path="BC-ERR-04001",
      derivation="the units assembled the wrong way round, time units over quantity units",
      label=f"{when}, {quantity} is {direction} at a rate of {magnitude_text} {time_plural} per {unit_single}.",
      mechanism="reversed_quantities",
   )
   amount = Distractor(
      error_path="BC-ERR-04003",
      derivation="the derivative value read as an amount, the total change in the quantity, rather than a rate",
      label=f"{when}, {quantity} has changed by a total of {_number_text(names['stated_value'])} {units}.",
      mechanism="conceptual_confusion",
   )

   if is_negative:
      third = Distractor(
         error_path="BC-ERR-04005",
         derivation="the negative rate reported as its magnitude and described as an increase",
         label=f"{when}, {quantity} is {opposite} at a rate of {magnitude_text} {rate_units}.",
         mechanism="sign_error",
      )
   else:
      third = Distractor(
         error_path="BC-ERR-99027",
         derivation="the instant replaced by the whole interval up to it, so the interpretation no longer says when the rate holds",
         label=f"Over the first {instant} {time_plural}, {quantity} is {direction} at a rate of {magnitude_text} {rate_units}.",
         mechanism="conceptual_confusion",
      )

   return key, steps, [inverted, amount, third]


def _second_order(names, context):
   letter, subject, quantity, units, time_plural, time_single, unit_single = context
   instant = names["instant"]
   magnitude_text = _number_text(names["magnitude"])
   is_negative = names["sign"] == "negative"
   direction = "decreasing" if is_negative else "increasing"
   opposite = "increasing" if is_negative else "decreasing"
   when = f"At time t = {instant} {time_plural}"
   rate_units = f"{units} per {time_single}"
   compound_units = f"{units} per {time_single} per {time_single}"
   changing_rate = f"the rate at which {quantity} is changing"

   second_value = f"{letter}''({instant})"
   rate_name = f"{letter}'"
   key = f"{when}, {changing_rate} is {direction} at a rate of {magnitude_text} {compound_units}."
   steps = [
      Step(
         text=(
            f"{math(second_value)} is the rate of change of {math(rate_name)}, the rate at which "
            f"{quantity} changes, so it is measured in {compound_units}."
         ),
         point_type_id="BC-PT-99008",
         rule="second derivative as the rate of change of a rate",
      ),
      Step(
         text=(
            f"The value is {'negative' if is_negative else 'positive'}, so at t = {instant} the rate of change of "
            f"{quantity} is itself {direction}, by {magnitude_text} {rate_units} for each {time_single}."
         ),
         point_type_id="BC-PT-99004",
         rule="sign of the second derivative gives the direction of change of the rate",
      ),
   ]

   rate_units_only = Distractor(
      error_path="BC-ERR-04001",
      derivation="the units of the first derivative given for a rate of a rate, one time unit short",
      label=f"{when}, {changing_rate} is {direction} at a rate of {magnitude_text} {rate_units}.",
      mechanism="conceptual_confusion",
   )
   rate_not_changing = Distractor(
      error_path="BC-ERR-99027",
      derivation="the interpretation speaks of the quantity and leaves out that it is the rate which is changing",
      label=f"{when}, {quantity} is {direction} at a rate of {magnitude_text} {compound_units}.",
      mechanism="conceptual_confusion",
   )

   if is_negative:
      third = Distractor(
         error_path="BC-ERR-04005",
         derivation="the negative value reported as a magnitude and described as an increase",
         label=f"{when}, {changing_rate} is {opposite} at a rate of {magnitude_text} {compound_units}.",
         mechanism="sign_error",
      )
   else:
      third = Distractor(
         error_path="BC-ERR-04003",
         derivation="the second derivative value read as the value of the rate itself, the first derivative",
         label=f"{when}, {quantity} is changing at a rate of {magnitude_text} {rate_units}.",
         mechanism="conceptual_confusion",
      )

   return key, steps, [rate_units_only, rate_not_changing, third]


def build(names):
   context = CONTEXTS[names["context"]]
   letter, subject, quantity, units, time_plural, time_single, unit_single = context
   instant = names["instant"]
   is_second = names["order"] == "second"
   primes = "''" if is_second else "'"
   statement = f"{letter}{primes}({instant}) = {_number_text(names['stated_value'])}"

   stem = (
      f"{subject[0].upper() + subject[1:]}, measured in {units}, is modeled by a twice-differentiable function "
      f"{letter} of time t, measured in {time_plural}. It is known that {math(statement)}. Using correct units, "
      f"interpret the meaning of {math(statement)} in the context of the problem."
   )

   if is_second:
      key_label, steps, distractors = _second_order(names, context)
   else:
      key_label, steps, distractors = _first_order(names, context)

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="no_calculator",
      command_verb="interpret",
   )
