"""BC-QA-06006, an amount or a net change from an inflow rate and an outflow rate, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_integral, tex

ARCHETYPE_ID = "BC-QA-06006"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "inflow_base", "type": "integer", "role": "safe", "domain": {"min": 4, "max": 9, "step": 1}},
      {"name": "inflow_swing", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"values": [2, 3, 4]}},
      {"name": "outflow_base", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "outflow_swing", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "horizon", "type": "real", "role": "safe", "domain": {"values": [2, 2.5, 3, 3.5, 4]}},
      {"name": "initial", "type": "integer", "role": "safe", "domain": {"min": 20, "max": 90, "step": 5}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["tank", "pond", "silo"]}},
      {"name": "ask", "type": "label", "role": "difficulty", "domain": {"values": ["amount", "change"]}},
   ],
   "constraints": [
      "not (inflow_swing == 3 and stretch == 2 and outflow_swing == 2 and horizon == 5 / 2)",
      "ask == 'change' or initial + (inflow_base - inflow_swing - outflow_base - outflow_swing) * horizon > 0",
   ],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
   ],
   "dial_bindings": [
      {"parameter": "ask", "difficulty_factor_id": "BC-DF-14", "settings": {"amount": "low", "change": "off"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["inflow_base", "inflow_swing", "outflow_base", "outflow_swing", "horizon", "context", "ask"]},
   ],
   "notes": (
      "Inflow E(t) = inflow_base + inflow_swing sin(t^2 / stretch) and outflow L(t) = outflow_base + outflow_swing "
      "cos(t / 2) on [0, horizon]. The amount ask adds the initial amount, the change ask does not. One combination of "
      "swings, stretch and horizon is excluded because its net change rounds to a whole number at three places."
   ),
}

CONTEXTS = {
   "tank": ("Water enters a storage tank", "leaves it", "gallons", "gallons per hour", "hours", "tank"),
   "pond": ("Water flows into a pond from a stream", "drains out of it", "cubic meters", "cubic meters per hour", "hours", "pond"),
   "silo": ("Grain is loaded into a silo", "is unloaded from it", "tons", "tons per hour", "hours", "silo"),
}

t = sympy.Symbol("t")


def build(names):
   entering, leaving, unit, rate_unit, time_unit, place = CONTEXTS[names["context"]]
   horizon = sympy.nsimplify(names["horizon"])
   horizon_text = f"{float(horizon):g}"
   initial = names["initial"]
   is_amount = names["ask"] == "amount"

   inflow = names["inflow_base"] + names["inflow_swing"] * sympy.sin(t**2 / names["stretch"])
   outflow_base = names["outflow_base"]
   outflow_wave = names["outflow_swing"] * sympy.cos(t / 2)
   outflow = outflow_base + outflow_wave
   degree_inflow = names["inflow_base"] + names["inflow_swing"] * sympy.sin(sympy.pi / 180 * t**2 / names["stretch"])
   degree_outflow = outflow_base + names["outflow_swing"] * sympy.cos(sympy.pi / 180 * t / 2)

   net_change = numeric_integral(inflow - outflow, t, 0, horizon)
   added_change = numeric_integral(inflow + outflow, t, 0, horizon)
   dropped_parentheses = numeric_integral(inflow - outflow_base + outflow_wave, t, 0, horizon)
   degree_change = numeric_integral(degree_inflow - degree_outflow, t, 0, horizon)
   level = initial if is_amount else 0
   key_value = level + net_change

   inflow_text = math(f"E(t) = {tex(inflow)}")
   outflow_text = math(f"L(t) = {tex(outflow)}")
   window_text = math(r"0 \le t \le " + horizon_text)
   integral_tex = rf"\int_{{0}}^{{{horizon_text}}} \left(E(t) - L(t)\right)\,dt"

   stem = (
      f"{entering} at a rate modeled by {inflow_text} {rate_unit} and {leaving} at a rate modeled by {outflow_text} "
      f"{rate_unit}, for {window_text}, where t is measured in {time_unit}."
   )

   if is_amount:
      stem += (
         f" At time t = 0 the {place} holds {initial} {unit}. Using a calculator, find the amount in the {place} at "
         f"time t = {horizon_text}."
      )
      setup = math(f"{initial} + " + integral_tex)
   else:
      stem += (
         f" Using a calculator, find the net change in the amount in the {place} from t = 0 to t = {horizon_text}."
      )
      setup = math(integral_tex)

   stem += " Show the setup for the calculation, and give the value correct to three decimal places."

   steps = [
      Step(
         text=f"The net rate is inflow minus outflow, {math('E(t) - L(t)')}, so the answer is {setup}.",
         point_type_id="BC-PT-99001",
         rule="net rate as inflow minus outflow",
      ),
      Step(
         text=f"With a calculator in radian mode, {math(integral_tex)} is approximately {decimal_text(net_change)} (more places are kept).",
         value=net_change,
         rule="numerical integration",
      ),
   ]

   if is_amount:
      steps.append(Step(
         text=f"Adding the initial amount gives about {decimal_text(key_value)} {unit}.",
         value=key_value,
         rule="initial amount plus net change",
      ))
   else:
      steps.append(Step(
         text=f"The net change is about {decimal_text(key_value)} {unit}, positive for an increase and negative for a decrease.",
         rule="net change",
      ))

   distractors = [
      Distractor(
         error_path="BC-ERR-08013",
         derivation="the inflow and outflow rates added instead of subtracted",
         value=level + added_change,
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-99009",
         derivation="L(t) substituted without parentheses, so only its constant term is subtracted and its cosine term is added",
         value=level + dropped_parentheses,
         mechanism="algebra_slip",
      ),
   ]

   if is_amount:
      distractors.append(Distractor(
         error_path="BC-ERR-06015",
         derivation=f"the integral of the net rate reported as the amount, with the initial {initial} {unit} left out",
         value=net_change,
         mechanism="forgot_constant",
      ))
   else:
      distractors.append(Distractor(
         error_path="BC-ERR-06032",
         derivation="the integral computed with the calculator in degree mode",
         value=degree_change,
         mechanism="algebra_slip",
      ))

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
