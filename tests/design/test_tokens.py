"""Gate 26's vocabulary and validator, checked against 08-design-brief.md itself.

docs/plan/11-phased-delivery.md item 26 says gate 26 reads hex values out of the token file the
operator produces and computes the ratios itself. This module is the schema, the validator and a
blank template that make that possible: it never authors a hex value, and the tests below never
compare a hand-typed list to another hand-typed list, they parse 08's own tables and sentences.
"""

import io
import json
import re
import subprocess
import sys
import tokenize
from pathlib import Path

import pytest

from app.design import contrast
from app.design import tokens
from app.design.tokens import (
   COLOUR_TOKENS,
   THEMES,
   TYPE_TOKENS,
   load_tokens,
   token_violations,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
BRIEF_PATH = REPO_ROOT / "docs" / "plan" / "08-design-brief.md"
TEMPLATE_PATH = REPO_ROOT / "docs" / "operator" / "design-tokens.template.json"
TOKENS_SOURCE_PATH = REPO_ROOT / "app" / "design" / "tokens.py"


def _brief_text():
   return BRIEF_PATH.read_text()


def _section(heading, next_heading):
   text = _brief_text()
   start = text.index("## " + heading)
   end = text.index("## " + next_heading, start)
   return text[start:end]


def _type_scale_names():
   section = _section("Type system", "Colour system")
   return set(re.findall(r"\|\s*`(type-[a-z-]+)`\s*\|", section))


def _large_type_names():
   section = _section("Type system", "Colour system")
   sentence = re.search(
      r"So (`type-[a-z-]+`(?: and `type-[a-z-]+`)*) may sit at 3:1",
      section,
   )

   assert sentence is not None, "08's large-text sentence was not found, the brief changed shape"

   return set(re.findall(r"`(type-[a-z-]+)`", sentence.group(1)))


def _colour_section():
   return _section("Colour system", "Spacing and layout")


def _accent_tint_names():
   """The accent tint ramp 08 states as a range, expanded from 08's own endpoints. The numbers
   are read out of the sentence, never typed here, so a brief that renames the ramp or widens it
   changes what this file expects.
   """
   section = _colour_section()
   range_match = re.search(r"`accent-tint-(\d+)` through `accent-tint-(\d+)`", section)

   assert range_match is not None, (
      "08's accent tint range sentence was not found, the brief changed shape"
   )

   first = int(range_match.group(1))
   last = int(range_match.group(2))

   assert last > first, (
      "08 states the accent tint ramp as a range, and {0} through {1} is not one".format(
         first, last
      )
   )

   return ["accent-tint-{0}".format(step) for step in range(first, last + 1)]


def _colour_token_names():
   section = _colour_section()
   backticked = set(re.findall(r"`([a-z][a-z0-9-]*)`", section))
   backticked = {name for name in backticked if not name.startswith("type-")}

   backticked.update(_accent_tint_names())

   return backticked


def _complete_tokens():
   theme = {}

   for name in COLOUR_TOKENS:
      theme[name] = "#888888"

   theme["text-primary"] = "#000000"
   theme["text-secondary"] = "#000000"
   theme["text-muted"] = "#000000"
   theme["text-on-accent"] = "#000000"
   theme["surface-page"] = "#ffffff"
   theme["surface-raised"] = "#ffffff"
   theme["surface-sunken"] = "#ffffff"
   theme["accent-base"] = "#ffffff"

   for name in _accent_tint_names():
      theme[name] = "#ffffff"

   theme["accent-contrast-text"] = "#000000"
   theme["state-correct"] = "#000000"
   theme["state-incorrect"] = "#000000"
   theme["focus-ring"] = "#000000"

   for name in TYPE_TOKENS:
      theme[name] = "inherit"

   return {theme_name: dict(theme) for theme_name in THEMES}


def test_the_type_tokens_are_the_nine_the_plan_tabulates():
   plan_names = _type_scale_names()

   assert len(plan_names) == 9
   assert set(TYPE_TOKENS.keys()) == plan_names


def test_only_the_two_large_type_tokens_carry_the_lower_floor():
   large_names = _large_type_names()

   assert large_names == {"type-display", "type-title"}

   for name, category in TYPE_TOKENS.items():
      is_large = name in large_names
      expected_category = "large" if is_large else "normal"

      assert category == expected_category


def test_the_accent_tint_ramp_is_the_range_08_states():
   """The ramp's endpoints are 08's, so widening or renaming the range in the brief changes what
   the vocabulary has to carry.
   """
   plan_tints = _accent_tint_names()
   code_tints = [name for name in COLOUR_TOKENS if name.startswith("accent-tint-")]

   assert code_tints == plan_tints


def test_the_template_carries_every_token_name_and_no_value():
   plan_names = _colour_token_names()

   assert set(COLOUR_TOKENS) == plan_names

   template = json.loads(TEMPLATE_PATH.read_text())

   assert set(template.keys()) == set(THEMES)

   fillable_names = set(COLOUR_TOKENS) | set(TYPE_TOKENS)

   for theme in THEMES:
      assert set(template[theme].keys()) == fillable_names

      for value in template[theme].values():
         assert value is None


def test_an_unfilled_template_reports_every_token_as_missing():
   tokens = load_tokens(TEMPLATE_PATH)
   violations = token_violations(tokens)

   for theme in THEMES:
      for name in COLOUR_TOKENS:
         found = any(theme in violation and name in violation for violation in violations)

         assert found, "no violation mentioned {0} in {1}".format(name, theme)


def test_a_filled_pair_below_the_floor_is_reported():
   tokens = _complete_tokens()
   tokens["light"]["text-primary"] = "#808080"
   tokens["light"]["surface-page"] = "#818181"

   violations = token_violations(tokens)

   found = any(
      "text-primary" in violation and "surface-page" in violation and "light" in violation
      for violation in violations
   )

   assert found


def _grey(level):
   return "#{0:02x}{0:02x}{0:02x}".format(level)


def _greys_astride_the_floor():
   """The lightest grey on white that still clears contrast.TEXT_CONTRAST_FLOOR, and the next
   grey up, which is the first one under it. Both are found with contrast.contrast_ratio, so no
   ratio and no hex value is written down here.
   """
   white = "#ffffff"
   clearing = [
      level
      for level in range(256)
      if contrast.contrast_ratio(_grey(level), white) >= contrast.TEXT_CONTRAST_FLOOR
   ]

   assert clearing, "no grey on white clears the floor, the contrast module changed shape"

   at_floor = max(clearing)
   below_floor = at_floor + 1

   assert below_floor < 256
   assert contrast.contrast_ratio(_grey(below_floor), white) < contrast.TEXT_CONTRAST_FLOOR

   return _grey(at_floor), _grey(below_floor), white


def test_a_filled_pair_at_the_floor_is_accepted(monkeypatch):
   at_floor, below_floor, white = _greys_astride_the_floor()
   filled = _complete_tokens()

   for theme in THEMES:
      for surface in ("surface-page", "surface-raised", "surface-sunken"):
         filled[theme][surface] = white

      filled[theme]["text-primary"] = at_floor

   assert token_violations(filled) == []

   for theme in THEMES:
      filled[theme]["text-primary"] = below_floor

   violations = token_violations(filled)
   mentions_the_pair = [
      violation
      for violation in violations
      if "text-primary" in violation and "surface-page" in violation
   ]

   assert len(mentions_the_pair) == len(THEMES)

   # No hex pair lands exactly on the floor in floating point, so the boundary itself, as
   # opposed to the closest sRGB neighbour on either side, is exercised by substituting the
   # ratio directly. This is what goes red if `ratio < TEXT_CONTRAST_FLOOR` ever became
   # `ratio <= TEXT_CONTRAST_FLOOR`.
   monkeypatch.setattr(
      tokens,
      "contrast_ratio",
      lambda foreground, background: contrast.TEXT_CONTRAST_FLOOR,
   )

   assert token_violations(_complete_tokens()) == []


def test_an_unknown_token_name_is_reported():
   tokens = _complete_tokens()
   tokens["light"]["accent-warning"] = "#123456"

   violations = token_violations(tokens)

   found = any("accent-warning" in violation and "light" in violation for violation in violations)

   assert found


def test_a_malformed_hex_value_is_reported():
   tokens = _complete_tokens()
   tokens["dark"]["text-primary"] = "not-a-colour"

   violations = token_violations(tokens)

   found = any("text-primary" in violation and "dark" in violation for violation in violations)

   assert found


def test_both_themes_are_checked_independently():
   tokens = _complete_tokens()
   tokens["dark"]["text-primary"] = "#808080"
   tokens["dark"]["surface-page"] = "#818181"

   violations = token_violations(tokens)

   has_dark_violation = any("dark" in violation and "text-primary" in violation for violation in violations)
   has_light_violation = any("light" in violation and "text-primary" in violation for violation in violations)

   assert has_dark_violation
   assert not has_light_violation


def test_the_floors_come_from_the_contrast_module():
   assert contrast.TEXT_CONTRAST_FLOOR == pytest.approx(4.5)
   assert contrast.LARGE_TEXT_CONTRAST_FLOOR == pytest.approx(3.0)

   source = TOKENS_SOURCE_PATH.read_text()
   number_literals = {
      token.string
      for token in tokenize.generate_tokens(io.StringIO(source).readline)
      if token.type == tokenize.NUMBER
   }

   assert "4.5" not in number_literals
   assert "3.0" not in number_literals
   assert "from app.design.contrast import" in source


def checked_foreground_names():
   """Every token the validator actually puts on one side of a contrast pair, found by giving
   each one in turn a value that cannot clear the floor and seeing whether it is reported.
   """
   reported = set()

   for name in tokens.COLOUR_TOKENS:
      filled = _complete_tokens()

      for theme in tokens.THEMES:
         filled[theme][name] = "#7f7f7f"

         for other in tokens.COLOUR_TOKENS:
            is_the_one_under_test = other == name

            if not is_the_one_under_test:
               filled[theme][other] = "#808080"

      for message in tokens.token_violations(filled):
         if name in message and ":1" in message:
            reported.add(name)

   return reported


def test_every_token_whose_name_says_text_is_contrast_checked():
   checked = checked_foreground_names()

   text_tokens = [name for name in tokens.COLOUR_TOKENS if "text" in name]

   unchecked = sorted(name for name in text_tokens if name not in checked)

   assert unchecked == [], (
      "08's contrast floors are stated over text, so a token whose role is text and which sits "
      f"in no checked pair can hold any value at all, and these do: {unchecked}"
   )


def test_the_semantic_colours_are_contrast_checked():
   checked = checked_foreground_names()

   semantic = [name for name in tokens.COLOUR_TOKENS if name.startswith("state-")]

   unchecked = sorted(name for name in semantic if name not in checked)

   assert unchecked == [], (
      "a correct or incorrect state is read on a surface, so its colour carries a floor too, "
      f"and these are checked against nothing: {unchecked}"
   )


def test_the_type_tokens_are_not_reported_as_unknown():
   """Entry criterion 5 puts the nine type-scale steps in the same operator file as the colours,
   so the checker the operator runs must recognise them rather than calling each one unknown.
   """
   tokens = load_tokens(TEMPLATE_PATH)
   violations = token_violations(tokens)
   unknown_reports = [violation for violation in violations if "unknown token" in violation]

   assert unknown_reports == []


def test_a_type_token_missing_from_the_file_is_reported():
   tokens = load_tokens(TEMPLATE_PATH)
   dropped = sorted(TYPE_TOKENS)[0]

   for theme in THEMES:
      del tokens[theme][dropped]

   violations = token_violations(tokens)
   mentions_the_dropped_token = [
      violation
      for violation in violations
      if "missing token {0}".format(dropped) in violation
   ]

   assert len(mentions_the_dropped_token) == len(THEMES)


def _reported_pairs_for(foreground_name, below_floor_on):
   """Gives foreground_name and one background the same grey, so that pair sits at 1:1, and
   returns every violation naming both."""
   filled = _complete_tokens()

   for theme in THEMES:
      filled[theme][foreground_name] = "#808080"
      filled[theme][below_floor_on] = "#808080"

   return [
      violation
      for violation in token_violations(filled)
      if foreground_name in violation and below_floor_on in violation
   ]


def test_accent_contrast_text_is_checked_on_every_accent_tint():
   tints = [name for name in COLOUR_TOKENS if name.startswith("accent-tint-")]

   assert tints

   for tint in tints:
      assert len(_reported_pairs_for("accent-contrast-text", tint)) == len(THEMES), tint


def test_accent_contrast_text_is_not_checked_on_accent_base():
   """The operator's approved loosening: 08 gives the primary button's text its own token,
   text-on-accent, which stays checked on accent-base, and accent-contrast-text is the tint-hue
   text for the tint backgrounds."""
   assert _reported_pairs_for("accent-contrast-text", "accent-base") == []
   assert len(_reported_pairs_for("text-on-accent", "accent-base")) == len(THEMES)


def test_check_tokens_prints_a_ratio_for_every_checked_pair():
   token_file_path = REPO_ROOT / "app" / "design" / "growth-tokens.json"
   result = subprocess.run(
      [sys.executable, str(REPO_ROOT / "tools" / "check_tokens.py"), str(token_file_path)],
      cwd=str(REPO_ROOT),
      capture_output=True,
      text=True,
   )
   printed_lines = result.stdout.splitlines()
   expected_prefixes = [
      "{0}: {1} on {2} is ".format(theme, foreground_name, background_name)
      for theme in THEMES
      for foreground_name, background_name in tokens.CONTRAST_PAIRS
   ]
   unprinted = [
      prefix
      for prefix in expected_prefixes
      if not any(line.startswith(prefix) for line in printed_lines)
   ]

   assert result.returncode == 0, result.stdout
   assert unprinted == []
   assert len(printed_lines) == len(expected_prefixes)
