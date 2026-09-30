"""docs/agent/drawing-design.md, The prompt, and docs/agent/drawing-build-plan.md, Slice 4.

Every example figure in prompts/agent/live_v2.md is one the server would draw: it reads, compiles and
is described, and the prose after it marks each of its steps once, in order, at the start of a
sentence. The prose never names the machinery, no point carries an option letter, every figure text
and sentence passes the interface writing checks, and the examples together cover the figures the
design lists. The template is ASCII with no dash, its prefix fits the token budget, and its variable
section is v1's with drawing added after the move.
"""
import re
from dataclasses import dataclass
from pathlib import Path

import pytest

from app.agent.drawing.compile import compile_figure
from app.agent.drawing.spec import elements_in_order, read_figure, shape_of
from app.evals import agent_checks, figure_checks
from app.providers.base import split_template, template_placeholders

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
V1_PATH = REPOSITORY_ROOT / "prompts" / "agent" / "live_v1.md"
V2_PATH = REPOSITORY_ROOT / "prompts" / "agent" / "live_v2.md"

MINIMUM_EXAMPLES = 12
TOKEN_BUDGET = 10000
CHARACTERS_PER_TOKEN = 3.1

EXAMPLE_PATTERN = re.compile(r"^Example (\d+)\. (.*?)\n(.*?)(?=^Example \d+\. |\Z)", re.MULTILINE | re.DOTALL)
BLOCK_PATTERN = re.compile(r"^```figure\n(.*?)\n```$", re.MULTILINE | re.DOTALL)
MARKER_PATTERN = re.compile(r"\[\[step:([A-Za-z0-9_]+)\]\]")
MATH_DELIMITERS = re.compile(r"\\[()]")
MACHINERY_WORDS = re.compile(
   r"\b(json|blocks?|markers?|fences?|roles?|given|constructed|highlight(?:ed|s)?|errors?|ghosts?)\b",
   re.IGNORECASE,
)
OPTION_LETTERS = set("ABCDE")
SENTENCE_ENDINGS = (".", "?")
BROWSING_FACTS = {"mode": "browsing", "turn_index": 0, "rules": (), "ids": ()}


@dataclass(frozen=True)
class Example:
   number: int
   situation: str
   text_before_figure: str
   block: str
   text_after_figure: str
   block_count: int


def _examples():
   prefix, _variable_section = split_template(V2_PATH.read_text())
   examples = []

   for match in EXAMPLE_PATTERN.finditer(prefix):
      reply = match.group(3).strip()
      blocks = list(BLOCK_PATTERN.finditer(reply))
      first_block = blocks[0] if blocks else None
      has_block = first_block is not None

      examples.append(Example(
         number=int(match.group(1)),
         situation=match.group(2),
         text_before_figure=reply[:first_block.start()] if has_block else reply,
         block=first_block.group(1) if has_block else "",
         text_after_figure=reply[first_block.end():] if has_block else "",
         block_count=len(blocks),
      ))

   return examples


EXAMPLES = _examples()
EXAMPLE_IDS = [f"example_{example.number}" for example in EXAMPLES]


def _prose(example):
   return MARKER_PATTERN.sub(" ", example.text_before_figure + " " + example.text_after_figure)


def _plain(text):
   return MATH_DELIMITERS.sub("", text).strip()


def _point_names(figure):
   """Every name the figure gives a point: a point's label, a triangle's vertex names, and any
   label or free text that is a single letter."""
   names = []

   for _step_id, element in elements_in_order(figure):
      shape = shape_of(element)
      value = element[shape]
      label = element.get("label")
      is_labelled_point = shape == "point" and label is not None

      if is_labelled_point:
         names.append(_plain(label))

      if shape == "triangle":
         names.extend(_plain(name) for name in value.get("names") or ())

      free_texts = [label] if label is not None else []
      carries_text = shape in ("text", "callout")

      if carries_text:
         free_texts.append(value["text"])

      for text in free_texts:
         plain = _plain(text)
         is_single_letter = len(plain) == 1 and plain.isalpha()

         if is_single_letter:
            names.append(plain)

   return names


def test_the_template_holds_at_least_twelve_examples_each_with_one_figure():
   assert len(EXAMPLES) >= MINIMUM_EXAMPLES

   for example in EXAMPLES:
      assert example.block_count == 1, f"example {example.number} holds {example.block_count} figures"


@pytest.mark.parametrize("example", EXAMPLES, ids=EXAMPLE_IDS)
def test_every_example_figure_reads_compiles_and_is_described(example):
   figure = read_figure(example.block)
   compile_figure(figure)
   verdict = figure_checks.figure_described(figure)

   assert verdict.passed, verdict.reason


