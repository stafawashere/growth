"""BC-QA-06018, an antiderivative matched to an inverse trigonometric form, directly or after completing the square."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-06018"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 15 of 2026-09-28"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "kind", "type": "label", "role": "difficulty", "domain": {"values": ["arctan", "arcsin"]}},
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["direct", "square"]}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "numerator", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 12, "step": 1}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
   ],
   "constraints": [
      "numerator != scale",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
      "numerator != scale",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-06", "settings": {"direct": "low", "square": "medium"}},
      {"parameter": "kind", "difficulty_factor_id": "BC-DF-15", "settings": {"arctan": "low", "arcsin": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["kind", "form", "scale", "numerator", "shift"]},
   ],
   "notes": "Integrands k/(a^2 + u^2) and k/sqrt(a^2 - u^2) with u = x, or u = x + h hidden in an expanded quadratic that must be completed to a square. The antiderivatives are (k/a) arctan(u/a) and k arcsin(u/a). The numerator is never equal to the scale, so dropping or inventing the factor 1/a always changes the answer.",
}

x = sympy.Symbol("x")


def _tex(expression):
   return sympy.latex(sympy.sympify(expression), ln_notation=True, inv_trig_style="full")


def _ratio_tex(inner, scale):
   return rf"\frac{{{tex(inner)}}}{{{scale}}}"


def _integrand(kind, inner, scale, numerator):
   if kind == "arctan":
      return numerator / sympy.expand(inner**2 + scale**2)

   return numerator / sympy.sqrt(sympy.expand(scale**2 - inner**2))


def _answers(kind, inner, scale, numerator):
   ratio = inner / scale
   tangent = sympy.Rational(numerator, scale) * sympy.atan(ratio)

   if kind == "arctan":
      return {
         "key": tangent,
         "factor": numerator * sympy.atan(ratio),
         "pattern": sympy.Rational(numerator, scale) * sympy.asin(ratio),
         "substitution": numerator * sympy.log(sympy.expand(inner**2 + scale**2)),
      }

   return {
      "key": numerator * sympy.asin(ratio),
      "factor": sympy.Rational(numerator, scale) * sympy.asin(ratio),
      "pattern": tangent,
      "substitution": 2 * numerator * sympy.sqrt(scale**2 - inner**2),
   }


def build(names):
   kind = names["kind"]
   is_square = names["form"] == "square"
   scale = int(names["scale"])
   numerator = int(names["numerator"])
   shift = int(names["shift"]) if is_square else 0
   inner = x + shift
   integrand = _integrand(kind, inner, scale, numerator)
   answers = _answers(kind, inner, scale, numerator)
   ratio_text = _ratio_tex(inner, scale)
   inner_text = tex(inner) if inner == x else rf"\left({tex(inner)}\right)"

   stem = f"Find the indefinite integral {math(r'\int ' + tex(integrand) + r'\,dx')}."
   steps = []

   if is_square:
      expanded = sympy.expand(inner**2 + scale**2) if kind == "arctan" else sympy.expand(scale**2 - inner**2)
      completed = rf"\left({tex(inner)}\right)^{{2}} + {scale**2}" if kind == "arctan" else rf"{scale**2} - \left({tex(inner)}\right)^{{2}}"
      steps.append(Step(
         text=f"Complete the square in the quadratic: {math(tex(expanded) + ' = ' + completed)}.",
         rule="completing the square",
      ))

   if kind == "arctan":
      pattern = rf"\frac{{d}}{{dx}} \arctan\left({ratio_text}\right) = \frac{{{scale}}}{{{scale**2} + {inner_text}^{{2}}}}"
      substitution = rf"u = {ratio_text}, \; dx = {scale}\,du"
      reduced = rf"\int \frac{{{numerator}}}{{{scale**2}\left(1 + u^{{2}}\right)}} \cdot {scale}\,du = {tex(sympy.Rational(numerator, scale))} \int \frac{{du}}{{1 + u^{{2}}}}"
   else:
      pattern = rf"\frac{{d}}{{dx}} \arcsin\left({ratio_text}\right) = \frac{{1}}{{\sqrt{{{scale**2} - {inner_text}^{{2}}}}}}"
      substitution = rf"u = {ratio_text}, \; dx = {scale}\,du"
      reduced = rf"\int \frac{{{numerator}}}{{{scale}\sqrt{{1 - u^{{2}}}}}} \cdot {scale}\,du = {numerator} \int \frac{{du}}{{\sqrt{{1 - u^{{2}}}}}}"

   steps.append(Step(
      text=f"The integrand has the shape of an inverse trigonometric derivative, {math(pattern)}.",
      rule="antiderivative read from a derivative rule",
   ))
   steps.append(Step(
      text=f"With {math(substitution)}, the integral becomes {math(reduced)}, which is {math(_tex(answers['key']) + ' + C')}.",
      value=answers["key"],
      rule="substitution into the inverse trigonometric form",
   ))

   if kind == "arctan":
      distractors = [
         Distractor("BC-ERR-06019", f"the factor 1/{scale} that dx = {scale} du introduces dropped", value=answers["factor"], mechanism="algebra_slip"),
         Distractor("BC-ERR-03017", "the inverse sine pattern used for a sum of squares", value=answers["pattern"], mechanism="conceptual_confusion"),
         Distractor("BC-ERR-06020", "the quadratic taken as u and dx treated as du, although 2x is not present, giving a logarithm", value=answers["substitution"], mechanism="conceptual_confusion"),
      ]
   else:
      distractors = [
         Distractor("BC-ERR-06019", f"the factor {scale} that dx = {scale} du introduces dropped, leaving 1/{scale}", value=answers["factor"], mechanism="algebra_slip"),
         Distractor("BC-ERR-03017", "the inverse tangent pattern used for a square root of a difference of squares", value=answers["pattern"], mechanism="conceptual_confusion"),
         Distractor("BC-ERR-06020", "the expression under the root taken as u and dx treated as du, although its derivative is not present", value=answers["substitution"], mechanism="conceptual_confusion"),
      ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=answers["key"]),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
