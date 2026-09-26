"""The theme-independent tokens P8's token audit moved out of the client: line heights, stroke
widths and the motion timing.

The line heights and the motion timing are read out of 08-design-brief.md's own table and sentence
rather than typed a second time, so a brief that changes a value changes what this file expects.
"""

import re
from pathlib import Path

from app.design import css
from app.design.tokens import (
   FIXED_LENGTH_TOKENS,
   LINE_HEIGHT_TOKENS,
   MOTION_TOKENS,
   STROKE_TOKENS,
   THEMES,
   TYPE_TOKENS,
   line_height_token_for,
   load_tokens,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
BRIEF_PATH = REPO_ROOT / "docs" / "plan" / "08-design-brief.md"
TOKEN_FILE_PATH = REPO_ROOT / "app" / "design" / "growth-tokens.json"


def _section(heading, next_heading):
   text = BRIEF_PATH.read_text()
   start = text.index("## " + heading)
   end = text.index("## " + next_heading, start)

   return text[start:end]


def _brief_line_heights():
   section = _section("Type system", "Colour system")
   rows = re.findall(r"^\| `(type-[a-z-]+)` \| \d+ px \| (\d+) px \|", section, re.MULTILINE)

   return {name: int(line_height) for name, line_height in rows}


def _stylesheet():
   return css.stylesheet_from_tokens(load_tokens(TOKEN_FILE_PATH))


def _root_blocks(stylesheet):
   return re.findall(r"^:root\s*\{(.*?)\}", stylesheet, re.DOTALL | re.MULTILINE)


def test_every_type_step_has_the_line_height_08s_table_pairs_with_it():
   brief_line_heights = _brief_line_heights()

   assert set(brief_line_heights) == set(TYPE_TOKENS)

   expected = {
      line_height_token_for(name): line_height
      for name, line_height in brief_line_heights.items()
   }

   assert LINE_HEIGHT_TOKENS == expected


def test_the_motion_tokens_are_the_one_duration_and_easing_08_gives():
   section = _section("Motion rules", "Interface writing")
   sentence = re.search(r"runs under roughly (\d+) ms and uses ([a-z-]+),", section)

   assert sentence is not None, "08's motion sentence was not found, the brief changed shape"

   assert MOTION_TOKENS == {
      "motion-duration": "{0}ms".format(sentence.group(1)),
      "motion-easing": sentence.group(2),
   }


def test_stroke_widths_are_positive_and_ordered_hairline_to_curve():
   widths = list(STROKE_TOKENS.values())

   assert list(STROKE_TOKENS) == ["stroke-hairline", "stroke-mark", "stroke-curve"]
   assert all(width > 0 for width in widths)
   assert widths == sorted(set(widths))


def test_every_fixed_length_is_emitted_once_in_a_root_block_whatever_the_token_file():
   stylesheet = _stylesheet()
   root_text = "\n".join(_root_blocks(stylesheet))

   assert len(FIXED_LENGTH_TOKENS) == len(LINE_HEIGHT_TOKENS) + len(STROKE_TOKENS)

   for name, value in FIXED_LENGTH_TOKENS.items():
      declaration = "{0}: {1}px;".format(css.custom_property_name(name), value)

      assert root_text.count(declaration) == 1, declaration
      assert stylesheet.count(css.custom_property_name(name) + ":") == 1, name


def test_no_fixed_length_rides_in_a_theme_block():
   stylesheet = _stylesheet()

   for theme in THEMES:
      block = re.search(r'\[data-theme="{0}"\]\s*\{{(.*?)\}}'.format(theme), stylesheet, re.DOTALL)

      assert block is not None

      for name in FIXED_LENGTH_TOKENS:
         assert css.custom_property_name(name) not in block.group(1)


def test_fixed_custom_properties_advertise_every_fixed_token_and_nothing_else():
   expected = {css.custom_property_name(name) for name in FIXED_LENGTH_TOKENS}

   assert set(css.FIXED_CUSTOM_PROPERTIES) == expected
   assert expected.isdisjoint(css.CUSTOM_PROPERTIES)
