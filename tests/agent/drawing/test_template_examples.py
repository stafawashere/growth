"""docs/agent/drawing-design.md, The prompt, and docs/agent/drawing-build-plan.md, Slice 4.

Every example figure in prompts/agent/live_v2.md is one the server would draw: it reads, compiles and
is described, and the prose after it marks each of its steps once, in order, at the start of a
sentence. The prose never names the machinery, no point carries an option letter, every figure text
and sentence passes the interface writing checks, and the examples together cover the figures the
design lists. The template is ASCII with no dash, its prefix fits the token budget, and its variable
section is v1's with drawing added after the move.

Every marks example (docs/agent/drawing-design.md, Marks on the page) reads and compiles against a
synthetic anchor list that holds the words it quotes; its prose marks each step of its marks, and of
the figure beside it when there is one, once, in order, after the block; no practice example marks
an option; and the examples cover the marks the build plan lists. The token budget was raised from
10,000 to 12,000 when the marks rules and examples took the prefix to about 11,655 tokens.
"""
import re
from dataclasses import dataclass
from pathlib import Path

import pytest

from app.agent.drawing.compile import compile_figure
from app.agent.drawing.marks import compile_marks, marks_in_order, read_marks
from app.agent.drawing.marks import shape_of as mark_shape_of
from app.agent.drawing.spec import elements_in_order, read_figure, shape_of
from app.evals import agent_checks, figure_checks
from app.providers.base import split_template, template_placeholders

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
V1_PATH = REPOSITORY_ROOT / "prompts" / "agent" / "live_v1.md"
V2_PATH = REPOSITORY_ROOT / "prompts" / "agent" / "live_v2.md"

MINIMUM_EXAMPLES = 12
TOKEN_BUDGET = 12000
MINIMUM_MARKS_EXAMPLES = 4
CHARACTERS_PER_TOKEN = 3.1

EXAMPLE_PATTERN = re.compile(r"^Example (\d+)\. (.*?)\n(.*?)(?=^Example \d+\. |^Marks on the page\. |\Z)", re.MULTILINE | re.DOTALL)
MARKS_EXAMPLE_PATTERN = re.compile(r"^Marks example (\d+)\. (.*?)\n(.*?)(?=^Marks example \d+\. |\Z)", re.MULTILINE | re.DOTALL)
BLOCK_PATTERN = re.compile(r"^```figure\n(.*?)\n```$", re.MULTILINE | re.DOTALL)
MARKS_BLOCK_PATTERN = re.compile(r"^```marks\n(.*?)\n```$", re.MULTILINE | re.DOTALL)
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


SYNTHETIC_ANCHORS = [
   {"id": "stem", "kind": "text", "text": "f is given by the graph shown. Find the average rate of change of f on the interval [1, 3]."},
   {"id": "item_figure", "kind": "graph", "window": {"x": [0, 5], "y": [-1, 9]}},
   {"id": "item_table", "kind": "table", "rows": 4, "columns": 2},
   {"id": "feedback", "kind": "text", "text": "The response used one width for every subinterval."},
   {"id": "solution_step_1", "kind": "text", "text": "Each subinterval contributes its width times the average of its endpoint values."},
   {"id": "solution_step_2", "kind": "text", "text": "A width of 2 for every subinterval would miss the widths, which are 2, 3 and 5."},
]


@dataclass(frozen=True)
class MarksExample:
   number: int
   situation: str
   reply: str
   marks_blocks: tuple
   figure_blocks: tuple


def _marks_examples():
   prefix, _variable_section = split_template(V2_PATH.read_text())
   examples = []

   for match in MARKS_EXAMPLE_PATTERN.finditer(prefix):
      reply = match.group(3).strip()
      examples.append(MarksExample(
         number=int(match.group(1)),
         situation=match.group(2),
         reply=reply,
         marks_blocks=tuple(MARKS_BLOCK_PATTERN.finditer(reply)),
         figure_blocks=tuple(BLOCK_PATTERN.finditer(reply)),
      ))

   return examples


MARKS_EXAMPLES = _marks_examples()
MARKS_EXAMPLE_IDS = [f"marks_example_{example.number}" for example in MARKS_EXAMPLES]


def _read_marks(example):
   return read_marks(example.marks_blocks[0].group(1), SYNTHETIC_ANCHORS)


def _marks_prose(example):
   prose = MARKS_BLOCK_PATTERN.sub(" ", BLOCK_PATTERN.sub(" ", example.reply))

   return MARKER_PATTERN.sub(" ", prose)


def test_the_template_holds_four_marks_examples_one_of_them_beside_a_figure():
   assert len(MARKS_EXAMPLES) >= MINIMUM_MARKS_EXAMPLES
   assert all(len(example.marks_blocks) == 1 for example in MARKS_EXAMPLES)
   assert any(len(example.figure_blocks) == 1 for example in MARKS_EXAMPLES)


