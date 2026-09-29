"""BC-QA-06017, a left, right, midpoint or trapezoidal sum with equal subintervals for a function given by a formula or a graph."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, figure, label, math, point_mark, tex

ARCHETYPE_ID = "BC-QA-06017"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 15 of 2026-09-28"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "source", "type": "label", "role": "difficulty", "domain": {"values": ["formula", "graph"]}},
      {"name": "method", "type": "label", "role": "difficulty", "domain": {"values": ["left", "right", "midpoint", "trapezoid"]}},
      {"name": "heights", "type": "integer", "role": "safe", "count": 9, "domain": {"min": -2, "max": 6, "step": 1}},
      {"name": "leading", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 9, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 4, "step": 1}},
      {"name": "pieces", "type": "integer", "role": "safe", "domain": {"values": [2, 3, 4]}},
      {"name": "width", "type": "rational", "role": "safe", "domain": {"values": ["1/2", 2, 3]}},
   ],
   "constraints": [
      "source == 'formula' or distinct([graph_left, graph_right, graph_mid, graph_trap, graph_left / 2, graph_right / 2, graph_mid / 2, graph_trap / 2, graph_bad_trap])",
      "source == 'graph' or distinct([formula_left, formula_right, formula_mid, formula_trap, formula_left / width, formula_right / width, formula_mid / width, formula_trap / width, formula_bad_trap])",
   ],
   "derived": [
      {"name": "graph_left", "expression": "2 * (heights[0] + heights[2] + heights[4] + heights[6])"},
      {"name": "graph_right", "expression": "2 * (heights[2] + heights[4] + heights[6] + heights[8])"},
      {"name": "graph_mid", "expression": "2 * (heights[1] + heights[3] + heights[5] + heights[7])"},
      {"name": "graph_trap", "expression": "(graph_left + graph_right) / 2"},
      {"name": "graph_bad_trap", "expression": "graph_trap + (heights[2] + 2 * heights[4] + 2 * heights[6] + heights[8])"},
      {"name": "value_0", "expression": "leading * start**2 + constant"},
      {"name": "value_1", "expression": "leading * (start + width)**2 + constant"},
      {"name": "value_2", "expression": "leading * (start + 2 * width)**2 + constant"},
      {"name": "value_3", "expression": "leading * (start + 3 * width)**2 + constant"},
      {"name": "value_4", "expression": "leading * (start + 4 * width)**2 + constant"},
      {"name": "middle_0", "expression": "leading * (start + width / 2)**2 + constant"},
      {"name": "middle_1", "expression": "leading * (start + width + width / 2)**2 + constant"},
      {"name": "middle_2", "expression": "leading * (start + 2 * width + width / 2)**2 + constant"},
      {"name": "middle_3", "expression": "leading * (start + 3 * width + width / 2)**2 + constant"},
      {"name": "formula_left", "expression": "width * sum([value_0, value_1, value_2, value_3][:pieces])"},
      {"name": "formula_right", "expression": "width * sum([value_1, value_2, value_3, value_4][:pieces])"},
      {"name": "formula_mid", "expression": "width * sum([middle_0, middle_1, middle_2, middle_3][:pieces])"},
      {"name": "formula_trap", "expression": "(formula_left + formula_right) / 2"},
      {"name": "formula_bad_trap", "expression": "2 * formula_trap - width * (value_0 + value_1) / 2"},
   ],
   "invariants": [
      "exact(key)",
      "key != 0",
   ],
   "dial_bindings": [
      {"parameter": "source", "difficulty_factor_id": "BC-DF-03", "settings": {"formula": "off", "graph": "low"}},
      {"parameter": "method", "difficulty_factor_id": "BC-DF-06", "settings": {"left": "off", "right": "off", "midpoint": "low", "trapezoid": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["method", "leading", "constant", "start", "pieces", "width"]},
      {"representation": "BC-REP-02", "figure_kind": "function_graph", "requires": ["method", "heights"]},
   ],
   "notes": "Formula: f(x) = m x^2 + c on [a, a + n w] with n equal subintervals of width w, never 1, and a >= 0 so f is monotone there. Graph: line segments through (k, h_k) for k = 0 to 8, four subintervals of width 2, so every sample point is a vertex. The sum of the sample values alone, the opposite endpoint, the wrong sum type, and a trapezoidal sum with only the first trapezoid halved are the distractors; the constraints keep all of them apart from the key.",
}

x = sympy.Symbol("x")

METHOD_WORDS = {
   "left": "a left Riemann sum",
   "right": "a right Riemann sum",
   "midpoint": "a midpoint Riemann sum",
   "trapezoid": "a trapezoidal sum",
}


def _sums(values_at, start, width, pieces):
   points = [start + index * width for index in range(pieces + 1)]
   heights = [values_at(point) for point in points]
   middles = [values_at(start + index * width + width / 2) for index in range(pieces)]
   left = width * sum(heights[:-1])
   right = width * sum(heights[1:])
   midpoint = width * sum(middles)
   trapezoid = (left + right) / 2
   bad_trapezoid = width * ((heights[0] + heights[1]) / 2 + sum(heights[index] + heights[index + 1] for index in range(1, pieces)))

   return {
      "points": points,
      "heights": heights,
      "middles": middles,
      "left": sympy.nsimplify(left),
      "right": sympy.nsimplify(right),
      "midpoint": sympy.nsimplify(midpoint),
      "trapezoid": sympy.nsimplify(trapezoid),
      "bad_trapezoid": sympy.nsimplify(bad_trapezoid),
   }


def _form_text(method, sums, width):
   width_tex = tex(width)

   if method == "trapezoid":
      terms = " + ".join(
         rf"\frac{{f({tex(sums['points'][index])}) + f({tex(sums['points'][index + 1])})}}{{2}}"
         for index in range(len(sums["points"]) - 1)
      )

      return rf"{width_tex}\left({terms}\right)"

   if method == "midpoint":
      inputs = [point + width / 2 for point in sums["points"][:-1]]
   elif method == "left":
      inputs = sums["points"][:-1]
   else:
      inputs = sums["points"][1:]

   terms = " + ".join(f"f({tex(point)})" for point in inputs)

   return rf"{width_tex}\left({terms}\right)"


def _distractors(method, sums, width):
   width_word = tex(width)

   if method == "left":
      return [
         Distractor("BC-ERR-06002", "right endpoints used where left endpoints were asked for", value=sums["right"], mechanism="reversed_quantities"),
         Distractor("BC-ERR-06003", f"the left sample values added without multiplying by the width {width_word}", value=sums["left"] / width, mechanism="conceptual_confusion"),
         Distractor("BC-ERR-99028", "a midpoint sum computed in place of the left sum", value=sums["midpoint"], mechanism="conceptual_confusion"),
      ]

   if method == "right":
      return [
         Distractor("BC-ERR-06002", "left endpoints used where right endpoints were asked for", value=sums["left"], mechanism="reversed_quantities"),
         Distractor("BC-ERR-06003", f"the right sample values added without multiplying by the width {width_word}", value=sums["right"] / width, mechanism="conceptual_confusion"),
         Distractor("BC-ERR-99028", "a trapezoidal sum computed in place of the right sum", value=sums["trapezoid"], mechanism="conceptual_confusion"),
      ]

   if method == "midpoint":
      return [
         Distractor("BC-ERR-99028", "the left endpoint of each subinterval used in place of its midpoint", value=sums["left"], mechanism="conceptual_confusion"),
         Distractor("BC-ERR-06003", f"the midpoint values added without multiplying by the width {width_word}", value=sums["midpoint"] / width, mechanism="conceptual_confusion"),
         Distractor("BC-ERR-99028", "a trapezoidal sum computed in place of the midpoint sum", value=sums["trapezoid"], mechanism="conceptual_confusion"),
      ]

   return [
      Distractor("BC-ERR-06004", "the factor of one half applied to the first trapezoid only", value=sums["bad_trapezoid"], mechanism="algebra_slip"),
      Distractor("BC-ERR-99028", "a left Riemann sum computed in place of the trapezoidal sum", value=sums["left"], mechanism="conceptual_confusion"),
      Distractor("BC-ERR-06003", f"the trapezoid heights averaged and added without multiplying by the width {width_word}", value=sums["trapezoid"] / width, mechanism="conceptual_confusion"),
   ]


def _graph_figure(heights):
   segments = [[[index, heights[index]] for index in range(9)]]
   low = min(min(heights), 0) - 1
   high = max(max(heights), 0) + 1
   vertex_list = ", ".join(f"({index}, {heights[index]})" for index in range(9))

   return figure(
      "function_graph",
      domain=(-0.5, 8.5),
      range_=(low, high),
      curves=[segments],
      marks=[point_mark(index, heights[index]) for index in range(9)],
      labels=[label("y = f(x)", 0.3, high - 0.4)],
      alt=f"The graph of f is made of line segments joining the points {vertex_list}.",
   )


def build(names):
   method = names["method"]
   is_graph = names["source"] == "graph"

   if is_graph:
      heights = [int(value) for value in names["heights"]]
      start, width, pieces = 0, sympy.Integer(2), 4
      sums = _sums(lambda point: heights[int(point)], start, width, pieces)
      stem = (
         f"The graph of the function f on the interval {math('[0, 8]')} consists of line segments, as shown. "
         f"Use {METHOD_WORDS[method]} with 4 subintervals of equal width to approximate {math(r'\int_{0}^{8} f(x)\,dx')}."
      )
      shown = _graph_figure(heights)
      representation = "BC-REP-02"
   else:
      leading = int(names["leading"])
      constant = int(names["constant"])
      start = sympy.Integer(int(names["start"]))
      width = sympy.nsimplify(names["width"])
      pieces = int(names["pieces"])
      function = leading * x**2 + constant
      end = start + pieces * width
      sums = _sums(lambda point: function.subs(x, point), start, width, pieces)
      integral = rf"\int_{{{tex(start)}}}^{{{tex(end)}}} f(x)\,dx"
      stem = (
         f"Let {math('f(x) = ' + tex(function))}. Use {METHOD_WORDS[method]} with {pieces} subintervals of equal width "
         f"to approximate {math(integral)}."
      )
      shown = None
      representation = "BC-REP-01"

   key_value = sums[method]
   width_text = f"The interval has length {math(tex(pieces * width))}, so each of the {pieces} subintervals has width {math(tex(width))}"
   steps = [
      Step(
         text=f"{width_text}, and the sum is {math(_form_text(method, sums, width))}.",
         point_type_id="BC-PT-99018",
         rule="form of the sum",
      ),
      Step(
         text=f"Reading the values of f and adding gives {math(tex(key_value))}.",
         value=key_value,
         point_type_id="BC-PT-99019",
         rule="value of the sum",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=_distractors(method, sums, width),
      representation=representation,
      calculator_status="no_calculator",
      command_verb="approximate",
      figure=shown,
   )
