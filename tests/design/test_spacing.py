"""Gate 26's spacing vocabulary, checked against 08-design-brief.md's own sentence.

08-design-brief.md fixes the nine spacing values itself, unlike the colours, so this test
parses them out of the brief's "Spacing and layout" sentence rather than typing them a second
time. There is no operator input to validate here, because the values are not the operator's
to choose.
"""

import re
from pathlib import Path

from app.design.tokens import SPACING_TOKENS

REPO_ROOT = Path(__file__).resolve().parents[2]
BRIEF_PATH = REPO_ROOT / "docs" / "plan" / "08-design-brief.md"


def _brief_text():
   return BRIEF_PATH.read_text()


def _section(heading, next_heading):
   text = _brief_text()
   start = text.index("## " + heading)
   end = text.index("## " + next_heading, start)
   return text[start:end]


def _spacing_scale_values():
   section = _section("Spacing and layout", "Motion rules")
   sentence = re.search(r"and it is used everywhere: ([0-9, ]+) px\.", section)

   assert sentence is not None, "08's spacing scale sentence was not found, the brief changed shape"

   return [int(value) for value in sentence.group(1).split(",")]


def test_spacing_tokens_are_the_nine_values_08_states_in_order():
   plan_values = _spacing_scale_values()

   assert len(plan_values) == 9
   assert list(SPACING_TOKENS.values()) == plan_values


def test_spacing_token_names_follow_the_space_px_convention():
   for name, value in SPACING_TOKENS.items():
      assert name == "space-{0}".format(value)
