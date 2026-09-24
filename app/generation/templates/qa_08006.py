"""BC-QA-08006, the time at which an accumulated amount is greatest, justified by a candidates test, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_roots
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-08006"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "period", "type": "integer", "role": "safe", "domain": {"values": [8, 10, 12, 16, 20, 24]}},
      {"name": "net", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "times", "type": "rational", "role": "safe", "domain": {"values": ["4/3", "3/2", "2", "3", "4", "5", "6", "8", "10"]}},
      {"name": "outflow", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "initial", "type": "integer", "role": "safe", "domain": {"min": 20, "max": 200, "step": 10}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["water", "sand", "oil"]}},
      {"name": "presentation", "type": "label", "role": "difficulty", "domain": {"values": ["net_rate", "in_and_out"]}},
   ],
   "constraints": [
      "is_integer(swing)",
      "swing <= 40",
   ],
   "derived": [
      {"name": "swing", "expression": "net * times"},
      {"name": "inflow_base", "expression": "outflow + net"},
   ],
   "invariants": [
      "winner_amount > runner_up_amount",
   ],
   "dial_bindings": [
      {"parameter": "presentation", "difficulty_factor_id": "BC-DF-12", "settings": {"net_rate": "off", "in_and_out": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["period", "net", "times", "outflow", "initial", "context", "presentation"]},
   ],
   "notes": "The net rate is net + swing cos(2 pi t / period) on one full period, with swing = net times 'times' and times above 1, so it changes sign twice: a local maximum, then a local minimum. The ratio 1/times decides the winner: at a quarter or more, the gain after the local minimum outweighs the dip and the absolute maximum is the right endpoint; at a fifth or less the interior local maximum wins. The band between is excluded by the domain of times, so no draw is close to a tie.",
}

CONTEXTS = {
   "water": ("water", "a storage tank", "the tank", "gallons", "hours"),
   "sand": ("sand", "a pile at a work site", "the pile", "tons", "hours"),
   "oil": ("oil", "a holding tank", "the tank", "barrels", "hours"),
}

t = sympy.Symbol("t")
s = sympy.Symbol("s")


def build(names):
   period = names["period"]
   swing = names["swing"]
   net = names["net"]
   outflow = names["outflow"]
   initial = names["initial"]
   inflow_base = names["inflow_base"]
   is_split = names["presentation"] == "in_and_out"
   material, holder, holder_again, units, time_units = CONTEXTS[names["context"]]

   wave = swing * sympy.cos(2 * sympy.pi * t / period)
   net_rate = net + wave
   amount = initial + net * t + sympy.integrate(wave, t)

   critical_times = numeric_roots(net_rate, t, 0, period, pieces=397)
   local_max_time, local_min_time = critical_times
   local_max_amount = amount.subs(t, local_max_time).evalf(30)
   local_min_amount = amount.subs(t, local_min_time).evalf(30)
   end_amount = initial + net * period
   change_only = net * period

   window = rf"0 \le t \le {period}"

   if is_split:
      inflow = inflow_base + wave
      rate_sentence = (
         f"{material.capitalize()} is added to {holder} at the rate {math('r(t) = ' + tex_f(inflow))} {units} per "
         f"{time_units[:-1]}, and removed at the constant rate of {outflow} {units} per {time_units[:-1]}, for {math(window)}."
      )
      derivative_text = f"{math(r"A'(t) = r(t) - " + str(outflow) + ' = ' + tex_f(net_rate))}"
   else:
      rate_sentence = (
         f"The amount of {material} in {holder} changes at the rate {math(r"A'(t) = " + tex_f(net_rate))} {units} per "
         f"{time_units[:-1]} for {math(window)}."
      )
      derivative_text = f"{math(r"A'(t) = " + tex_f(net_rate))}"

   stem = (
      f"{rate_sentence} At time {math('t = 0')} there are {initial} {units} of {material} in {holder_again}, and t is measured "
      f"in {time_units}. Using a calculator, find the time in {math(window)} at which the amount A(t) of {material} "
      "is greatest, and justify the answer. Show the setup for the calculations."
   )

   amount_setup = rf"A(t) = {initial} + \int_{{0}}^{{t}} \left({tex_f(net_rate.subs(t, s))}\right)\,ds"
   first = decimal_text(local_max_time)
   second = decimal_text(local_min_time)

   start_value = f"A(0) = {initial}"
   max_value = rf"A({first}) \approx {decimal_text(local_max_amount)}"
   min_value = rf"A({second}) \approx {decimal_text(local_min_amount)}"
   end_value = rf"A({period}) = {initial} + \int_{{0}}^{{{period}}} A'(s)\,ds = {end_amount}"

   steps = [
      Step(
         text=(
            f"The amount is {math(amount_setup)}, so {derivative_text}. Setting {math(r"A'(t) = 0")} and solving "
            f"with a calculator gives {math('t = ' + first)} and {math('t = ' + second)} in the interval."
         ),
         point_type_id="BC-PT-99013",
         rule="critical points of an accumulation function",
      ),
      Step(
         text=(
            f"The candidates are the critical points and both endpoints: {math(start_value)}, {math(max_value)}, "
            f"{math(min_value)}, and {math(end_value)}."
         ),
         point_type_id="BC-PT-99064",
         rule="candidates test",
      ),
      Step(
         text=(
            f"The largest candidate value is {end_amount}, at the endpoint, so the amount is greatest at "
            f"{math(f't = {period}')} {time_units}."
         ),
         point_type_id="BC-PT-99011",
         rule="candidates test conclusion",
      ),
   ]

   def option(time_text, value_text, reason):
      return f"The amount is greatest at t = {time_text}, where A is {value_text} {units}, {reason}."

   every_candidate = f"the largest of the values of A at t = 0, at both critical points and at t = {period}"
   endpoint_wins = end_amount > local_max_amount

   if endpoint_wins:
      conclusion = f"The largest candidate value is {end_amount}, at the endpoint, so the amount is greatest at {math(f't = {period}')} {time_units}."
      key_label = option(period, end_amount, every_candidate)
      distractors = [
         Distractor(
            error_path="BC-ERR-08016",
            derivation="the candidates test run on the two critical points only, leaving out both endpoints",
            label=option(first, decimal_text(local_max_amount), "the larger of the values of A at the two critical points"),
            mechanism="theorem_condition_ignored",
         ),
         Distractor(
            error_path="BC-ERR-99004",
            derivation="the sign change of A' from positive to negative at the first critical point taken as proof of the absolute maximum",
            label=option(first, decimal_text(local_max_amount), "because A' changes from positive to negative there"),
            mechanism="theorem_condition_ignored",
         ),
         Distractor(
            error_path="BC-ERR-08011",
            derivation="the amount at each candidate found from the integral alone, without the initial amount",
            label=option(period, change_only, every_candidate),
            mechanism="forgot_constant",
         ),
      ]
      winner_amount, runner_up_amount = end_amount, local_max_amount
   else:
      conclusion = f"The largest candidate value is about {decimal_text(local_max_amount)}, at the first critical point, so the amount is greatest at {math(f't = {first}')} {time_units}."
      key_label = option(first, decimal_text(local_max_amount), every_candidate)
      distractors = [
         Distractor(
            error_path="BC-ERR-99004",
            derivation="an incomplete candidates test that leaves out the interior critical point where A' changes from positive to negative",
            label=option(period, end_amount, f"the largest of the values of A at t = 0, at t = {second} and at t = {period}"),
            mechanism="theorem_condition_ignored",
         ),
         Distractor(
            error_path="BC-ERR-99004",
            derivation="a local argument at the right end: A' is positive just before the endpoint, so A is taken to be greatest there",
            label=option(period, end_amount, f"because A' is positive on the interval from t = {second} to t = {period}"),
            mechanism="theorem_condition_ignored",
         ),
         Distractor(
            error_path="BC-ERR-08011",
            derivation="the amount at each candidate found from the integral alone, without the initial amount",
            label=option(first, decimal_text(local_max_amount - initial), every_candidate),
            mechanism="forgot_constant",
         ),
      ]
      winner_amount, runner_up_amount = local_max_amount, end_amount

   steps[-1].text = conclusion

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="calculator",
      setup_required=True,
      command_verb="justify",
      notes={"winner_amount": winner_amount, "runner_up_amount": runner_up_amount},
   )
