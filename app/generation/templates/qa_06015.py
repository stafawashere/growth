"""BC-QA-06015, a definite integral of a contextual rate interpreted with units and interval."""
from app.generation.kit import Distractor, Instance, Key, Step, math

ARCHETYPE_ID = "BC-QA-06015"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["water", "cars", "sand", "oil", "people", "snow"]}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 12, "step": 1}},
      {"name": "length", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 10, "step": 1}},
      {"name": "display", "type": "label", "role": "difficulty", "domain": {"values": ["total", "average"]}},
      {"name": "direction", "type": "label", "role": "difficulty", "domain": {"values": ["accumulates", "depletes"]}},
   ],
   "constraints": [],
   "derived": [
      {"name": "finish", "expression": "start + length"},
   ],
   "invariants": [
      "finish > start",
      "len(key) > 40",
   ],
   "dial_bindings": [
      {"parameter": "display", "difficulty_factor_id": "BC-DF-02", "settings": {"total": "off", "average": "low"}},
      {"parameter": "direction", "difficulty_factor_id": "BC-DF-12", "settings": {"accumulates": "off", "depletes": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["context", "start", "length", "display", "direction"]},
   ],
   "notes": "The rate R(t) is positive throughout, so the plain integral is the amount that moved in the stated direction over the interval; the average display carries the factor 1 over the interval length.",
}

CONTEXTS = {
   "water": {
      "accumulates": ("Water is pumped into a tank", "the total amount of water pumped into the tank", "the average rate at which water is pumped into the tank"),
      "depletes": ("Water drains out of a tank", "the total amount of water that drains out of the tank", "the average rate at which water drains out of the tank"),
      "amount_units": "liters",
      "time_unit": "minute",
   },
   "cars": {
      "accumulates": ("Cars enter a parking garage", "the total number of cars that enter the garage", "the average rate at which cars enter the garage"),
      "depletes": ("Cars leave a parking garage", "the total number of cars that leave the garage", "the average rate at which cars leave the garage"),
      "amount_units": "cars",
      "time_unit": "hour",
   },
   "sand": {
      "accumulates": ("Sand is added to a pile", "the total volume of sand added to the pile", "the average rate at which sand is added to the pile"),
      "depletes": ("Sand is removed from a pile", "the total volume of sand removed from the pile", "the average rate at which sand is removed from the pile"),
      "amount_units": "cubic feet",
      "time_unit": "hour",
   },
   "oil": {
      "accumulates": ("Oil is pumped into a storage drum", "the total amount of oil pumped into the drum", "the average rate at which oil is pumped into the drum"),
      "depletes": ("Oil leaks out of a storage drum", "the total amount of oil that leaks out of the drum", "the average rate at which oil leaks out of the drum"),
      "amount_units": "gallons",
      "time_unit": "hour",
   },
   "people": {
      "accumulates": ("People enter a stadium", "the total number of people who enter the stadium", "the average rate at which people enter the stadium"),
      "depletes": ("People leave a stadium", "the total number of people who leave the stadium", "the average rate at which people leave the stadium"),
      "amount_units": "people",
      "time_unit": "minute",
   },
   "snow": {
      "accumulates": ("Snow accumulates on a flat roof", "the total depth of snow that accumulates on the roof", "the average rate at which snow accumulates on the roof"),
      "depletes": ("Snow melts off a flat roof", "the total depth of snow that melts off the roof", "the average rate at which snow melts off the roof"),
      "amount_units": "inches",
      "time_unit": "hour",
   },
}


def build(names):
   start = int(names["start"])
   finish = int(names["finish"])
   length = finish - start
   context = CONTEXTS[names["context"]]
   situation, total_phrase, average_phrase = context[names["direction"]]
   amount_units = context["amount_units"]
   time_unit = context["time_unit"]
   rate_units = f"{amount_units} per {time_unit}"
   is_average = names["display"] == "average"

   integral_tex = rf"\int_{{{start}}}^{{{finish}}} R(t)\,dt"
   displayed_tex = rf"\frac{{1}}{{{length}}}{integral_tex}" if is_average else integral_tex
   interval_text = f"from {math(f't = {start}')} to {math(f't = {finish}')} {time_unit}s"

   stem = (
      f"{situation} at a rate of R(t) {rate_units}, where R is a positive function and t is measured in "
      f"{time_unit}s. Using correct units, interpret the meaning of {math(displayed_tex)} in the context "
      "of the problem."
   )

   steps = [
      Step(
         text=f"R(t) is a rate measured in {rate_units}, so integrating it over time multiplies by {time_unit}s and gives an amount in {amount_units}.",
         rule="units of a definite integral of a rate",
      ),
      Step(
         text=f"The limits run {interval_text}, so {math(integral_tex)} is {total_phrase} {interval_text}.",
         rule="integral of a rate is the accumulated change",
      ),
   ]

   if is_average:
      key_label = f"It is {average_phrase} over the time interval {interval_text}, measured in {rate_units}."
      steps.append(Step(
         text=(
            f"Dividing by the length of the interval, {length} {time_unit}s, turns the amount into an average rate, "
            f"so the expression is {average_phrase} {interval_text}, in {rate_units}."
         ),
         rule="average value of a rate",
      ))
      distractors = [
         Distractor(
            error_path="BC-ERR-06030",
            derivation="the factor 1 over the interval length ignored, so the average is read as the total amount",
            label=f"It is {total_phrase} {interval_text}, measured in {amount_units}.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-99005",
            derivation="the average read correctly but given the units of the accumulated amount instead of the rate",
            label=f"It is {average_phrase} over the time interval {interval_text}, measured in {amount_units}.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-08017",
            derivation="the quantity and units named, the interval of the average never taken from the limits",
            label=f"It is {average_phrase} over the whole time the model covers, measured in {rate_units}.",
            mechanism="conceptual_confusion",
         ),
      ]
   else:
      key_label = f"It is {total_phrase} {interval_text}, measured in {amount_units}."
      steps.append(Step(
         text=f"The units are {rate_units} times {time_unit}s, which is {amount_units}.",
         rule="product of units",
      ))
      distractors = [
         Distractor(
            error_path="BC-ERR-99005",
            derivation="the accumulated amount given the units of the rate, with no multiplication by the time unit",
            label=f"It is {total_phrase} {interval_text}, measured in {rate_units}.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-08017",
            derivation="the accumulated quantity and its units named, the interval of accumulation never taken from the limits",
            label=f"It is {total_phrase} over the whole time the model covers, measured in {amount_units}.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-06029",
            derivation="the quantity and the interval named with no units attached",
            label=f"It is {total_phrase} {interval_text}.",
            mechanism="conceptual_confusion",
         ),
      ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="no_calculator",
      command_verb="interpret",
   )
