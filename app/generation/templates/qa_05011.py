"""BC-QA-05011, the largest volume of an open box folded from a square sheet."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-05011"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 14, "step": 1}},
      {"name": "height_cap", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 11, "step": 1}},
      {"name": "sheet_shape", "type": "label", "role": "safe", "domain": {"values": ["square", "rectangle", "strip"]}},
      {"name": "material", "type": "label", "role": "safe", "domain": {"values": ["cardboard", "steel", "plastic", "tin"]}},
      {"name": "purpose", "type": "label", "role": "safe", "domain": {"values": ["tray", "planter", "storage bin", "baking pan"]}},
      {"name": "length_unit", "type": "unit", "role": "safe", "domain": {"values": ["centimeters", "inches", "decimeters"]}},
      {"name": "domain_limit", "type": "label", "role": "difficulty", "domain": {"values": ["none", "binding"]}},
   ],
   "constraints": [
      "height_cap < optimum",
      "sheet_shape == 'square' or scale <= 10",
      "sheet_shape != 'strip' or scale <= 5",
   ],
   "derived": [
      {"name": "sheet_width", "expression": "6 * scale if sheet_shape == 'square' else (5 * scale if sheet_shape == 'rectangle' else 9 * scale)"},
      {"name": "sheet_length", "expression": "6 * scale if sheet_shape == 'square' else (8 * scale if sheet_shape == 'rectangle' else 24 * scale)"},
      {"name": "optimum", "expression": "2 * scale if sheet_shape == 'strip' else scale"},
   ],
   "invariants": [
      "exact(key)",
      "key > 0",
      "is_integer(key)",
   ],
   "dial_bindings": [
      {"parameter": "domain_limit", "difficulty_factor_id": "BC-DF-05", "settings": {"none": "off", "binding": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["scale", "height_cap", "sheet_shape", "material", "purpose", "length_unit", "domain_limit"]},
   ],
   "notes": (
      "Squares of side x are cut from the corners of a sheet sheet_width by sheet_length and the sides folded up, so "
      "V(x) = x (sheet_width - 2x)(sheet_length - 2x). The square sheet 6s by 6s has critical points s and 3s; the "
      "rectangle 5s by 8s has critical points s and 10s/3; the strip 9s by 24s has critical points 2s and 9s. The "
      "interior critical point is optimum. When the limit binds, the height can be at most height_cap, which is under "
      "optimum, so V is increasing on the whole "
      "contextual domain and the maximum sits at the right endpoint."
   ),
}

x = sympy.Symbol("x")
SINGULAR_UNITS = {"centimeters": "centimeter", "inches": "inch", "decimeters": "decimeter"}


def build(names):
   width = names["sheet_width"]
   length = names["sheet_length"]
   is_square = names["sheet_shape"] == "square"
   height_cap = names["height_cap"]
   unit = names["length_unit"]
   volume_unit = f"cubic {unit}"
   is_limited = names["domain_limit"] == "binding"

   base_width = width - 2 * x
   base_length = length - 2 * x
   volume = x * base_width * base_length
   rate = sympy.factor(sympy.diff(volume, x))
   critical_points = sorted(sympy.solve(rate, x))
   interior_critical = critical_points[0]
   edge_critical = critical_points[1]
   half_side = sympy.Rational(width, 2)

   if is_square:
      sheet_text = f"a square sheet of {names['material']} {width} {unit} on a side"
   else:
      sheet_text = f"a rectangular sheet of {names['material']} {width} {unit} by {length} {unit}"

   stem = (
      f"An open-top {names['purpose']} is made from {sheet_text} "
      "by cutting a square of side x from each corner and folding up the sides."
   )

   if is_limited:
      best_x = sympy.Integer(height_cap)
      cap_unit = SINGULAR_UNITS[unit] if height_cap == 1 else unit
      stem += f" The {names['purpose']} can be at most {height_cap} {cap_unit} tall."
      domain_text = math(rf"0 < x \le {height_cap}")
   else:
      best_x = interior_critical
      domain_text = math(rf"0 < x < {tex(half_side)}")

   stem += f" Find the largest possible volume of the {names['purpose']}, in {volume_unit}."

   best_base = base_width.subs(x, best_x)
   best_length = base_length.subs(x, best_x)
   best_volume = volume.subs(x, best_x)

   if is_square:
      volume_text = math(r"V(x) = x\left(" + tex(base_width) + r"\right)^{2}")
      base_text = f"a square base of side {math(tex(base_width))}"
      value_text = math(f"V({tex(best_x)}) = {tex(best_x)}" + r"\left(" + tex(best_base) + r"\right)^{2} = " + tex(best_volume))
   else:
      volume_text = math(r"V(x) = x\left(" + tex(base_width) + r"\right)\left(" + tex(base_length) + r"\right)")
      base_text = f"a base {math(tex(base_width))} by {math(tex(base_length))}"
      value_text = math(
         f"V({tex(best_x)}) = {tex(best_x)}" + r"\left(" + tex(best_base) + r"\right)\left(" + tex(best_length)
         + r"\right) = " + tex(best_volume)
      )

   rate_text = math("V'(x) = " + tex(rate))
   steps = [
      Step(
         text=(
            f"The {names['purpose']} has height x and {base_text}, so its volume is {volume_text}."
         ),
         rule="objective in one variable",
      ),
   ]

   if is_limited:
      steps.append(Step(
         text=f"The cut must be positive, less than half the sheet, and at most {height_cap}, so the domain is {domain_text}.",
         rule="contextual domain",
      ))
   else:
      steps.append(Step(
         text=f"The cut must be positive and less than half the sheet, so the domain is {domain_text}.",
         rule="contextual domain",
      ))

   steps.append(Step(
      text=(
         f"{rate_text}, which is zero at {math(f'x = {tex(interior_critical)}')} and {math(f'x = {tex(edge_critical)}')}; "
         f"only {math(f'x = {tex(interior_critical)}')} lies strictly inside the sheet."
      ),
      value=interior_critical,
      rule="critical points",
   ))

   if is_limited:
      increasing_text = math("V'(x) > 0")
      steps.append(Step(
         text=(
            f"The critical point {math(f'x = {tex(interior_critical)}')} is beyond the height limit, and {increasing_text} "
            f"for every x in {domain_text}, so V is increasing there and is largest at the right endpoint "
            f"{math(f'x = {height_cap}')}."
         ),
         rule="closed interval method",
      ))
   else:
      sign_text = math("V'(x)")
      steps.append(Step(
         text=(
            f"{sign_text} is positive for {math(f'0 < x < {tex(interior_critical)}')} and negative for "
            f"{math(f'{tex(interior_critical)} < x < {tex(half_side)}')}, and this is the only critical point in the "
            "domain, so V has its absolute maximum there."
         ),
         rule="first derivative test for an absolute extremum",
      ))

   steps.append(Step(
      text=f"The largest volume is {value_text} {volume_unit}.",
      value=best_volume,
      rule="evaluate the objective",
   ))

   distractors = [
      Distractor(
         error_path="BC-ERR-05024",
         derivation="the side of the cut square, where the maximum occurs, reported instead of the volume",
         value=best_x,
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-05024",
         derivation="the shorter side of the base at the optimum reported instead of the volume",
         value=best_base,
         mechanism="reversed_quantities",
      ),
   ]

   if is_limited:
      distractors.append(Distractor(
         error_path="BC-ERR-05052",
         derivation=f"the height limit left out of the domain, so the critical point x = {interior_critical} is used",
         value=volume.subs(x, interior_critical),
         mechanism="theorem_condition_ignored",
      ))
   elif is_square:
      distractors.append(Distractor(
         error_path="BC-ERR-05054",
         derivation=f"the critical point x = {edge_critical} from the factor of the base taken without checking what kind of point it is, giving the volume there",
         value=volume.subs(x, edge_critical),
         mechanism="theorem_condition_ignored",
      ))
   else:
      distractors.append(Distractor(
         error_path="BC-ERR-05024",
         derivation="the longer side of the base at the optimum reported instead of the volume",
         value=best_length,
         mechanism="reversed_quantities",
      ))

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=best_volume, units=volume_unit),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="no_calculator",
      command_verb="find",
   )
