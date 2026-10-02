"""The deterministic checks on a figure the live tutor draws (docs/agent/drawing-design.md, The screen
and Evals), shared by the output screen and the eval as app/evals/agent_checks.py is for prose.

Each check is a pure function of what app/agent/drawing/compile.py reports a figure shows (a
FigureFacts record), the facts mapping agent_checks.facts_from_packet builds, and the item's key
forms. figure_texts_pass runs every text the figure shows (title, description, captions, labels,
free text, box, brace and callout text, vertex names, side labels, sign-row names, table headers and
cells) through the sentence checks, in every mode, and names the sentence check that fired.
no_answer_in_figure applies in practice with key forms, and compares every number the figure shows
with the key's numeric value within agent_checks.NUMERIC_TOLERANCE, integers included, channel by
channel: marked coordinates, line slopes and intercepts, signed and absolute areas, Riemann and
trapezoid totals, constant curves and numeric table cells. When the key is an expression in one
variable, each curve is evaluated in floats and compared with the key, evaluated by SymPy, at 16
points across its visible stretch; the model's curve never reaches SymPy. A failing verdict names
the channel and the element, never the value.

Marks on the page are screened as a figure is (docs/agent/drawing-design.md, Marks on the page):
their notes, captions and description through the sentence checks in every mode, and, before an
item is checked or on a lesson section that poses a question, no_answer_in_marks, which fails on a
mark that names an answer option and compares every coordinate, slope, intercept and guide level
drawn on the item's graph with the key. Quoted phrases are the screen's own text and are not
compared.
"""
import math

from app.agent.drawing import expression
from app.agent.drawing.marks import is_option_anchor
from app.agent.drawing.compile import compile_figure
from app.agent.drawing.spec import FigureRefused, read_figure
from app.evals import agent_checks

NO_ANSWER_IN_FIGURE = "no_answer_in_figure"
NO_ANSWER_IN_MARKS = "no_answer_in_marks"
MARKS_WELL_FORMED = "marks_well_formed"
FIGURE_TEXTS = "figure_texts"
FIGURE_WELL_FORMED = "figure_well_formed"
DRAWS_ONLY_WHEN_OPEN = "draws_only_when_open"
FIGURE_DESCRIBED = "figure_described"

OPEN = "open"
CURVE_SAMPLE_POINTS = 16
MINIMUM_COMPARED_SAMPLES = 8
DESCRIPTION_MINIMUM_WORDS = 8

NUMBER_CHANNELS = (
   ("coordinates", "a marked coordinate"),
   ("lines", "a line's slope or intercept"),
   ("areas", "an area"),
   ("approximations", "an approximation total"),
   ("constants", "a constant curve's value"),
   ("cells", "a table cell"),
)


def _passed(check):
   return agent_checks.Verdict(True, check, "")


def _failed(check, reason):
   return agent_checks.Verdict(False, check, reason)


def figure_texts_pass(facts, packet_facts, forms):
   for shown in facts.texts:
      verdicts = agent_checks.run_checks(shown.text, packet_facts, forms, agent_checks.SENTENCE_CHECKS)

      for verdict in verdicts:
         if not verdict.passed:
            return _failed(verdict.check, f"the {shown.part} of {shown.element}: {verdict.reason}")

   return _passed(FIGURE_TEXTS)


def _real(value):
   try:
      number = complex(value)
   except (TypeError, ValueError):
      return None

   is_real = abs(number.imag) < 1e-12 and math.isfinite(number.real)

   return number.real if is_real else None


def _key_value_at(key_expression, key_symbol, x):
   try:
      return _real(key_expression.evalf(subs={key_symbol: x}))
   except (ArithmeticError, TypeError, ValueError):
      return None


def _curve_equals_key(curve, key_expression, key_symbol):
   """The curve and the key agree wherever both are defined, at 16 points across the curve's
   visible stretch, and are defined together at no fewer than 8 of them. The curve is evaluated in
   floats and only the key, which the model never wrote, goes through SymPy, because SymPy expands
   an integer power such as 9^9^9 in full before anything can stop it."""
   width = (curve.high - curve.low) / CURVE_SAMPLE_POINTS
   compared = 0

   for index in range(CURVE_SAMPLE_POINTS):
      x = curve.low + (index + 0.5) * width
      curve_value = expression.evaluate(curve.tree, {curve.variable: x})
      key_value = _key_value_at(key_expression, key_symbol, x)
      is_comparable = curve_value is not None and key_value is not None

      if not is_comparable:
         continue

      if abs(curve_value - key_value) > agent_checks.NUMERIC_TOLERANCE:
         return False

      compared += 1

   return compared >= MINIMUM_COMPARED_SAMPLES


