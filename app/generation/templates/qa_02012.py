"""BC-QA-02012, a derivative statement converted between prime and Leibniz notation and read."""
from app.generation.kit import Distractor, Instance, Key, Step, math

ARCHETYPE_ID = "BC-QA-02012"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "order", "type": "label", "role": "difficulty", "domain": {"values": ["first", "second"]}},
      {"name": "framing", "type": "label", "role": "difficulty", "domain": {"values": ["bare", "context"]}},
      {"name": "supplied", "type": "label", "role": "safe", "domain": {"values": ["prime", "leibniz"]}},
      {"name": "setting", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 3, "step": 1}},
      {"name": "at", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "value", "type": "integer", "role": "safe", "domain": {"min": -12, "max": 12, "step": 1, "exclude": [0]}},
   ],
   "constraints": [
      "order == 'first' or value > 0",
   ],
   "derived": [],
   "invariants": [
      "len(key) > 0",
   ],
   "dial_bindings": [
      {"parameter": "order", "difficulty_factor_id": "BC-DF-04", "settings": {"first": "off", "second": "low"}},
      {"parameter": "framing", "difficulty_factor_id": "BC-DF-05", "settings": {"bare": "off", "context": "low"}},
      {"parameter": "framing", "difficulty_factor_id": "BC-DF-16", "settings": {"bare": "off", "context": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["order", "supplied", "setting", "at", "value"]},
      {"representation": "BC-REP-04", "figure_kind": None, "requires": ["order", "supplied", "setting", "at", "value"]},
   ],
   "notes": (
      "A derivative statement at a point is supplied in prime or Leibniz notation and the student writes it in "
      "the other notation and says what it means. The second derivative keeps the value positive so that the "
      "squared-derivative misreading is not ruled out by its sign alone."
   ),
}

BARE_SETTINGS = [
   {"dependent": "y", "independent": "x", "function": "f"},
   {"dependent": "w", "independent": "t", "function": "g"},
   {"dependent": "s", "independent": "u", "function": "h"},
   {"dependent": "r", "independent": "z", "function": "k"},
]

CONTEXT_SETTINGS = [
   {
      "dependent": "V", "independent": "t", "function": "V",
      "intro": "The volume of water in a tank is V(t) liters, t minutes after a valve is opened.",
      "quantity": "the volume of water", "input": "time",
      "unit": "liters", "unit_one": "liter", "input_unit": "minutes", "input_unit_one": "minute",
   },
   {
      "dependent": "P", "independent": "t", "function": "P",
      "intro": "The number of bacteria in a culture is P(t) thousand, t hours after the culture is started.",
      "quantity": "the number of bacteria", "input": "time",
      "unit": "thousand bacteria", "unit_one": "thousand bacteria", "input_unit": "hours", "input_unit_one": "hour",
   },
   {
      "dependent": "T", "independent": "x", "function": "T",
      "intro": "The temperature at a point x meters from one end of a metal rod is T(x) degrees Celsius.",
      "quantity": "the temperature", "input": "the distance along the rod",
      "unit": "degrees Celsius", "unit_one": "degree Celsius", "input_unit": "meters", "input_unit_one": "meter",
   },
   {
      "dependent": "H", "independent": "t", "function": "H",
      "intro": "The height of a weather balloon is H(t) meters, t seconds after it is released.",
      "quantity": "the height of the balloon", "input": "time",
      "unit": "meters", "unit_one": "meter", "input_unit": "seconds", "input_unit_one": "second",
   },
]


def _leibniz(dependent, independent, at, order):
   if order == "second":
      return rf"\left. \frac{{d^{{2}}{dependent}}}{{d{independent}^{{2}}}} \right|_{{{independent}={at}}}"

   return rf"\left. \frac{{d{dependent}}}{{d{independent}}} \right|_{{{independent}={at}}}"


def _prime(function, at, order):
   marks = "''" if order == "second" else "'"

   return f"{function}{marks}({at})"


def _words(setting, is_context, order):
   """How the key and each misreading describe the quantity, in words and with units."""
   dependent = setting["dependent"]
   independent = setting["independent"]

   if is_context:
      quantity = setting["quantity"]
      given_input = setting["input"]
      rate_unit = f"{setting['unit']} per {setting['input_unit_one']}"
      swapped_unit = f"{setting['input_unit']} per {setting['unit_one']}"
   else:
      quantity = dependent
      given_input = independent
      rate_unit = ""
      swapped_unit = ""

   if order == "second":
      rate_unit = f"{rate_unit} per {setting['input_unit_one']}" if is_context else ""
      swapped_unit = f"{swapped_unit} per {setting['unit_one']}" if is_context else ""

      return {
         "key": f"the rate of change, with respect to {given_input}, of the rate of change of {quantity}",
         "swapped": f"the rate of change, with respect to {quantity}, of the rate of change of {given_input}",
         "square": f"the square of the rate of change of {quantity} with respect to {given_input}",
         "constant": f"the rate of change, with respect to {given_input}, of the rate of change of {quantity}, the same at every {independent},",
         "unit": rate_unit,
         "swapped_unit": swapped_unit,
         "square_unit": f"{setting['unit']} squared per {setting['input_unit_one']} squared" if is_context else "",
      }

   quotient_unit = f"{setting['unit']} per {setting['input_unit_one']}" if is_context else ""

   return {
      "key": f"the rate of change of {quantity} with respect to {given_input}",
      "swapped": f"the rate of change of {given_input} with respect to {quantity}",
      "quotient": f"{quantity} divided by {given_input}",
      "constant": f"the rate of change of {quantity} with respect to {given_input}, the same at every {independent},",
      "unit": rate_unit,
      "swapped_unit": swapped_unit,
      "quotient_unit": quotient_unit,
   }


