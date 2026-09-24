"""BC-QA-06014, a limit of Riemann sums converted to a definite integral, or the reverse."""
from app.generation.kit import Distractor, Instance, Key, Step, math

ARCHETYPE_ID = "BC-QA-06014"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "direction", "type": "label", "role": "difficulty", "domain": {"values": ["to_integral", "to_sum"]}},
      {"name": "function", "type": "label", "role": "safe", "domain": {"values": ["square", "cube", "root", "exponential"]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "width", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "convention", "type": "label", "role": "safe", "domain": {"values": ["right", "left"]}},
      {"name": "letter", "type": "label", "role": "safe", "domain": {"values": ["x", "t"]}},
   ],
   "constraints": [],
   "derived": [
      {"name": "finish", "expression": "start + width"},
   ],
   "invariants": [
      "finish > start",
      "start > 0",
   ],
   "dial_bindings": [
      {"parameter": "direction", "difficulty_factor_id": "BC-DF-04", "settings": {"to_integral": "off", "to_sum": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["direction", "function", "coefficient", "start", "width"]},
   ],
   "notes": "Every function is positive and increasing on [0, infinity) and the interval starts at a positive input, so the integral over [0, width] is smaller than the key's and no distractor integral has the key's value; the width is at least 2, so dropping or doubling it changes the value.",
}

FUNCTION_TEX = {
   "square": lambda argument: rf"\left({argument}\right)^{{2}}",
   "cube": lambda argument: rf"\left({argument}\right)^{{3}}",
   "root": lambda argument: rf"\sqrt{{{argument}}}",
   "exponential": lambda argument: rf"e^{{{argument}}}",
}

PLAIN_TEX = {
   "square": lambda variable: rf"{variable}^{{2}}",
   "cube": lambda variable: rf"{variable}^{{3}}",
   "root": lambda variable: rf"\sqrt{{{variable}}}",
   "exponential": lambda variable: rf"e^{{{variable}}}",
}


def _scaled(multiplier, body):
   return body if multiplier == 1 else f"{multiplier}{body}"


def _integral(low, high, multiplier, function, variable):
   return rf"\int_{{{low}}}^{{{high}}} {_scaled(multiplier, PLAIN_TEX[function](variable))}\,d{variable}"


def _sample(start, step):
   fraction = r"\frac{k}{n}" if step == 1 else rf"\frac{{{step}k}}{{n}}"

   return fraction if start == 0 else f"{start} + {fraction}"


def _sum(sample_start, sample_step, width_numerator, multiplier, function, first_index=1, with_width=True):
   last_index = "n" if first_index == 1 else "n-1"
   value = _scaled(multiplier, FUNCTION_TEX[function](_sample(sample_start, sample_step)))
   width = rf" \cdot \frac{{{width_numerator}}}{{n}}" if with_width else ""

   return rf"\lim_{{n\to\infty}} \sum_{{k={first_index}}}^{{{last_index}}} {value}{width}"


def build(names):
   function = names["function"]
   multiplier = int(names["coefficient"])
   start = int(names["start"])
   width = int(names["width"])
   finish = int(names["finish"])
   variable = names["letter"]
   key_integral = _integral(start, finish, multiplier, function, variable)
   key_sum = _sum(start, width, width, multiplier, function)

   if names["direction"] == "to_integral":
      first_index = 1 if names["convention"] == "right" else 0
      given = _sum(start, width, width, multiplier, function, first_index)
      stem = (
         f"Express {math(given)} as a definite integral in the variable {variable}, taking {variable} to be the "
         f"sample point {math(_sample(start, width))}."
      )
      steps = [
         Step(
            text=f"The factor {math(rf'\frac{{{width}}}{{n}}')} is the subinterval width, so the interval has length {width}.",
            rule="width of a uniform partition",
         ),
         Step(
            text=(
               f"The sample point is {math(_sample(start, width))}, which is {start} plus k widths, so the interval starts at "
               f"{variable} = {start} and ends at {variable} = {start} + {width} = {finish}."
            ),
            rule="sample point gives the lower limit",
         ),
         Step(
            text=f"The remaining factor is the function evaluated at the sample point, so the limit equals {math(key_integral)}.",
            rule="limit of Riemann sums as a definite integral",
         ),
      ]
      key_label = f"{math(key_integral)}"
      distractors = [
         Distractor(
            error_path="BC-ERR-06003",
            derivation=f"k/n read as the variable on [0, 1] with only 1/n as the width, so the factor {width} of the width is lost",
            label=f"{math(rf'\int_{{0}}^{{1}} ' + _scaled(multiplier, FUNCTION_TEX[function](f'{start} + {width}{variable}')) + rf'\,d{variable}')}",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-99028",
            derivation=f"the width {width}/n kept as a factor of the integrand as well as becoming d{variable}, so the width is counted twice",
            label=f"{math(_integral(start, finish, multiplier * width, function, variable))}",
            mechanism="algebra_slip",
         ),
         Distractor(
            error_path="BC-ERR-99032",
            derivation=f"the limits read as 0 to the width {width}, limits the sum never gives",
            label=f"{math(_integral(0, width, multiplier, function, variable))}",
            mechanism="wrong_limits",
         ),
      ]
   else:
      stem = (
         f"Write {math(key_integral)} as the limit of a right Riemann sum with n subintervals of equal width, "
         "using k as the index of summation."
      )
      steps = [
         Step(
            text=f"The interval [{start}, {finish}] has length {width}, so each of the n subintervals has width {math(rf'\Delta {variable} = \frac{{{width}}}{{n}}')}.",
            rule="width of a uniform partition",
         ),
         Step(
            text=f"The right endpoint of the kth subinterval is {math(f'{variable}_k = ' + _sample(start, width))}, for k = 1 to n.",
            rule="right endpoints",
         ),
         Step(
            text=f"Multiply the function value at each right endpoint by the width and take the limit: {math(key_sum)}.",
            rule="definite integral as a limit of Riemann sums",
         ),
      ]
      key_label = f"{math(key_sum)}"
      distractors = [
         Distractor(
            error_path="BC-ERR-06003",
            derivation="the function values at the right endpoints added with no subinterval width",
            label=f"{math(_sum(start, width, width, multiplier, function, with_width=False))}",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-99028",
            derivation=f"the width taken as 1/n as though the interval had length 1, although the sample points step by {width}/n",
            label=f"{math(_sum(start, width, 1, multiplier, function))}",
            mechanism="algebra_slip",
         ),
         Distractor(
            error_path="BC-ERR-99032",
            derivation=f"the sample points started at 0 instead of {start}, so the sum is over [0, {width}], an interval the integral never gives",
            label=f"{math(_sum(0, width, width, multiplier, function))}",
            mechanism="wrong_limits",
         ),
      ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="express",
   )
