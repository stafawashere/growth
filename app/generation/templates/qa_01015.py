"""BC-QA-01015, the intervals on which a rational or radical expression is continuous, read from its domain."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-01015"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 4, "step": 1, "exclude": [0]}},
      {"name": "zero", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "roots", "type": "integer", "role": "safe", "count": 2, "distinct": True, "order": "increasing", "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "family", "type": "label", "role": "difficulty", "domain": {"values": ["rational", "radical"]}},
   ],
   "constraints": [
      "family == 'radical' or (zero != roots[0] and zero != roots[1])",
   ],
   "derived": [],
   "invariants": [
      "'continuous on' in key",
   ],
   "dial_bindings": [
      {"parameter": "family", "difficulty_factor_id": "BC-DF-14", "settings": {"rational": "low", "radical": "medium"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["coefficient", "zero", "roots", "family"]},
   ],
   "notes": "Rational family: coefficient (x - zero) over the expanded (x - roots[0])(x - roots[1]), continuous on three open intervals. Radical family: coefficient times the square root of (x - roots[0]) over (x - roots[1]), continuous on [roots[0], roots[1]) and (roots[1], infinity).",
}

x = sympy.Symbol("x")


def _union(pieces):
   return math(r" \cup ".join(pieces))


def build(names):
   coefficient = names["coefficient"]
   zero = names["zero"]
   low, high = [int(value) for value in names["roots"]]
   is_radical = names["family"] == "radical"

   if is_radical:
      top = coefficient * sympy.sqrt(x - low)
      bottom = x - high
      rule_tex = rf"\frac{{{tex(top)}}}{{{tex(bottom)}}}"
      key_pieces = [rf"[{low}, {high})", rf"({high}, \infty)"]
      one_piece = [rf"[{low}, \infty)"]
      ignoring_radical = [rf"(-\infty, {high})", rf"({high}, \infty)"]
      closed = [rf"[{low}, {high}]", rf"[{high}, \infty)"]
      steps = [
         Step(text=f"The square root needs {math(tex(x - low) + r' \ge 0')}, so {math(rf'x \ge {low}')}.", rule="domain of a square root"),
         Step(text=f"The denominator is 0 at {math(f'x = {high}')}, so that input is excluded.", rule="domain of a quotient"),
         Step(
            text=(
               f"Quotients and roots are continuous on their domains, so f is continuous on {_union(key_pieces)}, "
               f"continuous from the right at {math(f'x = {low}')}, and never at {math(f'x = {high}')}."
            ),
            rule="continuity on the domain",
         ),
      ]
      first_wrong = Distractor(
         error_path="BC-ERR-01031",
         derivation=f"the excluded input {high} left inside the stated interval",
         label=f"f is continuous on {_union(one_piece)}.",
         mechanism="conceptual_confusion",
      )
      second_wrong = Distractor(
         error_path="BC-ERR-01031",
         derivation=f"the square root's domain ignored, so inputs below {low}, where f is undefined, are included",
         label=f"f is continuous on {_union(ignoring_radical)}.",
         mechanism="conceptual_confusion",
      )
   else:
      top = coefficient * (x - zero)
      bottom = sympy.expand((x - low) * (x - high))
      rule_tex = rf"\frac{{{tex(top)}}}{{{tex(bottom)}}}"
      key_pieces = [rf"(-\infty, {low})", rf"({low}, {high})", rf"({high}, \infty)"]
      closed = [rf"(-\infty, {low}]", rf"[{low}, {high}]", rf"[{high}, \infty)"]
      steps = [
         Step(text=f"The denominator factors as {math(tex((x - low) * (x - high)))}, which is 0 at {math(f'x = {low}')} and {math(f'x = {high}')}.", rule="zeros of the denominator"),
         Step(text=f"A rational function is continuous on its domain, so f is continuous on {_union(key_pieces)}.", rule="continuity on the domain"),
      ]
      first_wrong = Distractor(
         error_path="BC-ERR-01031",
         derivation=f"only one zero of the denominator found, so the excluded input {low} sits inside an interval",
         label=f"f is continuous on {_union([rf'(-\infty, {high})', rf'({high}, \infty)'])}.",
         mechanism="conceptual_confusion",
      )
      second_wrong = Distractor(
         error_path="BC-ERR-01031",
         derivation=f"only one zero of the denominator found, so the excluded input {high} sits inside an interval",
         label=f"f is continuous on {_union([rf'(-\infty, {low})', rf'({low}, \infty)'])}.",
         mechanism="conceptual_confusion",
      )

   stem = f"Let {math('f(x) = ' + rule_tex)}. Find the intervals on which f is continuous."
   key_label = f"f is continuous on {_union(key_pieces)}."
   distractors = [
      first_wrong,
      second_wrong,
      Distractor(
         error_path="BC-ERR-01032",
         derivation=f"closed brackets written at {high}{'' if is_radical else ' and ' + str(low)}, where f is not defined",
         label=f"f is continuous on {_union(closed)}.",
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
