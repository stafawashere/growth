"""BC-QA-06005, the value of a quantity from its rate of change and one known value."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_integral, tex

ARCHETYPE_ID = "BC-QA-06005"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "cubic", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 2, "step": 1}},
      {"name": "square", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "linear", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "span", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "known", "type": "integer", "role": "safe", "domain": {"min": 20, "max": 90, "step": 5}},
      {"name": "base_rate", "type": "integer", "role": "safe", "domain": {"min": 3, "max": 9, "step": 1}},
      {"name": "swing", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "horizon", "type": "real", "role": "safe", "domain": {"values": [2, 2.5, 3, 3.5, 4]}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["tank", "pile", "balloon"]}},
      {"name": "tool", "type": "label", "role": "difficulty", "domain": {"values": ["exact", "calculator"]}},
      {"name": "direction", "type": "label", "role": "difficulty", "domain": {"values": ["forward", "backward"]}},
   ],
   "constraints": [
      "cubic != 0 or square != 0",
      "tool == 'calculator' or distinct(exact_options)",
      "tool == 'calculator' or known + change > 0",
      "tool == 'calculator' or known - change > 0",
      "tool == 'exact' or direction == 'forward'",
      "tool == 'exact' or not (stretch == 5 and horizon == 4)",
   ],
   "derived": [
      {"name": "stop", "expression": "start + span"},
      {"name": "upper_only", "expression": "cubic * stop**3 + square * stop**2 + linear * stop"},
      {"name": "lower_only", "expression": "cubic * start**3 + square * start**2 + linear * start"},
      {"name": "change", "expression": "upper_only - lower_only"},
      {"name": "rate_difference", "expression": "3 * cubic * (stop**2 - start**2) + 2 * square * (stop - start)"},
      {"name": "exact_options", "expression": "[known + change, change, known + rate_difference, known + upper_only] if direction == 'forward' else [known - change, change, known - rate_difference, known + change]"},
   ],
   "invariants": [
      "tool == 'calculator' or exact(key)",
      "tool == 'exact' or nondegenerate_three_decimals(key)",
      "finite(key)",
   ],
   "dial_bindings": [
      {"parameter": "tool", "difficulty_factor_id": "BC-DF-07", "settings": {"exact": "off", "calculator": "low"}},
      {"parameter": "direction", "difficulty_factor_id": "BC-DF-14", "settings": {"forward": "off", "backward": "low"}},
   ],
   "calculator_guard": "tool == 'calculator' or exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["cubic", "square", "linear", "start", "span", "known", "context", "tool"]},
   ],
   "notes": (
      "The exact rate is 3 * cubic t^2 + 2 * square t + linear on [start, stop], whose antiderivative "
      "cubic t^3 + square t^2 + linear t has integer values; the backward direction gives the value at stop and "
      "asks for the value at start. The calculator rate is base_rate + swing * sin(t^2 / stretch) on [0, horizon], "
      "which has no elementary antiderivative. Stretch 5 with horizon 4 is excluded because the integral of the "
      "sine term is then within 0.0002 of 2, which would round the key to a whole number."
   ),
}

CONTEXTS = {
   "tank": ("Water flows into and out of a tank", "the amount of water in the tank", "gallons", "gallons per hour", "hours"),
   "pile": ("Sand is added to and removed from a pile", "the amount of sand in the pile", "tons", "tons per hour", "hours"),
   "balloon": ("Air is pumped into a balloon and leaks out of it", "the volume of air in the balloon", "liters", "liters per minute", "minutes"),
}

t = sympy.Symbol("t")


def _rounded_early(integral_value, known):
   """The integral rounded to one place before it is added, or to a whole number when one place
   happens to agree with the key at three decimals."""
   key = known + integral_value

   for places in (1, 0):
      early = known + sympy.Rational(str(round(float(integral_value), places)))
      coincides = round(float(early), 3) == round(float(key), 3)

      if not coincides:
         return early, places

   return known + sympy.Integer(round(float(integral_value)) + 1), -1


def build(names):
   if names["tool"] == "calculator":
      return _calculator_item(names)

   return _exact_item(names)


def _exact_item(names):
   opening, quantity, unit, rate_unit, time_unit = CONTEXTS[names["context"]]
   start = names["start"]
   stop = names["stop"]
   known = names["known"]
   antiderivative = names["cubic"] * t**3 + names["square"] * t**2 + names["linear"] * t
   rate = sympy.diff(antiderivative, t)
   change = antiderivative.subs(t, stop) - antiderivative.subs(t, start)
   rate_difference = rate.subs(t, stop) - rate.subs(t, start)
   is_forward = names["direction"] == "forward"
   change_tex = r"\left(" + tex(change) + r"\right)" if change < 0 else tex(change)
   integral_tex = rf"\int_{{{start}}}^{{{stop}}} \left({tex(rate)}\right)\,dt"
   rate_text = math(f"R(t) = {tex(rate)}")
   window_text = math(r"t \ge 0")

   if is_forward:
      known_time, asked_time = start, stop
      key_value = known + change
      relation = math(f"A({stop}) = A({start}) + " + integral_tex)
      combine = math(f"A({stop}) = {known} + {change_tex} = {tex(key_value)}")
   else:
      known_time, asked_time = stop, start
      key_value = known - change
      relation = math(f"A({start}) = A({stop}) - " + integral_tex)
      combine = math(f"A({start}) = {known} - {change_tex} = {tex(key_value)}")

   stem = (
      f"{opening}. Let A(t) be {quantity}, in {unit}, at time t {time_unit}, for {window_text}. The rate of change of "
      f"A is {rate_text} {rate_unit}. At time t = {known_time}, there are {known} {unit}. Find the value of "
      f"{math(f'A({asked_time})')}, in {unit}, and show the setup for the calculation."
   )

   antiderivative_text = math(r"\left[" + tex(antiderivative) + r"\right]_{" + str(start) + "}^{" + str(stop) + "} = " + tex(change))
   steps = [
      Step(text=f"The known value and the accumulated change combine as {relation}.", point_type_id="BC-PT-99033", rule="net change theorem"),
      Step(
         text=f"An antiderivative of the rate is {math(tex(antiderivative))}, so the integral is {antiderivative_text}.",
         value=change,
         point_type_id="BC-PT-99003",
         rule="Fundamental Theorem of Calculus",
      ),
      Step(text=f"So {combine} {unit}.", value=key_value, point_type_id="BC-PT-99004", rule="combine with the known value"),
   ]

   sign = 1 if is_forward else -1
   upper_only = antiderivative.subs(t, stop) if is_forward else antiderivative.subs(t, start)
   distractors = [
      Distractor(
         error_path="BC-ERR-06015",
         derivation=f"the integral of the rate from {start} to {stop} reported as the amount, with the known {known} {unit} left out",
         value=change,
         mechanism="forgot_constant",
      ),
      Distractor(
         error_path="BC-ERR-99012",
         derivation=f"the rate treated as its own antiderivative, so the change is taken as R({stop}) - R({start})",
         value=known + sign * rate_difference,
         mechanism="conceptual_confusion",
      ),
   ]

   if is_forward:
      distractors.append(Distractor(
         error_path="BC-ERR-99012",
         derivation=f"the antiderivative evaluated only at the upper limit {stop}, ignoring its value at the lower limit {start}",
         value=known + upper_only,
         mechanism="wrong_limits",
      ))
   else:
      distractors.append(Distractor(
         error_path="BC-ERR-99012",
         derivation=f"the limits run backward from {stop} to {start} but the change still added, so its sign is wrong",
         value=known + change,
         mechanism="sign_error",
      ))

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value, units=unit),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="no_calculator",
      command_verb="find",
   )


def _calculator_item(names):
   opening, quantity, unit, rate_unit, time_unit = CONTEXTS[names["context"]]
   known = names["known"]
   horizon = sympy.nsimplify(names["horizon"])
   rate = names["base_rate"] + names["swing"] * sympy.sin(t**2 / names["stretch"])
   degree_rate = names["base_rate"] + names["swing"] * sympy.sin(sympy.pi / 180 * t**2 / names["stretch"])
   integral_value = numeric_integral(rate, t, 0, horizon)
   degree_value = numeric_integral(degree_rate, t, 0, horizon)
   key_value = known + integral_value
   early_value, places = _rounded_early(integral_value, known)
   horizon_text = f"{float(horizon):g}"
   integral_tex = rf"\int_{{0}}^{{{horizon_text}}} R(t)\,dt"
   rate_text = math(f"R(t) = {tex(rate)}")
   window_text = math(r"t \ge 0")

   stem = (
      f"{opening}. Let A(t) be {quantity}, in {unit}, at time t {time_unit}, for {window_text}. The rate of change of "
      f"A is {rate_text} {rate_unit}. At time t = 0, there are {known} {unit}. Using a calculator, find "
      f"{math(f'A({horizon_text})')}. Show the setup for the calculation, and give the value correct to three decimal "
      "places."
   )

   relation = math(f"A({horizon_text}) = {known} + " + integral_tex)
   steps = [
      Step(text=f"The known value and the accumulated change combine as {relation}.", point_type_id="BC-PT-99033", rule="net change theorem"),
      Step(
         text=f"With a calculator in radian mode, {math(integral_tex)} is approximately {decimal_text(integral_value)} (more places are kept).",
         value=integral_value,
         point_type_id="BC-PT-99001",
         rule="numerical integration",
      ),
      Step(
         text=f"So {math(f'A({horizon_text})')} is about {decimal_text(key_value)} {unit}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="combine with the known value",
      ),
   ]

   if places == 1:
      rounding = "the integral rounded to one decimal place before the known amount is added"
   elif places == 0:
      rounding = "the integral rounded to a whole number before the known amount is added"
   else:
      rounding = "the integral rounded up to the next whole number before the known amount is added"

   distractors = [
      Distractor(
         error_path="BC-ERR-06015",
         derivation=f"the integral of the rate over [0, {horizon}] reported as the amount, with the initial {known} {unit} left out",
         value=integral_value,
         mechanism="forgot_constant",
      ),
      Distractor(
         error_path="BC-ERR-06032",
         derivation="the integral computed with the calculator in degree mode",
         value=known + degree_value,
         mechanism="algebra_slip",
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
      key=Key(form="numeric", value=key_value, decimals=3, units=unit),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
