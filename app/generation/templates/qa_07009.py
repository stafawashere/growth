"""BC-QA-07009, a logistic model read without solving: the limiting value and the value where growth is fastest."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-07009"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["factored", "expanded"]}},
      {"name": "capacity", "type": "integer", "role": "safe", "domain": {"min": 100, "max": 2000, "step": 100}},
      {"name": "rate", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1/3", "1/4", "1/5", "2/5"]}},
      {"name": "start_share", "type": "rational", "role": "safe", "domain": {"values": ["1/10", "1/5", "1/4", "3/10", "2/5"]}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["deer", "fish", "rumor", "app"]}},
   ],
   "constraints": [],
   "derived": [
      {"name": "initial", "expression": "capacity * start_share"},
      {"name": "half", "expression": "capacity / 2"},
   ],
   "invariants": [
      "is_integer(initial)",
      "0 < initial",
      "initial < half",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-02", "settings": {"factored": "off", "expanded": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-06", "figure_kind": None, "requires": ["form", "capacity", "rate", "start_share", "context"]},
   ],
   "notes": "The right side is r P (1 - P/M) or its expansion r P - (r/M) P^2, with zeros at 0 and M. The initial value lies strictly between 0 and M/2, so the solution rises to M and passes through M/2, where the quadratic right side is largest.",
}

CONTEXTS = {
   "deer": ("The number of deer P in a forest", "deer", "years"),
   "fish": ("The number of fish P in a lake", "fish", "months"),
   "rumor": ("The number of people P in a town who have heard a rumor", "people", "days"),
   "app": ("The number of people P who have installed an app", "people", "weeks"),
}


def _reading(units, limit_value, fastest_value):
   return (
      f"P approaches {math(tex(limit_value))} {units} as t increases without bound, and P is growing fastest when "
      f"{math('P = ' + tex(fastest_value))} {units}."
   )


def build(names):
   capacity = int(names["capacity"])
   rate = sympy.Rational(names["rate"])
   initial = int(names["initial"])
   half = sympy.Rational(capacity, 2)
   subject, units, time_unit = CONTEXTS[names["context"]]
   population = sympy.Symbol("P")

   if names["form"] == "factored":
      right_tex = rf"{tex(rate)}P\left(1 - \frac{{P}}{{{capacity}}}\right)"
   else:
      right_tex = f"{tex(rate * population)} - {tex(rate / capacity * population**2)}"

   stem = (
      f"{subject} is modeled by the differential equation {math(rf'\frac{{dP}}{{dt}} = {right_tex}')}, where t is "
      f"measured in {time_unit}, and {math(f'P(0) = {initial}')}. Without solving the equation, find the limit of P as t "
      "increases without bound, and the value of P at which P is growing fastest."
   )

   key_label = _reading(units, capacity, half)

   steps = [
      Step(
         text=f"The right side equals {math(tex(rate) + rf'P\left(1 - \frac{{P}}{{{capacity}}}\right)')}, which is 0 at P = 0 and at P = {capacity}, so the carrying capacity is {capacity}.",
         rule="zeros of the logistic right side",
      ),
      Step(
         text=(
            f"For 0 < P < {capacity} the right side is positive, and P(0) = {initial} lies in that range, so P increases "
            f"and approaches {capacity} {units} as t increases without bound."
         ),
         rule="sign of the rate gives the limit",
      ),
      Step(
         text=(
            f"The right side is a quadratic in P that opens downward with zeros at 0 and {capacity}, so it is largest "
            f"halfway between them, at P = {tex(half)} {units}; P passes through that value because it starts below it."
         ),
         rule="vertex of the quadratic rate",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-07042",
         derivation="the value of fastest growth reported as the carrying capacity itself",
         label=_reading(units, capacity, capacity),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-07040",
         derivation="the limiting value read from the other zero of the right side, P = 0",
         label=_reading(units, 0, half),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-07041",
         derivation="a limit named without using the sign of the rate, the initial value taken as the level the population settles at",
         label=_reading(units, initial, half),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-06",
      calculator_status="no_calculator",
      command_verb="find",
   )