@pytest.mark.parametrize("example", EXAMPLES, ids=EXAMPLE_IDS)
def test_the_prose_marks_every_step_once_in_order_after_the_figure(example):
   figure = read_figure(example.block)
   step_ids = [step["id"] for step in figure["steps"]]
   introduction = example.text_before_figure.strip()
   has_introduction = len(introduction) > 0 and introduction.endswith(SENTENCE_ENDINGS)

   assert has_introduction, "no sentence introduces the figure"
   assert MARKER_PATTERN.search(example.text_before_figure) is None, "a marker comes before the figure"

   markers = list(MARKER_PATTERN.finditer(example.text_after_figure))

   assert [marker.group(1) for marker in markers] == step_ids

   for marker in markers:
      preceding = example.text_after_figure[:marker.start()].rstrip()
      starts_sentence = preceding == "" or preceding.endswith(SENTENCE_ENDINGS)

      assert starts_sentence, f"[[step:{marker.group(1)}]] is not at the start of a sentence"


@pytest.mark.parametrize("example", EXAMPLES, ids=EXAMPLE_IDS)
def test_the_prose_never_names_the_figure_machinery(example):
   found = MACHINERY_WORDS.search(_prose(example))

   assert found is None, f"the prose says {found.group(0)!r}"


@pytest.mark.parametrize("example", EXAMPLES, ids=EXAMPLE_IDS)
def test_no_point_is_named_with_an_option_letter(example):
   names = _point_names(read_figure(example.block))
   letters = sorted(set(names) & OPTION_LETTERS)

   assert letters == []


@pytest.mark.parametrize("example", EXAMPLES, ids=EXAMPLE_IDS)
def test_every_figure_text_and_sentence_passes_the_interface_writing_checks(example):
   _spec, facts = compile_figure(read_figure(example.block))
   texts = figure_checks.figure_texts_pass(facts, BROWSING_FACTS, None)

   assert texts.passed, texts.reason

   verdicts = agent_checks.run_checks(_prose(example), BROWSING_FACTS, None, agent_checks.EVERY_TURN_CHECKS)
   failed = [verdict.check for verdict in verdicts if not verdict.passed]

   assert failed == []


def _shapes(figure):
   return [(shape_of(element), element) for _step_id, element in elements_in_order(figure)]


def _elements(figure, shape):
   return [element for key, element in _shapes(figure) if key == shape]


def _values(figure, shape):
   return [element[shape] for element in _elements(figure, shape)]


def _is_after_submission(situation):
   return situation.startswith("After submission")


def _is_lesson(situation):
   return situation.startswith("Lesson")


def _is_wrong_right_sum(element):
   is_right = element["riemann"]["rule"] == "right"
   is_wrong = element.get("role") == "error"

   return is_right and is_wrong


def _has_one_open_end(interval):
   ends = interval.get("open", [False, False])

   return len(set(ends)) == 2


def _secant_to_tangent_in_practice(situation, figure):
   is_practice = situation.startswith("Practice")
   has_secant = len(_values(figure, "secant")) > 0
   has_tangent = len(_values(figure, "tangent")) > 0
   fades = any(step.get("fade") for step in figure["steps"])
   covers = is_practice and has_secant and has_tangent and fades

   return covers


def _left_against_wrong_right_after_submission(situation, figure):
   sums = _elements(figure, "riemann")
   has_left = any(element["riemann"]["rule"] == "left" for element in sums)
   has_wrong_right = any(_is_wrong_right_sum(element) for element in sums)
   covers = _is_after_submission(situation) and has_left and has_wrong_right

   return covers


def _area_between_on_a_lesson(situation, figure):
   has_between = any("between" in value for value in _values(figure, "area"))
   covers = _is_lesson(situation) and has_between

   return covers


def _slope_field_with_a_solution(_situation, figure):
   has_field = len(_values(figure, "slope_field")) > 0
   has_solution = len(_values(figure, "solution")) > 0
   covers = has_field and has_solution

   return covers


def _sign_chart_after_submission(situation, figure):
   has_signs = len(_values(figure, "signs")) > 0
   covers = _is_after_submission(situation) and has_signs

   return covers


def _table_row_after_submission(situation, figure):
   is_table = figure["kind"] == "table"
   has_row = any("row" in value for value in _values(figure, "highlight"))
   covers = _is_after_submission(situation) and is_table and has_row

   return covers


