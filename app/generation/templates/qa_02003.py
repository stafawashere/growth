"""BC-QA-02003, a limit in difference quotient form evaluated as the derivative of a known function at a base point."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-02003"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "family", "type": "label", "role": "difficulty", "domain": {"values": ["sin", "cos", "sqrt", "ln", "square"]}},
      {"name": "base_index", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 4, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
      {"name": "increment", "type": "label", "role": "safe", "domain": {"values": ["h", "t", "s"]}},
      {"name": "shape", "type": "label", "role": "difficulty", "domain": {"values": ["increment", "two_point"]}},
   ],
   "constraints": [
      "family != 'sqrt' or coefficient > 0",
      "family != 'sqrt' or [2, 3, 4, 2, 5][base_index] != coefficient",
      "family != 'square' or [99, -1, 2, 99, 99][base_index] != coefficient",
   ],
   "derived": [],
   "invariants": [
      "'The limit is' in key",
   ],
   "dial_bindings": [
      {"parameter": "family", "difficulty_factor_id": "BC-DF-01", "settings": {"square": "off", "sqrt": "low", "ln": "low", "sin": "medium", "cos": "medium"}},
      {"parameter": "shape", "difficulty_factor_id": "BC-DF-01", "settings": {"increment": "off", "two_point": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["family", "base_index", "coefficient", "shape"]},
   ],
   "notes": "The limit is the derivative of coefficient times a familiar function at one of five base points per family, written with an increment or in two point form. Base points are chosen so that the function's value, its derivative and the derivative taken at the function's value are three different real numbers; the constraints remove the few coefficients for which two of them coincide or the square root would be taken of a negative value.",
}

x = sympy.Symbol("x")
pi = sympy.pi

FAMILIES = {
   "sin": (sympy.sin(x), [pi / 6, pi / 3, 2 * pi / 3, pi, 5 * pi / 6]),
   "cos": (sympy.cos(x), [pi / 6, pi / 3, 2 * pi / 3, 7 * pi / 6, 5 * pi / 6]),
   "sqrt": (sympy.sqrt(x), [sympy.Integer(4), sympy.Integer(9), sympy.Integer(16), sympy.Rational(1, 4), sympy.Integer(25)]),
   "ln": (sympy.log(x), [sympy.Integer(2), sympy.Integer(3), sympy.Rational(1, 2), sympy.Rational(1, 3), sympy.Integer(4)]),
   "square": (x**2, [sympy.Integer(3), sympy.Integer(-1), sympy.Rational(1, 2), sympy.Integer(-3), sympy.Integer(4)]),
}


def parts(names):
   base_function, bases = FAMILIES[names["family"]]
   function = names["coefficient"] * base_function
   base = bases[int(names["base_index"])]
   derivative = sympy.diff(function, x)
   value_at_base = function.subs(x, base)
   key_value = sympy.simplify(derivative.subs(x, base))
   wrong_base_value = sympy.simplify(derivative.subs(x, value_at_base))

   return function, base, derivative, value_at_base, key_value, wrong_base_value


def build(names):
   function, base, derivative, value_at_base, key_value, wrong_base_value = parts(names)
   increment = sympy.Symbol(names["increment"])
   is_two_point = names["shape"] == "two_point"

   if is_two_point:
      numerator = f"{tex(function)} - {tex(value_at_base)}" if not value_at_base.could_extract_minus_sign() else f"{tex(function)} + {tex(-value_at_base)}"
      limit_tex = rf"\lim_{{x \to {tex(base)}}} \frac{{{numerator}}}{{{tex(x - base)}}}"
   else:
      shifted = function.subs(x, sympy.Add(base, increment, evaluate=False))
      shifted_tex = tex(shifted)
      numerator = f"{shifted_tex} - {tex(value_at_base)}" if not value_at_base.could_extract_minus_sign() else f"{shifted_tex} + {tex(-value_at_base)}"
      limit_tex = rf"\lim_{{{increment} \to 0}} \frac{{{numerator}}}{{{increment}}}"

   stem = f"Find {math(limit_tex)}."
   function_text = math(f"f(x) = {tex(function)}")
   base_tex = tex(base)
   derivative_at_base = f"f'({base_tex})"
   derivative_rule = f"f'(x) = {tex(derivative)}"
   derivative_value = f"f'({base_tex}) = {tex(key_value)}"
   steps = [
      Step(
         text=f"The numerator is a difference of values of {function_text}, at a point approaching {math(tex(base))} and at {math(tex(base))} itself, and {math(f'f({tex(base)}) = {tex(value_at_base)}')}.",
         rule="recognise the difference quotient",
      ),
      Step(
         text=f"So the limit is {math(derivative_at_base)}, and {math(derivative_rule)}.",
         rule="limit definition of the derivative",
      ),
      Step(
         text=f"Evaluating, {math(derivative_value)}.",
         value=key_value,
         rule="derivative rule",
      ),
   ]

   key_label = f"The limit is {math(tex(key_value))}."
   distractors = [
      Distractor(
         error_path="BC-ERR-02024",
         derivation="the function's value at the base point reported instead of its derivative's value",
         label=f"The limit is {math(tex(value_at_base))}.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-02010",
         derivation="the constant in the numerator, f at the base point, taken as the base point, so the derivative is evaluated there",
         label=f"The limit is {math(tex(wrong_base_value))}.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-02009",
         derivation="the zero over zero form of the difference quotient taken to mean the limit does not exist",
         label="The limit does not exist.",
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
