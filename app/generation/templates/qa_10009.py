"""BC-QA-10009, a Lagrange error bound from a supplied bound on the next derivative."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-10009"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "given", "type": "label", "role": "difficulty", "domain": {"values": ["bound", "endpoints"]}},
      {"name": "degree", "type": "integer", "role": "safe", "domain": {"values": [2, 3, 4]}},
      {"name": "centre", "type": "integer", "role": "safe", "domain": {"values": [-2, -1, 1, 2, 3]}},
      {"name": "step", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "-1/2", "1/3", "-1/3", "2/3", "1/4", "-1/4", "3/4", "2/5", "-2/5"]}},
      {"name": "maximum", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 12, "step": 1}},
      {"name": "minimum", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 11, "step": 1}},
   ],
   "constraints": [
      "minimum < maximum",
      "centre != -2 * step",
      "abs(step) * (degree + 1) != 1",
   ],
   "derived": [
      {"name": "target", "expression": "centre + step"},
   ],
   "invariants": [
      "exact(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "given", "difficulty_factor_id": "BC-DF-14", "settings": {"bound": "off", "endpoints": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["given", "degree", "centre", "step", "maximum"]},
   ],
   "notes": "The polynomial of degree k about the centre approximates f at centre + step. Either the bound on the (k+1)th derivative is supplied, or that derivative is positive and increasing on the interval with its endpoint values given, so the maximum sits at the right end. The centre is never -2 step, so the target and the step differ in size.",
}


ORDINALS = {3: "third", 4: "fourth", 5: "fifth"}


def build(names):
   degree = int(names["degree"])
   centre = names["centre"]
   step = names["step"]
   target = names["target"]
   maximum = names["maximum"]
   minimum = names["minimum"]
   order = degree + 1
   ordinal = ORDINALS[order]
   is_supplied = names["given"] == "bound"

   low, high = sorted([centre, target])
   interval = math(rf"{tex(low)} \le x \le {tex(high)}")
   derivative = rf"f^{{({order})}}"
   distance = abs(step)
   bound = maximum * distance**order / sympy.factorial(order)

   if is_supplied:
      information = f"For all x in the interval {interval}, {math(rf'\left|{derivative}(x)\right| \le {maximum}')}."
      maximum_step = f"The bound on the {ordinal} derivative over the interval is given: {math(f'M = {maximum}')}."
   else:
      near, far = low, high
      information = (
         f"On the interval {interval}, {math(f'{derivative}(x)')} is positive and increasing, with "
         f"{math(f'{derivative}({tex(near)}) = {minimum}')} and {math(f'{derivative}({tex(far)}) = {maximum}')}."
      )
      maximum_step = f"An increasing positive function is largest at the right end of the interval, so {math(f'M = {derivative}({tex(far)}) = {maximum}')}."

   stem = (
      f"Let {math(f'P_{degree}(x)')} be the Taylor polynomial of degree {degree} for a function f about {math(f'x = {centre}')}. "
      f"{information} Use the Lagrange error bound to find an upper bound for {math(rf'\left|f({tex(target)}) - P_{degree}({tex(target)})\right|')}."
   )
   formula = rf"\frac{{M}}{{{order}!}} \left|{tex(target)} - {'(' + str(centre) + ')' if centre < 0 else centre}\right|^{{{order}}}"
   steps = [
      Step(text=f"A polynomial of degree {degree} needs the bound M on the {ordinal} derivative. {maximum_step}", rule="order of the bounding derivative"),
      Step(text=f"The Lagrange error bound is {math(rf'\left|f({tex(target)}) - P_{degree}({tex(target)})\right| \le {formula}')}.", point_type_id="BC-PT-99039", rule="Lagrange error bound form"),
      Step(text=f"With {math(f'M = {maximum}')} and distance {math(tex(distance))}, the bound is {math(rf'\frac{{{maximum}}}{{{sympy.factorial(order)}}} \left({tex(distance)}\right)^{{{order}}} = {tex(bound)}')}.", value=bound, point_type_id="BC-PT-99041", rule="evaluate the bound"),
   ]

   if is_supplied:
      third = Distractor("BC-ERR-10032", f"the power of the distance taken as {degree}, the degree of the polynomial, instead of {order}", value=maximum * distance**degree / sympy.factorial(order), mechanism="algebra_slip")
   else:
      third = Distractor("BC-ERR-10032", f"the derivative's value {minimum} at the near end used in place of its maximum {maximum}", value=minimum * distance**order / sympy.factorial(order), mechanism="conceptual_confusion")

   distractors = [
      Distractor("BC-ERR-10032", f"the factorial taken as {degree}! instead of {order}!", value=maximum * distance**order / sympy.factorial(degree), mechanism="algebra_slip"),
      Distractor("BC-ERR-10025", f"the bound evaluated at the input {target} itself instead of at its distance {distance} from the centre", value=maximum * abs(target) ** order / sympy.factorial(order), mechanism="algebra_slip"),
      third,
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=bound),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
