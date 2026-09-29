"""BC-QA-02014, an instantaneous rate asked for before the derivative is defined, answered as a limit of average rates."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-02014"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 15 of 2026-09-28"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "degree", "type": "integer", "role": "difficulty", "domain": {"values": [2, 3]}},
      {"name": "leading", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "linear", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 20, "step": 1}},
      {"name": "instant", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["height", "position", "volume"]}},
   ],
   "constraints": [
      "rate != 0",
      "distinct([rate, average, value, change])",
   ],
   "derived": [
      {"name": "rate", "expression": "degree * leading * instant**(degree - 1) + linear"},
      {"name": "average", "expression": "leading * instant**(degree - 1) + linear"},
      {"name": "value", "expression": "leading * instant**degree + linear * instant + constant"},
      {"name": "change", "expression": "leading * instant**degree + linear * instant"},
   ],
   "invariants": [
      "exact(key)",
      "key == rate",
   ],
   "dial_bindings": [
      {"parameter": "degree", "difficulty_factor_id": "BC-DF-06", "settings": {"2": "low", "3": "medium"}},
      {"parameter": "degree", "difficulty_factor_id": "BC-DF-15", "settings": {"2": "low", "3": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["degree", "leading", "linear", "constant", "instant", "context"]},
   ],
   "notes": "A quantity f(t) = a t^d + b t + c with d = 2 or 3 is given in context and the rate at one instant t0 is asked for, with no mention of a derivative or a limit: the productive-failure opener for BC-CON-02002. The canonical answer is the limit of the average rate over [t0, t0 + h] as h approaches 0, d a t0^(d - 1) + b. The distractors are the average rate over [0, t0], the value f(t0), and the change f(t0) - f(0); the constraints keep all four apart and the rate nonzero.",
}

t = sympy.Symbol("t")
h = sympy.Symbol("h")

CONTEXTS = {
   "height": ("y", "The height of a ball above the ground, in meters, is", "for time t in seconds", "the height of the ball changing", "seconds"),
   "position": ("s", "A particle moves along a line, and its position, in centimeters, is", "for time t in seconds", "the position of the particle changing", "seconds"),
   "volume": ("V", "The volume of water in a tank, in liters, is", "for time t in minutes", "the volume of water changing", "minutes"),
}


def build(names):
   degree = int(names["degree"])
   leading = int(names["leading"])
   linear = int(names["linear"])
   constant = int(names["constant"])
   instant = int(names["instant"])
   letter, opening, time_note, changing, unit = CONTEXTS[names["context"]]

   function = leading * t**degree + linear * t + constant
   rate = sympy.diff(function, t).subs(t, instant)
   shifted = sympy.expand((function.subs(t, instant + h) - function.subs(t, instant)) / h)
   value_at = function.subs(t, instant)
   start_value = function.subs(t, 0)

   stem = (
      f"{opening} {math(f'{letter}(t) = ' + tex(function))} {time_note}. "
      f"At what rate is {changing} at the instant t = {instant} {unit}?"
   )

   quotient = rf"\frac{{{letter}({instant} + h) - {letter}({instant})}}{{h}}"
   prime_at = f"{letter}'({instant})"
   steps = [
      Step(
         text=(
            f"An average rate is available over any interval, so take the short interval from t = {instant} to t = {instant} + h. "
            f"The average rate over it is {math(quotient)}."
         ),
         rule="average rate of change over a short interval",
      ),
      Step(
         text=f"Expanding and dividing by h leaves {math(quotient + ' = ' + tex(shifted))}, which still depends on the length h of the interval.",
         value=shifted,
         rule="difference quotient simplified",
      ),
      Step(
         text=(
            f"The rate at the instant is what these averages approach as h approaches 0: "
            f"{math(r'\lim_{h \to 0} ' + quotient + ' = ' + tex(rate))}. This limit is the derivative {math(prime_at)}."
         ),
         value=rate,
         rule="limit of the difference quotient",
      ),
   ]
   distractors = [
      Distractor("BC-ERR-02033", f"the average rate over the whole interval from t = 0 to t = {instant} reported as the rate at the instant", value=(value_at - start_value) / instant, mechanism="conceptual_confusion"),
      Distractor("BC-ERR-02027", f"the value {letter}({instant}) reported as the rate", value=value_at, mechanism="conceptual_confusion"),
      Distractor("BC-ERR-02001", f"the change {letter}({instant}) - {letter}(0) reported without dividing by the elapsed time", value=value_at - start_value, mechanism="algebra_slip"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=rate),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="no_calculator",
      command_verb="find",
   )
