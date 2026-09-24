"""BC-QA-06001, a left or right Riemann sum over the subintervals a table of rates indicates."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure

ARCHETYPE_ID = "BC-QA-06001"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

GAP_COUNT = 4

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "gaps", "type": "integer", "role": "safe", "count": 4, "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "even_gap", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "rates", "type": "integer", "role": "safe", "count": 5, "domain": {"min": 2, "max": 20, "step": 1}},
      {"name": "endpoint", "type": "label", "role": "safe", "domain": {"values": ["left", "right"]}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["tank", "traffic", "rain", "download"]}},
      {"name": "spacing", "type": "label", "role": "difficulty", "domain": {"values": ["uniform", "nonuniform"]}},
      {"name": "framing", "type": "label", "role": "difficulty", "domain": {"values": ["bare", "context"]}},
   ],
   "constraints": [
      "spacing == 'uniform' or not (gaps[0] == gaps[1] and gaps[1] == gaps[2] and gaps[2] == gaps[3])",
      "spacing == 'uniform' or total_time % 4 == 0",
      "spacing == 'nonuniform' or chosen_sum % 4 == 0",
      "distinct([chosen_sum, other_sum, chosen_values, third_option])",
   ],
   "derived": [
      {"name": "width_0", "expression": "gaps[0] if spacing == 'nonuniform' else even_gap"},
      {"name": "width_1", "expression": "gaps[1] if spacing == 'nonuniform' else even_gap"},
      {"name": "width_2", "expression": "gaps[2] if spacing == 'nonuniform' else even_gap"},
      {"name": "width_3", "expression": "gaps[3] if spacing == 'nonuniform' else even_gap"},
      {"name": "total_time", "expression": "width_0 + width_1 + width_2 + width_3"},
      {"name": "left_sum", "expression": "width_0 * rates[0] + width_1 * rates[1] + width_2 * rates[2] + width_3 * rates[3]"},
      {"name": "right_sum", "expression": "width_0 * rates[1] + width_1 * rates[2] + width_2 * rates[3] + width_3 * rates[4]"},
      {"name": "left_values", "expression": "rates[0] + rates[1] + rates[2] + rates[3]"},
      {"name": "right_values", "expression": "rates[1] + rates[2] + rates[3] + rates[4]"},
      {"name": "chosen_sum", "expression": "left_sum if endpoint == 'left' else right_sum"},
      {"name": "other_sum", "expression": "right_sum if endpoint == 'left' else left_sum"},
      {"name": "chosen_values", "expression": "left_values if endpoint == 'left' else right_values"},
      {"name": "third_option", "expression": "total_time * chosen_values / 4 if spacing == 'nonuniform' else chosen_sum / 4"},
   ],
   "invariants": [
      "exact(key)",
      "key == chosen_sum",
      "is_integer(key)",
   ],
   "dial_bindings": [
      {"parameter": "spacing", "difficulty_factor_id": "BC-DF-14", "settings": {"uniform": "off", "nonuniform": "low"}},
      {"parameter": "framing", "difficulty_factor_id": "BC-DF-05", "settings": {"bare": "off", "context": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-03", "figure_kind": "table", "requires": ["gaps", "rates", "spacing"]},
      {"representation": "BC-REP-05", "figure_kind": "table", "requires": ["gaps", "rates", "spacing", "context"]},
   ],
   "notes": (
      "Five table rows give four subintervals. With nonuniform spacing the widths are the drawn gaps and the total "
      "time is a multiple of 4, so the one-width distractor is a whole number; with uniform spacing every width is "
      "even_gap and the averaging distractor, the sum divided by 4, is a whole number. The Riemann sum itself is exact."
   ),
}

CONTEXTS = {
   "tank": ("Water is pumped into a tank at a rate of R(t) liters per minute", "minutes", "liters per minute", "liters"),
   "traffic": ("Cars pass a checkpoint at a rate of R(t) cars per hour", "hours", "cars per hour", "cars"),
   "rain": ("Rain falls on a field at a rate of R(t) millimeters per hour", "hours", "millimeters per hour", "millimeters"),
   "download": ("A file downloads at a rate of R(t) megabytes per second", "seconds", "megabytes per second", "megabytes"),
}


def build(names):
   widths = [names[f"width_{index}"] for index in range(GAP_COUNT)]
   rates = [int(value) for value in names["rates"]]
   times = [0]

   for width in widths:
      times.append(times[-1] + int(width))

   total_time = times[-1]
   is_left = names["endpoint"] == "left"
   endpoint = names["endpoint"]
   chosen_rates = rates[:GAP_COUNT] if is_left else rates[1:]
   other_rates = rates[1:] if is_left else rates[:GAP_COUNT]
   chosen_sum = sum(int(width) * rate for width, rate in zip(widths, chosen_rates))
   other_sum = sum(int(width) * rate for width, rate in zip(widths, other_rates))
   chosen_values = sum(chosen_rates)
   is_context = names["framing"] == "context"
   is_uniform = names["spacing"] == "uniform"
   integral_text = math(rf"\int_{{0}}^{{{total_time}}} R(t)\,dt")

   if is_context:
      opening, time_unit, rate_unit, amount_unit = CONTEXTS[names["context"]]
      window_text = math(r"0 \le t \le " + str(total_time))
      columns = [f"t ({time_unit})", f"R(t) ({rate_unit})"]
      stem = (
         f"{opening}, where t is measured in {time_unit} for {window_text}. Selected values of "
         f"R(t) are shown in the table. Using a {endpoint} Riemann sum with the four subintervals indicated by the "
         f"table, approximate {integral_text}. Show the setup for the sum, and give the answer in {amount_unit}."
      )
      representation = "BC-REP-05"
   else:
      amount_unit = None
      columns = ["t", "R(t)"]
      stem = (
         "The function R is differentiable, and selected values of R(t) are shown in the table. Using a "
         f"{endpoint} Riemann sum with the four subintervals indicated by the table, approximate {integral_text}. "
         "Show the setup for the sum."
      )
      representation = "BC-REP-03"

   rows = [[time, rate] for time, rate in zip(times, rates)]
   table = table_figure(
      columns,
      rows,
      alt="A table of R(t): " + "; ".join(f"at t = {time}, R(t) = {rate}" for time, rate in rows) + ".",
   )

   width_text = ", ".join(str(int(width)) for width in widths)
   products = " + ".join(f"{int(width)}({rate})" for width, rate in zip(widths, chosen_rates))
   unit_suffix = f" {amount_unit}" if amount_unit else ""
   steps = [
      Step(
         text=(
            f"The table gives four subintervals with endpoints {', '.join(str(time) for time in times)}, so their "
            f"widths are {width_text}."
         ),
         rule="subinterval widths from the table",
      ),
      Step(
         text=f"A {endpoint} Riemann sum uses the value of R at the {endpoint} end of each subinterval: {math(products)}.",
         point_type_id="BC-PT-99018",
         rule="Riemann sum",
      ),
      Step(
         text=f"So {integral_text} is approximately {math(str(chosen_sum))}{unit_suffix}.",
         value=sympy.Integer(chosen_sum),
         point_type_id="BC-PT-99019",
         rule="arithmetic",
      ),
   ]

   opposite = "right" if is_left else "left"
   distractors = [
      Distractor(
         error_path="BC-ERR-06002",
         derivation=f"the {opposite} endpoint of each subinterval used where a {endpoint} sum was asked for",
         value=sympy.Integer(other_sum),
         mechanism="wrong_limits",
      ),
      Distractor(
         error_path="BC-ERR-06003",
         derivation=f"the four {endpoint} endpoint values of R added with no widths",
         value=sympy.Integer(chosen_values),
         mechanism="conceptual_confusion",
      ),
   ]

   if is_uniform:
      distractors.append(Distractor(
         error_path="BC-ERR-99028",
         derivation="the Riemann sum divided by the number of subintervals, as though averaging the rate",
         value=sympy.Rational(chosen_sum, GAP_COUNT),
         mechanism="algebra_slip",
      ))
   else:
      distractors.append(Distractor(
         error_path="BC-ERR-06001",
         derivation=f"one common width, {total_time}/4, used for every subinterval although the table inputs are unevenly spaced",
         value=sympy.Rational(total_time * chosen_values, GAP_COUNT),
         mechanism="conceptual_confusion",
      ))

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=sympy.Integer(chosen_sum), units=amount_unit),
      steps=steps,
      distractors=distractors,
      representation=representation,
      calculator_status="calculator",
      figure=table,
      setup_required=True,
      command_verb="approximate",
      notes={"is_uniform": is_uniform},
   )
