"""BC-QA-07006, a differential equation and its initial condition written from a verbal rate statement."""
from app.generation.kit import Distractor, Instance, Key, Step, math

ARCHETYPE_ID = "BC-QA-07006"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["temperature", "concentration", "tank", "price"]}},
      {"name": "level", "type": "integer", "role": "safe", "domain": {"min": 20, "max": 95, "step": 5}},
      {"name": "gap", "type": "integer", "role": "safe", "domain": {"min": 5, "max": 60, "step": 5}},
      {"name": "approach", "type": "label", "role": "difficulty", "domain": {"values": ["from_below", "from_above"]}},
      {"name": "time_unit", "type": "label", "role": "safe", "domain": {"values": ["minutes", "hours"]}},
   ],
   "constraints": [
      "approach == 'from_above' or gap < level",
   ],
   "derived": [
      {"name": "initial", "expression": "level + gap if approach == 'from_above' else level - gap"},
   ],
   "invariants": [
      "initial > 0",
      "initial != level",
   ],
   "dial_bindings": [
      {"parameter": "approach", "difficulty_factor_id": "BC-DF-14", "settings": {"from_below": "off", "from_above": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-04", "figure_kind": None, "requires": ["context", "level", "gap", "approach", "time_unit"]},
   ],
   "notes": "The stem fixes k as a positive constant, so the rate toward the level is k times (level minus quantity) whichever side the quantity starts on; reversing the difference makes the quantity move away from the level.",
}

CONTEXTS = {
   "temperature": ("T", "The temperature T of a metal rod, in degrees Celsius, placed in a chamber held at {level} degrees Celsius", "the chamber temperature"),
   "concentration": ("C", "The concentration C of a medication in a patient's blood, in milligrams per liter, during an infusion that settles at {level} milligrams per liter", "the settling concentration"),
   "tank": ("H", "The height H of the water in a tank, in centimeters, connected to a reservoir whose water stands at {level} centimeters", "the reservoir height"),
   "price": ("P", "The price P of a product, in dollars, in a market whose equilibrium price is {level} dollars", "the equilibrium price"),
}


def _option(equation, letter, initial):
   return f"{math(equation)}, with {math(f'{letter}(0) = {initial}')}"


def build(names):
   level = int(names["level"])
   initial = int(names["initial"])
   letter, subject_template, level_name = CONTEXTS[names["context"]]
   subject = subject_template.format(level=level)
   time_unit = names["time_unit"]
   derivative = rf"\frac{{d{letter}}}{{dt}}"

   stem = (
      f"{subject} moves toward {level_name} at a rate proportional to the difference between {level_name} and {letter}. At time "
      f"{math('t = 0')} {time_unit}, {math(f'{letter} = {initial}')}. Using k for the positive constant of "
      f"proportionality, write a differential equation for {letter} as a function of t and state the initial condition."
   )

   key_equation = rf"{derivative} = k\left({level} - {letter}\right)"
   key_label = _option(key_equation, letter, initial)
   heading = "up toward" if initial < level else "down toward"

   steps = [
      Step(
         text=f"The dependent variable is {letter} and the independent variable is t in {time_unit}, so the rate is {math(derivative)}.",
         rule="naming the variables",
      ),
      Step(
         text=(
            f"Proportional to the difference means a constant multiple of it. With k positive, {math(f'k({level} - {letter})')} "
            f"is positive when {letter} is below {level} and negative when it is above, so {letter} moves {heading} {level} "
            f"from its starting value."
         ),
         rule="proportionality as a constant multiple",
      ),
      Step(
         text=f"The equation is {math(key_equation)}, and the initial condition, stated separately, is {math(f'{letter}(0) = {initial}')}.",
         rule="differential equation with initial condition",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-07001",
         derivation="proportional read as equal, so the constant k never appears",
         label=_option(rf"{derivative} = {level} - {letter}", letter, initial),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-07002",
         derivation=f"the difference written as {letter} minus the level, which with k positive drives {letter} away from {level}",
         label=_option(rf"{derivative} = k\left({letter} - {level}\right)", letter, initial),
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-07004",
         derivation=f"the initial value {initial} substituted for {letter} inside the equation, so the rate becomes a constant",
         label=_option(rf"{derivative} = k\left({level} - {initial}\right)", letter, initial),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-04",
      calculator_status="no_calculator",
      command_verb="write",
   )
