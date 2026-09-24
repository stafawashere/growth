"""BC-QA-09012, the area of a region bounded by a single polar curve, exact value without a calculator."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-09012"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "shape", "type": "label", "role": "difficulty", "domain": {"values": ["petal", "limacon"]}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "frequency", "type": "integer", "role": "safe", "domain": {"values": [2, 3, 4]}},
      {"name": "trig", "type": "label", "role": "safe", "domain": {"values": ["sin", "cos"]}},
      {"name": "sweep", "type": "label", "role": "safe", "domain": {"values": ["full", "first", "second", "third", "fourth"]}},
   ],
   "constraints": [
      "shape == 'petal' or constant > coefficient",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
      "finite(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "shape", "difficulty_factor_id": "BC-DF-14", "settings": {"limacon": "off", "petal": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-13", "figure_kind": None, "requires": ["shape", "constant", "coefficient", "frequency", "trig", "sweep"]},
   ],
   "notes": "A petal of r = coefficient trig(k theta) has its limits found from consecutive zeros of r; the limacon-type curve r = constant + coefficient trig(k theta) with constant above coefficient never reaches the origin, so each stated sweep of angles covers the region once. The petal ignores constant and sweep.",
}

theta = sympy.Symbol("theta")
SWEEPS = {
   "full": (sympy.Integer(0), 2 * sympy.pi),
   "first": (sympy.Integer(0), sympy.pi / 2),
   "second": (sympy.pi / 2, sympy.pi),
   "third": (sympy.pi, 3 * sympy.pi / 2),
   "fourth": (3 * sympy.pi / 2, 2 * sympy.pi),
}
WRONG_SWEEPS = {
   "full": (sympy.Integer(0), sympy.pi),
   "first": (sympy.Integer(0), 2 * sympy.pi),
   "second": (sympy.Integer(0), 2 * sympy.pi),
   "third": (sympy.Integer(0), 2 * sympy.pi),
   "fourth": (sympy.Integer(0), 2 * sympy.pi),
}


def _half_integral(integrand, limits):
   return sympy.simplify(sympy.integrate(integrand, (theta, limits[0], limits[1])) / 2)


def _limits_tex(limits):
   return tex(limits[0]), tex(limits[1])


def build(names):
   coefficient = names["coefficient"]
   frequency = names["frequency"]
   trig_function = sympy.sin if names["trig"] == "sin" else sympy.cos
   is_petal = names["shape"] == "petal"

   if is_petal:
      radius = coefficient * trig_function(frequency * theta)

      if names["trig"] == "sin":
         limits = (sympy.Integer(0), sympy.pi / frequency)
      else:
         limits = (-sympy.pi / (2 * frequency), sympy.pi / (2 * frequency))

      wrong_limits = (sympy.Integer(0), 2 * sympy.pi)
      stem = (
         f"The polar curve {math('r = ' + tex(radius))} is a rose with {2 * frequency if frequency % 2 == 0 else frequency} "
         "petals. Find the exact area of the region enclosed by one petal."
      )
      low_tex, high_tex = _limits_tex(limits)
      limits_step = Step(
         text=(
            f"One petal is traced between consecutive zeros of r, so the angles run from {math(r'\theta = ' + low_tex)} to "
            f"{math(r'\theta = ' + high_tex)}, where {math(tex(radius) + ' = 0')}."
         ),
         point_type_id="BC-PT-99001",
         rule="limits from zeros of r",
      )
   else:
      radius = names["constant"] + coefficient * trig_function(frequency * theta)
      limits = SWEEPS[names["sweep"]]
      wrong_limits = WRONG_SWEEPS[names["sweep"]]
      low_tex, high_tex = _limits_tex(limits)

      if names["sweep"] == "full":
         stem = f"Find the exact area of the region enclosed by the polar curve {math('r = ' + tex(radius))}."
         limit_reason = "Since r is never 0, the curve is traced once as the angle runs over a full turn"
      else:
         stem = (
            f"Find the exact area of the region bounded by the polar curve {math('r = ' + tex(radius))} and the rays "
            f"{math(r'\theta = ' + low_tex)} and {math(r'\theta = ' + high_tex)}."
         )
         limit_reason = "The two rays bound the angles of the region"

      limits_step = Step(
         text=f"{limit_reason}, so the angles run from {math(low_tex)} to {math(high_tex)}.",
         point_type_id="BC-PT-99001",
         rule="limits of the sweep",
      )

   key_value = _half_integral(radius**2, limits)
   no_half = 2 * key_value
   no_square = _half_integral(radius, limits)
   wrong_sweep = _half_integral(radius**2, wrong_limits)

   integral_tex = rf"\frac{{1}}{{2}}\int_{{{low_tex}}}^{{{high_tex}}} \left({tex(radius)}\right)^2\,d\theta"
   steps = [
      limits_step,
      Step(
         text=f"The area is one half the integral of the square of r: {math('A = ' + integral_tex)}.",
         point_type_id="BC-PT-99048",
         rule="polar area",
      ),
      Step(
         text=(
            f"Expand the square and use {math(r'\sin^2 u = \tfrac{1}{2}(1 - \cos 2u)')} or "
            f"{math(r'\cos^2 u = \tfrac{1}{2}(1 + \cos 2u)')} to integrate, giving {math('A = ' + tex(key_value))}."
         ),
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="power reduction",
      ),
   ]

   wrong_low, wrong_high = (str(sympy.sstr(end)).replace("*", " ") for end in wrong_limits)
   traces_twice = is_petal and frequency % 2 == 1
   sweep_error = "BC-ERR-09016" if traces_twice else "BC-ERR-09037"
   distractors = [
      Distractor(
         error_path="BC-ERR-09035",
         derivation="the factor of one half left off the polar area integral",
         value=no_half,
         mechanism="forgot_constant",
      ),
      Distractor(
         error_path="BC-ERR-09036",
         derivation="r integrated without being squared, one half the integral of r",
         value=no_square,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path=sweep_error,
         derivation=f"the area integral taken from {wrong_low} to {wrong_high} instead of over the angles that sweep the region",
         value=wrong_sweep,
         mechanism="wrong_limits",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-13",
      calculator_status="no_calculator",
      command_verb="find",
   )