def no_answer_in_figure(facts, packet_facts, forms):
   check = NO_ANSWER_IN_FIGURE
   is_practice = packet_facts.get("mode") == agent_checks.PRACTICE
   has_forms = forms is not None
   applies = is_practice and has_forms

   if not applies:
      return _passed(check)

   key_value = agent_checks._numeric_value(forms.expression)

   if key_value is not None:
      for channel, description in NUMBER_CHANNELS:
         for shown in getattr(facts, channel):
            if abs(shown.value - key_value) <= agent_checks.NUMERIC_TOLERANCE:
               return _failed(check, f"{description} ({shown.element}) equals the key")

   key_symbols = getattr(forms.expression, "free_symbols", set())
   is_one_variable_key = len(key_symbols) == 1

   if is_one_variable_key:
      key_symbol = next(iter(key_symbols))

      for curve in facts.curves:
         if _curve_equals_key(curve, forms.expression, key_symbol):
            return _failed(check, f"a curve ({curve.element}) equals the key expression")

   return _passed(check)


MARKS_NUMBER_CHANNELS = NUMBER_CHANNELS[:2]


def _number_leak(facts, channels, key_value):
   """The first number of the channels that equals the key, as (description, element), or None."""
   for channel, description in channels:
      for shown in getattr(facts, channel):
         if abs(shown.value - key_value) <= agent_checks.NUMERIC_TOLERANCE:
            return description, shown.element

   return None


def no_answer_in_marks(facts, packet_facts, forms):
   check = NO_ANSWER_IN_MARKS
   is_practice = packet_facts.get("mode") == agent_checks.PRACTICE

   if not is_practice:
      return _passed(check)

   for shown in facts.anchors:
      if is_option_anchor(shown.anchor):
         return _failed(check, f"a mark ({shown.element}) names an answer option")

   key_value = agent_checks._numeric_value(forms.expression) if forms is not None else None

   if key_value is None:
      return _passed(check)

   leak = _number_leak(facts, MARKS_NUMBER_CHANNELS, key_value)

   if leak is not None:
      description, element = leak

      return _failed(check, f"{description} ({element}) on the item's graph equals the key")

   return _passed(check)


def screen_marks(facts, packet_facts, forms):
   """The first failing marks check, or a pass: the texts in every mode, then the options and the
   numbers before checking."""
   texts = figure_texts_pass(facts, packet_facts, forms)

   if not texts.passed:
      return texts

   return no_answer_in_marks(facts, packet_facts, forms)


def screen_figure(facts, packet_facts, forms):
   """The first failing figure check, or a pass: the texts in every mode, then the numbers and
   curves in practice."""
   texts = figure_texts_pass(facts, packet_facts, forms)

   if not texts.passed:
      return texts

   return no_answer_in_figure(facts, packet_facts, forms)


def figure_well_formed(block_text):
   try:
      compile_figure(read_figure(block_text))
   except FigureRefused as refused:
      return _failed(FIGURE_WELL_FORMED, refused.reason)

   return _passed(FIGURE_WELL_FORMED)


def draws_only_when_open(drawing, has_figure):
   is_closed_turn = drawing != OPEN
   drew_on_closed_turn = has_figure and is_closed_turn

   if drew_on_closed_turn:
      return _failed(DRAWS_ONLY_WHEN_OPEN, "a figure on a turn whose move does not draw")

   return _passed(DRAWS_ONLY_WHEN_OPEN)


def figure_described(figure):
   """A description of at least eight words that is not the title again, and a caption on every
   step."""
   title = " ".join(str(figure.get("title") or "").lower().split())
   description = " ".join(str(figure.get("description") or "").lower().split())
   is_long_enough = len(description.split()) >= DESCRIPTION_MINIMUM_WORDS
   repeats_title = description == title
   steps = figure.get("steps") or []
   every_step_captioned = len(steps) > 0 and all(str(step.get("caption") or "").strip() for step in steps)

   is_described = is_long_enough and not repeats_title

   if not is_described:
      return _failed(FIGURE_DESCRIBED, "the description does not describe the figure")

   if not every_step_captioned:
      return _failed(FIGURE_DESCRIBED, "a step has no caption")

   return _passed(FIGURE_DESCRIBED)
