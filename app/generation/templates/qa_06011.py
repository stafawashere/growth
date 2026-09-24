"""BC-QA-06011, an improper integral that needs a substitution, evaluated or shown to diverge."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-06011"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "impropriety", "type": "label", "role": "difficulty", "domain": {"values": ["infinite", "unbounded"]}},
      {"name": "outcome", "type": "label", "role": "difficulty", "domain": {"values": ["converges", "diverges"]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "degree", "type": "integer", "role": "safe", "domain": {"values": [2, 3]}},
      {"name": "lower", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "root", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "gap", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
   ],
   "constraints": [
      "lower**degree + shift != degree*lower",
   ],
   "derived": [
      {"name": "upper", "expression": "root + gap"},
   ],
   "invariants": [
      "upper > root",
      "len(key) > 20",
   ],
   "dial_bindings": [
      {"parameter": "impropriety", "difficulty_factor_id": "BC-DF-08", "settings": {"infinite": "off", "unbounded": "low"}},
      {"parameter": "outcome", "difficulty_factor_id": "BC-DF-08", "settings": {"converges": "off", "diverges": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["impropriety", "outcome", "coefficient", "degree"]},
   ],
   "notes": "The integrand is c x^(m-1) over a power of x^m + b on [a, infinity), or of x^m - r^m on [r, s] where it is unbounded at r. The power is 2 or 1/2, chosen so the outcome is the one drawn; every case needs u = x^m + b or u = x^m - r^m first.",
}

x = sympy.Symbol("x")
u = sympy.Symbol("u")
bound = sympy.Symbol("R")


def _converges_label(value):
   return f"The integral converges to {math(tex(value))}."


def build(names):
   coefficient = int(names["coefficient"])
   degree = int(names["degree"])
   is_infinite = names["impropriety"] == "infinite"
   converges = names["outcome"] == "converges"
   half = sympy.Rational(1, 2)

   if is_infinite:
      power = 2 if converges else half
      lower_limit = int(names["lower"])
      inner = x**degree + int(names["shift"])
      near_u = inner.subs(x, lower_limit)
      limit_tex = rf"\lim_{{R\to\infty}} \int_{{{lower_limit}}}^{{R}}"
      reason = "the upper limit of integration is infinite"
      u_limits = rf"u = {tex(near_u)} \text{{ to }} u = {tex(inner.subs(x, bound))}"
   else:
      power = half if converges else 2
      lower_limit = int(names["root"])
      upper_limit = int(names["upper"])
      inner = x**degree - lower_limit**degree
      near_u = inner.subs(x, upper_limit)
      limit_tex = rf"\lim_{{R\to {lower_limit}^{{+}}}} \int_{{R}}^{{{upper_limit}}}"
      reason = f"the integrand is unbounded as x approaches {lower_limit} from the right"
      u_limits = rf"u = {tex(inner.subs(x, bound))} \text{{ to }} u = {tex(near_u)}"

   integrand = coefficient * x ** (degree - 1) / inner**power
   upper_tex = r"\infty" if is_infinite else str(upper_limit)
   integral_tex = rf"\int_{{{lower_limit}}}^{{{upper_tex}}} {tex(integrand)}\,dx"
   stem = f"Evaluate the improper integral {math(integral_tex)}, or show that it diverges."

   factor = sympy.Rational(coefficient, degree)
   u_antiderivative = factor * sympy.integrate(u ** (-power), u)
   substitution = rf"u = {tex(inner)},\ du = {tex(degree * x ** (degree - 1))}\,dx"

   steps = [
      Step(
         text=f"The integral is improper because {reason}, so write it as {math(limit_tex + ' ' + tex(integrand) + r'\,dx')}.",
         point_type_id="BC-PT-99053",
         rule="improper integral as a limit",
      ),
      Step(
         text=(
            f"Substitute {math(substitution)}. The limits become {math(u_limits)}, and an antiderivative in u is "
            f"{math(tex(u_antiderivative))}."
         ),
         point_type_id="BC-PT-99003",
         rule="substitution with changed limits",
      ),
   ]

   if converges:
      if is_infinite:
         key_value = factor / near_u
         original_limits = factor / lower_limit
         dropped_factor = sympy.Integer(coefficient) / near_u
         compound = sympy.Rational(coefficient, lower_limit)
         evaluation = (
            rf"\lim_{{R\to\infty}} \left( {tex(-factor / (inner.subs(x, bound)))} + {tex(factor / near_u)} \right) = "
            f"{tex(key_value)}"
         )
         original_note = f"the u antiderivative evaluated from u = {lower_limit} to infinity"
      else:
         key_value = 2 * factor * sympy.sqrt(near_u)
         original_limits = 2 * factor * (sympy.sqrt(upper_limit) - sympy.sqrt(lower_limit))
         dropped_factor = 2 * coefficient * sympy.sqrt(near_u)
         compound = 2 * coefficient * (sympy.sqrt(upper_limit) - sympy.sqrt(lower_limit))
         evaluation = (
            rf"\lim_{{R\to {lower_limit}^{{+}}}} \left( {tex(key_value)} - {tex(2 * factor)}\sqrt{{{tex(inner.subs(x, bound))}}} \right) = "
            f"{tex(key_value)}"
         )
         original_note = f"the u antiderivative evaluated from u = {lower_limit} to u = {upper_limit}"

      steps.append(Step(
         text=f"Evaluate the limit: {math(evaluation)}. The limit is finite, so the integral converges to {math(tex(key_value))}.",
         point_type_id="BC-PT-99005",
         rule="limit of the definite integrals",
      ))
      key_label = _converges_label(key_value)
      distractors = [
         Distractor(
            error_path="BC-ERR-06018",
            derivation=f"the original x limits kept after the substitution, {original_note}",
            label=_converges_label(original_limits),
            mechanism="wrong_limits",
         ),
         Distractor(
            error_path="BC-ERR-06019",
            derivation=f"the factor 1/{degree} that du introduces dropped",
            label=_converges_label(dropped_factor),
            mechanism="algebra_slip",
         ),
         Distractor(
            error_path="BC-ERR-06018",
            derivation=f"the original x limits kept after the substitution and the factor 1/{degree} dropped as well",
            label=_converges_label(compound),
            mechanism="compound",
         ),
      ]
   else:
      if is_infinite:
         finite_term = 2 * factor * sympy.sqrt(near_u)
         formula_value = -finite_term
         divergence = (
            rf"\lim_{{R\to\infty}} \left( {tex(2 * factor)}\sqrt{{{tex(inner.subs(x, bound))}}} - {tex(finite_term)} \right) = \infty"
         )
         formula_note = (
            "the p-integral formula for p > 1 applied with p = 1/2, which gives minus the antiderivative at the finite limit"
         )
         infinity_label = f"The integral converges to {math(r'\infty - ' + tex(finite_term))}."
         infinity_note = "infinity substituted for the variable and the difference written as a value, with no limit"
      else:
         finite_term = factor / near_u
         formula_value = -finite_term
         divergence = (
            rf"\lim_{{R\to {lower_limit}^{{+}}}} \left( {tex(-finite_term)} + {tex(factor / inner.subs(x, bound))} \right) = \infty"
         )
         formula_note = "the term at the singular endpoint, 1 over u at u = 0, treated as 0"
         infinity_label = f"The integral converges to {math(r'\infty - ' + tex(finite_term))}."
         infinity_note = "the singular endpoint substituted directly, 1 over 0 written as infinity, and the difference written as a value"

      steps.append(Step(
         text=f"Evaluate the limit: {math(divergence)}. The limit is infinite, so the integral diverges.",
         point_type_id="BC-PT-99004",
         rule="divergent limit",
      ))
      key_label = "The integral diverges."
      distractors = [
         Distractor(
            error_path="BC-ERR-06025",
            derivation=formula_note,
            label=_converges_label(formula_value),
            mechanism="theorem_condition_ignored",
         ),
         Distractor(
            error_path="BC-ERR-99007",
            derivation=infinity_note,
            label=infinity_label,
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-06019",
            derivation=f"the factor 1/{degree} from du dropped, then a finite value reported as in the first error",
            label=_converges_label(formula_value * degree),
            mechanism="compound",
         ),
      ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="evaluate",
      notes={"outcome": names["outcome"]},
   )
