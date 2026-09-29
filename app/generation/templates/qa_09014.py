"""BC-QA-09014, the area of a polar region asked for before the polar area integral is taught."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-09014"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 15 of 2026-09-28"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "region", "type": "label", "role": "difficulty", "domain": {"values": ["full", "half", "quarter"]}},
      {"name": "trig", "type": "label", "role": "safe", "domain": {"values": ["cos", "sin"]}},
      {"name": "frequency", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "base", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 15, "step": 1}},
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": -14, "max": 14, "step": 1, "exclude": [0]}},
   ],
   "constraints": [
      "abs(amplitude) < base",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "region", "difficulty_factor_id": "BC-DF-06", "settings": {"full": "low", "half": "low", "quarter": "medium"}},
      {"parameter": "region", "difficulty_factor_id": "BC-DF-15", "settings": {"full": "low", "half": "low", "quarter": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-13", "figure_kind": None, "requires": ["region", "trig", "frequency", "base", "amplitude"]},
   ],
   "notes": "r = a + b cos(k theta) or a + b sin(k theta) with 0 < |b| < a, so r > 0 and the curve is traced once on [0, 2 pi]. The region is the whole enclosed region, or the part swept between the rays theta = 0 and theta = pi or pi/2. The stem names no method: it is the productive-failure opener for BC-CON-09015, and the canonical solution builds the area from thin sectors of area one half r squared d theta. The distractors drop the one half, integrate r instead of r squared, or sweep the wrong angles.",
}

theta = sympy.Symbol("theta")

REGIONS = {
   "full": (0, 2 * sympy.pi),
   "half": (0, sympy.pi),
   "quarter": (0, sympy.pi / 2),
}
WRONG_SWEEP = {
   "full": (0, sympy.pi),
   "half": (0, sympy.pi / 2),
   "quarter": (0, 2 * sympy.pi),
}


def _half_integral(expression, bounds):
   low, high = bounds

   return sympy.simplify(sympy.integrate(expression, (theta, low, high)) / 2)


def build(names):
   region = names["region"]
   base = int(names["base"])
   amplitude = int(names["amplitude"])
   frequency = int(names["frequency"])
   wave = sympy.cos(frequency * theta) if names["trig"] == "cos" else sympy.sin(frequency * theta)
   radius = base + amplitude * wave
   low, high = REGIONS[region]

   key_value = _half_integral(radius**2, REGIONS[region])
   curve = math("r = " + tex(radius))

   if region == "full":
      stem = f"Find the area of the region enclosed by the polar curve {curve}."
   else:
      bounds = math(rf"0 \le \theta \le {tex(high)}")
      stem = (
         f"Find the area of the region bounded by the polar curve {curve} for {bounds} and the rays "
         f"{math(r'\theta = 0')} and {math(r'\theta = ' + tex(high))}."
      )

   integral = rf"\frac{{1}}{{2}} \int_{{{tex(low)}}}^{{{tex(high)}}} \left({tex(radius)}\right)^{{2}}\,d\theta"
   steps = [
      Step(
         text=(
            r"Cut the region into thin sectors by rays from the pole. A sector of radius r and small angle "
            rf"{math(r'\Delta\theta')} has area {math(r'\frac{1}{2} r^{2} \Delta\theta')}, the fraction "
            rf"{math(r'\frac{\Delta\theta}{2\pi}')} of the disc of area {math(r'\pi r^{2}')}."
         ),
         rule="area of a circular sector",
      ),
      Step(
         text=(
            f"Adding the sectors and letting the angles shrink turns the sum into an integral over the angles the region sweeps, "
            f"so the area is {math(integral)}."
         ),
         point_type_id="BC-PT-99048",
         rule="polar area integral",
      ),
      Step(
         text=f"Evaluating the integral gives {math(tex(key_value))}.",
         value=key_value,
         rule="definite integral evaluated",
      ),
   ]
   wrong_low, wrong_high = WRONG_SWEEP[region]
   distractors = [
      Distractor("BC-ERR-09035", "the sector area taken as r squared times the angle, so the factor one half is lost", value=2 * key_value, mechanism="algebra_slip"),
      Distractor("BC-ERR-09036", "the radius integrated instead of its square", value=_half_integral(radius, REGIONS[region]), mechanism="conceptual_confusion"),
      Distractor("BC-ERR-09037", f"the angles swept taken as {tex(wrong_low)} to {tex(wrong_high)} instead of the region's own angles", value=_half_integral(radius**2, WRONG_SWEEP[region]), mechanism="wrong_limits"),
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
