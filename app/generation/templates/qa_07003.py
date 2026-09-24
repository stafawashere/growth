"""BC-QA-07003, the particular solution of a separable differential equation through a given point."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-07003"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["exponential", "square_root"]}},
      {"name": "rate", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1, "exclude": [0]}},
      {"name": "power", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "initial", "type": "integer", "role": "safe", "domain": {"values": [-5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8, 9]}},
   ],
   "constraints": [
      "form == 'exponential' or initial > 0",
      "form == 'exponential' or rate > 0",
      "form == 'square_root' or abs(rate * start**(power + 1)) <= 6 * (power + 1)",
      "form == 'exponential' or initial**2 != rate * start**2",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-06", "settings": {"exponential": "low", "square_root": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-06", "figure_kind": None, "requires": ["form", "rate", "power", "start", "initial"]},
   ],
   "notes": "The exponential form is dy/dx = k x^n y with k a nonzero integer and n from 1 to 4, solved to y0 e^(k (x^(n+1) - x0^(n+1)) / (n+1)); the square root form is dy/dx = k x / y with y0 > 0, solved to the positive root of k x^2 + y0^2 - k x0^2. The antiderivative at the start is at most 6 in size, so values stay moderate. The initial value is never 1 or -1 and never equal to e raised to the antiderivative at the start, so dropping the constant always changes the answer.",
}



def _exponential(rate, power, start, initial, x, y):
   antiderivative = sympy.Rational(rate, power + 1) * x ** (power + 1)
   at_start = antiderivative.subs(x, start)
   key_value = initial * sympy.exp(antiderivative - at_start)
   right_side = rate * x**power * y
   constant = sympy.log(abs(initial)) - at_start

   steps = [
      Step(
         text=f"Separate the variables: {math(rf'\frac{{1}}{{{y}}}\,d{y} = {tex(rate * x**power)}\,d{x}')}.",
         point_type_id="BC-PT-99028",
         rule="separation of variables",
      ),
      Step(
         text=f"Antidifferentiate both sides: {math(rf'\ln|{y}| = {tex(antiderivative)} + C')}.",
         point_type_id="BC-PT-99029",
         rule="antiderivatives of both sides",
      ),
      Step(
         text=(
            f"Use the initial condition before exponentiating: {math(rf'\ln|{initial}| = {tex(at_start)} + C')}, so "
            f"{math('C = ' + tex(constant))}."
         ),
         point_type_id="BC-PT-99031",
         rule="constant from the initial condition",
      ),
      Step(
         text=(
            f"Then {math(rf'|{y}| = {abs(initial)}e^{{{tex(antiderivative - at_start)}}}')}, and {y} has the sign of "
            f"{initial} near the initial point, so {math(f'{y} = ' + tex(key_value))}."
         ),
         value=key_value,
         point_type_id="BC-PT-99032",
         rule="solve for y",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-07026",
         derivation="no constant of integration, so the initial condition is never used",
         value=sympy.exp(antiderivative),
         mechanism="forgot_constant",
      ),
      Distractor(
         error_path="BC-ERR-07029",
         derivation="ln|y| = F(x) + C exponentiated as y = e^F(x) + C, and C then found from the initial condition",
         value=sympy.exp(antiderivative) + initial - sympy.exp(at_start),
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-99014",
         derivation=f"x^{power} antidifferentiated as x^{power + 1} with no division by {power + 1}",
         value=initial * sympy.exp(rate * (x ** (power + 1) - start ** (power + 1))),
         mechanism="algebra_slip",
      ),
   ]

   return right_side, key_value, steps, distractors


def _square_root(rate, start, initial, x, y):
   radicand = rate * x**2 + initial**2 - rate * start**2
   key_value = sympy.sqrt(radicand)
   right_side = rate * x / y
   constant = sympy.Rational(initial**2 - rate * start**2, 2)

   steps = [
      Step(
         text=f"Separate the variables: {math(rf'{y}\,d{y} = {tex(rate * x)}\,d{x}')}.",
         point_type_id="BC-PT-99028",
         rule="separation of variables",
      ),
      Step(
         text=f"Antidifferentiate both sides: {math(rf'\frac{{{y}^2}}{{2}} = {tex(sympy.Rational(rate, 2) * x**2)} + C')}.",
         point_type_id="BC-PT-99029",
         rule="antiderivatives of both sides",
      ),
      Step(
         text=f"The initial condition gives {math(rf'\frac{{{initial**2}}}{{2}} = {tex(sympy.Rational(rate, 2) * start**2)} + C')}, so {math('C = ' + tex(constant))}.",
         point_type_id="BC-PT-99031",
         rule="constant from the initial condition",
      ),
      Step(
         text=(
            f"Then {math(f'{y}^2 = ' + tex(radicand))}, and since {y} is positive at the initial point, take the positive root: "
            f"{math(f'{y} = ' + tex(key_value))}."
         ),
         value=key_value,
         point_type_id="BC-PT-99032",
         rule="solve for y",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-07026",
         derivation="no constant of integration, so y^2 = k x^2 and the initial condition is never used",
         value=sympy.sqrt(rate * x**2),
         mechanism="forgot_constant",
      ),
      Distractor(
         error_path="BC-ERR-07029",
         derivation="the constant added after taking the square root instead of before, then fitted to the initial condition",
         value=sympy.sqrt(rate * x**2) + initial - sympy.sqrt(rate * start**2),
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-99014",
         derivation="y antidifferentiated as y^2 without the factor 1/2 while x keeps its 1/2, so the constant factor is misplaced",
         value=sympy.sqrt(sympy.Rational(rate, 2) * x**2 + initial**2 - sympy.Rational(rate, 2) * start**2),
         mechanism="algebra_slip",
      ),
   ]

   return right_side, key_value, steps, distractors


def build(names):
   rate = int(names["rate"])
   start = int(names["start"])
   initial = int(names["initial"])
   x = sympy.Symbol("x")
   y = sympy.Symbol("y")

   if names["form"] == "exponential":
      right_side, key_value, steps, distractors = _exponential(rate, int(names["power"]), start, initial, x, y)
   else:
      right_side, key_value, steps, distractors = _square_root(rate, start, initial, x, y)

   stem = (
      f"Find the particular solution {math('y = f(x)')} to the differential equation "
      f"{math(rf'\frac{{dy}}{{dx}} = {tex(right_side)}')} with the initial condition "
      f"{math(f'f({start}) = {initial}')}."
   )

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-06",
      calculator_status="no_calculator",
      command_verb="find",
   )