@pytest.mark.parametrize("example", MARKS_EXAMPLES, ids=MARKS_EXAMPLE_IDS)
def test_every_marks_example_reads_and_compiles_against_the_anchors(example):
   compile_marks(_read_marks(example), SYNTHETIC_ANCHORS)

   for block in example.figure_blocks:
      compile_figure(read_figure(block.group(1)))


def _step_ids_of(example):
   blocks = [(block, [step["id"] for step in _read_marks(example)["steps"]]) for block in example.marks_blocks]
   blocks += [(block, [step["id"] for step in read_figure(block.group(1))["steps"]]) for block in example.figure_blocks]

   return blocks


@pytest.mark.parametrize("example", MARKS_EXAMPLES, ids=MARKS_EXAMPLE_IDS)
def test_the_prose_marks_every_step_once_in_order_after_its_block(example):
   blocks = _step_ids_of(example)
   every_step = [step_id for _block, step_ids in blocks for step_id in step_ids]
   markers = [(marker.start(), marker.group(1)) for marker in MARKER_PATTERN.finditer(example.reply)]

   assert len(set(every_step)) == len(every_step), "a step id is used by both the figure and the marks"
   assert sorted(step_id for _start, step_id in markers) == sorted(every_step)

   for block, step_ids in blocks:
      marked = [(start, step_id) for start, step_id in markers if step_id in step_ids]

      assert [step_id for _start, step_id in marked] == step_ids
      assert all(start > block.end() for start, _step_id in marked)


@pytest.mark.parametrize("example", MARKS_EXAMPLES, ids=MARKS_EXAMPLE_IDS)
def test_the_marks_prose_never_names_the_machinery(example):
   found = MACHINERY_WORDS.search(_marks_prose(example))

   assert found is None, f"the prose says {found.group(0)!r}"


@pytest.mark.parametrize("example", MARKS_EXAMPLES, ids=MARKS_EXAMPLE_IDS)
def test_every_marks_text_and_sentence_passes_the_interface_writing_checks(example):
   _render, facts = compile_marks(_read_marks(example), SYNTHETIC_ANCHORS)
   texts = figure_checks.figure_texts_pass(facts, BROWSING_FACTS, None)
   verdicts = agent_checks.run_checks(_marks_prose(example), BROWSING_FACTS, None, agent_checks.EVERY_TURN_CHECKS)

   assert texts.passed, texts.reason
   assert [verdict.check for verdict in verdicts if not verdict.passed] == []


PRACTICE_MARKS_EXAMPLES = [example for example in MARKS_EXAMPLES if example.situation.startswith("Practice")]


@pytest.mark.parametrize("example", PRACTICE_MARKS_EXAMPLES, ids=[f"marks_example_{example.number}" for example in PRACTICE_MARKS_EXAMPLES])
def test_no_practice_example_marks_an_option_or_strikes(example):
   shapes = [mark_shape_of(mark) for _step_id, mark in marks_in_order(_read_marks(example))]
   _render, facts = compile_marks(_read_marks(example), SYNTHETIC_ANCHORS)
   options = [shown.anchor for shown in facts.anchors if shown.anchor.startswith("option_")]

   assert options == []
   assert "strike" not in shapes


def _marks_of(example):
   return [(mark_shape_of(mark), mark[mark_shape_of(mark)]) for _step_id, mark in marks_in_order(_read_marks(example))]


def _values_of(example, wanted):
   return [value for shape, value in _marks_of(example) if shape == wanted]


def _underline_and_ring_on_the_graph(example):
   has_underline = any(value["anchor"] == "stem" for value in _values_of(example, "underline"))
   has_ring = any("at" in value for value in _values_of(example, "ring"))

   return has_underline and has_ring


def _highlighted_table_row(example):
   return any("row" in value for value in _values_of(example, "highlight"))


def _strike_with_a_note_after_checking(example):
   is_after_submission = example.situation.startswith("After submission")
   has_strike = any(value["anchor"].startswith("solution_step_") for value in _values_of(example, "strike"))
   has_note = len(_values_of(example, "note")) > 0

   return is_after_submission and has_strike and has_note


def _points_from_the_stem_to_the_graph(arrow):
   starts_at_the_stem = arrow["from"]["anchor"] == "stem"
   ends_at_the_graph = arrow["to"]["anchor"] == "item_figure"

   return starts_at_the_stem and ends_at_the_graph


def _arrow_from_the_stem_to_the_graph(example):
   return any(_points_from_the_stem_to_the_graph(value) for value in _values_of(example, "arrow"))


MARKS_COVERAGE = (
   _underline_and_ring_on_the_graph,
   _highlighted_table_row,
   _strike_with_a_note_after_checking,
   _arrow_from_the_stem_to_the_graph,
)


def test_the_marks_examples_cover_what_the_build_plan_lists():
   missing = [covers.__name__ for covers in MARKS_COVERAGE if not any(covers(example) for example in MARKS_EXAMPLES)]

   assert missing == []
