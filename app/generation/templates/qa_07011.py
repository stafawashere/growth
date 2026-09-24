"""BC-QA-07011, a particular solution with the interval on which it holds, or written in accumulation form."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-07011"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["restricted", "accumulation"]}},
      {"name": "rate", "type": "integer", "role": "safe", "domain": {"values": [-3, -2, -1, 1, 2, 3]}},
      {"name": "initial", "type": "rational", "role": "safe", "domain": {"values": ["-3", "-2", "-1", "-1/2", "1/2", "1", "2", "3"]}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "integrand", "type": "label", "role": "safe", "domain": {"values": ["gauss", "sine", "cosine", "root"]}},
   ],
   "constraints": [],
   "derived": [
      {"name": "blowup", "expression": "start + 1 / (rate * initial)"},
   ],
   "invariants": [
      "len(key) > 20",
      "blowup != start",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-03", "settings": {"restricted": "off", "accumulation": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-06", "figure_kind": None, "requires": ["form", "rate", "initial", "start", "integrand"]},
   ],
   "notes": "The restricted form is dy/dx = k y^2 with y(x0) = y0, solved to 1 / (1/y0 - k (x - x0)), which blows up at x0 + 1/(k y0); the interval is the side containing x0, left of the blowup when k y0 > 0 and right of it otherwise, so both sides occur. The accumulation form is dy/dx = f(x) with f having no elementary antiderivative, solved to y0 plus the integral from x0 to x.",
}

x = sympy.Symbol("x")
t = sympy.Symbol("t")

INTEGRANDS = {
   "gauss": sympy.exp(-t**2),
   "sine": sympy.sin(t**2),
   "cosine": sympy.cos(t**2),
   "root": sympy.sqrt(1 + t**4),
}


def _with_interval(solution, boundary, left_side):
   relation = "<" if left_side else ">"

   return f"{math('y = ' + tex(solution))}, for {math(f'x {relation} {tex(boundary)}')}"


def _restricted(rate, initial, start):
   denominator = 1 / initial - rate * (x - start)
   solution = sympy.cancel(1 / denominator)
   blowup = start + 1 / (rate * initial)
   left_side = rate * initial > 0
   wrong_solution = sympy.cancel(1 / (rate * (x - start) + 1 / initial))
   wrong_blowup = start - 1 / (rate * initial)
   wrong_left_side = rate * initial < 0

   equation = rf"\frac{{dy}}{{dx}} = {tex(rate * sympy.Symbol('y')**2)}"
   stem = (
      f"Find the particular solution to the differential equation {math(equation)} with the initial condition "
      f"{math(f'y({start}) = {tex(initial)}')}, and state the interval on which the solution is valid."
   )

   side_word = "left" if left_side else "right"
   relation = "<" if left_side else ">"
   steps = [
      Step(
         text=(
            f"Separate and antidifferentiate: {math(rf'\int y^{{-2}}\,dy = \int {tex(rate)}\,dx')} gives "
            f"{math(rf'-\frac{{1}}{{y}} = {tex(rate * x)} + C')}, and the initial condition gives {math(f'C = {tex(-1 / initial - rate * start)}')}."
         ),
         rule="separation of variables",
      ),
      Step(
         text=f"Solving for y, {math('y = ' + tex(solution))}, which is undefined at {math(f'x = {tex(blowup)}')}.",
         rule="solve for y",
      ),
      Step(
         text=(
            f"A solution must be differentiable on an interval containing the initial input {start}, which lies to the "
            f"{side_word} of {math(tex(blowup))}, so the solution is valid for {math(f'x {relation} {tex(blowup)}')}."
         ),
         rule="interval of validity",
      ),
   ]

   key_label = _with_interval(solution, blowup, left_side)
   distractors = [
      Distractor(
         error_path="BC-ERR-07031",
         derivation=f"the domain taken as every x except the point x = {tex(blowup)}, which is not an interval",
         label=f"{math('y = ' + tex(solution))}, for all {math(rf'x \ne {tex(blowup)}')}",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-07031",
         derivation=f"the interval chosen on the side of x = {tex(blowup)} that does not contain the initial input {start}",
         label=_with_interval(solution, blowup, not left_side),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99014",
         derivation="y^(-2) antidifferentiated as 1/y instead of -1/y, and the interval then read from that wrong solution",
         label=_with_interval(wrong_solution, wrong_blowup, wrong_left_side),
         mechanism="sign_error",
      ),
   ]

   return stem, steps, key_label, distractors


def _accumulation(integrand, initial, start):
   rate_tex = tex(integrand.subs(t, x))
   integral_tex = rf"\int_{{{start}}}^{{x}} {tex(integrand)}\,dt"
   stem = (
      f"Find the particular solution to the differential equation {math(rf'\frac{{dy}}{{dx}} = {rate_tex}')} with the initial condition "
      f"{math(f'y({start}) = {tex(initial)}')}, written in terms of a definite integral."
   )

   steps = [
      Step(
         text=f"The right side depends on x alone and has no elementary antiderivative, so accumulate it from the initial input: {math(integral_tex)} is the change in y from x = {start}.",
         rule="accumulation of a rate",
      ),
      Step(
         text=f"Add the initial value: {math(f'y = {tex(initial)} + ' + integral_tex)}, which equals {math(tex(initial))} at x = {start} and has derivative {math(rate_tex)}.",
         rule="initial value plus the accumulated change",
      ),
   ]

   key_label = math(f"y = {tex(initial)} + " + integral_tex)
   distractors = [
      Distractor(
         error_path="BC-ERR-07032",
         derivation="the accumulated change written alone, without the initial value",
         label=math("y = " + integral_tex),
         mechanism="forgot_constant",
      ),
      Distractor(
         error_path="BC-ERR-07032",
         derivation="the initial value and the integral written with the differential dt left off",
         label=math(f"y = {tex(initial)} + " + rf"\int_{{{start}}}^{{x}} {tex(integrand)}"),
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-07038",
         derivation="the given rate treated as though it were the quantity itself, shifted to pass through the initial point",
         label=math("y = " + tex(initial + integrand.subs(t, x) - integrand.subs(t, start))),
         mechanism="conceptual_confusion",
      ),
   ]

   return stem, steps, key_label, distractors


def build(names):
   initial = sympy.Rational(names["initial"])
   start = int(names["start"])

   if names["form"] == "restricted":
      stem, steps, key_label, distractors = _restricted(int(names["rate"]), initial, start)
   else:
      stem, steps, key_label, distractors = _accumulation(INTEGRANDS[names["integrand"]], initial, start)

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-06",
      calculator_status="no_calculator",
      command_verb="find",
   )
