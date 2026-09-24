"""BC-QA-07008, an exponential growth or decay model built from two data values and solved."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-07008"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "change", "type": "label", "role": "difficulty", "domain": {"values": ["growth", "decay"]}},
      {"name": "factor", "type": "rational", "role": "safe", "domain": {"values": ["2", "3", "4", "3/2", "5/2"]}},
      {"name": "initial", "type": "integer", "role": "safe", "domain": {"min": 20, "max": 600, "step": 20}},
      {"name": "elapsed", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["bacteria", "mold", "insects", "users"]}},
   ],
   "constraints": [
      "change == 'growth' or is_integer(initial / factor)",
   ],
   "derived": [
      {"name": "ratio", "expression": "factor if change == 'growth' else 1 / factor"},
      {"name": "later", "expression": "initial * ratio"},
   ],
   "invariants": [
      "exact(key)",
      "later != initial",
      "is_integer(later)",
   ],
   "dial_bindings": [
      {"parameter": "change", "difficulty_factor_id": "BC-DF-12", "settings": {"growth": "off", "decay": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["change", "factor", "initial", "elapsed", "context"]},
   ],
   "notes": "The later value is the initial value times the drawn factor or its reciprocal, a whole number, so k = ln(ratio) / elapsed is exact and the key P0 e^(kt) has no decimal. The ratio is never e to the elapsed time, so the constant-free model k = 1 is always wrong, and the initial value is never 1, so the single-pair constant differs from the key's.",
}

t = sympy.Symbol("t")

CONTEXTS = {
   "bacteria": ("The number of bacteria B in a culture", "B", "bacteria", "hours"),
   "mold": ("The mass M of a mold colony, in grams,", "M", "grams", "days"),
   "insects": ("The number of insects N in a colony", "N", "insects", "weeks"),
   "users": ("The number of active users U of an online service", "U", "users", "months"),
}


def build(names):
   initial = int(names["initial"])
   later = int(names["later"])
   ratio = sympy.Rational(names["ratio"])
   elapsed = int(names["elapsed"])
   subject, letter, units, time_unit = CONTEXTS[names["context"]]

   rate_constant = sympy.log(ratio) / elapsed
   key_value = initial * sympy.exp(rate_constant * t)

   stem = (
      f"{subject} changes at a rate proportional to {letter}, where t is measured in {time_unit}. At {math('t = 0')}, "
      f"{math(f'{letter} = {initial}')} {units}, and at {math(f't = {elapsed}')}, {math(f'{letter} = {later}')} {units}. "
      f"Find an expression for {math(f'{letter}(t)')}."
   )

   steps = [
      Step(
         text=(
            f"The model is {math(rf'\frac{{d{letter}}}{{dt}} = k{letter}')}. Separating and integrating gives "
            f"{math(rf'\ln|{letter}| = kt + C')}, so {math(f'{letter} = {letter}_0 e^{{kt}}')}, and the value at t = 0 gives "
            f"{math(f'{letter}_0 = {initial}')}."
         ),
         rule="separation of variables for proportional growth",
      ),
      Step(
         text=(
            f"The second value gives {math(f'{later} = {initial} e^{{{elapsed}k}}')}, so "
            f"{math(f'k = ' + tex(rate_constant))}."
         ),
         rule="constant from a second data pair",
      ),
      Step(
         text=f"Therefore {math(f'{letter}(t) = ' + tex(key_value))} {units}.",
         value=key_value,
         rule="particular solution",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-07034",
         derivation="a straight-line model through the two data values, a constant rate of change instead of a constant relative rate",
         value=initial + sympy.Rational(later - initial, elapsed) * t,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-07036",
         derivation=f"k read from the later value alone, {later} = e^({elapsed}k), with the initial value left out",
         value=initial * sympy.exp(sympy.log(later) / elapsed * t),
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-07001",
         derivation=f"the rate written equal to {letter} with no constant, so k is 1 and the second value is never used",
         value=initial * sympy.exp(t),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value, units=units),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="no_calculator",
      command_verb="find",
   )
