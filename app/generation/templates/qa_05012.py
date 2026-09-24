"""BC-QA-05012, points of an implicit relation where the tangent line is horizontal."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-05012"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "across", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "up", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "loop", "type": "label", "role": "safe", "domain": {"values": ["q1s1", "q1s2", "q1s3", "q2s1", "q2s2"]}},
      {"name": "facing", "type": "integer", "role": "safe", "domain": {"values": [1, -1]}},
      {"name": "derivative", "type": "label", "role": "difficulty", "domain": {"values": ["given", "derive"]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "point_count == 2",
   ],
   "dial_bindings": [
      {"parameter": "derivative", "difficulty_factor_id": "BC-DF-08", "settings": {"given": "off", "derive": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["across", "up", "loop", "facing", "derivative"]},
   ],
   "notes": (
      "The relation is (y - up)^2 = m u^2 (u + 3q) with u = facing (x - across) and m = q s^2, a nodal cubic. The "
      "numerator of dy/dx vanishes at u = 0 and u = -2q; at u = 0 the curve passes through (across, up) where the "
      "denominator vanishes as well, so only u = -2q gives horizontal tangents, at y = up plus or minus 2 s q^2. The "
      "denominator alone vanishes at u = -3q, the vertical tangent."
   ),
}

x, y = sympy.symbols("x y")


def _point_text(point):
   return math(f"({tex(point[0])}, {tex(point[1])})")


def _points_label(points):
   if len(points) == 1:
      return f"The tangent line is horizontal only at the point {_point_text(points[0])}."

   pieces = [_point_text(point) for point in points]
   listed = ", ".join(pieces[:-1]) + f" and {pieces[-1]}"

   return f"The tangent line is horizontal only at the points {listed}."


def build(names):
   across = names["across"]
   up = names["up"]
   facing = names["facing"]
   q_value = int(names["loop"][1])
   s_value = int(names["loop"][3])
   m_value = q_value * s_value**2

   u = facing * (x - across)
   relation_right = m_value * u**2 * (u + 3 * q_value)
   numerator = sympy.factor(sympy.diff(relation_right, x))
   denominator = 2 * (y - up)
   derivative = numerator / denominator

   lift = 2 * s_value * q_value**2
   turning_x = across - facing * 2 * q_value
   vertical_x = across - facing * 3 * q_value
   key_points = [(turning_x, up + lift), (turning_x, up - lift)]
   singular = (across, up)

   left_tex = tex((y - up) ** 2) if up != 0 else "y^{2}"
   coefficient_tex = "" if m_value == 1 else str(m_value)
   u_tex = tex(u)
   square_tex = "x^{2}" if across == 0 else r"\left(" + u_tex + r"\right)^{2}"
   relation_tex = f"{left_tex} = {coefficient_tex}{square_tex}" + r"\left(" + tex(u + 3 * q_value) + r"\right)"
   derivative_tex = r"\frac{dy}{dx} = " + tex(derivative)

   stem = f"Consider the curve given by {math(relation_tex)}."

   if names["derivative"] == "given":
      stem += f" The derivative is {math(derivative_tex)}."

   stem += " Find all points on the curve at which the tangent line is horizontal."

   steps = []

   if names["derivative"] == "derive":
      implicit_text = math(r"2\left(" + tex(y - up) + r"\right)\frac{dy}{dx} = " + tex(numerator))
      steps.append(Step(
         text=f"Differentiating implicitly, {implicit_text}, so {math(derivative_tex)}.",
         rule="implicit differentiation",
      ))

   steps += [
      Step(
         text=(
            f"The numerator is zero where {math(f'x = {across}')} or {math(f'x = {turning_x}')}. At "
            f"{math(f'x = {across}')} the curve gives {math(f'y = {up}')}, where the denominator is also zero, so no "
            "horizontal tangent is decided there."
         ),
         rule="numerator zero with a nonzero denominator",
      ),
      Step(
         text=(
            f"At {math(f'x = {turning_x}')} the relation gives {math(tex((y - up) ** 2) + f' = {lift**2}')}, so "
            f"{math(f'y = {up + lift}')} or {math(f'y = {up - lift}')}, and the denominator is not zero at either."
         ),
         rule="solve the relation and the condition together",
      ),
      Step(text=_points_label(key_points), rule="report both coordinates"),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-05057",
         derivation=f"every zero of the numerator kept, including ({across}, {up}) where the denominator is zero too",
         label=_points_label([singular] + key_points),
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-05059",
         derivation=f"the input x = {turning_x} reported alone where points were asked for",
         label=f"The tangent line is horizontal only where {math(f'x = {turning_x}')}.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-03012",
         derivation="the denominator set to zero instead of the numerator, which gives the vertical tangent",
         label=_points_label([(vertical_x, up)]),
         mechanism="reversed_quantities",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=_points_label(key_points)),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
      notes={"point_count": len(key_points)},
   )