def _amount(value, unit):
   return f"{value} {unit}" if unit else f"{value}"


def build(names):
   order = names["order"]
   is_context = names["framing"] == "context"
   settings = CONTEXT_SETTINGS if is_context else BARE_SETTINGS
   setting = settings[int(names["setting"])]
   at = int(names["at"])
   value = int(names["value"])
   supplied_prime = names["supplied"] == "prime"

   dependent = setting["dependent"]
   independent = setting["independent"]
   function = setting["function"]
   leibniz = _leibniz(dependent, independent, at, order)
   prime = _prime(function, at, order)
   words = _words(setting, is_context, order)
   where = f"when {independent} = {at}"

   if is_context:
      intro = setting["intro"]
   else:
      intro = f"Let {math(f'{dependent} = {function}({independent})')} be a twice-differentiable function."

   if supplied_prime:
      supplied, target, target_name = prime, leibniz, "Leibniz"
   else:
      supplied, target, target_name = leibniz, prime, "prime"

   stem = (
      f"{intro} Suppose that {math(f'{supplied} = {value}')}. Write this statement in {target_name} notation, "
      "and state what it means."
   )

   key_label = f"{math(f'{target} = {value}')}, so {words['key']} {where} is {_amount(value, words['unit'])}."

   if order == "second":
      if supplied_prime:
         square_form = rf"\left(\frac{{d{dependent}}}{{d{independent}}}\right)^{{2}} = {value} \text{{ at }} {independent} = {at}"
         constant_form = rf"\frac{{d^{{2}}{dependent}}}{{d{independent}^{{2}}}} = {value}"
         swapped_form = rf"\left. \frac{{d^{{2}}{independent}}}{{d{dependent}^{{2}}}} \right|_{{{independent}={at}}} = {value}"
      else:
         square_form = rf"\left({function}'({at})\right)^{{2}} = {value}"
         constant_form = f"{function}''({independent}) = {value}"
         swapped_form = f"{target} = {value}"

      distractors = [
         Distractor(
            error_path="BC-ERR-03022",
            derivation="the second derivative written as the square of the first derivative",
            label=f"{math(square_form)}, so {words['square']} {where} is {_amount(value, words['square_unit'])}.",
         ),
         Distractor(
            error_path="BC-ERR-02030",
            derivation="the point of evaluation dropped, so a value at one input is read as the second derivative function",
            label=f"{math(constant_form)}, so {words['constant']} is {_amount(value, words['unit'])}.",
         ),
         Distractor(
            error_path="BC-ERR-04017",
            derivation="the roles of the two variables exchanged, so the derivative is read with respect to the dependent variable",
            label=f"{math(swapped_form)}, so {words['swapped']} {where} is {_amount(value, words['swapped_unit'])}.",
         ),
      ]
   else:
      quotient_form = rf"\frac{{{function}({at})}}{{{at}}} = {value}"

      if supplied_prime:
         constant_form = rf"\frac{{d{dependent}}}{{d{independent}}} = {value}"
         swapped_form = rf"\left. \frac{{d{independent}}}{{d{dependent}}} \right|_{{{independent}={at}}} = {value}"
      else:
         constant_form = f"{function}'({independent}) = {value}"
         swapped_form = f"{target} = {value}"

      distractors = [
         Distractor(
            error_path="BC-ERR-02029",
            derivation="the Leibniz fraction read as the quotient of the two quantities at the point",
            label=f"{math(quotient_form)}, so {words['quotient']} {where} is {_amount(value, words['quotient_unit'])}.",
         ),
         Distractor(
            error_path="BC-ERR-02030",
            derivation="the point of evaluation dropped, so a value at one input is read as the derivative function",
            label=f"{math(constant_form)}, so {words['constant']} is {_amount(value, words['unit'])}.",
         ),
         Distractor(
            error_path="BC-ERR-04017",
            derivation="the roles of the two variables exchanged, so the derivative is read with respect to the dependent variable",
            label=f"{math(swapped_form)}, so {words['swapped']} {where} is {_amount(value, words['swapped_unit'])}.",
         ),
      ]

   for distractor in distractors:
      distractor.mechanism = "conceptual_confusion"

   derivative_kind = "second derivative" if order == "second" else "derivative"
   steps = [
      Step(
         text=(
            f"In {math(supplied)} the function is {function}, the independent variable is {independent}, and the "
            f"{derivative_kind} is evaluated at {independent} = {at}, so the statement is about one input only."
         ),
         rule="read the notation",
      ),
      Step(
         text=f"In {target_name} notation the same statement is {math(f'{target} = {value}')}.",
         rule="convert the notation",
      ),
      Step(
         text=f"It says that {words['key']} {where} is {_amount(value, words['unit'])}.",
         rule="interpret the derivative",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-04" if is_context else "BC-REP-01",
      calculator_status="no_calculator",
      command_verb="write",
      notes={"order": order},
   )
