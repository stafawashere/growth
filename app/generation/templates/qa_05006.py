"""BC-QA-05006, an absolute extremum on a closed interval by the candidates test."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-05006"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "first_critical", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 1, "step": 1}},
      {"name": "gap", "type": "integer", "role": "safe", "domain": {"values": [2, 4]}},
      {"name": "left", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "right", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "orientation", "type": "integer", "role": "safe", "domain": {"values": [1, -1]}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": -12, "max": 12, "step": 1}},
      {"name": "extreme", "type": "label", "role": "safe", "domain": {"values": ["maximum", "minimum"]}},
      {"name": "root", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 4, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "family", "type": "label", "role": "difficulty", "domain": {"values": ["cubic", "reciprocal"]}},
   ],
   "constraints": [
      "family == 'reciprocal' or low >= -5",
      "family == 'reciprocal' or high <= 6",
      "family == 'reciprocal' or value_low != value_high",
      "family == 'reciprocal' or (extreme == 'maximum' and max(value_low, value_high) > max(value_first, value_second)) or (extreme == 'minimum' and min(value_low, value_high) < min(value_first, value_second))",
      "family == 'reciprocal' or distinct([best, local_best, opposite, location])",
      "family == 'reciprocal' or best != 0",
      "family == 'cubic' or root - left >= 1",
      "family == 'cubic' or distinct([inner_best, outer_value, endpoint_other, root])",
      "family == 'cubic' or inner_best != 0",
   ],
   "derived": [
      {"name": "second_critical", "expression": "first_critical + gap"},
      {"name": "low", "expression": "first_critical - left"},
      {"name": "high", "expression": "first_critical + gap + right"},
      {"name": "value_low", "expression": "orientation * (low**3 - 3 * (first_critical + gap / 2) * low**2 + 3 * first_critical * (first_critical + gap) * low) + shift"},
      {"name": "value_high", "expression": "orientation * (high**3 - 3 * (first_critical + gap / 2) * high**2 + 3 * first_critical * (first_critical + gap) * high) + shift"},
      {"name": "value_first", "expression": "orientation * (first_critical**3 - 3 * (first_critical + gap / 2) * first_critical**2 + 3 * first_critical * (first_critical + gap) * first_critical) + shift"},
      {"name": "value_second", "expression": "orientation * ((first_critical + gap)**3 - 3 * (first_critical + gap / 2) * (first_critical + gap)**2 + 3 * first_critical * (first_critical + gap)**2) + shift"},
      {"name": "best", "expression": "max(value_low, value_high) if extreme == 'maximum' else min(value_low, value_high)"},
      {"name": "local_best", "expression": "max(value_first, value_second) if extreme == 'maximum' else min(value_first, value_second)"},
      {"name": "opposite", "expression": "min(value_low, value_high, value_first, value_second) if extreme == 'maximum' else max(value_low, value_high, value_first, value_second)"},
      {"name": "location", "expression": "low if value_low == best else high"},
      {"name": "inner_low", "expression": "root - left"},
      {"name": "inner_high", "expression": "root + right"},
      {"name": "inner_best", "expression": "orientation * 2 * coefficient * root + shift"},
      {"name": "outer_value", "expression": "-orientation * 2 * coefficient * root + shift"},
      {"name": "inner_value_low", "expression": "orientation * coefficient * (root - left + root**2 / (root - left)) + shift"},
      {"name": "inner_value_high", "expression": "orientation * coefficient * (root + right + root**2 / (root + right)) + shift"},
      {"name": "endpoint_other", "expression": "max(inner_value_low, inner_value_high) if orientation == 1 else min(inner_value_low, inner_value_high)"},
   ],
   "invariants": [
      "exact(key)",
      "key == (best if family == 'cubic' else inner_best)",
   ],
   "dial_bindings": [
      {"parameter": "family", "difficulty_factor_id": "BC-DF-01", "settings": {"cubic": "low", "reciprocal": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["first_critical", "gap", "left", "right", "orientation", "shift", "extreme", "root", "coefficient", "family"]},
   ],
   "notes": "Two families, drawn equally often. Cubic: f'(x) = 3k(x - p)(x - q) with both critical points inside [a, b] and the requested extremum at an endpoint, so leaving out the endpoints gives the local extreme value. Reciprocal: f(x) = k(m x + m s^2 / x) + d on [s - l, s + r] inside x > 0, whose absolute minimum (k = 1) or maximum (k = -1) is at the interior critical point s, while the critical point -s lies outside the interval and gives a more extreme value if it is wrongly kept.",
}

x = sympy.Symbol("x")


def _reciprocal(names):
   root = int(names["root"])
   coefficient = int(names["coefficient"])
   orientation = int(names["orientation"])
   low = int(names["inner_low"])
   high = int(names["inner_high"])
   is_minimum = orientation == 1
   extreme = "minimum" if is_minimum else "maximum"
   function = orientation * coefficient * (x + root**2 / x) + names["shift"]
   derivative = sympy.diff(function, x)
   candidates = [low, root, high]
   values = {candidate: function.subs(x, candidate) for candidate in candidates}
   key_value = values[root]
   outer_value = function.subs(x, -root)
   choose_other = max if is_minimum else min
   endpoint_other = choose_other(values[low], values[high])

   stem = (
      f"Let {math('f(x) = ' + tex(function))}. Find the absolute {extreme} value of f on the closed interval "
      f"{math(rf'\left[{low}, {high}\right]')}. Justify the answer."
   )

   derivative_statement = "f'(x) = " + tex(derivative)
   table = ", ".join(f"{math(f'f({candidate}) = {tex(values[candidate])}')}" for candidate in candidates)
   steps = [
      Step(
         text=(
            f"{math(derivative_statement)}, which is 0 at x = {root} and x = {-root}. Only x = {root} lies in the "
            "interval, so it is the one critical point to test."
         ),
         point_type_id="BC-PT-99013",
         rule="critical points in the interval",
      ),
      Step(
         text=f"Evaluate f at the critical point and at both endpoints: {table}.",
         point_type_id="BC-PT-99011",
         rule="candidates test",
      ),
      Step(
         text=(
            f"The {'smallest' if is_minimum else 'largest'} of these values is {math(tex(key_value))}, at x = {root}, so the "
            f"absolute {extreme} value of f on the interval is {math(tex(key_value))}."
         ),
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="compare the candidates",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-05025",
         derivation=f"the critical point x = {-root}, outside the interval, kept as a candidate, and f({-root}) reported",
         value=outer_value,
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-05028",
         derivation=f"the absolute {'maximum' if is_minimum else 'minimum'} chosen from the correct candidate values",
         value=endpoint_other,
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-05024",
         derivation=f"the input x = {root} at which the extremum occurs reported in place of its value",
         value=sympy.Integer(root),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )


def build(names):
   if names["family"] == "reciprocal":
      return _reciprocal(names)

   first = int(names["first_critical"])
   second = int(names["second_critical"])
   low = int(names["low"])
   high = int(names["high"])
   orientation = int(names["orientation"])
   is_maximum = names["extreme"] == "maximum"
   function = orientation * (x**3 - sympy.Rational(3, 2) * (first + second) * x**2 + 3 * first * second * x) + names["shift"]
   derivative = sympy.factor(sympy.diff(function, x))
   candidates = [low, first, second, high]
   values = {candidate: function.subs(x, candidate) for candidate in candidates}
   choose = max if is_maximum else min
   opposite_choose = min if is_maximum else max
   best_input = choose(candidates, key=lambda candidate: values[candidate])
   key_value = values[best_input]

   stem = (
      f"Let {math('f(x) = ' + tex(function))}. Find the absolute {names['extreme']} value of f on the closed interval "
      f"{math(rf'\left[{low}, {high}\right]')}. Justify the answer."
   )

   derivative_statement = "f'(x) = " + tex(derivative)
   table = ", ".join(f"{math(f'f({candidate}) = {tex(values[candidate])}')}" for candidate in candidates)
   steps = [
      Step(
         text=f"{math(derivative_statement)}, which is 0 at x = {first} and x = {second}, both inside the interval.",
         point_type_id="BC-PT-99013",
         rule="critical points",
      ),
      Step(
         text=f"Evaluate f at the critical points and at both endpoints: {table}.",
         point_type_id="BC-PT-99011",
         rule="candidates test",
      ),
      Step(
         text=(
            f"The {'largest' if is_maximum else 'smallest'} of these values is {math(tex(key_value))}, at x = {best_input}, so the "
            f"absolute {names['extreme']} value of f on the interval is {math(tex(key_value))}."
         ),
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="compare the candidates",
      ),
   ]

   local_best = choose(values[first], values[second])
   opposite = opposite_choose(values.values())
   distractors = [
      Distractor(
         error_path="BC-ERR-05026",
         derivation=f"both endpoints left out of the comparison, so only f({first}) and f({second}) are compared",
         value=local_best,
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-05028",
         derivation=f"the absolute {'minimum' if is_maximum else 'maximum'} chosen from the correct candidate values",
         value=opposite,
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-05024",
         derivation=f"the input x = {best_input} at which the extremum occurs reported in place of its value",
         value=sympy.Integer(best_input),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
