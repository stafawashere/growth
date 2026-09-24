"""BC-QA-99008, the total amount that arrives from a rate over an interval, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_integral, tex

ARCHETYPE_ID = "BC-QA-99008"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "base_rate", "type": "integer", "role": "safe", "domain": {"min": 6, "max": 15, "step": 1}},
      {"name": "swing", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 2, "step": 1}},
      {"name": "length", "type": "integer", "role": "safe", "domain": {"min": 3, "max": 5, "step": 1}},
      {"name": "initial", "type": "integer", "role": "safe", "domain": {"min": 20, "max": 90, "step": 10}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["tank", "park", "hopper"]}},
      {"name": "outflow", "type": "label", "role": "difficulty", "domain": {"values": ["absent", "present"]}},
   ],
   "constraints": [
      "not (stretch == 5 and start == 0 and length == 4 and swing <= 3)",
   ],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "outflow", "difficulty_factor_id": "BC-DF-15", "settings": {"absent": "off", "present": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {
         "representation": "BC-REP-05",
         "figure_kind": None,
         "requires": ["base_rate", "swing", "stretch", "start", "length", "initial", "context"],
      },
   ],
   "notes": "The inflow rate is base_rate + swing sin(t^2 / stretch), positive because base_rate exceeds swing; the initial amount, and the outflow rate when present, are in the stem but play no part in the total that arrives. The integral of sin(t^2 / 5) over [0, 4] is within 0.0002 of 2, so that interval with a swing of 2 or 3 would round to a whole number and is excluded.",
}

CONTEXTS = {
   "tank": ("Water flows into a tank", "gallons", "hour", "water flows out through a drain", "The tank holds", "gallons of water"),
   "park": ("Visitors enter an amusement park", "people", "hour", "visitors leave the park", "The park holds", "people"),
   "hopper": ("Grain is poured into a hopper", "kilograms", "minute", "grain drains from the bottom of the hopper", "The hopper holds", "kilograms of grain"),
}

t = sympy.Symbol("t")
DEGREE = sympy.pi / 180


def build(names):
   base_rate = names["base_rate"]
   swing = names["swing"]
   stretch = names["stretch"]
   start = names["start"]
   end = start + names["length"]
   initial = names["initial"]
   has_outflow = names["outflow"] == "present"
   action, units, time_unit, outflow_phrase, holding, holding_units = CONTEXTS[names["context"]]

   inflow = base_rate + swing * sympy.sin(t**2 / stretch)
   key_value = numeric_integral(inflow, t, start, end)
   degree_value = numeric_integral(base_rate + swing * sympy.sin(t**2 / stretch * DEGREE), t, start, end)
   endpoint_difference = sympy.N(inflow.subs(t, end) - inflow.subs(t, start), 30)
   amount_present = key_value + initial

   outflow = sympy.Rational(base_rate, 2) + t
   outflow_sentence = (
      f" During the same time, {outflow_phrase} at the rate {math('D(t) = ' + tex(outflow))} {units} per {time_unit}."
      if has_outflow else ""
   )
   stem = (
      f"{action} at the rate {math('R(t) = ' + tex(inflow))} {units} per {time_unit}, where t is measured in "
      f"{time_unit}s for {math(rf'0 \le t \le {end + 1}')}. {holding} {initial} {holding_units} at time {math('t = 0')}."
      f"{outflow_sentence} Using a calculator, find the total number of {units} that arrive during the time interval "
      f"{math(rf'{start} \le t \le {end}')}. Show the setup, and give the value correct to three decimal places."
   )

   integral_tex = rf"\int_{{{start}}}^{{{end}}} \left({tex(inflow)}\right)\,dt"
   steps = [
      Step(
         text=(
            f"The amount that arrives is the integral of the inflow rate over the interval, {math(integral_tex)}, "
            "and nothing is added for the starting amount or taken away."
         ),
         point_type_id="BC-PT-99001",
         rule="accumulation of a rate",
      ),
      Step(
         text=f"With the calculator in radian mode, the integral is about {decimal_text(key_value)} {units}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="numerical integration",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-08012",
         derivation="the amount present at the end reported, the starting amount added to the integral of the inflow",
         value=amount_present,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-06032",
         derivation="the integral evaluated with the calculator in degree mode",
         value=degree_value,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-99012",
         derivation="the rate evaluated at the endpoints and subtracted, R(b) - R(a), in place of its integral",
         value=endpoint_difference,
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=key_value, decimals=3, units=units),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
