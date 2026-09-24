"""BC-QA-04002, a derivative approximated from a table by an average rate of change, with units."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure, tex

ARCHETYPE_ID = "BC-QA-04002"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "times", "type": "integer", "role": "safe", "count": 5, "distinct": True, "order": "increasing", "domain": {"min": 0, "max": 12, "step": 1}},
      {"name": "readings", "type": "integer", "role": "safe", "count": 5, "distinct": True, "order": "increasing", "domain": {"min": 10, "max": 90, "step": 1}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["reservoir", "runner", "oven", "download", "crowd", "rainfall"]}},
      {"name": "trend", "type": "label", "role": "difficulty", "domain": {"values": ["increasing", "decreasing"]}},
   ],
   "constraints": [
      "distinct([key_rate, left_rate, right_rate, change])",
   ],
   "derived": [
      {"name": "column", "expression": "readings if trend == 'increasing' else [readings[4], readings[3], readings[2], readings[1], readings[0]]"},
      {"name": "change", "expression": "column[3] - column[1]"},
      {"name": "key_rate", "expression": "(column[3] - column[1]) / (times[3] - times[1])"},
      {"name": "left_rate", "expression": "(column[2] - column[1]) / (times[2] - times[1])"},
      {"name": "right_rate", "expression": "(column[3] - column[2]) / (times[3] - times[2])"},
   ],
   "invariants": [
      "exact(key)",
      "key == key_rate",
      "key != 0",
   ],
   "dial_bindings": [
      {"parameter": "trend", "difficulty_factor_id": "BC-DF-12", "settings": {"increasing": "off", "decreasing": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-03", "figure_kind": "table", "requires": ["times", "readings", "trend", "context"]},
   ],
   "notes": "Five tabulated readings at increasing times; the named interval runs from the second to the fourth row and brackets the point of interest at the third row, so the one-sided pairs are the wrong-row distractors.",
}

CONTEXTS = {
   "reservoir": ("R", "the amount of water in a reservoir", "t", "days", "day", "millions of gallons", "million gallons"),
   "runner": ("D", "the distance a runner has covered on a trail", "t", "minutes", "minute", "meters", "meters"),
   "oven": ("H", "the temperature inside an oven", "t", "minutes", "minute", "degrees Fahrenheit", "degrees Fahrenheit"),
   "download": ("F", "the amount of a file that has downloaded", "t", "seconds", "second", "megabytes", "megabytes"),
   "crowd": ("P", "the number of people inside a stadium", "t", "minutes", "minute", "hundreds of people", "hundreds of people"),
   "rainfall": ("W", "the depth of water in a rain barrel", "t", "hours", "hour", "centimeters", "centimeters"),
}


def build(names):
   letter, subject, variable, time_plural, time_single, units_heading, units = CONTEXTS[names["context"]]
   times = [int(value) for value in names["times"]]
   column = [int(value) for value in names["column"]]
   low_time, point_time, high_time = times[1], times[2], times[3]
   low_value, point_value, high_value = column[1], column[2], column[3]

   change = sympy.Integer(high_value - low_value)
   key_value = change / (high_time - low_time)
   left_value = sympy.Rational(point_value - low_value, point_time - low_time)
   right_value = sympy.Rational(high_value - point_value, high_time - point_time)
   rate_units = f"{units} per {time_single}"
   derivative_at_point = f"{letter}'({point_time})"

   table = table_figure(
      [f"{variable} ({time_plural})", f"{letter}({variable}) ({units_heading})"],
      [[str(time), str(value)] for time, value in zip(times, column)],
      alt=(
         f"The table lists {letter}({variable}) at five times, "
         + "; ".join(f"{letter}({time}) = {value}" for time, value in zip(times, column))
         + "."
      ),
   )

   stem = (
      f"The function {letter} is differentiable, and {letter}({variable}) gives {subject}, in {units_heading}, at time "
      f"{variable} {time_plural}. Selected values of {letter}({variable}) are given in the table. Using the average rate of "
      f"change of {letter} over the interval {math(rf'{low_time} \le {variable} \le {high_time}')}, approximate "
      f"{math(derivative_at_point)}. Give the exact value of the approximation and indicate units of measure."
   )

   difference_tex = rf"\frac{{{letter}({high_time}) - {letter}({low_time})}}{{{high_time} - {low_time}}}"
   numbers_tex = rf"\frac{{{high_value} - {low_value}}}{{{high_time} - {low_time}}}"
   quotient_tex = derivative_at_point + r" \approx " + difference_tex + " = " + numbers_tex + " = " + tex(key_value)
   steps = [
      Step(
         text=(
            f"The interval {math(rf'{low_time} \le {variable} \le {high_time}')} uses the rows at {variable} = {low_time} "
            f"and {variable} = {high_time}, so the change in {letter} is {math(f'{high_value} - {low_value} = {tex(change)}')}."
         ),
         value=change,
         point_type_id="BC-PT-99005",
         rule="difference of tabulated values",
      ),
      Step(
         text=(
            f"Dividing by the change in time, {math(quotient_tex)}."
         ),
         value=key_value,
         point_type_id="BC-PT-99005",
         rule="average rate of change as a difference quotient",
      ),
      Step(
         text=f"The units are those of {letter} over those of {variable}: {rate_units}.",
         point_type_id="BC-PT-99006",
         rule="units of a rate",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-02001",
         derivation=f"the change {letter}({high_time}) - {letter}({low_time}) reported without dividing by the change in time",
         value=change,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-02004",
         derivation=f"the rows at {variable} = {low_time} and {variable} = {point_time} used in place of the named interval",
         value=left_value,
         mechanism="wrong_limits",
      ),
      Distractor(
         error_path="BC-ERR-02004",
         derivation=f"the rows at {variable} = {point_time} and {variable} = {high_time} used in place of the named interval",
         value=right_value,
         mechanism="wrong_limits",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value, units=rate_units),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-03",
      calculator_status="no_calculator",
      figure=table,
      command_verb="approximate",
   )
