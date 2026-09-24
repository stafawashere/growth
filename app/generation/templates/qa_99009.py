"""BC-QA-99009, a density accumulated over depth and scaled by a constant cross-section, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_integral, tex

ARCHETYPE_ID = "BC-QA-99009"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "surface_density", "type": "integer", "role": "safe", "domain": {"min": 20, "max": 60, "step": 5}},
      {"name": "swing", "type": "integer", "role": "safe", "domain": {"min": 4, "max": 12, "step": 2}},
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "top", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 2, "step": 1}},
      {"name": "thickness", "type": "integer", "role": "safe", "domain": {"min": 3, "max": 6, "step": 1}},
      {"name": "side", "type": "rational", "role": "safe", "domain": {"values": ["3/2", "2", "5/2", "3", "7/2"]}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["plankton", "sediment"]}},
      {"name": "area_form", "type": "label", "role": "difficulty", "domain": {"values": ["area", "side"]}},
   ],
   "constraints": [
      "side**2 != thickness",
      "not (stretch == 2 and top == 2 and thickness == 3 and side == Rational(7, 2))",
   ],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "area_form", "difficulty_factor_id": "BC-DF-11", "settings": {"area": "off", "side": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {
         "representation": "BC-REP-05",
         "figure_kind": None,
         "requires": ["surface_density", "swing", "stretch", "top", "thickness", "side", "context"],
      },
   ],
   "notes": "The density is surface_density + swing sin(h^2 / stretch) per cubic meter, positive because surface_density exceeds swing; the column has a square horizontal cross-section, given either by its area or by its side. The area never equals the thickness, so dropping the area and dividing by the thickness give different numbers. Four draws with stretch 2 on [2, 5] and side 3.5 land within 0.0005 of a whole number, so that combination is excluded.",
}

CONTEXTS = {
   "plankton": ("plankton", "cells per cubic meter", "a vertical column of lake water", "the number of plankton cells", "cells"),
   "sediment": ("suspended sediment", "grams per cubic meter", "a vertical column of river water", "the mass, in grams, of sediment", "grams"),
}

h = sympy.Symbol("h")
DEGREE = sympy.pi / 180


def build(names):
   surface_density = names["surface_density"]
   swing = names["swing"]
   stretch = names["stretch"]
   top = names["top"]
   bottom = top + names["thickness"]
   side = names["side"]
   area = side**2
   is_side = names["area_form"] == "side"
   quantity, density_units, column, request, count_units = CONTEXTS[names["context"]]

   density = surface_density + swing * sympy.sin(h**2 / stretch)
   integral_value = numeric_integral(density, h, top, bottom)
   key_value = area * integral_value
   degree_value = area * numeric_integral(surface_density + swing * sympy.sin(h**2 / stretch * DEGREE), h, top, bottom)
   average_times_area = key_value / (bottom - top)

   side_text = f"{float(side):g}"
   area_text = f"{float(area):g}"

   if is_side:
      cross_section = f"horizontal cross-sections that are squares with side {side_text} meters"
   else:
      cross_section = f"horizontal cross-sections of constant area {area_text} square meters"

   stem = (
      f"The density of {quantity} in {column} is modeled by {math(r'\rho(h) = ' + tex(density))} {density_units}, where h "
      f"is the depth below the surface in meters. Consider the column, which has {cross_section}. Using a calculator, "
      f"find {request} in the column between the depths "
      f"{math(f'h = {top}')} and {math(f'h = {bottom}')} meters. Show the setup, and give the value correct to three "
      "decimal places."
   )

   area_step_text = (
      f"Each cross-section is a square of side {side_text}, so its area is {math(f'{side_text}^2 = {area_text}')} square meters. "
      if is_side else ""
   )
   integral_tex = rf"{area_text}\int_{{{top}}}^{{{bottom}}} \left({tex(density)}\right)\,dh"
   steps = [
      Step(
         text=(
            f"{area_step_text}A thin slab of thickness dh holds about {math(area_text + r'\,\rho(h)\,dh')}, so the total is "
            f"{math(integral_tex)}."
         ),
         point_type_id=None,
         rule="accumulation of a density",
      ),
      Step(
         text=f"With the calculator in radian mode the integral is about {decimal_text(integral_value)}.",
         value=integral_value,
         rule="numerical integration",
      ),
      Step(
         text=f"Multiplying by the area {area_text} gives about {decimal_text(key_value)}.",
         value=key_value,
         rule="constant cross-section",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-99005",
         derivation="the integral of the density reported without the area, an amount per square meter given as the count",
         value=integral_value,
         mechanism="forgot_constant",
      ),
      Distractor(
         error_path="BC-ERR-06032",
         derivation="the integral evaluated with the calculator in degree mode, then multiplied by the area",
         value=degree_value,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-99015",
         derivation="the result divided by the thickness of the layer, the average density times the area reported",
         value=average_times_area,
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=key_value, decimals=3, units=count_units),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