def _ladder_triangle_with_an_arrow(_situation, figure):
   right_triangles = [value for value in _values(figure, "triangle") if value["kind"] == "right"]
   has_labelled_sides = any("sides" in value for value in right_triangles)
   has_arrow = len(_values(figure, "vector")) > 0
   covers = has_labelled_sides and has_arrow

   return covers


def _parametric_velocity_with_legs(_situation, figure):
   has_path = len(_values(figure, "parametric")) > 0
   has_legs = any(value.get("legs") for value in _values(figure, "vector"))
   covers = has_path and has_legs

   return covers


def _polar_with_rays(_situation, figure):
   has_polar = len(_values(figure, "polar")) > 0
   has_two_rays = len(_values(figure, "segment")) >= 2
   covers = has_polar and has_two_rays

   return covers


def _partial_sums_to_a_limit_line(_situation, figure):
   has_sums = any(value.get("sums") for value in _values(figure, "sequence"))
   has_limit_line = len(_values(figure, "hline")) > 0
   covers = has_sums and has_limit_line

   return covers


def _interval_open_and_closed_after_submission(situation, figure):
   has_mixed_ends = any(_has_one_open_end(value) for value in _values(figure, "interval"))
   covers = _is_after_submission(situation) and has_mixed_ends

   return covers


def _rate_in_and_rate_out(_situation, figure):
   has_box = len(_values(figure, "box")) > 0
   has_two_arrows = len(_values(figure, "vector")) >= 2
   covers = has_box and has_two_arrows

   return covers


def _hole_approached_from_each_side(situation, figure):
   poses_no_question = "poses no question" in situation
   has_hole = any(element.get("open") for element in _elements(figure, "point"))
   has_two_approaches = len(_values(figure, "vector")) >= 2
   covers = _is_lesson(situation) and poses_no_question and has_hole and has_two_approaches

   return covers


def _circle_triangle_kinds_and_brace(_situation, figure):
   kinds = {value["kind"] for value in _values(figure, "triangle")}
   has_circle = len(_values(figure, "circle")) > 0
   has_brace = len(_values(figure, "brace")) > 0
   has_two_kinds = len(kinds) >= 2
   covers = has_circle and has_brace and has_two_kinds

   return covers


REQUIRED_COVERAGE = (
   _secant_to_tangent_in_practice,
   _left_against_wrong_right_after_submission,
   _area_between_on_a_lesson,
   _slope_field_with_a_solution,
   _sign_chart_after_submission,
   _table_row_after_submission,
   _ladder_triangle_with_an_arrow,
   _parametric_velocity_with_legs,
   _polar_with_rays,
   _partial_sums_to_a_limit_line,
   _interval_open_and_closed_after_submission,
   _rate_in_and_rate_out,
   _hole_approached_from_each_side,
   _circle_triangle_kinds_and_brace,
)


def test_the_examples_cover_every_figure_the_design_lists():
   figures = [(example.situation, read_figure(example.block)) for example in EXAMPLES]
   missing = []

   for covers in REQUIRED_COVERAGE:
      is_covered = any(covers(situation, figure) for situation, figure in figures)

      if not is_covered:
         missing.append(covers.__name__)

   assert missing == []


def test_the_template_is_ascii_with_no_dash():
   text = V2_PATH.read_text()

   assert chr(0x2014) not in text
   assert chr(0x2013) not in text
   assert text.isascii(), "a character outside ASCII, such as an emoji, is in the template"


def test_the_prefix_is_under_the_token_budget():
   prefix, _variable_section = split_template(V2_PATH.read_text())
   estimated_tokens = len(prefix) / CHARACTERS_PER_TOKEN

   assert estimated_tokens < TOKEN_BUDGET, f"{len(prefix)} characters, about {estimated_tokens:.0f} tokens"


def _field_lines(variable_section):
   return [line for line in variable_section.splitlines() if line.strip()]


def test_the_variable_section_is_v1s_fields_with_drawing_after_the_move():
   _v1_prefix, v1_variables = split_template(V1_PATH.read_text())
   prefix, variables = split_template(V2_PATH.read_text())
   v1_lines = _field_lines(v1_variables)
   v2_lines = _field_lines(variables)
   drawing_line = "Drawing: {{ drawing }}"

   assert template_placeholders(prefix) == set()
   assert "{{" not in prefix
   assert template_placeholders(variables) == template_placeholders(v1_variables) | {"drawing"}
   assert v2_lines.count(drawing_line) == 1

   drawing_index = v2_lines.index(drawing_line)

   assert v2_lines[drawing_index - 1] == "Move: {{ move }}"
   assert v2_lines[:drawing_index] + v2_lines[drawing_index + 1:] == v1_lines
