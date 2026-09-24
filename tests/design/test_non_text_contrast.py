"""WCAG 2.2 SC 1.4.11 on the mastery map and the calibration curve: every colour they draw a mark
with holds 3:1 against every surface, in both themes (08, Colour system and Accessibility)."""
import copy
from pathlib import Path

from app.design import tokens
from app.design.contrast import NON_TEXT_CONTRAST_FLOOR, contrast_ratio

TOKEN_FILE_PATH = Path(__file__).resolve().parents[2] / "app" / "design" / "growth-tokens.json"


def test_every_graphic_colour_holds_the_non_text_floor_on_every_surface_in_both_themes():
   token_file = tokens.load_tokens(TOKEN_FILE_PATH)
   below = []

   for theme in tokens.THEMES:
      for graphic, surface in tokens.GRAPHIC_CONTRAST_PAIRS:
         ratio = contrast_ratio(token_file[theme][graphic], token_file[theme][surface])
         is_below = ratio < NON_TEXT_CONTRAST_FLOOR

         if is_below:
            below.append(f"{theme}: {graphic} on {surface} is {ratio:.2f}:1")

   assert NON_TEXT_CONTRAST_FLOOR == 3.0
   assert len(tokens.GRAPHIC_CONTRAST_PAIRS) == len(tokens.GRAPHIC_TOKENS) * len(tokens.SURFACES)
   assert below == []


def test_the_token_gate_refuses_a_graphic_colour_that_only_the_non_text_floor_catches():
   token_file = tokens.load_tokens(TOKEN_FILE_PATH)
   faint = copy.deepcopy(token_file)
   faint["light"]["accent-base"] = faint["light"]["accent-tint-4"]

   violations = tokens.token_violations(faint)

   assert tokens.token_violations(token_file) == []
   assert any("accent-base on surface-raised" in violation for violation in violations)
