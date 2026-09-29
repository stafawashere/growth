"""BC-QA-07012, whether a differential equation is separable decided, and a separable one separated."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-07012"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 15 of 2026-09-28"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "separable", "type": "label", "role": "difficulty", "domain": {"values": ["yes", "no"]}},
      {"name": "factor", "type": "label", "role": "safe", "domain": {"values": ["linear", "square", "cube", "exponential", "cosine", "sine"]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1, "exclude": [0]}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "constant != 0",
      "coefficient != 0",
   ],
   "dial_bindings": [
      {"parameter": "separable", "difficulty_factor_id": "BC-DF-15", "settings": {"yes": "low", "no": "low"}},
      {"parameter": "separable", "difficulty_factor_id": "BC-DF-11", "settings": {"yes": "low", "no": "off"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-06", "figure_kind": None, "requires": ["separable", "factor", "coefficient", "constant"]},
   ],
   "notes": "Separable: dy/dx = a g(x) y + a c g(x), printed expanded, which factors as a g(x)(y + c). Not separable: dy/dx = a g(x) y + c with c nonzero and g not constant, since f f_xy = f_x f_y fails for f = a g y + c. The separated form keeps every y factor with dy and every x factor with dx.",
}

x = sympy.Symbol("x")
y = sympy.Symbol("y")

FACTORS = {
   "linear": x,
   "square": x**2,
   "cube": x**3,
   "exponential": sympy.exp(x),
   "cosine": sympy.cos(x),
   "sine": sympy.sin(x),
}

NOT_SEPARABLE = "The equation cannot be separated."


def _separated(y_part, x_part):
   return rf"\( \frac{{dy}}{{{tex(y_part)}}} = {tex(x_part)}\,dx \)"


def _termwise(first_term, second_term):
   combined = sympy.Add(first_term, second_term, evaluate=False)

   return rf"\( \frac{{dy}}{{y}} = \left({tex(combined)}\right)dx \)"


def build(names):
   is_separable = names["separable"] == "yes"
   coefficient = int(names["coefficient"])
   constant = int(names["constant"])
   factor = FACTORS[names["factor"]]
   x_part = coefficient * factor

   if is_separable:
      right_side = sympy.Add(x_part * y, coefficient * constant * factor, evaluate=False)
   else:
      right_side = sympy.Add(x_part * y, constant, evaluate=False)

   equation = r"\frac{dy}{dx} = " + tex(right_side)
   stem = (
      f"Consider the differential equation {math(equation)}. Decide whether it can be solved by separation of variables. "
      "If it can, write it with every factor involving y on the side of dy and every factor involving x on the side of dx; "
      "if it cannot, say so."
   )

   if is_separable:
      factored = tex(x_part) + r"\left(" + tex(y + constant) + r"\right)"
      steps = [
         Step(
            text=f"The two terms share the factor {math(tex(x_part))}, so {math(equation + ' = ' + factored)}, a function of x times a function of y.",
            rule="right side factored into a function of x times a function of y",
         ),
         Step(
            text=f"Divide by {math(tex(y + constant))} and multiply by dx: {_separated(y + constant, x_part)}.",
            point_type_id="BC-PT-99028",
            rule="separation of variables",
         ),
      ]
      key_label = _separated(y + constant, x_part)
      distractors = [
         Distractor("BC-ERR-07028", "only the first term divided by y, as though the sum split term by term", label=_termwise(x_part, coefficient * constant * factor), mechanism="algebra_slip"),
         Distractor("BC-ERR-99014", f"the factor {tex(y + constant)} multiplied onto the dy side instead of divided", label=rf"\( \left({tex(y + constant)}\right)dy = {tex(x_part)}\,dx \)", mechanism="algebra_slip"),
         Distractor("BC-ERR-07024", "dx moved across with y still on the side of dx, so nothing was separated", label=rf"\( dy = {factored}\,dx \)", mechanism="conceptual_confusion"),
      ]
   else:
      steps = [
         Step(
            text=(
               f"Separation needs {math(tex(right_side))} to be a function of x times a function of y. The term {math(tex(constant))} "
               f"contains no y and no factor {math(tex(factor))}, so no such factorisation exists."
            ),
            rule="test for a product of a function of x and a function of y",
         ),
         Step(
            text=(
               f"Equivalently, for {math('F = ' + tex(right_side))} a product form would force {math('F F_{xy} = F_x F_y')}, "
               f"which fails because the difference is {math(tex(sympy.simplify(right_side * sympy.diff(right_side, x, y) - sympy.diff(right_side, x) * sympy.diff(right_side, y))))}. "
               "The equation cannot be separated."
            ),
            point_type_id="BC-PT-99028",
            rule="separability decided",
         ),
      ]
      key_label = NOT_SEPARABLE
      distractors = [
         Distractor("BC-ERR-07028", "the first term divided by y and the constant left beside it, as though the sum factored", label=_termwise(x_part, constant), mechanism="algebra_slip"),
         Distractor("BC-ERR-07028", f"the constant treated as though it carried the factor {tex(x_part)}, so the sum was factored falsely", label=_separated(y + constant, x_part), mechanism="conceptual_confusion"),
         Distractor("BC-ERR-07024", "dx moved across with y still on the side of dx, so nothing was separated", label=rf"\( dy = \left({tex(right_side)}\right)dx \)", mechanism="conceptual_confusion"),
      ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-06",
      calculator_status="no_calculator",
      command_verb="determine",
   )
